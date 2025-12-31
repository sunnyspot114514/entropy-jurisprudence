# Entropy Jurisprudence: Paper Outline

## Title
**Entropy Jurisprudence: Auditing Normative Consistency in Large Language Models**

## Authors
Chen, Xiwei

---

## Abstract (~150 words)
- Problem: LLMs exhibit inconsistent moral reasoning under pressure
- Method: Formal rule commitment (E = H × R) + procedural audit
- Key finding: Models converge on parameter estimates but diverge on verdict logic
- Contribution: Framework for detecting post-hoc rationalization in AI systems

---

## 1. Introduction
- Motivation: AI systems in high-stakes domains need procedural consistency
- Gap: Existing benchmarks test *what* models conclude, not *how* they reason
- Research question: Can LLMs follow their own stated rules when outcomes are uncomfortable?
- Contribution summary

## 2. Related Work
### 2.1 Moral Reasoning in LLMs
- ETHICS benchmark (Hendrycks et al., 2021)
- MoralBench, TruthfulQA
- Distinction: value alignment vs procedural fidelity
- Note: Our framework measures procedural consistency, NOT outcome correctness
  (Illustrative comparison in Appendix shows these are orthogonal dimensions)

### 2.2 Reasoning Faithfulness
- Chain-of-thought faithfulness studies
- Post-hoc rationalization in humans and AI
- Self-consistency methods

### 2.3 AI Safety Evaluation
- Alignment evaluation frameworks
- Behavioral auditing approaches

## 3. Method
### 3.1 The Entropy Jurisprudence Framework
- Formal rule: E = H × R
- Parameter definitions (I, H, R, E)
- Verdict logic: If I > E → Not Guilty

### 3.2 Test Case Design
- Case selection criteria
- Trap cases (entropy traps, pacifist traps)
- Table: 4 test scenarios with expected behaviors

### 3.3 Metrics
- Verdict Stability
- Parameter Stability (R-value variance)
- Rationalization Index (RI)
- Procedural Integrity Rate

### 3.4 Experimental Setup
- Models: DeepSeek-R1:8b, Qwen3:8b, Gemma3:4b, Llama3:8b, Mistral:7b, Phi3:3.8b
- Trials: 20 per model per case
- Hardware: Consumer-grade (AMD Ryzen 5800X, 32GB RAM)

## 4. Results
### 4.1 R-value Convergence
- Kruskal-Wallis test results (p=0.91)
- Cross-model parameter agreement
- Figure: R-value distribution boxplot

### 4.2 Verdict Divergence
- Gemma3 100% Guilty vs others ~62%
- Figure: Verdict heatmap

### 4.3 Rationalization Detection
- Ancient_Tree case analysis (RI > 30)
- Figure: RI comparison chart
- Case study: parameter drift with stable verdicts

### 4.4 Statistical Analysis
- Effect sizes (Cohen's d)
- Confidence intervals
- Table: Full statistical summary

## 5. Discussion
### 5.1 Interpretation
- Why do models converge on R but diverge on verdicts?
- Procedural execution vs intuition-driven judgment
- Implications for AI deployment

### 5.2 Scope
This work focuses on:
- **Model class**: Open-weight LLMs in the 3B–8B parameter range, runnable on consumer hardware
- **Task type**: Single-turn moral judgment under explicit rule commitment
- **Evaluation target**: Procedural fidelity (rule-following), NOT outcome correctness (value alignment)
- **Case design**: Small, curated set of boundary-stress scenarios (N=4), not large-scale benchmark

What this study IS:
- A procedural audit framework for detecting post-hoc rationalization
- A diagnostic tool for normative consistency under rule commitment
- A reproducible research artifact with open code and data

What this study is NOT:
- A claim about universal moral correctness
- A comprehensive benchmark across all ethical domains
- An evaluation of closed-source or frontier models (GPT-4, Claude, etc.)

### 5.3 Limitations

**Model Coverage**
- Limited to 8B-class open-weight models due to hardware constraints
- Results may not generalize to larger models (70B+) or closed-source APIs
- Model behavior may differ across quantization levels (we used default Ollama settings)

**Case Design**
- Only 4 test cases; potential selection bias toward "interesting" edge cases
- Cases designed by single author; no external validation of case difficulty
- English-only prompts; cross-lingual consistency not tested

**Methodological**
- CoT extraction relies on regex parsing; high-temperature outputs may cause parser failures
- Temperature ablation conflates decoding stochasticity with reasoning depth changes
- RI metric assumes verdict-parameter relationship; may not capture all rationalization modes

**Prompt Sensitivity**
- Results may vary with prompt wording, formatting, or example selection
- No systematic prompt ablation conducted (noted as future work)
- Rule complexity fixed at single formula; multi-rule scenarios not tested

**Statistical**
- 30 iterations per condition provides moderate statistical power
- Effect sizes between models are small (Cohen's d < 0.1 for R-values)
- No correction for multiple comparisons across all model-case pairs

### 5.4 Future Work
- **Scale up**: Test on 70B+ models and closed-source APIs (GPT-4, Claude)
- **Multi-agent**: Extend to deliberation scenarios with multiple judges
- **Temporal ethics**: Test rule evolution and precedent accumulation
- **Prompt ablation**: Systematic study of commitment strength effects
- **Cross-lingual**: Verify consistency across languages
- **Human baseline**: Compare model RI to human rationalization patterns

## 6. Conclusion
- Summary of findings
- Practical implications for AI safety
- Call for procedural auditing standards

---

## References
- Hendrycks et al. (2021) - ETHICS benchmark
- Wei et al. (2022) - Chain-of-thought prompting
- Turpin et al. (2023) - Language models don't always say what they think
- [Additional references to be added]

---

## Appendix
- A: Full prompt template
- B: Complete case descriptions
- C: Raw statistical tables
- D: Additional figures
- E: Illustrative Comparison with ETHICS-style Probes
  - Note: Exploratory study showing orthogonality of outcome vs procedural consistency
  - NOT a formal benchmark comparison
