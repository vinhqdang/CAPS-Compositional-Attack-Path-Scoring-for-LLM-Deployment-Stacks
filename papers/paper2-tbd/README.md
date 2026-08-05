# Paper 2 — direction not yet settled

**Status:** Scoping. No formulation committed. No manuscript started.

## Why this is still `tbd`

The extension proposed in conversation (latent shared-primitive correlation + per-edge
friction + polynomial critical path + #P-hard aggregation + diversity as a control) was
checked against prior art and found to be **substantially not novel** — every component has
established precedent in either the classical attack-graph literature or the 2025–2026
agentic-security literature. See [`notes/prior-art.md`](notes/prior-art.md) for the
component-by-component assessment and citations.

Nothing should be built here until a direction survives a systematic prior-art search.

## Candidate directions

| Direction | Novelty | Effort | Fit |
|---|---|---|---|
| Calibration — measure $\alpha$ and $E$ from AgentDojo / InjecAgent / ASB | Low (delivers §5.4's promise) | Medium | Good for a journal extension |
| Automated topology extraction from LangGraph / MCP / OTel | Low–medium; AgentFlow occupies much of it | Medium | Tooling / systems venue |
| Budget-constrained mitigation placement | Low; graph-coloring and CySecTool precedent exists | Medium | Needs calibration first |
| Quantitative risk over agentic dataflow graphs (data→instruction confusion as the per-hop event) | Unclear — possibly partly occupied by arXiv:2606.20510 | High | Would need the systematic search first |

## Venue note

The stated target is a mid-tier journal extension, which typically requires 30–40% new
content — **not** a novel theorem. The calibration direction satisfies that bar and is
achievable; chasing novel mathematics in a field publishing this densely carries real risk of
being scooped mid-project. Worth deciding deliberately which constraint actually binds.

## Prerequisites regardless of direction

Paper 1 has published claims the shared library does not implement. Any follow-up inherits
them, so these come first — see the gap table in
[`../paper1-caps-jdsis/README.md`](../paper1-caps-jdsis/README.md):

1. Implement the $k_{max}$ bound the paper claims, or switch to Dijkstra over $-\log$
   weights and drop the bound honestly.
2. Write the missing scalability benchmark behind Table 4.
3. Derive or remove the $P_{node}=0.1$ zero-day residual.
4. Decide whether `Vulnerability.impact` and `Connection.trust_boundary` become live inputs
   or get removed from the schema.

## Ground rule

Paper 1's numbers are published. New scoring semantics go in a **new module**
(e.g. `caps/engine_corr.py`), never by mutating `caps/engine.py`.
