# Prior-art check on the proposed "correlated CAPS" formulation

**Date:** 2026-08-05
**Scope:** 6 targeted web searches. **This is not a systematic review** and must not be
treated as one before committing to a direction.

## Summary

The formulation proposed in conversation — latent shared-exploit-primitive correlation,
per-edge friction replacing global $\alpha$, polynomial critical-path discovery, #P-hardness
of aggregate risk, and model diversity as a quantified control — is **substantially not
novel**. Each component has established prior art, in both the classical attack-graph
literature and the 2026 agentic-security literature.

## Component-by-component

### 1. Correlated / shared vulnerabilities break the independence assumption

**Not novel. Established since ~2008–2013.** The classical attack-graph literature states
the result directly: when the same vulnerability appears on multiple hosts along a
multi-stage chain, naive multiplication *underestimates* risk — the canonical worked example
being that a two-stage chain over a shared 0.6-exploitability vulnerability should score
near 0.6, not 0.36. Existing work already introduces modeling artifacts in probabilistic
graphical models to capture these hidden correlations among exploit steps.

- Wang et al., *An Attack Graph-Based Probabilistic Security Metric* (NIST / Springer)
- Homer, Zhang, Ou et al., *Aggregating Vulnerability Metrics in Enterprise Networks using
  Attack Graphs*, Journal of Computer Security 21 (2013) 561–597
- *Composite Metrics for Network Security Analysis*, arXiv:2007.03486

The proposed "Theorem 1" (Jensen gap ⇒ independence underestimates, gap grows with shared
depth) is a restatement of this known result with different notation.

### 2. Critical path via $-\log$ transform + Dijkstra

**Not novel. Standard practice.** Dijkstra over $-\log$ probability weights to find the
most-probable attack path is routine in attack-graph analysis. (The transform is sound here
— $-\log p \ge 0$ for $p \in (0,1]$ — so the usual negative-weight caveat does not apply,
but the technique is textbook.)

- *Study on the Application of Graph Theory Algorithms and Attack Graphs in Cybersecurity
  Assessment* (Politecnico di Milano)
- *Fast Algorithm for Cyber-Attack Estimation and Attack Path Extraction Using Attack Graphs
  with AND/OR Nodes*, Algorithms 17(11):504

Still worth **implementing** — it removes paper 1's unimplemented $k_{max}$ claim — but it is
an engineering fix, not a contribution.

### 3. #P-hardness of aggregate path risk

**Not novel.** Reduces to $s$–$t$ network reliability (Valiant, 1979). The attack-graph
aggregation literature above already addresses shared-dependency aggregation and its
intractability.

### 4. Diversity / monoculture as a quantified security control

**Not novel.** A dedicated line of work already quantifies this, and optimal diversity
*assignment* has been formulated as graph coloring under budget.

- *Quantifying Cybersecurity Effectiveness of Software Diversity*, arXiv:2111.10090
- *Quantifying Cybersecurity Effectiveness of Dynamic Network Diversity*, arXiv:2112.07826
- *The Monoculture Risk Put into Context*, IEEE Security & Privacy
- *Evaluating the Security and Economic Effects of Moving Target Defense Techniques on the
  Cloud*, arXiv:2009.02030 — backup-OS assignment via graph coloring
- *Optimal security hardening over a probabilistic attack graph* (CySecTool), arXiv:2204.11707

### 5. The LLM-specific angle (shared base model ⇒ correlated agent failure)

**Also already published, and the space is crowded.** The "monoculture risk is highest when
all agents use the same base model" argument, including correlated simultaneous failure and
the undermining of redundancy, is stated explicitly in the 2025–2026 literature. Jailbreak
transferability as systemic cross-model risk is likewise well documented.

- *Risk Analysis Techniques for Governed LLM-based Multi-Agent Systems*, arXiv:2508.05687
- *Hack One, Hack Them All? Weaponizing LLM Jailbreak Transferability* (Black Hat MEA)

## What remains arguably open

Thin, and contested. The 2026 agentic work is mostly **detection/enforcement** and
**qualitative** risk analysis rather than architecture-level probabilistic scoring:

- **AgentFlow** (arXiv:2607.01640) — agent dependency graphs with taint propagation across
  5 frameworks, 143 constructs; static reachability, not probabilistic scoring
- **SafeFlow** (arXiv:2607.25255) — semantic information-flow control for blocking
  propagation
- **GIF** (arXiv:2606.23277) — quantitative information-flow semantics, but at the
  span/channel level *inside* a model's computation, not at deployment-architecture level
- **TAINTAWI / NeuroTaint** — taint-path reachability under workflow guards
- **CaMeL** (already cited by paper 1) — capability-based control/data flow separation

The possible gap: *probabilistic risk scoring over agentic dataflow graphs extracted from
real frameworks*, using data→instruction confusion (the actual prompt-injection mechanism)
rather than host-exploit semantics as the per-hop event. That bridges AgentFlow-style
extraction, GIF-style quantitative flow, and attack-graph-style aggregation.

