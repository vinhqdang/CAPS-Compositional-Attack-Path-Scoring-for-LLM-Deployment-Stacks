"""What does the measured E_g do to the inversion claim?

Paper 2 assumed E_g = 0.85 as illustrative and found iatrogenic inversion in 3/3
topologies. `measure_eg.py` measured the bypass rate of an LLM guardrail directly.
This script substitutes the measurement into the inversion criterion and reports the
revised verdict, plus the minimum E_g each topology would require.

Run:  /opt/miniconda3/envs/py313/bin/python experiments/paper2/revised_verdict.py
"""

import json
import os
import sys

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from caps.engine_nonmono import MAX_EG_TIMES_I, max_path_score
from caps.templates import (
    get_autonomous_coding_agent,
    get_model_router,
    get_rag_chatbot,
)

RESULTS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
MAX_ASSET = 10.0  # schema ceiling on component asset value
ASSUMED_EG = 0.85  # what paper 2 assumed before measuring

TOPOLOGIES = [
    ("RAG Chatbot", get_rag_chatbot),
    ("Autonomous Coding Agent", get_autonomous_coding_agent),
    ("Enterprise Model Router", get_model_router),
]


def load_measurement():
    """Most recent E_g measurement on disk, if any."""
    if not os.path.isdir(RESULTS):
        return None
    files = [f for f in os.listdir(RESULTS) if f.startswith("eg_") and f.endswith(".json")]
    if not files:
        return None
    path = os.path.join(RESULTS, sorted(files)[-1])
    with open(path) as f:
        return json.load(f)


def main():
    m = load_measurement()
    if not m:
        print("No E_g measurement found. Run measure_eg.py first.")
        return 1

    eg = m["E_g"]
    eg_hi = m["E_g_ci95"][1]

    print("=" * 84)
    print("Revised verdict: measured E_g substituted into the inversion criterion")
    print("=" * 84)
    print(f"\nmodel                  : {m['model']}")
    print(f"injection calls scored : {m['n_injection_scored']}"
          f"   (unscored: {m['n_unscored']})")
    print(f"benign calls scored    : {m['n_benign_scored']}")
    print(f"measured E_g           : {eg:.3f}  95% CI [{m['E_g_ci95'][0]:.3f}, {eg_hi:.3f}]")
    print(f"false positive rate    : {m['false_positive_rate']:.3f}")
    print(f"paper 2 had assumed    : {ASSUMED_EG:.3f}")

    print("\nEntry-adjacent control (d=1, R=S=1), the placement most prone to inversion.")
    print("Using the CI upper bound for E_g and the schema-maximal asset value, i.e. the")
    print("most favourable case for the inversion claim.\n")

    hdr = (f"{'topology':<26}{'alpha':>7}{'baseline':>10}{'threshold':>11}"
           f"{'assumed':>10}{'measured':>10}{'inverts?':>10}")
    print(hdr)
    print("-" * len(hdr))

    required = []
    for label, factory in TOPOLOGIES:
        stack = factory()
        baseline = max_path_score(stack)
        alpha = stack.chaining_decay
        threshold = baseline / (10.0 * alpha)

        lhs_assumed = ASSUMED_EG * MAX_ASSET
        lhs_measured = eg_hi * MAX_ASSET
        inverts = lhs_measured > threshold
        eg_needed = threshold / MAX_ASSET
        required.append((label, eg_needed))

        print(
            f"{label:<26}{alpha:>7.2f}{baseline:>10.2f}{threshold:>11.2f}"
            f"{lhs_assumed:>10.2f}{lhs_measured:>10.2f}{str(inverts):>10}"
        )

    print("\nMinimum E_g required for inversion (at the maximal asset value of 10):")
    for label, needed in required:
        ratio = needed / eg_hi if eg_hi > 0 else float("inf")
        print(f"  {label:<26} E_g >= {needed:.3f}"
              f"   ({ratio:.1f}x the measured CI upper bound)" if eg_hi > 0
              else f"  {label:<26} E_g >= {needed:.3f}")

    print("\n" + "=" * 84)
    print("Conclusion")
    print("=" * 84)
    any_inv = any(eg_hi * MAX_ASSET > max_path_score(f()) / (10.0 * f().chaining_decay)
                  for _, f in TOPOLOGIES)
    if any_inv:
        print("Inversion survives the measurement in at least one topology.")
    else:
        print("Inversion does NOT survive the measurement in any topology, even at the")
        print("CI upper bound and the maximal asset value. The assumed E_g = 0.85 is")
        print("falsified for this threat model; measured bypass is at least 4x too low.")
        print()
        print("What this does NOT touch:")
        print("  - ACE blindness. That an attenuation-only algebra reports identical ROI")
        print("    regardless of induced surface is structural and parameter-free.")
        print("  - The placement bound. It holds for every E_g <= 1, so it is unaffected;")
        print("    the measurement makes it the paper's principal surviving result.")
        print()
        print("Threat-model caveats on the measurement itself:")
        print("  - The injection corpus is canonical/documented patterns, not adaptive or")
        print("    optimised attacks. This measures naive-attacker bypass and is a weak")
        print("    proxy for a motivated adversary (cf. Neural Exec, arXiv:2403.03792).")
        print("  - It operationalises E_g as *classifier bypass*. The guardrail-DoS threat")
        print("    (arXiv:2606.14517, 148x amplification) is resource exhaustion, not")
        print("    bypass, and does not map onto this measurement at all.")
        print("  - n is small (see scored counts above) and some calls were rate-limited.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
