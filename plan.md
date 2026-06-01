# CAPS: Compositional Attack Path Scoring for LLM Deployment Stacks

This document outlines the design and implementation plan for **CAPS**, a Python library and CLI tool to model, score, and analyze compositional attack paths in Large Language Model (LLM) deployment stacks.

## Goal Description

LLM deployment stacks integrate heterogeneous components: user interfaces, prompt gateways, orchestrators/agent frameworks (e.g., LangChain), retrieval systems (vector databases), tools (e.g., calculators, search engines, code executors), local file systems, and downstream APIs. Traditional security audits focus on individual component vulnerabilities (e.g., CVSS). However, in modern LLM stacks, severe security breaches often result from **compositional attacks**—where multiple individually low or medium-risk vulnerabilities are chained together (e.g., an indirect prompt injection that manipulates the orchestrator to call a database tool with malicious arguments).

**CAPS** addresses this by representing the LLM stack as a directed graph, modeling vulnerabilities and defense controls, identifying all potential end-to-end attack paths from attacker entry points to high-value assets, and mathematically scoring the cumulative risk.

---

## Proposed Scoring Model

CAPS represents the stack as a graph $G = (V, E)$.

1. **Components ($V$)**:
   - Each component $v \in V$ has an **Asset Value** $I(v) \in [1, 10]$ representing its sensitivity/impact if compromised.
   - Each component has zero or more **Vulnerabilities** $vuln \in Vuln(v)$, each with a base **Exploitability** $E(vuln) \in (0, 1]$.
   - Each component has zero or more **Mitigations** $mit \in Mit(v)$, each with an **Effectiveness** $M(mit) \in [0, 1)$.

2. **Effective Exploitability**:
   A vulnerability's likelihood of successful exploit is reduced by the mitigations active on that component:
   $$E_{eff}(vuln) = E(vuln) \times \prod_{mit \in Mit(v)} (1 - M(mit))$$

3. **Compositional Path scoring**:
   An attack path $P = (v_1, v_2, \dots, v_k)$ is a sequence of hops from an entry node $v_1$ to a target node $v_k$.
   The cumulative probability of path exploitation $P_{exploit}(P)$ is modeled as the product of the effective exploitabilities of the chained vulnerabilities at each node:
   $$P_{exploit}(P) = \alpha^{k-1} \prod_{i=1}^k E_{eff}(vuln_i)$$
   where $\alpha \in (0, 1]$ is a **chaining decay factor** representing the complexity of coordinating multi-hop exploits (default: 0.9).

4. **Path Risk Score**:
   $$S(P) = P_{exploit}(P) \times I(v_k) \times 10$$
   The resulting score scales from $0$ to $100$.

5. **Mitigation Recommendation**:
   The engine will calculate the "Mitigation ROI" by evaluating which hypothetical security control yields the maximum reduction in the critical path score.

---

## Directory Structure

```
c:\work\CAPS-Compositional-Attack-Path-Scoring-for-LLM-Deployment-Stacks/
├── caps/
│   ├── __init__.py
│   ├── models.py       # Pydantic schemas (Stack, Component, Connection, Vulnerability, Mitigation, Path)
│   ├── engine.py       # Core path analysis & scoring engine using networkx
│   ├── templates.py    # Predefined LLM deployment stack templates
│   ├── cli.py          # Command Line Interface (using rich for stunning terminal UI)
│   └── report.py       # Export reports to JSON or interactive HTML/CSS (using Jinja2)
├── tests/
│   ├── __init__.py
│   ├── test_engine.py  # Unit tests for path calculations and scoring formulas
│   └── test_cli.py     # CLI parameter and output verification tests
├── pyproject.toml      # Build metadata and dependencies for pip/conda
├── README.md           # Beautiful landing page documentation
└── plan.md             # Mirror of this plan in the workspace for user reference
```

---

## Proposed Changes

### Configuration Layer