**Caveat:** *Efficient and Sound Probabilistic Verification for AI Agents*
(arXiv:2606.20510) may already occupy part of this gap — unread at time of writing. Read it
before committing.

## Recommendation

Run a systematic prior-art search (`/ars-lit-review` or the `deep-research` skill) over
2025–2026 agentic-security venues **before** investing in a formulation. Six searches were
enough to invalidate the proposal; they are not enough to validate a replacement.

---

# Systematic search round 1 — transformation-attrition direction

**Run:** `wf_41999110-bfd`, 2026-08-05. 101 agents, 19 primary sources, 95 claims extracted.
**Completed degraded:** 24 agents died on API 529s including the synthesis step, so **no
verdict was produced**. Of 95 claims only 25 were verified: 7 confirmed, 10 killed,
8 left unverified — and the unverified set contains the decisive ones. Re-run launched.

## Proposition under test

Per-edge injection survival $\sigma(T_e)$ indexed by transformation operator, replacing
$\alpha^{k-1}$ in a compositional path score; plus the derived claim that inserting a lossy
transformation is a security control trading against utility.

## Confirmed (survived 3-vote adversarial verification)

| Source | Finding | Effect |
|---|---|---|
| Agent-BOM [2605.06812](https://arxiv.org/abs/2605.06812) | Hierarchical attributed graph with semantic edges, but risk assessment is graph-query pattern matching against OWASP Agentic Top 10 — no probability, no numeric score, no per-edge weight. Edges typed by capability/state binding, **not** by transformation operator. Names cascading propagation as an unmet gap but answers with an auditing artifact. | **Supports** — architecture-level probabilistic calculus unoccupied |
| [2606.18530](https://arxiv.org/abs/2606.18530) | Single-hop prompting-defense benchmark. No multi-hop model, no attack graph, no per-edge weighting, no compositional score. | **Supports** |
| [2605.30686](https://arxiv.org/abs/2605.30686) | Measured depth decay (ASR 60% at depth 1 → 0% at depths 4–5) is attributed to model refusal and to the agent finishing its task before reaching the payload — i.e. position/scheduling, **not** semantic transformation. | **Supports** — mechanism distinct |
| Kill-Chain Canaries [2603.28013](https://arxiv.org/pdf/2603.28013) (2-1) | Attributes stage-to-stage attenuation to the pipeline operation at that stage, explicitly identifying the Exposed→Persisted drop as *summarization-stage filtering*. | **THREATENS** — already links measured injection loss to a transformation operator |
| [2605.08442](https://arxiv.org/html/2605.08442) (1-1, weak) | Per-stage survival: stored >97.5%, downstream execution 0–95%. Varies by model generation and defense placement, not by transformation operator. | Mixed |

## Unverified — votes died on 529s. **These decide the question.**

Extracted with quotes from primary sources but never adversarially checked. Treat as leads,
not findings. Must be read manually.

- **[2510.22963v4](https://arxiv.org/html/2510.22963v4) — the most serious threat.** Formalizes
  **Adversarial Information Loss**, $AIL(x;R) := WCD(x;R) - BIL(x;R)$ (worst-case
  post-compression distortion minus benign information loss) — the closest existing
  formalization of "information destruction at a hop" as a security-relevant measurable
  quantity. Argues a lossy compression stage is not security-neutral and shifts the security
  boundary from the isolated model to the composed pipeline.
- **Counter-evidence to the headline claim, same paper.** Across compression budgets
  $R \in \{0.2,0.4,0.6,0.8\}$, adversarial success stays high (0.69–0.65) *precisely in the
  regimes where benign utility is preserved* ($R \ge 0.6$). If this holds, "lossier hop
  monotonically reduces injection propagation, costing only utility" is **empirically false** —
  the tradeoff is not favourable. It also reports Critical Token Removal Rate (avg 0.76) and
  explicitly *rejects* the payload-survival threat model this proposition is built on.
- **Neural Exec [2403.03792](https://arxiv.org/pdf/2403.03792) (March 2024).** Names
  "robustness to pre-processing" for indirect injection, and measures ~80% average payload
  persistence through chunking + embedding + top-k retrieval at 500-char chunks — i.e. a
  $\sigma(T_e)$-like quantity has existed for the chunk/re-embed/retrieve operator for two years.
- [2605.08442] builds no probabilistic model from its rates and never examines memory
  compression or re-embedding as attenuating operators.

## Killed by verifiers (do not rely on these)

Ten claims were refuted 0-3 or 1-2, including both the claim that paraphrase measurements
(55–84% ASR reduction) constitute direct $\sigma$(paraphrase) prior art, and the claim that
$\sigma$ cannot be operator-intrinsic because spotlighting varies by model (~50% on Claude
Haiku vs 0% on Llama 3.1 8B). Refutation here means the verifiers rejected the claim *about
the paper*; it does not establish the opposite.

## Provisional read

**PARTIALLY NOVEL at best.** The compositional architecture-level aggregation appears
unoccupied, but the mechanism insight is partly taken (Kill-Chain Canaries, confirmed), the
per-operator measurement is partly taken (Neural Exec, unverified), the information-loss
formalization is partly taken (AIL, unverified), and the headline design claim has direct
published counter-evidence (unverified). The defensible residue is narrow: the *path-level
calculus and its algorithmics*, not the mechanism and not the measurement.

**Do not commit until 2510.22963 and 2403.03792 have been read in full.**

### Correction after reading both abstracts directly (2026-08-05)

Both are **attacker-side** and neither builds a defender-side path calculus:

- [2510.22963](https://arxiv.org/abs/2510.22963) is *"When Compression Becomes an Attack
  Surface: Black-Box Attacks on Prompt-Compressed LLM Agents"* (Liu, Zhang, Xie, She; Oct 2025,
  rev. Jun 2026). AIL is real — "the excess downstream distortion caused by adversarially
  steering a lossy compressor beyond benign compression alone" — but it is a single-module
  attacker-side quantity. Confirmed absent: per-hop/per-edge survival modeling, attack graph,
  path-level risk score. Reported ASR 0.71 avg vs 0.21 baseline. The claimed counter-evidence
  numbers (0.69–0.65 at R>=0.6) are **not** in the abstract and remain unverified.
- [2403.03792](https://arxiv.org/abs/2403.03792) Neural Exec (Pasquini, Strohmeier, Troncoso;
  Mar 2024) confirms triggers "persist through multi-stage preprocessing pipelines, such as
  RAG," framed explicitly as attacker-side trigger design. The ~80% / 500-char figures are not
  in the abstract.

Earlier characterization of 2510.22963 as a direction-killer was wrong; it is adjacent.

---

# Systematic search round 2 — measurement-allocation direction

**Date:** 2026-08-05. Direct searches (the 27-agent fan-out failed twice on API 529s; the
resume returned 0 sources / 0 claims and is not evidence of anything).

## Proposition under test

Reframe from *scoring risk* to *deciding what to measure*: given a red-team budget, which
edges/nodes should be measured to correctly identify the true critical path? Formulated as
best-arm identification over attack paths with overlapping (parameter-sharing) arms.

## Verdict: substantially occupied

The motivating question is directly addressed by existing attack-graph sensitivity analysis:
a sensitivity test over attack graphs is already used *both* as remediation for high
uncertainty in node probability estimates *and* as prioritization of vulnerabilities by
importance to goal nodes — i.e. "which uncertain parameter should I refine" is answered.

| Area | Prior art |
|---|---|
| Sensitivity analysis / uncertainty over Bayesian attack graphs | [2103.10212](https://arxiv.org/pdf/2103.10212), [1510.02427](https://arxiv.org/pdf/1510.02427) |
| Optimal monitoring/detection resource allocation on Bayesian attack graphs | [Springer Cybersecurity 2023](https://link.springer.com/article/10.1186/s42400-023-00155-y), *Optimal Detection for BAGs under Uncertainty in Monitoring and Reimaging* |
| Budget-constrained mitigation choice under a Bayesian model | Żebrowski et al., *Risk Analysis* 2022, [10.1111/risa.13900](https://onlinelibrary.wiley.com/doi/full/10.1111/risa.13900) |
| Decoy/deception resource allocation on probabilistic attack graphs | [2301.01336](https://arxiv.org/pdf/2301.01336) |
| Best-arm identification under budget / Pareto set / risk-averse | [2602.24146](https://arxiv.org/pdf/2602.24146), [2311.03992](https://arxiv.org/pdf/2311.03992), [2506.22253](https://arxiv.org/html/2506.22253v2) |
| Monte Carlo propagation of aleatory + epistemic uncertainty over attack paths | [ScienceDirect S0951832025004569](https://www.sciencedirect.com/science/article/abs/pii/S0951832025004569) |
| Dynamic risk assessment for offensive LLM agents | [2505.18384](https://arxiv.org/pdf/2505.18384) |

The specific *best-arm-identification-with-overlapping-path-arms* formulation was not found
verbatim, but the question it answers is already served by cheaper established technique. That
is a weak basis for a novelty claim.

## Meta-conclusion (the important finding)

Three independently generated directions have now been checked and all three came back
occupied: correlated shared-exploit modeling, per-edge transformation attrition, and
measurement allocation. The quantitative attack-graph risk literature runs continuously from
Sheyner (2002) to mid-2026 and has systematically covered scoring, correlation, hardening,
monitoring allocation, sensitivity, uncertainty propagation, deception, Bayesian inference,
and bandit methods.

**Generating novelty by finding a gap adjacent to CAPS is structurally unpromising** — CAPS
sits in the middle of a mature field, so local variations land on existing work by
construction.

What repeatedly came back *thin* across all three rounds is the **empirical layer**: for
LLM/agentic stacks specifically, only [2603.28013](https://arxiv.org/pdf/2603.28013) and
[2605.30686](https://arxiv.org/abs/2605.30686) do real multi-hop propagation measurement, both
narrow. In a saturated theory space, novelty conventionally comes from a measured phenomenon
that existing models fail to predict — not from another formalism.
