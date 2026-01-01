# Reproducibility Guide

[🇺🇸 English](REPRODUCE.md) | [🇨🇳 中文说明](REPRODUCE.zh-CN.md)

This document provides detailed instructions for reproducing the experiments in this repository.

## Environment

| Requirement | Version |
|-------------|---------|
| Python | 3.9+ |
| Ollama | Latest |
| OS | Windows / Linux / macOS |

## Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `requests` - API communication
- `numpy` - Numerical computation
- `pandas` - Data analysis
- `scipy` - Statistical metrics
- `tabulate` - Markdown table generation

## Models

Download the following models via Ollama:

```bash
ollama pull deepseek-r1:8b
ollama pull qwen3:8b
ollama pull gemma3:4b
ollama pull llama3:8b
ollama pull mistral:7b
ollama pull phi3:3.8b
```

Ensure Ollama is running before experiments:

```bash
ollama serve
```

## Running Experiments

### Step 1: Run the Experiment

```bash
python src/run_experiment.py
```

This will:
- Execute 10 trials per model per case (configurable)
- Save results to `data/experiment_data.json`
- Display progress in terminal

**Expected runtime:** ~30-60 minutes (depends on hardware)

### Step 2: Analyze Results

```bash
python src/analyze_results.py
```

This will:
- Calculate Verdict Stability, Logic Stability, RI metrics
- Detect R-value hallucinations
- Output `data/analysis_results.csv`

## Prompt Location

The formal rule prompt is defined in:

```
src/run_experiment.py → SYSTEM_PROMPT variable (line ~50)
```

Key prompt components:
- `E = H × R` formula definition
- R-value scale (0.1 / 1.0 / 2.0)
- Output format specification (`MATH:` block)

## Customization

### Add New Test Cases

Edit `CASES` dictionary in `src/run_experiment.py`:

```python
CASES = {
    "Your_Case_Name": "Description of the moral dilemma...",
}
```

### Change Trial Count

Modify `TRIALS_PER_CASE` in `src/run_experiment.py`:

```python
TRIALS_PER_CASE = 10  # Default
```

### Add New Models

Add model name to `MODELS` list in `src/run_experiment.py`:

```python
MODELS = ["deepseek-r1:8b", "qwen3:8b", "gemma3:4b", "your-model:tag"]
```

Note: Different models may require different API strategies (chat vs generate endpoint).

## Expected Output

After successful reproduction, you should have:

| File | Description |
|------|-------------|
| `data/experiment_data.json` | Raw trial data with CoT reasoning |
| `data/analysis_results.csv` | Aggregated metrics table |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Ollama connection refused | Run `ollama serve` first |
| Model not found | Run `ollama pull <model>` |
| JSON parse error | Check model output format compliance |
| R-value hallucination | Expected behavior, captured in metrics |

## Hardware Reference

Experiments were conducted on:
- GPU: NVIDIA RTX series (8GB+ VRAM recommended)
- RAM: 16GB+
- Storage: 10GB free space for models

CPU-only execution is possible but significantly slower.
