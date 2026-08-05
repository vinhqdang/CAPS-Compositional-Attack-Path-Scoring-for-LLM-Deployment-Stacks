import os
import sys

# Make the shared `caps` package importable when this script is run from anywhere,
# without requiring an editable install.
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from caps.templates import get_rag_chatbot, get_autonomous_coding_agent, get_model_router
from caps.engine import AnalysisEngine

def evaluate(name, stack):
    engine = AnalysisEngine(stack)
    caps_paths = engine.analyze_paths()
    caps_max = max((p["score"] for p in caps_paths), default=0)
    
    # Baseline 1: Max Component Score (Max CVSS * Impact * 10)
    # Independent component scoring ignoring mitigations (or assuming base exploitability)
    b1_max = 0
    for c in stack.components:
        for v in c.vulnerabilities:
            score = v.exploitability * c.asset_value * 10
            if score > b1_max: b1_max = score
            
    # Baseline 3: ADTree Product without decay (alpha = 1.0)
    stack_b3 = stack.model_copy(deep=True)
    stack_b3.chaining_decay = 1.0
    engine_b3 = AnalysisEngine(stack_b3)
    b3_paths = engine_b3.analyze_paths()
    b3_max = max((p["score"] for p in b3_paths), default=0)
    
    print(f"{name:20s} | B1: {b1_max:5.1f} | B3: {b3_max:5.1f} | CAPS: {caps_max:5.1f}")

evaluate("RAG Chatbot", get_rag_chatbot())
evaluate("Autonomous Agent", get_autonomous_coding_agent())
evaluate("Model Router", get_model_router())
