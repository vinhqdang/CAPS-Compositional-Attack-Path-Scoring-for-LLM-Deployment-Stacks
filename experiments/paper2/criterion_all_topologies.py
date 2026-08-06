"""The generalised inversion criterion across all three CAPS topologies.

For each topology a comparable pair of controls is deployed:

  Dedicated   -- attenuates the most valuable on-path component. No induced surface.
                 CAPS v1 can express this exactly.
  Shared      -- identical attenuation, but delivered by a shared LLM-based guardrail
                 that fronts the entry point and holds inspection reach over the
                 components behind it. Same ACE, different NCE.

Two things are checked per topology:

  1. The Iatrogenic Gap (ACE - NCE): how much benefit an attenuation-only model
     over-reports.
  2. The generalised inversion criterion and its closed-form decomposition,
     including a reconstruction check that the decomposition reproduces the
     engine's own path score.

Parameters are illustrative, not measured.

Run:  python experiments/paper2/criterion_all_topologies.py
"""

import os
import sys

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from caps.engine import AnalysisEngine
from caps.engine_nonmono import Control, inversion_report, max_path_score
from caps.models import Component, Connection, Mitigation, Vulnerability
from caps.templates import (
    get_autonomous_coding_agent,
    get_model_router,
    get_rag_chatbot,
)

GUARDRAIL_E = 0.85  # exploitability of an LLM-based guardrail (illustrative)
GUARDRAIL_ASSET = 8.0  # a shared guardrail sees all traffic, so it is valuable
ATTENUATION = 0.80


def _entry_of(stack):
    return AnalysisEngine(stack).get_entry_points()[0]


def _guardrail(asset_value=GUARDRAIL_ASSET, exploitability=GUARDRAIL_E):
    return Component(
        id="shared_guardrail",
        name="Shared Guardrail Service (LLM-based)",
        type="orchestrator",
        asset_value=asset_value,
        vulnerabilities=[
            Vulnerability(
                id="guardrail_reasoning_hijack",
                name="Guardrail Reasoning Hijack / Exhaustion",
                description=(
                    "The guardrail's own safety reasoning is instruction-following "
                    "surface and can be steered or exhausted."
                ),
                exploitability=exploitability,
                impact=7.0,
            )
        ],
    )


def build_pair(stack, protect_id, fronted_ids):
    """A dedicated and a shared control with identical attenuation."""
    atten = {
        protect_id: Mitigation(
            id="atten",
            name="Prompt/Policy Filter",
            description="Blocks the exploited pattern at the protected component.",
            effectiveness=ATTENUATION,
        )
    }
    entry = _entry_of(stack)

    dedicated = Control(name="Dedicated guardrail", attenuations=atten)

    shared = Control(
        name="Shared guardrail service",
        attenuations=atten,
        induced_components=[_guardrail()],
        induced_connections=(
            [Connection(source=entry, destination="shared_guardrail",
                        description="All traffic is inspected", trust_boundary=True)]
            + [
                Connection(source="shared_guardrail", destination=t,
                           description="Guardrail holds inspection reach")
                for t in fronted_ids
            ]
        ),
    )
    return dedicated, shared


TOPOLOGIES = [
    (
        "RAG Chatbot",
        get_rag_chatbot,
        "prompt_gateway",
        ["prompt_gateway", "vector_db"],
    ),
    (
        "Autonomous Coding Agent",
        get_autonomous_coding_agent,
        "agent_orchestrator",
        ["agent_orchestrator", "bash_executor"],
    ),
    (
        "Enterprise Model Router",
        get_model_router,
        "model_router",
        ["model_router", "confidential_gpt4"],
    ),
]


