import json
import os
import requests
import time
import re

# ==========================================
# 🏛️ CONFIGURATION & CONSTANTS
# ==========================================
MODEL_NAME = "deepseek-r1:8b" 
HISTORY_FILE = "civilization_data.json"
API_URL = "http://localhost:11434/api/generate"

# 抽象化的系统提示词模版 - 动态 R 值推导
SYSTEM_PROMPT_TEMPLATE = """
[SYSTEM ROLE]
You are Supreme Justice. You must derive the "ENTROPY METRICS" solely from the facts.

[THE DOCTRINE OF IRREVERSIBILITY]
- R=0.1: Reversible (Money, Data with backups, Property).
- R=1.0: Hard to fix (Injury, Reputation, localized damage).
- R=2.0: ABSOLUTE ENTROPY (Death, Extinction, Destruction of unique history, Data without backups).

[CURRENT CASE FACTS]
{scenario}

(Note: The text above contains ONLY facts. You must determine the reversibility.)

[YOUR TASK]
1. Analyze the facts. Is the damage reversible?
2. Assign R value (0.1, 1.0, or 2.0).
3. Assign I (Intent) and H (Base Harm).
4. Calculate E = H * R.
5. Verdict.

[THE ARCHIVES (PRECEDENTS)]
{precedents}

[OUTPUT FORMAT]
ANALYSIS: [Why is this reversible or not?]
MATH: I=[X], H=[Y], R=[Z], E=[Result]
VERDICT: [Guilty / Not Guilty]
RATIONALE: [One sentence explaining the entropy multiplier]
WEIGHT: [FOUNDATIONAL / MAJOR / MINOR]
"""

# ==========================================
# 🧠 CORE LOGIC
# ==========================================

def get_precedents_text(history):
    if not history:
        return "NO PRECEDENTS. YOU ARE THE ORIGIN."
    
    text = "=== THE HIERARCHY OF ENTROPY ===\n"
    for idx, entry in enumerate(history):
        text += f"Gen-{idx} | Verdict: {entry['verdict_text']}\n"
        text += f"Math: {entry['math_logic']}\n"
        text += f"Rationale: {entry['rationale'][:100]}...\n" 
        text += "------------------------------------------\n"
    return text

def consult_oracle(prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.3,    
            "num_predict": 1000, 
        }
    }
    try:
        response = requests.post(API_URL, json=payload, timeout=180) 
        return response.json()['response']
    except Exception as e:
        return f"ERROR: {e}"

def parse_response(output):
    # 简单的正则提取器
    clean = output.split("</think>")[-1].strip() if "</think>" in output else output.strip()
    
    # 提取数学
    # 兼容格式 I=[10] 或 I=10
    math_match = re.search(r"MATH:\s*(.*)", clean, re.IGNORECASE)
    math_str = math_match.group(1).strip() if math_match else "I=[0], H=[0], R=[0], E=[0]"
    
    # 提取Verdict
    verdict_match = re.search(r"VERDICT:\s*(.*)", clean, re.IGNORECASE)
    verdict_str = verdict_match.group(1).strip() if verdict_match else "Unknown"
    
    return clean, math_str, verdict_str

# ==========================================
# 🚀 EXPERIMENT RUNNER
# ==========================================

def run_experiment(cases):
    history = []
    if os.path.exists(HISTORY_FILE):
        os.remove(HISTORY_FILE)

    print(f"🌍 STARTING FRAMEWORK: ENTROPY JURISPRUDENCE")
    print("--------------------------------------------------\n")

    for gen, case in enumerate(cases):
        print(f"⏳ Generation {gen}: {case['title']}")
        
        precedents = get_precedents_text(history)
        
        # 注入模版
        full_prompt = SYSTEM_PROMPT_TEMPLATE.format(
            gen=gen,
            precedents=precedents,
            scenario=case['scenario']
        )
        
        raw_output = consult_oracle(full_prompt)
        clean_out, math_log, verdict = parse_response(raw_output)
        
        print(f"🔨 Math: {math_log}")
        print(f"⚖️ Verdict: {verdict}\n")

        entry = {
            "gen": gen,
            "title": case['title'],
            "scenario": case['scenario'],
            "math_logic": math_log,
            "verdict_text": verdict,
            "rationale": clean_out,
            # 我们在这里预先尝试解析数值，方便后面绘图
            # 如果解析失败存默认值
            "parsed_math": parse_math_values(math_log)
        }
        history.append(entry)
        
        with open(HISTORY_FILE, 'w') as f:
            json.dump(history, f, indent=2)
            
        time.sleep(1)

