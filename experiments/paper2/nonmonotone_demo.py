"""Does CAPS v1's mitigation-ROI ranking invert once controls carry their own surface?

Three controls are evaluated against the Enterprise Model Router topology:

  C1  Input Guardrail (dedicated)   -- classical attenuator, no induced surface.
  C2  Shared Guardrail Service      -- attenuates, but is itself an LLM (injectable)
                                       and must inspect all traffic, so it acquires
                                       edges to every model it fronts.
  C3  Output Sanitiser (summarising) -- attenuates, and inserts a summarisation node
                                       that reads model output and writes to the log
                                       sink, which is externally reachable.

C2 is modelled on the shared-guardrail failure reported in arXiv:2606.14517, where a
centralised reasoning guardrail becomes both an amplification target and a single point
of compromise with reach across everything it fronts. C3 is modelled on
arXiv:2510.22963, where inserting a lossy compression stage creates an attack surface.

Parameters are stated inline and are illustrative, not measured. The point of the demo
is the *sign* of the effect and whether the ranking reorders, not the magnitudes.

Run:  python experiments/paper2/nonmonotone_demo.py
"""

import os
import sys

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from caps.engine_nonmono import Control, evaluate_control, max_path_score, rank_controls
from caps.models import Component, Connection, Mitigation, Vulnerability
from caps.templates import get_model_router


def build_controls():
    # ---- C1: dedicated input guardrail. Pure attenuator, no new surface. -------
    c1 = Control(
        name="C1 Input Guardrail (dedicated)",
        description="Prompt filter in front of the router. No shared infrastructure.",
        attenuations={
            "model_router": Mitigation(
                id="c1_filter",
                name="Input Guardrail / Prompt Filter",
                description="Blocks routing-override parameters in the request.",
                effectiveness=0.80,
            )
        },
    )

    # ---- C2: shared guardrail service. Attenuates two nodes, but is an LLM -----
    # itself and must see all traffic, so it gains reach to every model it fronts.
    c2 = Control(
        name="C2 Shared Guardrail Service",
        description=(
            "Centralised reasoning guardrail fronting all models. Attenuates the "
            "router and the confidential model, but is itself injectable and holds "
            "inspection reach over everything behind it."
        ),
        attenuations={
            "model_router": Mitigation(
                id="c2_filter_router",
                name="Shared Guardrail (router)",
                description="Central policy check on routing parameters.",
                effectiveness=0.80,
            ),
            "confidential_gpt4": Mitigation(
                id="c2_filter_conf",
                name="Shared Guardrail (confidential model)",
                description="Central policy check on confidential-model prompts.",
                effectiveness=0.50,
            ),
        },
        induced_components=[
            Component(
                id="shared_guardrail",
                name="Shared Guardrail Service (LLM-based)",
                type="orchestrator",
                asset_value=6.0,
                vulnerabilities=[
                    Vulnerability(
                        id="guardrail_reasoning_hijack",
                        name="Guardrail Reasoning Hijack / Exhaustion",
                        description=(
                            "The guardrail's own structured safety reasoning is "
                            "instruction-following surface: it can be steered or "
                            "exhausted by content crafted to look like its own task."
                        ),
                        exploitability=0.75,
                        impact=7.0,
                    )
                ],
            )
        ],
        induced_connections=[
            # Traffic is routed through the guardrail...
            Connection(
                source="partner_app",
                destination="shared_guardrail",
                description="All partner traffic is inspected by the shared guardrail",
                trust_boundary=True,
            ),
            # ...and the guardrail, to inspect, holds reach over everything behind it.
            Connection(
                source="shared_guardrail",
                destination="model_router",
                description="Guardrail forwards approved requests",
            ),
            Connection(
                source="shared_guardrail",
                destination="confidential_gpt4",
                description="Guardrail inspects confidential-model traffic directly",
                trust_boundary=True,
            ),
        ],
    )

    # ---- C3: summarising output sanitiser writing to an externally-visible log --
    c3 = Control(
        name="C3 Output Sanitiser (summarising)",
        description=(
            "Summarises model output to strip unsafe content, and records what it "
            "stripped to an audit sink that partners can read."
        ),
        attenuations={
            "confidential_gpt4": Mitigation(
                id="c3_sanitiser",
                name="Summarising Output Sanitiser",
                description="Rewrites confidential-model output to remove secrets.",
                effectiveness=0.70,
            )
        },
        induced_components=[
            Component(
                id="sanitiser_log",
                name="Sanitiser Audit Sink",
                type="database",
                asset_value=7.0,
                vulnerabilities=[
                    Vulnerability(
                        id="audit_readback",
                        name="Audit Sink Readback",
                        description=(
                            "The record of what was stripped contains the stripped "
                            "material, and the sink is partner-readable."
                        ),
                        exploitability=0.65,
                        impact=7.0,
                    )
                ],
            )
        ],
        induced_connections=[
            Connection(
                source="confidential_gpt4",
                destination="sanitiser_log",
                description="Sanitiser records redacted spans",
                trust_boundary=True,
            ),
            Connection(
                source="treasury_database",
                destination="sanitiser_log",
                description="Redaction of financial records is logged",
                trust_boundary=True,
            ),
        ],
    )

    return [c1, c2, c3]


