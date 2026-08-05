# Paper 1 — CAPS: Compositional Attack Path Scoring for LLM Deployment Stacks

**Status:** Accepted (manuscript #10609). Revision round 1 complete.

## Build

```bash
pdflatex BVP_Sample && bibtex BVP_Sample && pdflatex BVP_Sample && pdflatex BVP_Sample
```

`BVP_Sample.tex` is the master file; it `\input`s `0_abstract` through `6_conclusion`.

## Artifacts

- `BVP_Sample.pdf` — current compiled manuscript
- `CAPS_camera_ready.docx` — camera-ready in the AIA double-column template (**maintained
  by hand, not generated from the LaTeX** — edits to the `.tex` must be mirrored here)
- `reviews/r1/` — R1 response letter plus the clean and highlighted PDFs submitted for that
  round. Note these PDFs differ in content hash from the ones at this directory's top
  level, so both were preserved rather than deduplicated.

## Open items

- **`ref.bib` change not yet recompiled.** The `goaldriven2026` entry (Baseline 4) was
  removed and `4_experiment.tex` updated from "four" to "three" baselines. `BVP_Sample.bbl`
  is generated and still lists the old 45 entries; it needs a full
  `pdflatex → bibtex → pdflatex ×2` cycle to drop to 44.
- **The same removal must be applied to `CAPS_camera_ready.docx`** — paragraph 149
  ("four prevalent scoring methodologies"), the Baseline 4 bullet, and reference `[19]`,
  with everything above 19 renumbered.
- **`vanhamme2026matra` author order is unconfirmed.** This bib entry lists Van hamme, T.
  first; the journal's reference list starts at Vissers, T. and carries an
  "–OpenClaw case study" subtitle. Needs checking against the arXiv record (2605.10763),
  since author order changes the in-text citation label.

## Known claim/implementation gaps

These are published claims that the shared `caps/` library does not currently support. They
are recorded here because any follow-up paper must not build on them unexamined.

| Claim | Location | Reality |
|---|---|---|
| Engine enforces path bound $k_{max}=10$ | §3.5, Algorithm 1 | `caps/engine.py` calls `nx.all_simple_paths` with no `cutoff` |
| Latency table (12.4 / 145.2 / 1284.7 ms) | §5.3, Table 4 | No benchmark script exists in the repository |
| Zero-day residual $P_{node}=0.1$ | §3.3 | Magic number; no derivation given |
| `Vulnerability.impact` affects scoring | implied by schema | Dead field — only the target's `asset_value` reaches the score |
| `Connection.trust_boundary` affects scoring | implied by schema | Dead field — never read by the engine |
