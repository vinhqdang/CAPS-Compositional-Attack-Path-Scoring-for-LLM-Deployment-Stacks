import networkx as nx
from typing import List, Dict, Any, Tuple, Optional
from caps.models import DeploymentStack, Component, Vulnerability, Mitigation


class AnalysisEngine:
    def __init__(self, stack: DeploymentStack):
        self.stack = stack
        self.graph = self._build_graph()

    def _build_graph(self) -> nx.DiGraph:
        """Convert the DeploymentStack into a NetworkX directed graph."""
        g = nx.DiGraph()
        
        # Add all nodes
        for comp in self.stack.components:
            g.add_node(comp.id, component=comp)
            
        # Add all edges
        for conn in self.stack.connections:
            # Check if source and destination exist in stack components to prevent errors
            if g.has_node(conn.source) and g.has_node(conn.destination):
                g.add_edge(
                    conn.source, 
                    conn.destination, 
                    description=conn.description, 
                    trust_boundary=conn.trust_boundary
                )
                
        return g

    def get_entry_points(self) -> List[str]:
        """Identify entry points for an attacker in the stack."""
        entry_points = []
        for node, data in self.graph.nodes(data=True):
            comp = data.get("component")
            if comp:
                # Designated attacker/user nodes, or nodes with type 'user'/'attacker'
                if comp.type in ["attacker", "user"] or "attacker" in comp.id.lower():
                    entry_points.append(node)
                    
        # Fallback: if no entry nodes explicitly defined, use nodes with in-degree 0
        if not entry_points:
            entry_points = [node for node, deg in self.graph.in_degree() if deg == 0]
            
        return entry_points

    def get_target_nodes(self) -> List[str]:
        """Identify high-value targets (sensitive assets)."""
        targets = []
        for node, data in self.graph.nodes(data=True):
            comp = data.get("component")
            if comp and comp.asset_value >= 5.0 and comp.type not in ["attacker", "user"]:
                targets.append(node)
        return targets

    def _calculate_node_exploitability(self, comp: Component) -> Tuple[float, Optional[Vulnerability]]:
        """Calculate the max effective exploitability of a component and identify the exploited vulnerability."""
        if comp.type in ["attacker", "user"]:
            return 1.0, None
            
        if not comp.vulnerabilities:
            # Baseline probability of exploit for a component with no explicitly declared vulnerabilities
            # representing zero-days or standard attack surface
            return 0.1, None

        max_expl = -1.0
        worst_vuln = None
        
        for vuln in comp.vulnerabilities:
            eff_expl = comp.get_effective_exploitability(vuln.id)
            if eff_expl > max_expl:
                max_expl = eff_expl
                worst_vuln = vuln
                
        return max_expl, worst_vuln

    def analyze_paths(self) -> List[Dict[str, Any]]:
        """Find and score all simple attack paths from entry points to targets."""
        entry_points = self.get_entry_points()
        target_nodes = self.get_target_nodes()
        
        all_scored_paths = []

        for source in entry_points:
            for target in target_nodes:
                if source == target:
                    continue
                    
                # Find all simple paths (no cycles)
                try:
                    paths = list(nx.all_simple_paths(self.graph, source, target))
                except nx.NetworkXNoPath:
                    continue
                
                for path in paths:
                    path_components = []
                    path_vulnerabilities = []
                    exploitability_product = 1.0
                    
                    for node in path:
                        comp = self.graph.nodes[node]["component"]
                        path_components.append(comp)
                        
                        # Node exploitability and vulnerability
                        expl_score, vuln = self._calculate_node_exploitability(comp)
                        exploitability_product *= expl_score
                        path_vulnerabilities.append(vuln)
                        
                    # Apply chaining decay factor for path length
                    path_len = len(path)
                    decay_factor = self.stack.chaining_decay ** (path_len - 1)
                    
                    cumulative_likelihood = exploitability_product * decay_factor
                    target_comp = self.graph.nodes[target]["component"]
                    
                    # Score represents probability * impact * 10 (ranges 0 to 100)
                    path_score = cumulative_likelihood * target_comp.asset_value * 10
                    
                    all_scored_paths.append({
                        "path": path,
                        "components": path_components,
                        "vulnerabilities": path_vulnerabilities,
                        "likelihood": cumulative_likelihood,
                        "target_impact": target_comp.asset_value,
                        "score": round(path_score, 3)
                    })
                    
        # Sort paths by score descending
        all_scored_paths.sort(key=lambda x: x["score"], reverse=True)
        return all_scored_paths

    def get_critical_path(self) -> Optional[Dict[str, Any]]:
        """Get the highest scoring attack path in the stack."""
        paths = self.analyze_paths()
        return paths[0] if paths else None

    def recommend_mitigations(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Evaluate hypothetical mitigations along the critical path and rank by score reduction."""
        critical_path_info = self.get_critical_path()
        if not critical_path_info:
            return []
            
        current_max_score = critical_path_info["score"]
        if current_max_score <= 0:
            return []

        recommendations = []
        
        # We only need to mitigate components on the critical path to disrupt it!
        # Standard generic mitigations we can suggest based on component types
        standard_mitigations = [
            {
                "name": "Input Guardrail / Prompt Filter",
                "desc": "Validates inputs, filtering out known injection patterns and adversarial prompts.",
                "effectiveness": 0.8,
                "applicable_types": ["orchestrator", "user", "api"]
            },
            {
                "name": "Secure Output Guardrail",
                "desc": "Validates model output to prevent downstream injection and block execution of dangerous commands.",
                "effectiveness": 0.85,
                "applicable_types": ["orchestrator"]
            },
            {
                "name": "Sandboxed Tool Execution",
                "desc": "Runs tools (like code executors or calculators) in an isolated, short-lived container.",
                "effectiveness": 0.95,
                "applicable_types": ["tool"]
            },
            {
                "name": "Least-Privilege Database Access (RBAC)",
                "desc": "Limits database credentials to select queries, disabling writes, updates, or admin controls.",
                "effectiveness": 0.75,
                "applicable_types": ["database", "vector_db"]
            },
            {
                "name": "Strict Parameter Type Validation",
                "desc": "Enforces strict type casting and parameter checks for tool invocations.",
                "effectiveness": 0.7,
                "applicable_types": ["tool", "api"]
            }
        ]

        # Keep track of already evaluated recommendations to avoid duplicates
        evaluated_keys = set()

        for node in critical_path_info["path"]:
            comp = self.graph.nodes[node]["component"]
            if comp.type in ["attacker"]:
                continue  # Cannot mitigate the attacker itself!

            for mit_template in standard_mitigations:
                # Check if this mitigation is applicable to this component type
                if comp.type not in mit_template["applicable_types"]:
                    continue
                    
                key = (comp.id, mit_template["name"])
                if key in evaluated_keys:
                    continue
                evaluated_keys.add(key)

                # Simulate adding this mitigation to the component
                temp_mitigation = Mitigation(
                    id=f"temp_mit_{comp.id}",
                    name=mit_template["name"],
                    description=mit_template["desc"],
                    effectiveness=mit_template["effectiveness"]
                )
                
                # Backup current mitigations
                original_mitigations = list(comp.mitigations)
                
                # Apply simulated mitigation
                comp.mitigations.append(temp_mitigation)
                
                # Recalculate stack score
                new_paths = self.analyze_paths()
                new_max_score = new_paths[0]["score"] if new_paths else 0.0
                score_reduction = current_max_score - new_max_score
                
                # Restore original mitigations
                comp.mitigations = original_mitigations
                
                if score_reduction > 0.01:
                    percentage_reduction = (score_reduction / current_max_score) * 100
                    recommendations.append({
                        "component_id": comp.id,
                        "component_name": comp.name,
                        "mitigation_name": mit_template["name"],
                        "description": mit_template["desc"],
                        "effectiveness": mit_template["effectiveness"],
                        "score_before": current_max_score,
                        "score_after": round(new_max_score, 3),
                        "score_reduction": round(score_reduction, 3),
                        "percentage_reduction": round(percentage_reduction, 1)
                    })

        # Also evaluate custom mitigations for the actual vulnerabilities configured on the critical path
        # by simulating fixing/securing each specific vulnerability on the critical path.
        for node in critical_path_info["path"]:
            comp = self.graph.nodes[node]["component"]
            for vuln in comp.vulnerabilities:
                key = (comp.id, f"Patch {vuln.name}")
                if key in evaluated_keys:
                    continue
                evaluated_keys.add(key)
                
                # Simulate patching this vulnerability (removing it)
                original_vulns = list(comp.vulnerabilities)
                comp.vulnerabilities = [v for v in comp.vulnerabilities if v.id != vuln.id]
                
                new_paths = self.analyze_paths()
                new_max_score = new_paths[0]["score"] if new_paths else 0.0
                score_reduction = current_max_score - new_max_score
                
                comp.vulnerabilities = original_vulns
                
                if score_reduction > 0.01:
                    percentage_reduction = (score_reduction / current_max_score) * 100
                    recommendations.append({
                        "component_id": comp.id,
                        "component_name": comp.name,
                        "mitigation_name": f"Patch Vulnerability: {vuln.name}",
                        "description": f"Completely resolve the '{vuln.name}' vulnerability via software update or input filter.",
                        "effectiveness": 1.0,
                        "score_before": current_max_score,
                        "score_after": round(new_max_score, 3),
                        "score_reduction": round(score_reduction, 3),
                        "percentage_reduction": round(percentage_reduction, 1)
                    })

        # Sort recommendations by score reduction descending
        recommendations.sort(key=lambda x: x["score_reduction"], reverse=True)
        return recommendations[:limit]
