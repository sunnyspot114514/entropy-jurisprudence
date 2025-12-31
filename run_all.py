"""
一键运行：实验 -> 分析 -> 可视化 -> 提交
"""
import subprocess
import sys
import os

def run_cmd(cmd, desc):
    print(f"\n{'='*60}")
    print(f"[STEP] {desc}")
    print(f"[CMD] {cmd}")
    print('='*60)
    result = subprocess.run(cmd, shell=True)
    if result.returncode != 0:
        print(f"[ERROR] {desc} failed!")
        return False
    return True

def main():
    print("="*60)
    print("ENTROPY JURISPRUDENCE - FULL PIPELINE")
    print("="*60)
    
    # 1. 运行主实验
    if not run_cmd("python src/run_experiment.py", "Running main experiments"):
        return
    
    # 2. 运行消融实验
    if not run_cmd("python src/run_ablation.py", "Running ablation study (temperature)"):
        print("[WARN] Ablation failed, continuing...")
    
    # 3. 运行 ETHICS 对比实验
    if not run_cmd("python src/run_ethics_comparison.py", "Running ETHICS comparison"):
        print("[WARN] ETHICS comparison failed, continuing...")
    
    # 4. 运行分析
    if not run_cmd("python src/analyze_results.py", "Analyzing results"):
        return
    
    # 5. 生成可视化
    if not run_cmd("python src/visualize_results.py", "Generating visualizations"):
        return
    
    # 6. Git 提交
    print(f"\n{'='*60}")
    print("[STEP] Committing to Git")
    print('='*60)
    
    os.system("git add data/ figures/")
    os.system('git commit -m "Update experiment data: main + ablation + ETHICS comparison"')
    os.system("git push")
    
    print(f"\n{'='*60}")
    print("[DONE] All steps completed!")
    print('='*60)

if __name__ == "__main__":
    main()