#### [NEW] [pyproject.toml](file:///c:/work/CAPS-Compositional-Attack-Path-Scoring-for-LLM-Deployment-Stacks/pyproject.toml)
Defines build configuration and pins dependencies:
- `networkx` for graph graph-theory operations.
- `rich` for a beautiful, premium console experience with emojis, tables, and colored graphs.
- `pydantic` for strict typing and schema validation.
- `jinja2` for HTML report generation.
- `pytest` for testing.

---

### Core Components

#### [NEW] [models.py](file:///c:/work/CAPS-Compositional-Attack-Path-Scoring-for-LLM-Deployment-Stacks/caps/models.py)
Defines the Pydantic data models for configuration file parsing (JSON/YAML) and program representation.
- `Vulnerability`: ID, name, description, base exploitability ($E \in (0, 1]$), impact.
- `Mitigation`: ID, name, description, effectiveness ($M \in [0, 1)$).
- `Component`: ID, name, type (e.g., orchestrator, database, user), asset_value ($I \in [1, 10]$), vulnerabilities, mitigations.
- `Connection`: Source component ID, destination component ID, trust boundary crossed (boolean).
- `DeploymentStack`: Components, connections, chaining decay factor ($\alpha$).

#### [NEW] [engine.py](file:///c:/work/CAPS-Compositional-Attack-Path-Scoring-for-LLM-Deployment-Stacks/caps/engine.py)
Main calculation driver:
- Converts the `DeploymentStack` into a `networkx.DiGraph`.
- Finds all paths from entry points (components with `type="attacker"` or designated entry nodes) to all nodes with an `asset_value >= 7.0` (target nodes).
- Implements the path scoring algorithm.
- Computes hypothetical mitigation recommendations by calculating:
  $$\Delta Score = Score_{current} - Score_{with\_mitigation}$$

#### [NEW] [templates.py](file:///c:/work/CAPS-Compositional-Attack-Path-Scoring-for-LLM-Deployment-Stacks/caps/templates.py)
Provides three pre-configured deployment architecture models:
1. **RAG-based Chatbot**: Vulnerable to indirect prompt injection via poisoned reference files, allowing an attacker to pull unauthorized data.
2. **Autonomous Coding Agent**: Vulnerable to direct/indirect prompt injection, chaining into a sandboxing escape or arbitrary shell execution on a local database tool.
3. **Enterprise Model Router**: A multi-model gateway with insecure IAM controls allowing lateral movement to highly confidential models.

#### [NEW] [cli.py](file:///c:/work/CAPS-Compositional-Attack-Path-Scoring-for-LLM-Deployment-Stacks/caps/cli.py)
A gorgeous console interface utilizing `rich`:
- Emojis, styled titles, and layout panels.
- Tables representing components, active vulnerabilities, and mitigation strategies.
- An ASCII or tree-like visualization of critical attack paths.
- Step-by-step mitigation advice.
- Commands:
  - `caps list-templates`: List predefined stack designs.
  - `caps analyze <file_or_template>`: Run the scoring model.
  - `caps recommend <file_or_template>`: Run the mitigation ROI analysis.
  - `caps export <file_or_template> --output <path.html>`: Generate HTML report.

#### [NEW] [report.py](file:///c:/work/CAPS-Compositional-Attack-Path-Scoring-for-LLM-Deployment-Stacks/caps/report.py)
Generates high-fidelity HTML reports utilizing CSS grid layouts, vibrant gradients, and responsive panels, providing a premium visual output.

---

## Verification Plan

### Automated Tests
We will write extensive unit and integration tests under `tests/`:
- **Formula accuracy**: Assert that mitigations correctly scale down exploitability, and multi-hop paths correctly apply the chaining decay factor.
- **Cycle detection**: Verify that networkx handles cyclic connections gracefully without infinite loops.
- **Export reliability**: Assert that the HTML report generator compiles and outputs valid HTML.

We will run the tests using:
```bash
conda run -n py313 pytest -v
```

### Manual Verification
We will run the CLI tool inside the `py313` environment to analyze all templates:
```bash
conda run -n py313 caps list-templates
conda run -n py313 caps analyze rag-chatbot
conda run -n py313 caps recommend rag-chatbot
conda run -n py313 caps export rag-chatbot --output report.html
```
We will verify that the HTML file opens and displays beautiful responsive graphics.