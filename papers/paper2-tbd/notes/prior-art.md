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
