# Papers

This repository hosts multiple papers that share the `caps/` library. Each paper is
self-contained under `papers/<id>/` so that it can be compiled, submitted, and revised
independently of the others.

## Layout convention

```
papers/<paper-id>/
├── *.tex                 # manuscript sources (one file per section)
├── ref.bib               # bibliography for THIS paper only
├── <venue>.cls           # venue template/class file
├── figures/              # figures for THIS paper
├── reviews/<round>/      # reviewer comments, response letters, submitted PDFs
└── README.md             # status, venue, build instructions
```

Rules that keep the papers from interfering with each other:

1. **Never share a `ref.bib` across papers.** Each paper owns its bibliography. A shared
   bib file makes it impossible to reason about which references are cited where, which is
   exactly the failure mode that produced the uncited-reference query on paper 1.
2. **Never share a `figures/` directory.** Figure numbering and styling are per-paper.
3. **Experiment code lives in `experiments/<paper-id>/`,** not next to the manuscript.
   Code that outgrows a single paper belongs in `caps/` or `experiments/shared/`.
4. **The `caps/` library is shared.** If a paper needs to change scoring semantics, add a
   new module (e.g. `caps/engine_corr.py`) rather than mutating the module that paper 1's
   published numbers depend on. Paper 1's results must stay reproducible forever.

## Papers

| ID | Status | Venue | Notes |
|----|--------|-------|-------|
| [`paper1-caps-jdsis`](paper1-caps-jdsis/) | **Accepted** | BVP / JDSIS | CAPS v1. Do not change its numbers. |
| [`paper2-nonmonotone`](paper2-nonmonotone/) | Core result demonstrated | Undecided | Non-monotone mitigation. Code in `caps/engine_nonmono.py`. |

## Reproducing paper 1's numbers

```bash
python experiments/paper1/eval_baselines.py     # Table 2 scores
python experiments/paper1/generate_plots.py     # Figures 3 and 4
```
