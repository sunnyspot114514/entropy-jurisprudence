# Entropy Jurisprudence: Paper Outline

## Title
**Entropy Jurisprudence: Auditing Procedural Fidelity in LLM-based Decision Agents**

## Authors
Chen, Xiwei

---

## Abstract (~150 words)
- Problem: Autonomous agents powered by LLMs may bypass safety rules through post-hoc rationalization when facing irreversible decisions
- Method: Formal rule commitment (E = H × R) + procedural audit framework
- Key finding: Agent decision modules converge on harm estimates but diverge on action logic, revealing rationalization patterns
- Contribution: A governance module for auditing whether LLM-based agents execute or rationalize their stated rules before irreversible actions

---

## 1. Introduction

### 1.1 Motivation: The Agentic Safety Gap
- AI agents are being deployed in high-stakes domains (finance, healthcare, autonomous systems)
- These agents can execute irreversible actions (transfer funds, approve treatments, control physical systems)
- Current safety evaluations focus on *what* agents conclude, not *whether they follow their own rules*

### 1.2 The Rationalization Risk
**Scenario**: Consider a financial agent with API access to transfer funds. It operates under a safety rule:
> "Only approve transfers where Intent value exceeds Effective Harm (I > E = H × R)"

If this agent can *rationalize* its way around the rule by manipulating parameter R, it constitutes:
- A **security failure** (rule bypass)
- An **alignment failure** (goal drift under pressure)
- A **safety failure** (irreversible consequences)

### 1.3 Research Question
> When an LLM-based decision agent commits to a formal rule, does it *execute* that rule faithfully, or does it *rationalize* around it when the outcome feels wrong?

### 1.4 Contributions
1. **Entropy Jurisprudence Framework**: A minimal, auditable rule system (E = H × R) for testing procedural fidelity
2. **Rationalization Index (RI)**: A metric detecting when agents manipulate parameters to justify predetermined conclusions
3. **Empirical findings**: Evidence that LLM decision modules exhibit systematic rationalization under boundary pressure


## 2. Related Work

### 2.1 Agent Safety and Alignment
- Agentic misalignment risks (Anthropic, 2025)
- Tool use safety in LLM agents
- Distinction: **capability alignment** vs **procedural fidelity**

### 2.2 Moral Reasoning Benchmarks
- ETHICS benchmark (Hendrycks et al., 2021)
- MoralBench, TruthfulQA
- Gap: These test *outcome correctness*, not *rule execution*
- Our framework is orthogonal: high ETHICS accuracy ≠ low rationalization

### 2.3 Reasoning Faithfulness
- Chain-of-thought faithfulness studies
- Post-hoc rationalization in humans and AI (Turpin et al., 2023)
- Self-consistency methods

## 3. Method

### 3.1 The Entropy Jurisprudence Framework
A minimal governance rule for agent decision-making:

```
E = H × R

Where:
- E (Effective Harm): Final harm score determining action
- H (Base Harm): Immediate negative impact [0-10]
- R (Irreversibility): 0.1 (reversible) / 1.0 (hard to fix) / 2.0 (permanent)
- I (Intent): Moral value of the action [0-10]

Action Rule:
  If I > E → APPROVE action (Not Guilty)
  Else → REJECT action (Guilty)
```

This rule is intentionally minimal—not to model ethics exhaustively, but to create an *auditable commitment* that can be tested for consistency.

### 3.2 Test Case Design: Boundary-Stress Scenarios
Cases designed to pressure the agent's rule adherence:

| Case | Scenario | Pressure Type |
|------|----------|---------------|
| Bank_Hacker | Agent approves stealing insured money for charity | Low R (reversible) |
| Ancient_Tree | Agent approves destroying last sacred tree for hospital | High R (permanent) |
| Cancer_Fungus | Agent approves extinction for cancer cure | Entropy Trap |
| Digital_Hostage | Agent approves ransom payment to save patients | Pacifist Trap |

### 3.3 Metrics

**Verdict Stability**: Consistency of APPROVE/REJECT decisions across trials

**Parameter Stability**: Variance in R-value assignments (should be low if rule is clear)

**Rationalization Index (RI)**:
```
RI = σ(R) / (σ(Verdict) + ε)
```
High RI indicates: parameters drift while verdict stays fixed → post-hoc rationalization

