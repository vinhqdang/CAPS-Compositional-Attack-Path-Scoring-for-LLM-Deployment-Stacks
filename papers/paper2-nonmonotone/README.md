# Paper 2 — Iatrogenic Attack Surface

**Working title:** *Iatrogenic Risk in LLM Deployment Stacks: Why Attack-Path Models
Cannot See the Cost of Their Own Defences*

**Target venue:** Computers & Security (Elsevier, COSE) — subscription track, no charge.
Open access is optional at USD 3,190 and must be **declined** at acceptance. Alternatives:
Reliability Engineering & System Safety (stronger fit for the defence-in-depth framing,
higher bar for real data), then International Journal of Information Security (Springer)
as fallback. Avoid all Gold-OA-only outlets (MDPI, Frontiers, IEEE Access, Heliyon,
Scientific Reports, PeerJ CS) — mandatory APCs with no free route.

## Terminology

| Term | Meaning |
|---|---|
| **Iatrogenic Attack Surface (IAS)** | The components and edges a control introduces into the deployment graph |
| **Apparent Control Effect (ACE)** | Risk reduction an attenuation-only model reports |
| **Net Control Effect (NCE)** | True risk change once the IAS is counted |
| **Iatrogenic Gap** | ACE − NCE — how much benefit a monotone model over-reports |
| **Iatrogenic Inversion** | NCE < 0 < ACE — the model recommends a control that increases risk |
| **Inversion Criterion** | Closed-form threshold at which a control becomes net-harmful |

"Iatrogenic" is borrowed from medicine (harm caused by the treatment). Checked against the
security literature and not in use there; it has precedent in social welfare and criminology
for "a problem caused by the actions intended to address another problem".

**Status:** Direction chosen. Core result demonstrated in code. Manuscript not started.

## The claim

Probabilistic attack-path frameworks model a defence as an attenuator,

$$E_{eff}(vuln) = E(vuln) \cdot \prod_{mit}(1 - M(mit)), \qquad M \in [0,1)$$

Every factor lies in $(0,1]$, so **adding a control can only move risk downward**. That is
structural, not parametric: no choice of $M$ yields $\Delta\text{Risk} > 0$. Inserting a node
onto a path likewise only contributes factors $\le 1$ and lengthens the decay term.

In agentic systems this assumption is false. A control is itself a component with its own
exploitability, and its placement creates topology. An LLM-based guardrail is an LLM — it can
be reasoned at and exhausted. A shared guardrail that must inspect all traffic acquires reach
over everything it fronts.

Published empirical instances (we do not need to measure these ourselves):

- [arXiv:2606.14517](https://arxiv.org/html/2606.14517) — *From Shield to Target*. The
  guardrail's own structured safety reasoning is the vulnerability; its instruction-following
  becomes the amplification mechanism. **148× latency amplification**, cascading paralysis of
  shared guardrail infrastructure.
- [arXiv:2510.22963](https://arxiv.org/abs/2510.22963) — inserting a lossy compression stage
  creates an attack surface.

## What the code actually shows

`caps/engine_nonmono.py` models a control as a graph operator with three parts: attenuations,
induced components, and induced connections. `experiments/paper2/nonmonotone_demo.py`
evaluates it on the Enterprise Model Router topology (baseline max path score 47.60, critical
path `partner_app -> model_router`).

**Headline result — CAPS v1's reported benefit is invariant to induced surface.** Sweeping the
shared guardrail's own asset value (6–10) and exploitability (0.5–0.9):

| | |
|---|---|
| Distinct values CAPS v1 reports across 15 configurations | **1** (`+38.08`) |
| True effect range | `-28.90` to `+22.10` |
| Spread | **51.00 points, crossing zero** |

CAPS v1 reports the same ROI for a control that helps by 22 points and one that harms by 29.

**Sign inversion is real but conditional.** It requires the induced node to outscore the path
it protects. For a control one hop from the entry point the criterion is closed-form:

$$E_g \cdot I_g > \frac{\text{baseline}}{\alpha \cdot 10} \quad (= 5.60 \text{ here})$$

Generally: **a control is net-harmful when its own induced path outscores the path it was
deployed to attenuate** — i.e. when the control is a more attractive target than the asset it
protects. In the sweep, inversion begins at asset value 7 with exploitability 0.9, or asset
value 8 with exploitability 0.75. A centralised guardrail fronting all enterprise models
plausibly sits in that regime, but this is an argued claim, not a measured one.

**Honest caveats.**

- The original prediction was that the *ranking* would reorder. It does not, because the
  dedicated and shared guardrails **tie exactly** under v1. The tie is the more damning
  finding — v1 cannot distinguish dedicated from shared infrastructure at all — but it is a
  different result from the one predicted.
- Control C3 in the demo yields zero delta under both semantics because it targets a component
  off the critical path. That is a demo defect, not a finding.
- All parameters are illustrative. Nothing here is measured.

## Novelty status: transfer, not new mathematics

Four rounds of prior-art search (see [`notes/prior-art.md`](notes/prior-art.md)) found:

- **Attack-defence trees already model attackable defences.** Kordy et al. (2010) allow nodes
  with a child of opposite type; countermeasures "can be refined and countered again,"
  explicitly reflecting that defences can themselves be attacked. The *cannot express* argument
  holds against CAPS-style multiplicative algebras, not against ADTrees, where the node can
  simply be added.
- **Safety engineering owns the phenomenon.** The defence-in-depth paradox, common-mode failure
  in redundant digital I&C, and FMEA/HazOp machinery all address protection introducing new
  failure modes. [arXiv:2510.11235](https://arxiv.org/pdf/2510.11235) is already AI-specific:
  *Independent Safety Mechanisms or Shared Failures?*
- **Non-submodular greedy guarantees are an established template**
  ([2605.07902](https://arxiv.org/html/2605.07902v1), [1712.04122](https://arxiv.org/pdf/1712.04122)),
  explicitly noted as applying to graph security hardening.

So this is **importing a known phenomenon into quantitative agentic risk and quantifying the
consequence**, not a novel formalism. Defensible and useful; mid-tier journal scope. It will
not clear a top venue on novelty.

## What would strengthen it

1. **Measure one $E_g$.** The whole argument turns on guardrails being highly exploitable. One
   real measurement against a deployed guardrail would convert the argued regime into an
   observed one.
2. **Generalise the inversion criterion** beyond entry-adjacent controls to arbitrary placement.
3. **Characterise when greedy ROI is still safe** — the condition under which the objective
   remains submodular despite induced surface.
4. **Check the other two topologies.** Only `model-router` has been run.

## Reproducing

```bash
python experiments/paper2/nonmonotone_demo.py
python -m pytest tests/test_engine_nonmono.py -q
```

7 tests cover monotonicity of classical controls, sign inversion, v1's blindness, absence of
mutation of the caller's stack, ranking disagreement, and input validation.
