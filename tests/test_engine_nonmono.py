import pytest

from caps.engine_nonmono import Control, evaluate_control, max_path_score, rank_controls
from caps.models import Component, Connection, DeploymentStack, Mitigation, Vulnerability
from caps.templates import get_model_router


def _linear_stack():
    """A -> B(target). Attacker node A, orchestrator target B."""
    return DeploymentStack(
        name="Linear",
        components=[
            Component(id="A", name="Attacker", type="attacker", asset_value=1.0),
            Component(
                id="B",
                name="Target",
                type="orchestrator",
                asset_value=8.0,
                vulnerabilities=[
                    Vulnerability(id="vB", name="vB", exploitability=0.8, impact=8.0)
                ],
            ),
        ],
        connections=[Connection(source="A", destination="B")],
        chaining_decay=1.0,
    )


def test_classical_control_is_monotone():
    """A control with no induced surface can only reduce risk -- CAPS v1 semantics."""
    stack = _linear_stack()
    control = Control(
        name="filter",
        attenuations={"B": Mitigation(id="m", name="m", effectiveness=0.75)},
    )
    assert control.is_classical

    r = evaluate_control(stack, control)
    # 0.8 * (1 - 0.75) = 0.2 ; score = 0.2 * 8.0 * 10 = 16.0 ; baseline = 64.0
    assert r["baseline"] == pytest.approx(64.0)
    assert r["score_full"] == pytest.approx(16.0)
    assert r["delta_full"] == pytest.approx(48.0)
    # With no induced surface the two semantics must agree exactly.
    assert r["delta_v1"] == pytest.approx(r["delta_full"])
    assert r["sign_inverted"] is False


def test_induced_surface_can_invert_the_sign():
    """A control whose own node outscores the path it protects is net-harmful."""
    stack = _linear_stack()
    control = Control(
        name="shared guardrail",
        attenuations={"B": Mitigation(id="m", name="m", effectiveness=0.75)},
        induced_components=[
            Component(
                id="G",
                name="Guardrail",
                type="orchestrator",
                asset_value=10.0,
                vulnerabilities=[
                    Vulnerability(id="vG", name="vG", exploitability=0.9, impact=9.0)
                ],
            )
        ],
        induced_connections=[
            Connection(source="A", destination="G"),
            Connection(source="G", destination="B"),
        ],
    )
    assert not control.is_classical

    r = evaluate_control(stack, control)
    # CAPS v1 sees only the attenuation, so it reports the same benefit as above.
    assert r["delta_v1"] == pytest.approx(48.0)
    # The induced node itself scores 0.9 * 10.0 * 10 = 90.0 > baseline 64.0.
    assert r["score_full"] == pytest.approx(90.0)
    assert r["delta_full"] < 0
    assert r["sign_inverted"] is True


def test_caps_v1_delta_is_blind_to_induced_surface():
    """The v1 delta is invariant to induced surface; the true delta is not."""
    stack = _linear_stack()

    def make(asset_value, exploitability):
        return Control(
            name=f"g({asset_value},{exploitability})",
            attenuations={"B": Mitigation(id="m", name="m", effectiveness=0.75)},
            induced_components=[
                Component(
                    id="G",
                    name="G",
                    type="orchestrator",
                    asset_value=asset_value,
                    vulnerabilities=[
                        Vulnerability(
                            id="vG", name="vG", exploitability=exploitability, impact=5.0
                        )
                    ],
                )
            ],
            induced_connections=[
                Connection(source="A", destination="G"),
                Connection(source="G", destination="B"),
            ],
        )

    results = [evaluate_control(stack, make(a, e)) for a in (5.0, 8.0, 10.0) for e in (0.4, 0.9)]

    v1_values = {r["delta_v1"] for r in results}
    true_values = {r["delta_full"] for r in results}

    assert len(v1_values) == 1, "v1 must report one value across all configurations"
    assert len(true_values) > 1, "the true effect must vary"


def test_control_application_does_not_mutate_the_original_stack():
    stack = get_model_router()
    before_components = len(stack.components)
    before_connections = len(stack.connections)
    before_score = max_path_score(stack)

    control = Control(
        name="c",
        attenuations={"model_router": Mitigation(id="m", name="m", effectiveness=0.8)},
        induced_components=[
            Component(id="X", name="X", type="tool", asset_value=6.0)
        ],
        induced_connections=[Connection(source="partner_app", destination="X")],
    )
    control.apply(stack)

    assert len(stack.components) == before_components
    assert len(stack.connections) == before_connections
    assert max_path_score(stack) == pytest.approx(before_score)


def test_ranking_disagreement_is_detectable():
    """Two controls that tie under v1 can differ materially once surface is counted."""
    stack = get_model_router()
    atten = {"model_router": Mitigation(id="m", name="m", effectiveness=0.80)}

    dedicated = Control(name="dedicated", attenuations=atten)
    shared = Control(
        name="shared",
        attenuations=atten,
        induced_components=[
            Component(
                id="G",
                name="G",
                type="orchestrator",
                asset_value=6.0,
                vulnerabilities=[
                    Vulnerability(id="vG", name="vG", exploitability=0.75, impact=7.0)
                ],
            )
        ],
        induced_connections=[
            Connection(source="partner_app", destination="G"),
            Connection(source="G", destination="model_router"),
        ],
    )

    ranking_v1, ranking_full = rank_controls(stack, [dedicated, shared])

    # Identical under v1 ...
    assert ranking_v1[0]["delta_v1"] == pytest.approx(ranking_v1[1]["delta_v1"])
    # ... but the dedicated control is strictly better once surface is accounted for.
    by_name = {r["name"]: r for r in ranking_full}
    assert by_name["dedicated"]["delta_full"] > by_name["shared"]["delta_full"]
    assert ranking_full[0]["name"] == "dedicated"


def test_unknown_target_component_is_rejected():
    stack = _linear_stack()
    control = Control(
        name="bad",
        attenuations={"does_not_exist": Mitigation(id="m", name="m", effectiveness=0.5)},
    )
    with pytest.raises(ValueError, match="unknown component"):
        control.apply(stack)


def test_duplicate_induced_component_is_rejected():
    stack = _linear_stack()
    control = Control(
        name="bad",
        induced_components=[Component(id="B", name="dup", type="tool", asset_value=2.0)],
    )
    with pytest.raises(ValueError, match="duplicate component"):
        control.apply(stack)
