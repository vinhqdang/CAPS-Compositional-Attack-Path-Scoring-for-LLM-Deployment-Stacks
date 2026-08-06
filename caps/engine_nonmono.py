"""Non-monotone mitigation semantics for compositional attack-path scoring.

CAPS v1 (``caps.engine``) models a mitigation purely as an attenuator:

    E_eff(vuln) = E(vuln) * prod_{mit} (1 - M(mit)),   M in [0, 1)

Because every factor lies in (0, 1], adding a mitigation can only ever multiply a
node's exploitability *downward*. Inserting a node onto a path likewise only adds
factors <= 1 and lengthens the chain, so the decay term shrinks the score further.
The consequence is structural rather than parametric: **CAPS v1 cannot represent a
control whose deployment increases risk.** No choice of M produces dRisk > 0.

This module relaxes that. A ``Control`` is a graph operator with three parts:

1. ``attenuations`` -- the classical effect: reduce exploitability at target nodes.
2. ``induced_components`` -- the control is itself a component, with its own
   vulnerabilities. An LLM-based guardrail is an LLM, so it can be reasoned at,
   exhausted, and turned.
3. ``induced_connections`` -- the control's placement creates edges. An inline
   guardrail that must inspect all traffic acquires reach to everything it
   inspects, which is new topology that did not exist before deployment.

Risk is then non-monotone in the control set: parts (2) and (3) can outweigh (1).

This module deliberately does not modify ``caps.engine``. Paper 1's published
numbers must stay reproducible.
"""

from copy import deepcopy
from typing import Dict, List, Optional, Tuple

from caps.engine import AnalysisEngine
from caps.models import Component, Connection, DeploymentStack, Mitigation


class Control:
    """A security control modelled as a graph operator, not just an attenuator."""

    def __init__(
        self,
        name: str,
        attenuations: Optional[Dict[str, Mitigation]] = None,
        induced_components: Optional[List[Component]] = None,
        induced_connections: Optional[List[Connection]] = None,
        description: str = "",
    ):
        # component_id -> Mitigation applied to it
        self.name = name
        self.attenuations = attenuations or {}
        self.induced_components = induced_components or []
        self.induced_connections = induced_connections or []
        self.description = description

    @property
    def is_classical(self) -> bool:
        """True if this control has no induced surface, i.e. CAPS v1 can express it."""
        return not self.induced_components and not self.induced_connections

    def apply(self, stack: DeploymentStack) -> DeploymentStack:
        """Return a new stack with this control deployed."""
        s = deepcopy(stack)

        for comp_id, mit in self.attenuations.items():
            comp = s.get_component(comp_id)
            if comp is None:
                raise ValueError(f"control '{self.name}' targets unknown component '{comp_id}'")
            comp.mitigations.append(deepcopy(mit))

        existing = {c.id for c in s.components}
        for comp in self.induced_components:
            if comp.id in existing:
                raise ValueError(f"control '{self.name}' induces duplicate component '{comp.id}'")
            s.components.append(deepcopy(comp))

        for conn in self.induced_connections:
            s.connections.append(deepcopy(conn))

        return s


def max_path_score(stack: DeploymentStack) -> float:
    """Maximum attack-path score for a stack, using the paper-1 scoring engine."""
    paths = AnalysisEngine(stack).analyze_paths()
    return paths[0]["score"] if paths else 0.0


def evaluate_control(stack: DeploymentStack, control: Control) -> Dict[str, float]:
    """Score a control both ways: CAPS v1 semantics and non-monotone semantics.

    ``delta_v1`` is the risk reduction CAPS v1 would report -- attenuation only,
    induced surface ignored, which is the only thing its algebra can see.
    ``delta_full`` accounts for the induced components and connections too.

    A positive delta means risk went down (a benefit). A negative ``delta_full``
    with a positive ``delta_v1`` is a sign inversion: the control is recommended
    by CAPS v1 and is actually harmful.
    """
    baseline = max_path_score(stack)

    attenuation_only = Control(
        name=control.name, attenuations=control.attenuations
    ).apply(stack)
    score_v1 = max_path_score(attenuation_only)

    score_full = max_path_score(control.apply(stack))

    return {
        "baseline": round(baseline, 3),
        "score_v1": round(score_v1, 3),
        "score_full": round(score_full, 3),
        "delta_v1": round(baseline - score_v1, 3),
        "delta_full": round(baseline - score_full, 3),
        "sign_inverted": (baseline - score_v1) > 0 > (baseline - score_full),
    }


def rank_controls(
    stack: DeploymentStack, controls: List[Control]
) -> Tuple[List[Dict], List[Dict]]:
    """Rank controls under both semantics.

    Returns ``(ranking_v1, ranking_full)``, each sorted best-first by its own
    notion of benefit. Where the two orderings disagree, CAPS v1's mitigation-ROI
    recommendation is wrong.
    """
    rows = []
    for c in controls:
        r = evaluate_control(stack, c)
        r["name"] = c.name
        r["is_classical"] = c.is_classical
        rows.append(r)

    ranking_v1 = sorted(rows, key=lambda r: r["delta_v1"], reverse=True)
    ranking_full = sorted(rows, key=lambda r: r["delta_full"], reverse=True)
    return ranking_v1, ranking_full
