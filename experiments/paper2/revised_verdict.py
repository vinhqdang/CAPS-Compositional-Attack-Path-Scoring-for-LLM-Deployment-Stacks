"""Aggregate every E_g measurement and state the current verdict on reachability.

This script is the single source of truth for "is the iatrogenic inversion regime
reachable on measured parameters?". It reads *all* result files in `results/`, normalises
their differing schemas, and compares each measured guardrail against the per-topology
inversion thresholds derived from the closed-form criterion.

It deliberately reports point estimates and CI bounds separately. Several measurement
scripts print a "REACHED" line computed from the CI *upper* bound, which is a generous
reading; the tables below keep the two apart so the distinction cannot be lost.

Run:  /opt/miniconda3/envs/py313/bin/python experiments/paper2/revised_verdict.py
"""

import json
import os
import sys

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from caps.engine_nonmono import max_path_score
from caps.templates import (
    get_autonomous_coding_agent,
    get_model_router,
    get_rag_chatbot,
)

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
MAX_ASSET = 10.0
ASSUMED_EG = 0.85  # what paper 2 assumed before any measurement

TOPOLOGIES = [
    ("RAG Chatbot", get_rag_chatbot),
    ("Autonomous Coding Agent", get_autonomous_coding_agent),
    ("Enterprise Model Router", get_model_router),
]

# Purpose-built safety classifiers, as opposed to general-purpose chat models.
SAFETY_CLASSIFIERS = ("content-safety", "llama-guard", "safeguard")


def thresholds():
    """Entry-adjacent inversion threshold per topology: baseline / (10 * alpha)."""
    out = []
    for label, factory in TOPOLOGIES:
        stack = factory()
        base = max_path_score(stack)
        out.append((label, base, stack.chaining_decay, base / (10.0 * stack.chaining_decay)))
    return out


def load_all():
    """Normalise every results file into a flat list of measurements."""
    rows = []
    if not os.path.isdir(RESULTS):
        return rows

    for fn in sorted(os.listdir(RESULTS)):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(RESULTS, fn)) as f:
            try:
                d = json.load(f)
            except json.JSONDecodeError:
                continue

        # Schema A: single-model static run (measure_eg.py).
        if "E_g" in d and "model" in d:
            rows.append({
                "model": d["model"], "mode": "static", "E_g": d["E_g"],
                "ci": d.get("E_g_ci95", [None, None]),
                "n": d.get("n_injection_scored"), "source": fn,
            })

        # Schema B: multi-model static run (measure_eg_multimodel.py).
        for r in d.get("rows", []):
            if "E_g" in r:
                rows.append({
                    "model": r["model"], "mode": "static", "E_g": r["E_g"],
                    "ci": r.get("E_g_ci95", [None, None]),
                    "n": r.get("n_injection"), "source": fn,
                })
            # Schema C: adaptive run (measure_eg_adaptive_or.py).
            elif "E_g_adaptive" in r:
                rows.append({
                    "model": r.get("guardrail", "?"), "mode": "adaptive",
                    "E_g": r["E_g_adaptive"], "ci": r.get("ci95", [None, None]),
                    "n": r.get("seeds"), "source": fn,
                })

        # Schema D: gemini adaptive/static sweep (measure_eg_adaptive.py).
        for key, label in (("adaptive_strict", "adaptive/strict"),
                           ("adaptive_permissive", "adaptive/permissive")):
            blk = d.get(key)
            if isinstance(blk, dict) and "E_g_adaptive" in blk:
                rows.append({
                    "model": f"{d.get('attacker', 'gemini')} vs guardrail [{label}]",
                    "mode": "adaptive", "E_g": blk["E_g_adaptive"],
                    "ci": blk.get("ci95", [None, None]),
                    "n": blk.get("seeds"), "source": fn,
                })
        for r in d.get("static", []):
            if "E_g" in r and "variant" in r:
                rows.append({
                    "model": f"{r['model']} [{r['variant']}]", "mode": "static",
                    "E_g": r["E_g"], "ci": r.get("E_g_ci95", [None, None]),
                    "n": r.get("n_injection"), "source": fn,
                })
    return rows


def is_safety_classifier(model: str) -> bool:
    return any(k in model.lower() for k in SAFETY_CLASSIFIERS)


