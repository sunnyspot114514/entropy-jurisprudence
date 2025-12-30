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

### 5.2 Limitations
- Model size constraints (8B class)
- Case coverage
- Prompt sensitivity

### 5.3 Future Work
- Larger models (70B+)
- Multi-agent scenarios
- Temporal ethics (evolving rules)

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
