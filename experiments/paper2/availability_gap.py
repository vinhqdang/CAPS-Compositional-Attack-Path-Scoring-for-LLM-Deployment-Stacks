"""The guardrail-DoS threat is unrepresentable in a scalar impact model.

arXiv:2606.14517 reports that a reasoning guardrail can be driven into extended
deliberation, giving 148x latency amplification and paralysing shared guardrail
infrastructure. That threat has near-zero confidentiality impact and large availability
impact. CAPS v1 scores paths against a single scalar ``asset_value``, so there is no
coefficient that can express it.

This script deploys one shared guardrail and scores it twice:

  1. Scalar (CAPS v1 semantics) -- the guardrail's asset value is one number.
  2. Dimension-aware -- the guardrail is a *low* confidentiality asset (it holds no
     secrets of its own) but a *high* availability asset (everything behind it stops
     when it stops), and its vulnerability is a resource-exhaustion one.

Run:
    /opt/miniconda3/envs/py313/bin/python experiments/paper2/availability_gap.py
"""

import os
import sys

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from caps.engine_multidim import DIMENSIONS, ImpactVector, evaluate_control_dim
from caps.engine_nonmono import Control, evaluate_control
from caps.models import Component, Connection, Mitigation, Vulnerability
from caps.templates import get_model_router

# The guardrail as an availability asset: it holds no secrets (low C), it cannot forge
# results (low-ish I), but every request behind it fails when it is saturated (high A).
GUARDRAIL_IMPACT = ImpactVector(c=3.0, i=4.0, a=9.5)

# Its scalar stand-in under CAPS v1 -- a modest single number, since on a
# confidentiality reading the guardrail simply is not very valuable.
GUARDRAIL_SCALAR = 3.0


def build():
    stack = get_model_router()

    guardrail = Component(
        id="shared_guardrail",
        name="Shared Reasoning Guardrail",
        type="orchestrator",
        asset_value=GUARDRAIL_SCALAR,
        vulnerabilities=[
            Vulnerability(
                id="guardrail_exhaustion",
                name="Reasoning Exhaustion / DoS Amplification",
                description=(
                    "Content shaped like the guardrail's own safety-analysis task drives "
                    "it into extended deliberation. Latency amplification cascades to "
                    "every request behind it (arXiv:2606.14517)."
                ),
                exploitability=0.80,
                impact=9.5,
            )
        ],
    )

    control = Control(
        name="Shared reasoning guardrail",
        attenuations={
            "model_router": Mitigation(
                id="gr_router",
                name="Shared guardrail policy check",
                effectiveness=0.80,
            )
        },
        induced_components=[guardrail],
        induced_connections=[
            Connection(source="partner_app", destination="shared_guardrail",
                       description="All traffic inspected", trust_boundary=True),
            Connection(source="shared_guardrail", destination="model_router",
                       description="Approved requests forwarded"),
        ],
        removed_connections=[("partner_app", "model_router")],
    )
    return stack, control


def main():
    stack, control = build()

    print("=" * 78)
    print("The availability gap: one control, two scoring models")
    print("=" * 78)
    print(f"\nGuardrail impact vector : C={GUARDRAIL_IMPACT.c}, "
          f"I={GUARDRAIL_IMPACT.i}, A={GUARDRAIL_IMPACT.a}")
    print(f"Guardrail scalar value  : {GUARDRAIL_SCALAR}  (a confidentiality reading)")
    print(f"Vulnerability           : resource exhaustion, E=0.80")

    # ---- 1. scalar semantics, i.e. what CAPS v1 sees --------------------------
    scalar = evaluate_control(stack, control)
    print("\n" + "-" * 78)
    print("1. Scalar model (CAPS v1)")
    print("-" * 78)
    print(f"  baseline        : {scalar['baseline']:.2f}")
    print(f"  ACE (reported)  : {scalar['ace']:+.2f}")
    print(f"  NCE (true)      : {scalar['nce']:+.2f}")
    print(f"  verdict         : {'HARMFUL' if scalar['nce'] < 0 else 'BENEFICIAL'}")
    print("\n  The guardrail's DoS exposure is invisible here: its scalar asset value is")
    print("  low, so as a path target it barely registers, and the exhaustion")
    print("  vulnerability contributes nothing the score can distinguish from any other.")

    # ---- 2. dimension-aware --------------------------------------------------
    dim = evaluate_control_dim(
        stack,
        control,
        impacts_before=None,
        impacts_after={"shared_guardrail": GUARDRAIL_IMPACT},
    )
    print("\n" + "-" * 78)
    print("2. Dimension-aware model")
    print("-" * 78)
    print(f"  {'dim':<6}{'before':>10}{'after':>10}{'NCE':>10}{'verdict':>14}")
    for d in DIMENSIONS:
        r = dim[d]
        print(f"  {d.upper():<6}{r['before']:>10.2f}{r['after']:>10.2f}"
              f"{r['nce']:>+10.2f}{('HARMFUL' if r['harmful'] else 'beneficial'):>14}")

    print(f"\n  dimension-crossing iatrogenesis: {dim['dimension_crossing']}")

    print("\n" + "=" * 78)
    print("Conclusion")
    print("=" * 78)
    if dim["dimension_crossing"]:
        helped = [d.upper() for d in DIMENSIONS if dim[d]["nce"] > 0]
        harmed = [d.upper() for d in DIMENSIONS if dim[d]["nce"] < 0]
        print(f"The same control reduces risk on {', '.join(helped)} and increases it on")
        print(f"{', '.join(harmed)}. No scalar summary can report both, because it sums")
        print("quantities that are not commensurable. The guardrail-DoS threat is not")
        print("mis-scored by CAPS v1 -- it is unrepresentable.")
    else:
        print("No dimension-crossing effect at these parameters; the control's sign is")
        print("consistent across dimensions, so the scalar model loses less than argued.")
    print("\nThis is a limitation of the impact model, distinct from the iatrogenic")
    print("attack-surface argument. It needs naming separately in the paper.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
