import pytest
from caps.models import DeploymentStack, Component, Connection, Vulnerability, Mitigation
from caps.engine import AnalysisEngine
from caps.templates import get_rag_chatbot, get_autonomous_coding_agent


def test_graph_construction():
    stack = get_rag_chatbot()
    engine = AnalysisEngine(stack)
    
    assert engine.graph is not None
    assert len(engine.graph.nodes) == 5
    assert len(engine.graph.edges) == 6
    
    # Check node metadata inclusion
    assert engine.graph.nodes["prompt_gateway"]["component"].name == "LLM Prompt Gateway (Orchestrator)"


def test_entry_and_targets():
    stack = get_rag_chatbot()
    engine = AnalysisEngine(stack)
    
    entry_points = engine.get_entry_points()
    assert "attacker" in entry_points or "chat_ui" in entry_points
    
    targets = engine.get_target_nodes()
    # customer_db has asset value 9.5 >= 5.0 and type database
    assert "customer_db" in targets
    # vector_db has asset value 7.5 >= 5.0 and type vector_db
    assert "vector_db" in targets
    # attacker should NOT be a target
    assert "attacker" not in targets


def test_effective_exploitability():
    stack = get_rag_chatbot()
    gateway = stack.get_component("prompt_gateway")
    
    # Base exploitability for indirect_prompt_injection is 0.85
    # regex filter mitigation effectiveness is 0.30
    # Effective exploitability = 0.85 * (1 - 0.30) = 0.595
    eff = gateway.get_effective_exploitability("indirect_prompt_injection")
    assert eff == pytest.approx(0.595)


def test_path_scoring_with_decay():
    # Simple linear chain to test formula precisely:
    # A (attacker) -> B (orchestrator, asset 5, vuln 0.8) -> C (database, asset 10, vuln 0.9)
    # decay = 0.9
    stack = DeploymentStack(
        name="Precise Test Stack",
        components=[
            Component(id="A", name="Attacker", type="attacker", asset_value=1.0),
            Component(
                id="B", 
                name="Middle", 
                type="orchestrator", 
                asset_value=5.0,
                vulnerabilities=[Vulnerability(id="vB", name="vB", exploitability=0.8, impact=5.0)]
            ),
            Component(
                id="C", 
                name="Target", 
                type="database", 
                asset_value=10.0,
                vulnerabilities=[Vulnerability(id="vC", name="vC", exploitability=0.9, impact=10.0)]
            )
        ],
        connections=[
            Connection(source="A", destination="B"),
            Connection(source="B", destination="C")
        ],
        chaining_decay=0.9
    )
    
    engine = AnalysisEngine(stack)
    paths = engine.analyze_paths()
    
    # Path is: A -> B -> C
    # Node exploitabilities:
    # A (attacker) = 1.0
    # B (orchestrator) = 0.8
    # C (database) = 0.9
    # Exploitability product = 1.0 * 0.8 * 0.9 = 0.72
    # Chaining decay for 2 hops (path length 3): 0.9 ** 2 = 0.81
    # Joint likelihood = 0.72 * 0.81 = 0.5832
    # Score = 0.5832 * asset_value(C) * 10 = 0.5832 * 10 * 10 = 58.32
    p_abc = next((p for p in paths if p["path"] == ["A", "B", "C"]), None)
    assert p_abc is not None
    assert p_abc["likelihood"] == pytest.approx(0.5832)
    assert p_abc["score"] == pytest.approx(58.32)


def test_cycle_handling():
    # Setup a cycle: A -> B -> C -> B
    # Simple paths should prevent infinite loops and find A -> B -> C correctly.
    stack = DeploymentStack(
        name="Cycle Test Stack",
        components=[
            Component(id="A", name="Attacker", type="attacker", asset_value=1.0),
            Component(id="B", name="Orch", type="orchestrator", asset_value=5.0),
            Component(id="C", name="DB", type="database", asset_value=10.0)
        ],
        connections=[
            Connection(source="A", destination="B"),
            Connection(source="B", destination="C"),
            Connection(source="C", destination="B")
        ],
        chaining_decay=1.0
    )
    
    engine = AnalysisEngine(stack)
    paths = engine.analyze_paths()
    
    # Should resolve path without infinite loops
    assert len(paths) > 0
    p_abc = next((p for p in paths if p["path"] == ["A", "B", "C"]), None)
    assert p_abc is not None


def test_mitigation_roi():
    stack = get_autonomous_coding_agent()
    engine = AnalysisEngine(stack)
    
    recs = engine.recommend_mitigations()
    assert len(recs) > 0
    
    # Recommendations should be sorted by score reduction descending
    for i in range(len(recs) - 1):
        assert recs[i]["score_reduction"] >= recs[i+1]["score_reduction"]
