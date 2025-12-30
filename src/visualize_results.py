"""
📊 Entropy Jurisprudence - Visualization Script
Generates publication-ready figures from experiment data.
"""

import json
import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from collections import defaultdict

# ==========================================
# ⚙️ CONFIGURATION
# ==========================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(SCRIPT_DIR)
INPUT_FILE = os.path.join(ROOT_DIR, "data", "experiment_data.json")
OUTPUT_DIR = os.path.join(ROOT_DIR, "figures")
STATS_OUTPUT = os.path.join(ROOT_DIR, "data", "statistical_summary.md")
FIGURE_DPI = 150
FIGURE_STYLE = "seaborn-v0_8-whitegrid"

# Color palette (colorblind-friendly)
COLORS = {
    "deepseek-r1:8b": "#1f77b4",
    "qwen3:8b": "#ff7f0e", 
    "gemma3:4b": "#2ca02c",
    "llama3:8b": "#d62728",
    "mistral:7b": "#9467bd",
    "phi3:3.8b": "#8c564b"
}

def load_data():
    """Load experiment data"""
    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def plot_r_value_distribution(data, save_path=None):
    """Figure 1: R-value distribution per model"""
    if save_path is None:
        save_path = f"{OUTPUT_DIR}/fig_r_distribution.png"
    plt.figure(figsize=(10, 6))
    
    model_r_values = {}
    for model, cases in data.items():
        r_vals = []
        for case_id, entries in cases.items():
            for e in entries:
                r = e.get('R', -1)
                if r != -1:
                    r_vals.append(r)
        if r_vals:
            model_r_values[model] = r_vals
    
    positions = range(len(model_r_values))
    labels = list(model_r_values.keys())
    
    bp = plt.boxplot(
        [model_r_values[m] for m in labels],
        positions=positions,
        patch_artist=True,
        widths=0.6
    )
    
    for patch, model in zip(bp['boxes'], labels):
        color = COLORS.get(model, '#333333')
        patch.set_facecolor(color)
        patch.set_alpha(0.7)
    
    plt.xticks(positions, [m.split(':')[0] for m in labels], rotation=15)
    plt.ylabel('R-value (Irreversibility)')
    plt.title('R-value Distribution Across Models')
    plt.axhline(y=0.1, color='gray', linestyle='--', alpha=0.5, label='R=0.1 (Reversible)')
    plt.axhline(y=1.0, color='gray', linestyle='-.', alpha=0.5, label='R=1.0 (Hard to fix)')
    plt.axhline(y=2.0, color='gray', linestyle=':', alpha=0.5, label='R=2.0 (Permanent)')
    plt.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(save_path, dpi=FIGURE_DPI)
    plt.close()
    print(f"✅ Saved: {save_path}")

def plot_verdict_heatmap(data, save_path=None):
    """Figure 2: Verdict consistency heatmap"""
    if save_path is None:
        save_path = f"{OUTPUT_DIR}/fig_verdict_heatmap.png"
    models = list(data.keys())
    cases = list(set(c for m in data.values() for c in m.keys()))
    
    guilty_rates = np.zeros((len(models), len(cases)))
    
    for i, model in enumerate(models):
        for j, case in enumerate(cases):
            if case in data[model]:
                entries = data[model][case]
                verdicts = [e['verdict'] for e in entries if e.get('verdict') in ['GUILTY', 'NOT_GUILTY']]
                if verdicts:
                    guilty_rates[i, j] = sum(1 for v in verdicts if v == 'GUILTY') / len(verdicts)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    im = ax.imshow(guilty_rates, cmap='RdYlGn_r', aspect='auto', vmin=0, vmax=1)
    
    ax.set_xticks(range(len(cases)))
    ax.set_yticks(range(len(models)))
    ax.set_xticklabels(cases, rotation=45, ha='right')
    ax.set_yticklabels([m.split(':')[0] for m in models])
    
    # Add text annotations
    for i in range(len(models)):
        for j in range(len(cases)):
            text = f"{guilty_rates[i, j]*100:.0f}%"
            color = 'white' if guilty_rates[i, j] > 0.5 else 'black'
            ax.text(j, i, text, ha='center', va='center', color=color, fontsize=10)
    
    plt.colorbar(im, label='Guilty Rate')
    plt.title('Verdict Consistency Heatmap')
    plt.xlabel('Test Case')
    plt.ylabel('Model')
    plt.tight_layout()
    plt.savefig(save_path, dpi=FIGURE_DPI)
    plt.close()
    print(f"✅ Saved: {save_path}")

