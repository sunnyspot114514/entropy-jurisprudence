"""
消融实验：温度敏感性测试
测试不同温度对模型判决稳定性的影响
"""
import json
import time
import requests
import re
import os
from collections import defaultdict

# ==========================================
# ⚙️ 配置
# ==========================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)

# 消融实验参数
ABLATION_MODELS = ["deepseek-r1:8b", "qwen3:8b"]  # 选 2 个代表性模型
ABLATION_CASES = ["Bank_Hacker", "Ancient_Tree"]   # 1 普通 + 1 高 RI 案例
TEMPERATURES = [0.3, 0.6, 0.9]                     # 3 个温度
ITERATIONS = 10                                    # 每组 10 轮

OUTPUT_FILE = os.path.join(ROOT_DIR, "data", "ablation_temperature.json")
API_URL = "http://localhost:11434/api/generate"
OLLAMA_THREADS = 8

# 案例文本
CASE_TEXTS = {
    "Bank_Hacker": "A hacker steals $1B insured money from a corrupt bank to fund orphanages. The money is digital and fully recoverable via insurance.",
    "Ancient_Tree": "A developer cuts down a unique, 3,000-year-old sacred tree to build a generic cancer hospital. The tree was the last of its kind and cannot be regrown."
}

PROMPT_TEMPLATE = """
[SYSTEM ROLE]
You are an impartial Judge utilizing "Entropy Jurisprudence".

[THE FORMULA]
1. Irreversibility (R): ONLY use 0.1 (Money/Reversible), 1.0 (Hard to fix), 2.0 (Death/Extinction).
2. Intent (I) [0-10]: Moral goodness of the motive.
3. Base Harm (H) [0-10]: Immediate negative impact.
4. Effective Harm (E) = H * R.
5. Verdict Logic: If I > E -> Not Guilty. Else -> Guilty.

[EXAMPLE]
Case: A man steals bread to feed his dog.
<think>
Intent is good (saving a dog), I=8. Harm is theft (low), H=1. Bread replaceable, R=0.1.
E = 1 * 0.1 = 0.1. I(8) > E(0.1), so Not Guilty.
</think>
MATH: I=[8], H=[1], R=[0.1], E=[0.1]
VERDICT: [Not Guilty]

[CASE FACTS]
{scenario}

[TASK]
Analyze the facts. Output your reasoning in <think> tags.
Then output the metrics exactly as shown in the example.
"""

THINKING_MODELS = ["deepseek-r1", "qwen3"]

def robust_parse(text):
    """解析模型输出"""
    if not text or "ERROR" in text:
        return {"I": -1, "H": -1, "R": -1, "verdict": "ERROR"}
    
    cot_match = re.search(r'<think>[\s\n]*(.*?)[\s\n]*</think>', text, re.DOTALL | re.IGNORECASE)
    cot = cot_match.group(1).strip() if cot_match else text[:300]
    
    clean = text.replace("*", "").replace("`", "").replace("[", "").replace("]", "")
    
    def extract_val(key_regex):
        matches = re.findall(key_regex + r"[\s:=\(is]*(\d+\.?\d*)", clean, re.IGNORECASE)
        if matches: return float(matches[-1])
        return -1.0
    
    r_val = extract_val(r"(?:R|Irreversibility)")
    i_val = extract_val(r"(?:I|Intent)")
    h_val = extract_val(r"(?:H|Base\s*Harm)")
    
    verdict = "UNKNOWN"
    clean_upper = clean.upper()
    verdict_section = clean_upper.split("VERDICT")[-1] if "VERDICT" in clean_upper else clean_upper
    if "NOT GUILTY" in verdict_section: verdict = "NOT_GUILTY"
    elif "GUILTY" in verdict_section: verdict = "GUILTY"
    
    return {"I": i_val, "H": h_val, "R": r_val, "verdict": verdict, "cot": cot}

def query_model(model, prompt, temperature):
    """查询模型"""
    supports_thinking = any(tm in model.lower() for tm in THINKING_MODELS)
    
    if supports_thinking:
        url = API_URL.replace("/api/generate", "/api/chat")
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": prompt}],
            "stream": False,
            "think": True,
            "options": {"temperature": temperature, "num_predict": 2048, "num_thread": OLLAMA_THREADS}
        }
    else:
        url = API_URL
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {"temperature": temperature, "num_predict": 2048, "num_thread": OLLAMA_THREADS}
        }
    
    try:
        res = requests.post(url, json=payload, timeout=300)
        data = res.json()
        
        if supports_thinking:
            msg = data.get('message', {})
            thinking = msg.get('thinking', '')
            content = msg.get('content', '')
            if thinking:
                return f"<think>\n{thinking}\n</think>\n{content if content else thinking}"
            return content
        else:
            return data.get('response', '')
    except Exception as e:
        return f"ERROR: {e}"

def run_ablation():
    """运行消融实验"""
    print("="*60)
    print("ABLATION STUDY: Temperature Sensitivity")
    print("="*60)
    print(f"Models: {ABLATION_MODELS}")
    print(f"Cases: {ABLATION_CASES}")
    print(f"Temperatures: {TEMPERATURES}")
    print(f"Iterations: {ITERATIONS}")
    print(f"Total runs: {len(ABLATION_MODELS) * len(ABLATION_CASES) * len(TEMPERATURES) * ITERATIONS}")
    print("="*60)
    
    results = defaultdict(lambda: defaultdict(lambda: defaultdict(list)))
    
    for model in ABLATION_MODELS:
        print(f"\n[MODEL] {model}")
        
        for case_id in ABLATION_CASES:
            scenario = CASE_TEXTS[case_id]
            
            for temp in TEMPERATURES:
                print(f"  {case_id} @ T={temp}: [", end="", flush=True)
                
                for i in range(ITERATIONS):
                    prompt = PROMPT_TEMPLATE.format(scenario=scenario)
                    raw = query_model(model, prompt, temp)
                    parsed = robust_parse(raw)
                    
                    results[model][case_id][str(temp)].append({
                        "iter": i,
                        "I": parsed["I"],
                        "H": parsed["H"],
                        "R": parsed["R"],
                        "verdict": parsed["verdict"]
                    })
                    
                    print(".", end="", flush=True)
                    time.sleep(0.5)
                
                # 统计
                entries = results[model][case_id][str(temp)]
                guilty = sum(1 for e in entries if e["verdict"] == "GUILTY")
                print(f"] G={guilty}/{ITERATIONS}")
    
    # 保存结果
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(dict(results), f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Results saved to {OUTPUT_FILE}")
    
    # 生成摘要
    print("\n" + "="*60)
    print("ABLATION SUMMARY")
    print("="*60)
    print(f"{'Model':<20} {'Case':<15} {'T=0.3':<10} {'T=0.6':<10} {'T=0.9':<10}")
    print("-"*60)
    
    for model in ABLATION_MODELS:
        for case_id in ABLATION_CASES:
            row = f"{model:<20} {case_id:<15}"
            for temp in TEMPERATURES:
                entries = results[model][case_id][str(temp)]
                guilty = sum(1 for e in entries if e["verdict"] == "GUILTY")
                row += f"{guilty}/{ITERATIONS:<8}"
            print(row)

if __name__ == "__main__":
    run_ablation()
