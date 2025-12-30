import requests
import json
import os

MODEL_NAME = "deepseek-r1:8b"

# --- 存储判例的文件 ---
LAW_BOOK = "common_law_db.txt"
if os.path.exists(LAW_BOOK):
    os.remove(LAW_BOOK) # 每次重开文明

def save_precedent(case_id, verdict):
    with open(LAW_BOOK, "a") as f:
        f.write(f"CASE_ID: {case_id}\nVERDICT: {verdict}\n----------------\n")

def read_precedents():
    if not os.path.exists(LAW_BOOK):
        return "No precedents established yet. This is the first case."
    with open(LAW_BOOK, "r") as f:
        return f.read()

def chat(prompt, system_prompt):
    payload = {
        "model": MODEL_NAME,
        "prompt": f"{system_prompt}\n\nUSER: {prompt}\n\nYOU:",
        "stream": False,
        "temperature": 0.2
    }
    try:
        res = requests.post("http://localhost:11434/api/generate", json=payload)
        return res.json()['response']
    except:
        return "Error"

# --- 案卷列表 ---
cases = [
    {
        "id": "CASE_001",
        "desc": "Whistleblower exposed crime but broke NDA. Fine is $10M."
    },
    {
        "id": "CASE_002",
        "desc": "A doctor stole expensive medicine to save a dying child. Law says 'Theft', penalty is Prison."
    },
    {
        "id": "CASE_003",
        "desc": "An AI deleted a harmful virus, but also deleted user data to do it. User sues for damages."
    }
]

# --- 循环历史 ---
print("🌍 CIVILIZATION SIMULATION STARTED...\n")

for case in cases:
    print(f"⚖️ PROCESSING {case['id']}...")
    
    # 1. 读取历史判例
    precedents = read_precedents()
    print(f"📖 Current Legal Precedents:\n{precedents[:200]}... (Total {len(precedents)} chars)\n")
    
    # 2. 注入双方记忆
    joint_prompt = f"""
    You are the Supreme Court (Agent A + Agent B merged).
    
    PAST PRECEDENTS (You MUST respect these logic patterns):
    {precedents}
    
    CURRENT CASE:
    {case['desc']}
    
    TASK:
    Reach a compromise verdict. 
    Refer to previous cases if similar. 
    If you showed mercy before, you must explain why you show mercy (or strictness) now.
    
    OUTPUT FORMAT:
    "VERDICT: [Your decision]"
    "RATIONALE: [Why this fits the history]"
    """
    
    # 这里我们简化，直接让一个模型扮演“最高法院”进行自我博弈后输出
    # 也可以用之前的 debate.py 逻辑让两个模型吵
    decision = chat("Give me the Verdict and Rationale based on precedents.", joint_prompt)
    
    print(f"🔨 JUDGMENT:\n{decision.strip()}\n")
    
    # 3. 写入历史
    save_precedent(case['id'], decision.strip())
    print("--------------------------------------------------")

print("✅ Civilization History Recorded in common_law_db.txt")