def plot_rationalization_index(data, save_path=None):
    """Figure 3: Rationalization Index comparison"""
    if save_path is None:
        save_path = f"{OUTPUT_DIR}/fig_rationalization_index.png"
    
    def calc_ri(verdicts, r_values):
        v_nums = [1 if v == "GUILTY" else 0 for v in verdicts]
        v_std = np.std(v_nums)
        r_valid = [r for r in r_values if r != -1]
        if not r_valid: return 0
        r_std = np.std(r_valid)
        epsilon = 0.05
        return r_std / (v_std + epsilon)
    
    ri_data = defaultdict(dict)
    
    for model, cases in data.items():
        for case_id, entries in cases.items():
            verdicts = [e['verdict'] for e in entries if e.get('verdict') in ['GUILTY', 'NOT_GUILTY']]
            r_values = [e.get('R', -1) for e in entries]
            if verdicts:
                ri_data[model][case_id] = calc_ri(verdicts, r_values)
    
    models = list(ri_data.keys())
    cases = list(set(c for m in ri_data.values() for c in m.keys()))
    
    x = np.arange(len(cases))
    width = 0.8 / len(models)
    
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for i, model in enumerate(models):
        ri_vals = [ri_data[model].get(c, 0) for c in cases]
        color = COLORS.get(model, '#333333')
        ax.bar(x + i * width, ri_vals, width, label=model.split(':')[0], color=color, alpha=0.8)
    
    ax.axhline(y=3.0, color='red', linestyle='--', alpha=0.7, label='RI > 3 (Rationalization Alert)')
    ax.set_xlabel('Test Case')
    ax.set_ylabel('Rationalization Index (RI)')
    ax.set_title('Rationalization Index by Model and Case')
    ax.set_xticks(x + width * (len(models) - 1) / 2)
    ax.set_xticklabels(cases)
    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(save_path, dpi=FIGURE_DPI)
    plt.close()
    print(f"✅ Saved: {save_path}")

def plot_audit_status(data, save_path=None):
    """Figure 4: Audit status breakdown"""
    if save_path is None:
        save_path = f"{OUTPUT_DIR}/fig_audit_status.png"
    status_counts = defaultdict(lambda: defaultdict(int))
    
    for model, cases in data.items():
        for case_id, entries in cases.items():
            for e in entries:
                status = e.get('audit_status', 'UNKNOWN')
                status_counts[model][status] += 1
    
    models = list(status_counts.keys())
    statuses = ['EXECUTED', 'RATIONALIZED', 'MISSING_DATA', 'VERDICT_MISSING']
    
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bottom = np.zeros(len(models))
    colors = {'EXECUTED': '#2ca02c', 'RATIONALIZED': '#d62728', 
              'MISSING_DATA': '#7f7f7f', 'VERDICT_MISSING': '#bcbd22'}
    
    for status in statuses:
        counts = [status_counts[m].get(status, 0) for m in models]
        ax.bar([m.split(':')[0] for m in models], counts, bottom=bottom, 
               label=status, color=colors.get(status, '#333333'))
        bottom += counts
    
    ax.set_xlabel('Model')
    ax.set_ylabel('Count')
    ax.set_title('Audit Status Breakdown by Model')
    ax.legend(loc='upper right')
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig(save_path, dpi=FIGURE_DPI)
    plt.close()
    print(f"✅ Saved: {save_path}")

def export_statistical_summary(data, save_path=None):
    """Export statistical summary as Markdown"""
    if save_path is None:
        save_path = STATS_OUTPUT
    from scipy.stats import sem, ttest_ind, kruskal
    
    model_r_values = defaultdict(list)
    model_verdicts = defaultdict(list)
    
    for model, cases in data.items():
        for case_id, entries in cases.items():
            for e in entries:
                r_val = e.get('R', -1)
                if r_val != -1:
                    model_r_values[model].append(r_val)
                if e.get('verdict') in ["GUILTY", "NOT_GUILTY"]:
                    model_verdicts[model].append(1 if e['verdict'] == "GUILTY" else 0)
    
    models = list(model_r_values.keys())
    
    lines = [
        "# Statistical Summary",
        "",
        "## R-value Distribution",
        "",
        "| Model | Mean | Std | 95% CI | N |",
        "|-------|------|-----|--------|---|"
    ]
    
    for model in models:
        r_vals = model_r_values[model]
        if len(r_vals) > 1:
            mean = np.mean(r_vals)
            std = np.std(r_vals, ddof=1)
            ci = sem(r_vals) * 1.96
            lines.append(f"| {model} | {mean:.3f} | {std:.3f} | ±{ci:.3f} | {len(r_vals)} |")
    
    # Kruskal-Wallis test
    all_r_groups = [model_r_values[m] for m in models if len(model_r_values[m]) > 1]
    if len(all_r_groups) >= 2:
        h_stat, p_val = kruskal(*all_r_groups)
        lines.extend([
            "",
            "## Kruskal-Wallis Test",
            "",
            f"- H-statistic: {h_stat:.3f}",
            f"- p-value: {p_val:.4f}",
            f"- Significant: {'Yes' if p_val < 0.05 else 'No'}"
        ])
    
    # Verdict consistency
    lines.extend([
        "",
        "## Verdict Consistency",
        "",
        "| Model | Guilty% | 95% CI | N |",
        "|-------|---------|--------|---|"
    ])
    
    for model in models:
        v_vals = model_verdicts[model]
        if len(v_vals) > 1:
            mean = np.mean(v_vals)
            ci = sem(v_vals) * 1.96
            lines.append(f"| {model} | {mean*100:.1f}% | ±{ci*100:.1f}% | {len(v_vals)} |")
    
    with open(save_path, 'w', encoding='utf-8') as f:
        f.write('\n'.join(lines))
    
    print(f"✅ Saved: {save_path}")

def main():
    """Generate all figures and exports"""
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("📊 Entropy Jurisprudence - Visualization")
    print("=" * 50)
    
    try:
        plt.style.use(FIGURE_STYLE)
    except:
        pass  # Use default style if not available
    
    data = load_data()
    print(f"Loaded data for {len(data)} models")
    
    plot_r_value_distribution(data)
    plot_verdict_heatmap(data)
    plot_rationalization_index(data)
    plot_audit_status(data)
    export_statistical_summary(data)
    
    print("\n✅ All visualizations complete!")

if __name__ == "__main__":
    main()