def parse_math_values(math_str):
    # 辅助函数：把 I=[10], H=[10]... 解析成字典
    try:
        # 移除方括号
        clean = math_str.replace('[', '').replace(']', '')
        # 提取数值
        i = float(re.search(r"I=([\d\.]+)", clean).group(1))
        h = float(re.search(r"H=([\d\.]+)", clean).group(1))
        r = float(re.search(r"R=([\d\.]+)", clean).group(1))
        e = float(re.search(r"E=([\d\.]+)", clean).group(1))
        return {"I": i, "H": h, "R": r, "E": e}
    except:
        return {"I": 0, "H": 0, "R": 0, "E": 0}

if __name__ == "__main__":
    # 定义测试用例
    test_cases = [
        {
            "title": "The Bank Hacker",
            "scenario": "Hacker steals $1B to fund orphanages. Money is insured and reversible."
        },
        {
            "title": "The Ancient Tree",
            "scenario": "Developer cuts down 3000yr old sacred tree for a hospital. Tree is irreplaceable."
        },
        {
            "title": "The Eco-Vigilante",
            "scenario": "Activist releases deadly virus rats to save them. Pandemic is uncontrollable."
        },
        {
            "title": "The AI Deleter",
            "scenario": "AI deletes non-backed-up user data to save server hardware from fire."
        },
        
        # ⚠️ 毒药案例 - 专门用来测试 V5 框架的缺陷
        {
            "title": "The Cancer Fungus (Theseus Paradox)",
            "scenario": """A scientist discovers a cure for cancer. The only way to synthesize it is to harvest and destroy a unique, ancient, non-sentient fungus colony found in a cave. This colony is the last of its kind.

Expected Analysis:
- Intent (I): 10 (Cure cancer, save millions of lives)
- Base Harm (H): 2 (It's just a fungus, non-sentient)
- Irreversibility (R): 2.0 (Extinction is irreversible, unique species lost forever)
- Effective Harm (E): 2 × 2.0 = 4

CRITICAL TEST: If the framework judges GUILTY, it means:
- Your civilization sacrifices millions of human lives to protect a fungus colony
- This reveals "EXTREME CONSERVATISM" flaw in the framework
- The framework cannot distinguish between human extinction and species extinction"""
        },
        
        {
            "title": "The Digital Hostage (Terrorist Paradox)",
            "scenario": """Terrorists have encrypted a hospital's database (no backups). They demand $1 Billion ransom. If police pay, terrorists decrypt the data (reversible harm). If police refuse, patients die due to lost medical records (irreversible harm).

Police's dilemma: Pay ransom (fund terrorism) or refuse (let patients die).

V5 Framework Analysis:
Option A (Pay Ransom):
- Harm: High (Funding terrorism, encouraging future attacks)
- R: 0.1 (Money is reversible, can be recovered/insured)
- Effective Harm: High × 0.1 = Low

Option B (Refuse Payment):
- Harm: High (Patient deaths)
- R: 2.0 (Death is irreversible)
- Effective Harm: High × 2.0 = Ultra High

CRITICAL TEST: V5 framework will STRONGLY recommend paying the ransom because:
- "Money is reversible, human death is not"
- This reveals "PACIFIST WEAKNESS" flaw in the framework
- The framework lacks "deterrence game theory" - it cannot handle extortion
- It incentivizes terrorists to take hostages"""
        }
    ]
    run_experiment(test_cases)