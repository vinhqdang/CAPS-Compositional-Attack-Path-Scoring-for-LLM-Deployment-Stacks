import pytest

from caps.engine import AnalysisEngine
from caps.engine_multidim import (
    DIMENSIONS,
    ImpactVector,
    analyze_paths_dim,
    default_impacts,
    evaluate_control_dim,
    max_score_dim,
)
from caps.engine_nonmono import Control
from caps.models import Component, Connection, Mitigation, Vulnerability
from caps.templates import get_model_router, get_rag_chatbot


def test_uniform_impacts_reproduce_v1_exactly():
    """With no impact overrides, every dimension must equal the scalar CAPS v1 score."""
    for factory in (get_rag_chatbot, get_model_router):
        stack = factory()
        v1 = AnalysisEngine(stack).analyze_paths()[0]["score"]
        for dim in DIMENSIONS:
            assert max_score_dim(stack, dim) == pytest.approx(v1, abs=0.01)


def test_default_impacts_mirror_asset_value():
    stack = get_model_router()
    table = default_impacts(stack)
    for comp in stack.components:
        assert table[comp.id] == ImpactVector.uniform(comp.asset_value)


def test_invalid_dimension_is_rejected():
    with pytest.raises(ValueError, match="dimension must be one of"):
        analyze_paths_dim(get_model_router(), "confidentiality")


def test_target_selection_is_dimension_aware():
    """A node below threshold on one dimension and above it on another is a target
    only in the dimension where it qualifies."""
    stack = get_model_router()
    # partner_app is type 'user' so it is never a target; use public_llama, which has
    # asset_value 4.0 and is therefore below the 5.0 threshold by default.
    assert all(
        "public_llama" not in p["path"][-1] for p in analyze_paths_dim(stack, "a")
    )

    overrides = {"public_llama": ImpactVector(c=4.0, i=4.0, a=9.0)}
    targets_a = {p["path"][-1] for p in analyze_paths_dim(stack, "a", overrides)}
    targets_c = {p["path"][-1] for p in analyze_paths_dim(stack, "c", overrides)}

    assert "public_llama" in targets_a
    assert "public_llama" not in targets_c


def test_dimension_crossing_iatrogenesis_is_detected():
    """A guardrail that is a low-C but high-A asset helps on C and harms on A."""
    stack = get_model_router()
    guardrail = Component(
        id="G",
        name="Shared Guardrail",
        type="orchestrator",
        asset_value=3.0,
        vulnerabilities=[
            Vulnerability(
                id="exhaust",
                name="Reasoning Exhaustion",
                exploitability=0.80,
                impact=9.5,
            )
        ],
    )
    control = Control(
        name="shared guardrail",
        attenuations={
            "model_router": Mitigation(id="m", name="m", effectiveness=0.80)
        },
        induced_components=[guardrail],
        induced_connections=[
            Connection(source="partner_app", destination="G"),
            Connection(source="G", destination="model_router"),
        ],
        removed_connections=[("partner_app", "model_router")],
    )

    out = evaluate_control_dim(
        stack, control, impacts_after={"G": ImpactVector(c=3.0, i=4.0, a=9.5)}
    )

    assert out["c"]["nce"] > 0, "should reduce confidentiality risk"
    assert out["a"]["nce"] < 0, "should increase availability risk"
    assert out["a"]["harmful"] is True
    assert out["dimension_crossing"] is True


def test_no_dimension_crossing_when_impacts_are_uniform():
    """A control with a uniform-impact induced node cannot cross dimensions."""
    stack = get_model_router()
    control = Control(
        name="c",
        attenuations={"model_router": Mitigation(id="m", name="m", effectiveness=0.8)},
        induced_components=[
            Component(
                id="G",
                name="G",
                type="orchestrator",
                asset_value=6.0,
                vulnerabilities=[
                    Vulnerability(id="v", name="v", exploitability=0.5, impact=6.0)
                ],
            )
        ],
        induced_connections=[
            Connection(source="partner_app", destination="G"),
            Connection(source="G", destination="model_router"),
        ],
    )
    out = evaluate_control_dim(stack, control)
    signs = {out[d]["nce"] for d in DIMENSIONS}
    assert len(signs) == 1, "uniform impacts must give identical NCE per dimension"
    assert out["dimension_crossing"] is False