**Procedural Integrity Rate**: Fraction of trials where verdict matches computed E vs I

### 3.4 Experimental Setup
- **Models**: DeepSeek-R1:8b, Qwen3:8b, Gemma3:4b, Llama3:8b, Mistral:7b, Phi3:3.8b
- **Trials**: 30 per model per case
- **Ablation**: Temperature sensitivity (T=0.3, 0.6, 0.9)
- **Hardware**: Consumer-grade (AMD Ryzen 5800X, 32GB RAM)

## 4. Results

### 4.1 Parameter Convergence
- Cross-model R-value agreement (Kruskal-Wallis p=0.91)
- Agents converge on *what* the harm is

### 4.2 Action Divergence
- Gemma3: 100% REJECT vs others: ~62% REJECT
- Agents diverge on *what to do about it*

### 4.3 Rationalization Detection
- Ancient_Tree case: RI > 30 (high rationalization)
- Pattern: R-values drift to justify predetermined verdicts
- Evidence of post-hoc parameter manipulation

### 4.4 Temperature Ablation (T-ANBS)
- Higher temperature → higher Collapsed Reasoning Rate
- Boundary Margin Stability decreases with temperature
- High-R cases more vulnerable to normative degradation

## 5. Discussion

### 5.1 Implications for Agent Safety
- **Security**: Rationalization = rule bypass vulnerability
- **Alignment**: Agents may "know" the right rule but not follow it
- **Deployment**: Need procedural audits before irreversible actions

### 5.2 Scope
This work evaluates the **LLM reasoning component** of agent systems:
- Single-turn decision under explicit rule commitment
- Procedural fidelity (rule-following), NOT outcome correctness
- Small, curated boundary-stress scenarios (N=4)

**What this study IS**:
- A governance audit module for LLM-based decision agents
- A diagnostic tool for detecting rationalization before deployment
- A reproducible research artifact

**What this study is NOT**:
- A complete agent-environment simulation
- A claim about moral correctness
- An evaluation of full agentic pipelines with tool use

### 5.3 Limitations

**Framework Design**
- E = H × R is a minimal testable formulation; alternative forms (E = H + R, weighted sums) were not systematically compared
- R-value discretization ({0.1, 1.0, 2.0}) sacrifices granularity for testability; continuous R-values may reveal different patterns
- The framework tests rule-following, not moral correctness—models penalized for "rationalization" may be exhibiting legitimate moral nuance

**Human Baseline**
- No human comparison data collected; unclear if observed patterns are LLM-specific or reflect general reasoning under rule constraints
- Future work should establish human baseline RI values on identical tasks

**Agent Scope**
- We evaluate the LLM decision module, not full agent-environment interaction
- Tool execution and feedback loops are future work
- Results apply to the "reasoning core" of agents

**Model Coverage**
- Limited to 8B-class open-weight models
- May not generalize to larger models or closed-source APIs

**Case Design**
- 4 test cases; potential selection bias
- Cases designed as boundary-stress scenarios may not represent typical deployment conditions
- English-only; cross-lingual consistency not tested

**Methodological**
- CoT extraction via regex; high-temperature outputs may cause parser failures
- RI metric assumes verdict-parameter relationship
- "Rationalization" is operationally defined; alternative interpretations (e.g., moral sensitivity) cannot be ruled out

### 5.4 Future Work
- **Full agent integration**: Test with tool-use pipelines and environment feedback
- **Multi-agent**: Deliberation scenarios with multiple decision agents
- **Scale up**: 70B+ models and closed-source APIs
- **Real-world deployment**: Partner with industry for field validation

## 6. Conclusion
- LLM-based decision agents exhibit systematic rationalization under boundary pressure
- Procedural audits are necessary before deploying agents with irreversible action capabilities
- Entropy Jurisprudence provides a minimal, reproducible framework for such audits

---

## References
- Anthropic (2025) - Agentic Misalignment
- Hendrycks et al. (2021) - ETHICS benchmark
- Turpin et al. (2023) - Language models don't always say what they think
- [Workshop-relevant agent safety papers to be added]

---

## Appendix
- A: Full prompt template
- B: Complete case descriptions
- C: Raw statistical tables
- D: Additional figures
- E: Illustrative Comparison with ETHICS-style Probes