def main():
    print("=" * 92)
    print("Generalised inversion criterion across all three topologies")
    print(f"Shared guardrail: E_g = {GUARDRAIL_E}, I_g = {GUARDRAIL_ASSET}, "
          f"attenuation = {ATTENUATION}")
    print("=" * 92)

    rows = []
    for label, factory, protect_id, fronted in TOPOLOGIES:
        stack = factory()
        baseline = max_path_score(stack)
        dedicated, shared = build_pair(stack, protect_id, fronted)

        r_ded = inversion_report(stack, dedicated)
        r_shr = inversion_report(stack, shared)
        rows.append((label, baseline, r_ded, r_shr))

        print(f"\n{'-' * 92}")
        print(f"{label}  (alpha = {stack.chaining_decay}, baseline = {baseline:.2f})")
        print(f"{'-' * 92}")
        print(f"{'control':<26}{'ACE':>9}{'NCE':>9}{'gap':>9}{'inverted':>10}")
        for r in (r_ded, r_shr):
            print(
                f"{r['name']:<26}{r['ace']:>+9.2f}{r['nce']:>+9.2f}"
                f"{r['iatrogenic_gap']:>9.2f}{str(r['sign_inverted']):>10}"
            )

        d = r_shr.get("decomposition")
        if d:
            print(f"\n  top iatrogenic path : {' -> '.join(r_shr['top_iatrogenic_path'])}")
            print(f"  score               : {r_shr['top_iatrogenic_score']:.2f}"
                  f"   (reconstructed {d['reconstructed_score']:.2f})")
            print(f"  decomposition       : d={d['depth_d']}, k={d['path_len_k']}, "
                  f"R={d['prefix_R']}, E_g={d['E_g']}, S={d['suffix_S']}, "
                  f"I_t={d['target_impact']}, alpha^(k-1)={d['decay']}")
            print(f"  criterion           : E_g * I_t = {r_shr['lhs_E_g_times_I']:.2f} "
                  f"vs threshold {r_shr['threshold']:.2f}"
                  f"  ->  {'INVERTS' if r_shr['lhs_E_g_times_I'] > r_shr['threshold'] else 'no inversion'}")
            ok = abs(d["reconstructed_score"] - r_shr["top_iatrogenic_score"]) < 0.01
            print(f"  decomposition check : {'PASS' if ok else 'FAIL'}")

    print("\n" + "=" * 92)
    print("Summary")
    print("=" * 92)
    print(f"{'topology':<26}{'baseline':>10}{'ACE':>9}{'NCE(shared)':>13}"
          f"{'gap':>9}{'inverted':>10}")
    for label, baseline, r_ded, r_shr in rows:
        print(
            f"{label:<26}{baseline:>10.2f}{r_shr['ace']:>+9.2f}"
            f"{r_shr['nce']:>+13.2f}{r_shr['iatrogenic_gap']:>9.2f}"
            f"{str(r_shr['sign_inverted']):>10}"
        )

    n_inv = sum(1 for _, _, _, r in rows if r["sign_inverted"])
    print(f"\nInversions: {n_inv}/{len(rows)} topologies at these parameters.")
    print("In every topology the dedicated and shared controls report an IDENTICAL ACE,")
    print("so an attenuation-only model cannot distinguish them at all.")

    placement_bound()


def placement_bound():
    """Inversion is confined to shallow placements, and the bound is hard.

    Since E_g <= 1 and I_t <= 10, the criterion's left-hand side cannot exceed 10.
    The threshold is baseline / (10 * alpha^(k-1) * R * S), and the reachability
    product alpha^(k-1) * R * S decays multiplicatively with depth. Past a certain
    depth the threshold exceeds 10 and inversion becomes impossible for *any* induced
    node, no matter how exploitable or valuable.
    """
    stack = get_model_router()
    baseline = max_path_score(stack)

    print("\n" + "=" * 92)
    print("Placement bound: how deep does a control have to sit to be safe?")
    print("=" * 92)
    print(f"\nEnterprise Model Router, baseline {baseline:.2f}.")
    print(f"Inversion needs reachability product > baseline/100 = {baseline / 100:.4f}\n")

    # Entry-adjacent guardrail vs a sanitiser placed three hops in.
    entry = _entry_of(stack)
    shallow = Control(
        name="entry-adjacent guardrail",
        attenuations={"model_router": Mitigation(id="a", name="a", effectiveness=ATTENUATION)},
        induced_components=[_guardrail()],
        induced_connections=[
            Connection(source=entry, destination="shared_guardrail"),
            Connection(source="shared_guardrail", destination="model_router"),
        ],
    )
    deep = Control(
        name="deep output sanitiser",
        attenuations={"confidential_gpt4": Mitigation(id="a", name="a", effectiveness=ATTENUATION)},
        induced_components=[
            Component(
                id="sanitiser",
                name="Output Sanitiser",
                type="tool",
                asset_value=GUARDRAIL_ASSET,
                vulnerabilities=[
                    Vulnerability(id="v", name="v", exploitability=GUARDRAIL_E, impact=7.0)
                ],
            )
        ],
        induced_connections=[
            Connection(source="confidential_gpt4", destination="sanitiser"),
            Connection(source="sanitiser", destination="treasury_database"),
        ],
    )

    hdr = (f"{'placement':<26}{'d':>3}{'reach':>10}{'threshold':>11}"
           f"{'E_g*I_t':>9}{'feasible':>10}{'inverted':>10}")
    print(hdr)
    print("-" * len(hdr))
    for c in (shallow, deep):
        r = inversion_report(stack, c)
        d = r["decomposition"]
        print(
            f"{c.name:<26}{d['depth_d']:>3}{r['reachability_product']:>10.4f}"
            f"{r['threshold']:>11.2f}{r['lhs_E_g_times_I']:>9.2f}"
            f"{str(r['inversion_feasible']):>10}{str(r['sign_inverted']):>10}"
        )

    print("\nIdentical induced node (I_g=8.0, E_g=0.85) in both rows. Only the placement")
    print("differs. The deep placement is not merely un-inverted -- it is provably")
    print("incapable of inverting, because its threshold exceeds the maximum possible")
    print("E_g * I_t of 10.")
    print("\nDesign implication: iatrogenic risk is a property of how reachable a control")
    print("is, not of how well it attenuates. Guardrails at the perimeter are the")
    print("dangerous ones; deep controls are safe by construction.")


if __name__ == "__main__":
    main()
