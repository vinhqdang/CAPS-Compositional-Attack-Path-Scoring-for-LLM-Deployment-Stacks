"""Dimension-aware path scoring: giving availability risk somewhere to live.

CAPS v1 scores a path as ``P_exploit(P) * I(v_k) * 10`` where ``I`` is a single scalar
``asset_value``. That scalar conflates the three impact dimensions CVSS keeps separate:
confidentiality, integrity, availability.

The consequence is a blind spot rather than an inaccuracy. The guardrail
denial-of-service reported in arXiv:2606.14517 -- where a reasoning guardrail is driven
into extended deliberation, giving 148x latency amplification and paralysing shared
guardrail infrastructure -- has almost no confidentiality or integrity impact and a large
availability impact. In a scalar model there is no coefficient that expresses that. The
threat is not mis-scored; it is unrepresentable.

This module attaches an impact *vector* to components without touching
``caps.models.Component``, so paper 1's published numbers stay reproducible. Impacts
default to the component's scalar ``asset_value`` replicated across all three dimensions,
which reproduces v1 exactly when no vector is supplied.

The interesting consequence, once dimensions are separated, is that iatrogenesis can be
**dimension-crossing**: a control can reduce confidentiality risk while simultaneously
increasing availability risk. A scalar model reports only the net of a quantity it should
never have summed.
"""

from typing import Dict, List, NamedTuple, Optional

import networkx as nx

from caps.engine import AnalysisEngine
from caps.models import DeploymentStack

DIMENSIONS = ("c", "i", "a")
TARGET_THRESHOLD = 5.0  # mirrors AnalysisEngine.get_target_nodes


class ImpactVector(NamedTuple):
    """Per-dimension impact, each on the same 0-10 scale as ``asset_value``."""

    c: float
    i: float
    a: float

    @classmethod
    def uniform(cls, value: float) -> "ImpactVector":
        return cls(value, value, value)


ImpactTable = Dict[str, ImpactVector]


def default_impacts(stack: DeploymentStack) -> ImpactTable:
    """Every component's scalar asset value replicated across all dimensions."""
    return {c.id: ImpactVector.uniform(c.asset_value) for c in stack.components}


def resolve_impacts(
    stack: DeploymentStack, overrides: Optional[ImpactTable] = None
) -> ImpactTable:
    table = default_impacts(stack)
    if overrides:
        table.update(overrides)
    return table


def analyze_paths_dim(
    stack: DeploymentStack,
    dimension: str,
    impacts: Optional[ImpactTable] = None,
) -> List[Dict]:
    """Score attack paths against one impact dimension.

    Target selection is dimension-aware: a node is a target if *that dimension's*
    impact clears the threshold. This matters for exactly the case that motivates the
    module -- a guardrail may have modest confidentiality value while being a
    high-availability asset, and so is a target in one dimension and not the other.
    """
    if dimension not in DIMENSIONS:
        raise ValueError(f"dimension must be one of {DIMENSIONS}, got {dimension!r}")

    table = resolve_impacts(stack, impacts)
    engine = AnalysisEngine(stack)
    graph = engine.graph

    entries = engine.get_entry_points()
    targets = [
        n
        for n, data in graph.nodes(data=True)
        if (comp := data.get("component")) is not None
        and comp.type not in ("attacker", "user")
        and getattr(table[n], dimension) >= TARGET_THRESHOLD
    ]

    scored = []
    for src in entries:
        for tgt in targets:
            if src == tgt:
                continue
            try:
                paths = list(nx.all_simple_paths(graph, src, tgt))
            except nx.NetworkXNoPath:
                continue
            for path in paths:
                product = 1.0
                for node in path:
                    expl, _ = engine._calculate_node_exploitability(
                        graph.nodes[node]["component"]
                    )
                    product *= expl
                likelihood = product * stack.chaining_decay ** (len(path) - 1)
                impact = getattr(table[tgt], dimension)
                scored.append(
                    {
                        "path": path,
                        "dimension": dimension,
                        "likelihood": likelihood,
                        "target_impact": impact,
                        "score": round(likelihood * impact * 10, 3),
                    }
                )

    scored.sort(key=lambda r: r["score"], reverse=True)
    return scored


def max_score_dim(
    stack: DeploymentStack, dimension: str, impacts: Optional[ImpactTable] = None
) -> float:
    paths = analyze_paths_dim(stack, dimension, impacts)
    return paths[0]["score"] if paths else 0.0


def evaluate_control_dim(
    stack: DeploymentStack,
    control,
    impacts_before: Optional[ImpactTable] = None,
    impacts_after: Optional[ImpactTable] = None,
) -> Dict[str, Dict[str, float]]:
    """Net Control Effect per dimension.

    ``impacts_after`` supplies vectors for components the control introduces (which do
    not exist in ``stack`` and so cannot be in ``impacts_before``).

    A positive NCE means risk fell in that dimension. Signs differing across dimensions
    is dimension-crossing iatrogenesis: the control genuinely helps on one axis and
    genuinely harms on another, and no scalar summary can report both.
    """
    deployed = control.apply(stack)

    merged_after = dict(impacts_before or {})
    merged_after.update(impacts_after or {})

    out = {}
    for dim in DIMENSIONS:
        before = max_score_dim(stack, dim, impacts_before)
        after = max_score_dim(deployed, dim, merged_after)
        out[dim] = {
            "before": round(before, 3),
            "after": round(after, 3),
            "nce": round(before - after, 3),
            "harmful": (before - after) < 0,
        }

    signs = {d: out[d]["nce"] for d in DIMENSIONS}
    out["dimension_crossing"] = any(v > 0 for v in signs.values()) and any(
        v < 0 for v in signs.values()
    )
    return out