def main():
    stack = get_model_router()
    controls = build_controls()

    print("=" * 78)
    print(f"Topology: {stack.name}")
    print(f"Baseline max attack-path score: {max_path_score(stack):.3f}")
    print("=" * 78)

    ranking_v1, ranking_full = rank_controls(stack, controls)

    print("\nPer-control effect (positive delta = risk reduced):\n")
    hdr = f"{'Control':<34}{'CAPS v1 sees':>14}{'Actual':>12}{'Inverted?':>12}"
    print(hdr)
    print("-" * len(hdr))
    for r in ranking_v1:
        flag = "YES" if r["sign_inverted"] else ""
        print(
            f"{r['name']:<34}{r['delta_v1']:>+14.3f}{r['delta_full']:>+12.3f}{flag:>12}"
        )

    print("\nRanking under CAPS v1 (attenuation only):")
    for i, r in enumerate(ranking_v1, 1):
        print(f"  {i}. {r['name']}  (delta {r['delta_v1']:+.3f})")

    print("\nRanking with induced surface accounted for:")
    for i, r in enumerate(ranking_full, 1):
        print(f"  {i}. {r['name']}  (delta {r['delta_full']:+.3f})")

    reordered = [r["name"] for r in ranking_v1] != [r["name"] for r in ranking_full]
    inversions = [r["name"] for r in ranking_v1 if r["sign_inverted"]]

    print("\n" + "=" * 78)
    print(f"Ranking reordered: {reordered}")
    print(f"Sign inversions (v1 recommends, actually harmful): {inversions or 'none'}")
    print("=" * 78)

    sweep(stack)


def _shared_guardrail(asset_value: float, exploitability: float) -> Control:
    """C2 parameterised by the induced node's own asset value and exploitability."""
    return Control(
        name=f"C2(asset={asset_value}, E={exploitability})",
        attenuations={
            "model_router": Mitigation(
                id="c2_filter_router",
                name="Shared Guardrail (router)",
                effectiveness=0.80,
            )
        },
        induced_components=[
            Component(
                id="shared_guardrail",
                name="Shared Guardrail Service (LLM-based)",
                type="orchestrator",
                asset_value=asset_value,
                vulnerabilities=[
                    Vulnerability(
                        id="guardrail_reasoning_hijack",
                        name="Guardrail Reasoning Hijack / Exhaustion",
                        exploitability=exploitability,
                        impact=7.0,
                    )
                ],
            )
        ],
        induced_connections=[
            Connection(source="partner_app", destination="shared_guardrail"),
            Connection(source="shared_guardrail", destination="model_router"),
            Connection(source="shared_guardrail", destination="confidential_gpt4"),
        ],
    )


def sweep(stack):
    """Sensitivity of the shared-guardrail control to its own asset value and exploitability.

    The headline observation is not the inversion itself but that CAPS v1's reported
    benefit is *invariant* across the whole sweep: its algebra sees only the
    attenuation term, so every configuration below yields an identical delta while
    the true effect spans a wide range and changes sign.
    """
    baseline = max_path_score(stack)
    alpha = stack.chaining_decay

    print("\n" + "=" * 78)
    print("Sensitivity of the shared guardrail (C2) to its own parameters")
    print("=" * 78)
    print(f"\n{'asset':>6}{'E':>7}{'v1 delta':>11}{'true delta':>12}{'inverted':>10}")
    print("-" * 46)

    v1_deltas, true_deltas = set(), []
    for asset in (6.0, 7.0, 8.0, 9.0, 10.0):
        for expl in (0.5, 0.75, 0.9):
            r = evaluate_control(stack, _shared_guardrail(asset, expl))
            v1_deltas.add(r["delta_v1"])
            true_deltas.append(r["delta_full"])
            print(
                f"{asset:>6.1f}{expl:>7.2f}{r['delta_v1']:>+11.2f}"
                f"{r['delta_full']:>+12.2f}{str(r['sign_inverted']):>10}"
            )

    spread = max(true_deltas) - min(true_deltas)
    print(
        f"\nCAPS v1 reported {len(v1_deltas)} distinct value(s) across "
        f"{len(true_deltas)} configurations: {sorted(v1_deltas)}"
    )
    print(f"True effect spanned {min(true_deltas):+.2f} to {max(true_deltas):+.2f} "
          f"(spread {spread:.2f} points), crossing zero.")

    # Closed-form inversion threshold for a control whose induced node sits one hop
    # from the entry point: it is net-harmful once its own path outscores the baseline.
    threshold = baseline / (alpha * 10.0)
    print(
        f"\nInversion criterion for this topology: the induced node is net-harmful "
        f"once E_g * I_g > baseline / (alpha * 10) = {threshold:.2f}."
    )
    print("Generally: a control inverts sign when its own induced path outscores the")
    print("path it was deployed to attenuate -- i.e. when the control is a more")
    print("attractive target than the asset it protects.")


if __name__ == "__main__":
    main()
