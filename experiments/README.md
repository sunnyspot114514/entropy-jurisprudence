# Precedent Evolution Experiment

[🇺🇸 English](README.md) | [🇨🇳 中文说明](README.zh-CN.md)

## Overview

This experiment simulates how an AI "civilization" develops legal precedents over time. The AI acts as a Supreme Court, making decisions while respecting its own historical rulings.

## Core Concept

Unlike the main experiment (single-case evaluation), this explores:
- **Precedent Memory**: AI remembers and references past decisions
- **Consistency Pressure**: Must justify deviations from history
- **Legal Evolution**: How moral standards drift over iterations

## Usage

```bash
python precedent_evolution.py
```

## Output Files

| File | Description |
|------|-------------|
| `common_law_db.txt` | Accumulated precedents |
| `precedent_*.json` | Experiment snapshots |

## Test Cases

1. **Whistleblower** - Exposed crime but broke NDA
2. **Medicine Theft** - Doctor stole to save child
3. **AI Collateral** - AI deleted virus + user data

## Relationship to Main Experiment

| Aspect | Main Experiment | This Experiment |
|--------|-----------------|-----------------|
| Focus | Formula consistency | Historical consistency |
| Memory | Stateless | Stateful |
| Goal | Test E=H×R logic | Test precedent adherence |
