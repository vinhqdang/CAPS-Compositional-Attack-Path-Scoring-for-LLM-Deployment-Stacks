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

Terminology (paper 2):

    Iatrogenic Attack Surface (IAS)
        The components and edges a control introduces -- parts (2) and (3) above.
    Apparent Control Effect (ACE)
        The risk reduction an attenuation-only model reports. Sees part (1) only.
    Net Control Effect (NCE)
        The true risk change once the IAS is counted.
    Iatrogenic Gap
        ACE - NCE. How much benefit a monotone model over-reports.
    Iatrogenic Inversion
        NCE < 0 < ACE. The model recommends a control that increases risk.

"Iatrogenic" is borrowed from medicine: harm caused by the treatment itself.

This module deliberately does not modify ``caps.engine``. Paper 1's published
numbers must stay reproducible.
"""

from copy import deepcopy
from typing import Dict, List, Optional, Tuple

from caps.engine import AnalysisEngine
from caps.models import Component, Connection, DeploymentStack, Mitigation


# The schema caps vulnerability exploitability at 1.0 and component asset value at
# 10.0, so the product E_g * I_t that drives an iatrogenic path is bounded above by 10.
# This ceiling is what makes the placement bound below a hard guarantee rather than a
# heuristic.
MAX_EG_TIMES_I = 10.0


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

    ace = baseline - score_v1  # Apparent Control Effect
    nce = baseline - score_full  # Net Control Effect

    return {
        "baseline": round(baseline, 3),
        "score_v1": round(score_v1, 3),
        "score_full": round(score_full, 3),
        # delta_v1 / delta_full are kept as the primary key names; ACE / NCE are the
        # paper's terminology for the same two quantities.
        "delta_v1": round(ace, 3),
        "delta_full": round(nce, 3),
        "ace": round(ace, 3),
        "nce": round(nce, 3),
        "iatrogenic_gap": round(ace - nce, 3),
        "sign_inverted": ace > 0 > nce,
    }


def induced_signature(control: Control) -> Tuple[set, set]:
    """The component ids and (source, destination) edges this control introduces."""
    nodes = {c.id for c in control.induced_components}
    edges = {(c.source, c.destination) for c in control.induced_connections}
    return nodes, edges


def _uses_induced_surface(path: List[str], nodes: set, edges: set) -> bool:
    if any(n in nodes for n in path):
        return True
    return any((a, b) in edges for a, b in zip(path, path[1:]))


def iatrogenic_paths(stack: DeploymentStack, control: Control) -> List[Dict]:
    """Scored attack paths that exist only because the control was deployed.

    A path qualifies if it traverses an induced component or an induced edge. Paths
    that existed before deployment cannot exceed the baseline maximum (attenuation
    only ever lowers scores), so any path above baseline must appear here.
    """
    nodes, edges = induced_signature(control)
    deployed = control.apply(stack)
    engine = AnalysisEngine(deployed)

    out = []
    for info in engine.analyze_paths():
        if _uses_induced_surface(info["path"], nodes, edges):
            out.append(info)
    return out


def inversion_report(stack: DeploymentStack, control: Control) -> Dict:
    """Full iatrogenic analysis of a control, including the generalised criterion.

    The criterion in closed form. Let the highest-scoring iatrogenic path be
    ``P = <v_1 ... v_k>`` with the induced node ``g`` at position ``i`` (so ``g`` sits
    ``d = i`` hops from the entry point). Write ``R`` for the product of node
    exploitabilities strictly before ``g``, and ``S`` for the product strictly after.
    Then

        score(P) = R * E_g * S * alpha^(k-1) * I_{v_k} * 10

    and the control is net-harmful exactly when ``score(P) > baseline``, i.e.

        E_g * I_{v_k} > baseline / (10 * alpha^(k-1) * R * S)

    The entry-adjacent special case is ``d = 1``, ``R = 1`` (the entry node contributes
    exploitability 1.0), ``S = 1`` and ``v_k = g``, which recovers
    ``E_g * I_g > baseline / (alpha * 10)``.

    **Placement bound.** Because ``E_g <= 1`` and ``I_t <= 10``, the left-hand side is
    capped at 10. So inversion is *impossible* -- for any induced node, however
    exploitable or valuable -- whenever

        alpha^(k-1) * R * S  <=  baseline / 100

    The reachability product decays multiplicatively with depth, so deep controls are
    safe by construction and only shallow, easily-reached controls can be net-harmful.
    ``inversion_feasible`` reports which side of this bound a placement falls on.
    """
    base = evaluate_control(stack, control)
    baseline = base["baseline"]
    alpha = stack.chaining_decay

    paths = iatrogenic_paths(stack, control)
    report = dict(base)
    report["name"] = control.name
    report["n_iatrogenic_paths"] = len(paths)

    if not paths:
        report["top_iatrogenic_score"] = 0.0
        report["decomposition"] = None
        report["threshold"] = None
        return report

    top = paths[0]
    report["top_iatrogenic_score"] = top["score"]
    report["top_iatrogenic_path"] = list(top["path"])

    deployed = control.apply(stack)
    engine = AnalysisEngine(deployed)
    induced_nodes, _ = induced_signature(control)

    per_node = [
        engine._calculate_node_exploitability(deployed.get_component(n))[0]
        for n in top["path"]
    ]

    idx = next(
        (i for i, n in enumerate(top["path"]) if n in induced_nodes), None
    )
    if idx is None:
        # The path uses an induced edge but no induced node; no g to isolate.
        report["decomposition"] = None
        report["threshold"] = None
        return report

    k = len(top["path"])
    prefix = 1.0
    for e in per_node[:idx]:
        prefix *= e
    suffix = 1.0
    for e in per_node[idx + 1 :]:
        suffix *= e

    e_g = per_node[idx]
    target_impact = top["target_impact"]
    decay = alpha ** (k - 1)

    denom = 10.0 * decay * prefix * suffix
    report["decomposition"] = {
        "depth_d": idx,
        "path_len_k": k,
        "prefix_R": round(prefix, 5),
        "E_g": round(e_g, 5),
        "suffix_S": round(suffix, 5),
        "target_impact": target_impact,
        "decay": round(decay, 5),
        # Sanity check: the decomposition must reproduce the engine's own score.
        "reconstructed_score": round(
            prefix * e_g * suffix * decay * target_impact * 10.0, 3
        ),
    }
    report["threshold"] = round(baseline / denom, 5) if denom > 0 else None
    report["lhs_E_g_times_I"] = round(e_g * target_impact, 5)

    # Placement bound. The schema caps exploitability at 1.0 and asset value at 10.0,
    # so E_g * I_t <= MAX_EG_TIMES_I. If the threshold exceeds that ceiling, no choice
    # of the induced node's own parameters can make this control net-harmful: the
    # placement is safe by construction.
    report["inversion_feasible"] = (
        report["threshold"] is not None and MAX_EG_TIMES_I > report["threshold"]
    )
    report["reachability_product"] = round(decay * prefix * suffix, 6)
    report["reachability_floor"] = round(baseline / MAX_EG_TIMES_I / 10.0, 6)
    return report


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
