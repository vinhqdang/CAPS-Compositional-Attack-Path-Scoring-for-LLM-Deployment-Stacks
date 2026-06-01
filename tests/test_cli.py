import os
import json
import pytest
from caps import cli


def test_get_severity_style():
    assert cli.get_severity_style(85.0) == "critical"
    assert cli.get_severity_style(55.0) == "high"
    assert cli.get_severity_style(25.0) == "medium"
    assert cli.get_severity_style(5.0) == "low"


def test_get_severity_label():
    assert cli.get_severity_label(85.0) == "CRITICAL"
    assert cli.get_severity_label(55.0) == "HIGH"
    assert cli.get_severity_label(25.0) == "MEDIUM"
    assert cli.get_severity_label(5.0) == "LOW"


def test_load_stack_from_template():
    stack = cli.load_stack_from_source("rag-chatbot")
    assert stack.name == "RAG Chatbot Stack"
    assert len(stack.components) == 5


def test_cmd_save_template(tmp_path):
    class Args:
        template = "rag-chatbot"
        output = str(tmp_path / "temp_template.json")
        
    cli.cmd_save_template(Args())
    
    assert os.path.exists(Args.output)
    
    with open(Args.output, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    assert data["name"] == "RAG Chatbot Stack"
    assert len(data["components"]) == 5


def test_cmd_export_html(tmp_path):
    class Args:
        source = "rag-chatbot"
        output = str(tmp_path / "temp_report.html")
        
    cli.cmd_export(Args())
    
    assert os.path.exists(Args.output)
    
    with open(Args.output, "r", encoding="utf-8") as f:
        content = f.read()
        
    assert "<title>CAPS | Compositional Attack Path Scoring Report</title>" in content
    assert "RAG Chatbot Stack" in content
