# CAPS: Compositional Attack Path Scoring for LLM Deployment Stacks

[![Python 3.13](https://img.shields.io/badge/python-3.13-blue.svg)](https://www.python.org/downloads/release/python-3130/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Build Status](https://img.shields.io/badge/tests-passing-brightgreen.svg)](#verification-and-automated-tests)

**CAPS** is a comprehensive Python library and Command-Line Interface (CLI) tool designed to model, analyze, and score multi-hop **compositional attack paths** in Large Language Model (LLM) deployment architectures.

In modern enterprise applications, AI agents and LLMs are chained with APIs, vector stores, and custom tools. Traditional vulnerability assessment mechanisms (e.g., CVSS) fail to capture **compound risk**, where multiple individually "low" or "medium" vulnerabilities are composed to trigger critical system compromises (e.g., an indirect prompt injection leading to shell command execution). CAPS visualizes and scores these threat vectors using topological graphs, providing robust, data-backed security auditing.

---

## ⚡ Core Concepts & Mathematical Model

CAPS represents an LLM deployment stack as a directed graph $G = (V, E)$.

1. **Components ($V$)**:
   - Each component $v \in V$ has an **Asset Value** (impact rating) $I(v) \in [1, 10]$.
   - Each component has zero or more **Vulnerabilities** $vuln \in Vuln(v)$ with a base **Exploitability** $E(vuln) \in (0, 1]$.
   - Each component has zero or more **Mitigations** $mit \in Mit(v)$ with an **Effectiveness** rating $M(mit) \in [0, 1)$.

2. **Effective Exploitability**:
   Active mitigations scale down a vulnerability's susceptibility to exploitation:
   $$E_{eff}(vuln) = E(vuln) \times \prod_{mit \in Mit(v)} (1 - M(mit))$$

3. **Joint Path Exploitability**:
   For any attack path $P = (v_1, v_2, \dots, v_k)$, the joints likelihood of exploitation is the product of individual hop exploitabilities, penalized by a **chaining decay factor** $\alpha$ representing coordination difficulty:
   $$P_{exploit}(P) = \alpha^{k-1} \prod_{i=1}^k E_{eff}(vuln_i)$$

4. **Compositional Path score**:
   $$S(P) = P_{exploit}(P) \times I(v_k) \times 10$$
   The resulting risk score scales from `0` (no risk) to `100` (highest threat).

---

## 📦 Project Structure

```
CAPS-Compositional-Attack-Path-Scoring-for-LLM-Deployment-Stacks/
├── caps/
│   ├── __init__.py
│   ├── models.py       # Pydantic schema representations
│   ├── engine.py       # NetworkX path calculations & mitigation simulation ROI
│   ├── templates.py    # Preconfigured LLM stacks (RAG, Code Agent, Router)
│   ├── report.py       # High-fidelity CSS grid HTML/CSS report compiler
│   └── cli.py          # Premium console UI formatting utilizing Rich
├── tests/
│   ├── test_engine.py  # Unit tests for paths, decay, and mathematics
│   └── test_cli.py     # Integration tests for commands and exports
├── pyproject.toml      # Build metadata and package configuration
├── README.md           # Visual landing page and documentation
└── plan.md             # Implementation blueprint
```

---

## 📝 Academic Manuscript

The `manuscripts/` directory contains the LaTeX source code for the academic paper detailing the CAPS framework. It includes comprehensive evaluations across three topologies (RAG Chatbot, Autonomous Agent, and Model Router) and highlights the efficacy of the chaining decay factor $\alpha$ and Mitigation ROI prioritization. The `figures/` subdirectory contains generated architectural diagrams, including the `method_overview.png` and `rag_topology.png`.

---

## 🚀 Setup Instructions

CAPS runs beautifully in the **py313** Conda environment which is already pre-configured in this workspace.

### Environment Activation
To configure and use the pre-packaged python environment:
```powershell
conda activate py313
```

### Running CLI directly
Ensure all dependencies are resolved by executing commands directly with the `py313` Python environment:
```powershell
& "C:\Users\vinh.dq4\AppData\Local\anaconda3\envs\py313\python.exe" -m caps.cli --help
```

---

## 🛠️ CLI Usage & Command Reference

CAPS features a styled CLI console that formats graphs, paths, trees, and tables.

### 1. List Preconfigured Architectures
Browse built-in stacks containing pre-mapped vulnerabilities:
```powershell
& "C:\Users\vinh.dq4\AppData\Local\anaconda3\envs\py313\python.exe" -m caps.cli list-templates
```

### 2. Analyze Attack Paths
Analyze a stack to map all possible simple paths from entry nodes to targets, visualizes the critical chain as a tree, and print scores:
```powershell
& "C:\Users\vinh.dq4\AppData\Local\anaconda3\envs\py313\python.exe" -m caps.cli analyze rag-chatbot
```

### 3. Mitigation ROI Recommendations
Simulate the security impact of adding standard or custom mitigations, ranking recommendations by the highest risk score reduction:
```powershell
& "C:\Users\vinh.dq4\AppData\Local\anaconda3\envs\py313\python.exe" -m caps.cli recommend autonomous-coding-agent
```

### 4. Export Interactive HTML Report
Compile the topology metadata, attack path tree, vulnerability items, and ROI tables into a stunning, responsive HTML/CSS dashboard:
```powershell
& "C:\Users\vinh.dq4\AppData\Local\anaconda3\envs\py313\python.exe" -m caps.cli export model-router --output report.html
```

### 5. Custom Stack Customization
Export a template stack to a JSON file to serve as a customizable template, and analyze it directly:
```powershell
# Save template to a JSON configuration
& "C:\Users\vinh.dq4\AppData\Local\anaconda3\envs\py313\python.exe" -m caps.cli save-template rag-chatbot -o my_custom_stack.json

# Analyze your custom JSON configuration
& "C:\Users\vinh.dq4\AppData\Local\anaconda3\envs\py313\python.exe" -m caps.cli analyze my_custom_stack.json
```

---

## 🧪 Verification and Automated Tests

The test suite validates path scoring calculations, cycle limits, custom validations, and HTML export reliability. Run tests using `pytest`:

```powershell
& "C:\Users\vinh.dq4\AppData\Local\anaconda3\envs\py313\python.exe" -m pytest -v
```

All unit and integration tests compile and execute cleanly in **< 1.5 seconds**.

---

## 🛡️ Preconfigured Architectures Details

1. **RAG Chatbot Stack (`rag-chatbot`)**:
   - Represents a corporate assistant exposed to indirect prompt injection via poisoned documents scraped into a Pinecone DB. Demonstrates how prompt injection translates to database hijacking via tool misuse.
2. **Autonomous Coding Agent Stack (`autonomous-coding-agent`)**:
   - Represents a LangGraph/CrewAI coding agent scanning git files. Explores arbitrary shell execution commands running directly on the host VM.
3. **Enterprise Model Router Stack (`model-router`)**:
   - Represents an enterprise gateway router directing calls to public standard models or confidential databases. Features role confusion and data leakage pathways.