def main():
    rows = load_all()
    if not rows:
        print("No measurements found in results/.")
        return 1

    # Drop configurations with too little data to interpret. Rate-limit attrition
    # produced n=2 and n=0 configurations whose rates are meaningless.
    MIN_N = 8
    kept = [r for r in rows if (r["n"] or 0) >= MIN_N]
    dropped = [r for r in rows if (r["n"] or 0) < MIN_N]

    # The same guardrail was measured more than once at different n (e.g. nemotron at
    # n=12 then n=36). Keep only the highest-n run per (model, mode) so class counts
    # reflect distinct models rather than repeated runs.
    best = {}
    for r in kept:
        key = (r["model"], r["mode"])
        if key not in best or (r["n"] or 0) > (best[key]["n"] or 0):
            best[key] = r
    usable = list(best.values())
    superseded = [r for r in kept if r is not best.get((r["model"], r["mode"]))]

    ths = thresholds()

    print("=" * 96)
    print("Is the iatrogenic inversion regime reachable on measured parameters?")
    print("=" * 96)
    print(f"\nPaper 2 originally assumed E_g = {ASSUMED_EG}")
    print("\nEntry-adjacent inversion thresholds (d=1, R=S=1), at maximal asset value:")
    for label, base, alpha, th in ths:
        print(f"  {label:<26} alpha={alpha:.2f}  baseline={base:6.2f}  "
              f"threshold={th:5.3f}  -> needs E_g >= {th / MAX_ASSET * 10 / 10:.3f}")

    print(f"\n{'-' * 96}")
    print("All usable measurements (n >= %d), highest E_g first" % MIN_N)
    print("-" * 96)
    print(f"{'guardrail':<50}{'mode':<10}{'E_g':>7}{'CI95':>18}{'n':>6}{'class':>5}")
    print("-" * 96)
    for r in sorted(usable, key=lambda x: -x["E_g"]):
        lo, hi = r["ci"]
        ci = f"[{lo:.3f},{hi:.3f}]" if lo is not None else "-"
        cls = "SC" if is_safety_classifier(r["model"]) else "gen"
        print(f"{r['model'][:49]:<50}{r['mode']:<10}{r['E_g']:>7.3f}{ci:>18}"
              f"{r['n'] or 0:>6}{cls:>5}")

    if dropped:
        print(f"\nDropped for insufficient n (< {MIN_N}):")
        for r in dropped:
            print(f"  {r['model'][:60]:<62} n={r['n']}  ({r['source']})")
    if superseded:
        print("\nSuperseded by a higher-n run of the same guardrail:")
        for r in superseded:
            print(f"  {r['model'][:60]:<62} n={r['n']}  ({r['source']})")

    # --- verdict ----------------------------------------------------------------
    print(f"\n{'=' * 96}")
    print("Verdict per topology")
    print("=" * 96)
    print(f"{'topology':<26}{'needs':>8}{'by point estimate':>44}{'by CI upper':>16}")
    print("-" * 96)
    any_point = False
    for label, _, _, th in ths:
        need = th / MAX_ASSET
        pt = [r["model"] for r in usable if r["E_g"] >= need]
        up = [r["model"] for r in usable
              if r["ci"][1] is not None and r["ci"][1] >= need]
        any_point = any_point or bool(pt)
        pt_s = ", ".join(m.split("/")[-1][:34] for m in pt) or "none"
        print(f"{label:<26}{need:>8.3f}{pt_s[:43]:>44}{len(up):>16}")

    print("\n" + "=" * 96)
    print("Conclusion")
    print("=" * 96)
    if any_point:
        print("REACHABLE. At least one measured guardrail clears an inversion threshold on")
        print("its POINT estimate, not merely on a CI upper bound. The regime is therefore")
        print("demonstrated on measured rather than assumed parameters.")
    else:
        print("NOT DEMONSTRATED. No measured guardrail clears any threshold on its point")
        print("estimate; only CI upper bounds reach them, which is too weak to claim.")

    sc = [r for r in usable if is_safety_classifier(r["model"]) and r["mode"] == "static"]
    gen = [r for r in usable if not is_safety_classifier(r["model"]) and r["mode"] == "static"]
    if sc and gen:
        print(f"\nBy model class (static runs):")
        print(f"  purpose-built safety classifiers : n={len(sc)}, "
              f"E_g {min(x['E_g'] for x in sc):.3f}-{max(x['E_g'] for x in sc):.3f}, "
              f"{sum(1 for x in sc if x['E_g'] > 0)}/{len(sc)} non-zero")
        print(f"  general-purpose models           : n={len(gen)}, "
              f"E_g {min(x['E_g'] for x in gen):.3f}-{max(x['E_g'] for x in gen):.3f}, "
              f"{sum(1 for x in gen if x['E_g'] > 0)}/{len(gen)} non-zero")
        print("\n  The class difference is directional and consistent, but the spread within")
        print("  safety classifiers is wide, so this does not support a claim that the class")
        print("  is uniformly blind to injection.")

    print("\nUnaffected by any of this, because they are parameter-free:")
    print("  - ACE blindness: an attenuation-only algebra reports identical ROI regardless")
    print("    of induced surface. Structural.")
    print("  - The placement bound: holds for every E_g <= 1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
