import sys
import os
import json
import argparse
from typing import List

# Force stdout/stderr to utilize UTF-8 to prevent charmap UnicodeEncodeErrors in Windows legacy consoles
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich.tree import Tree
from rich.theme import Theme

from caps.models import DeploymentStack
from caps import templates
from caps.engine import AnalysisEngine
from caps.report import generate_html_report

# Custom color scheme for a premium look
custom_theme = Theme({
    "info": "cyan",
    "warning": "yellow",
    "error": "red",
    "success": "green",
    "critical": "bold red",
    "high": "bold orange3",
    "medium": "bold yellow",
    "low": "bold green",
    "brand": "bold purple"
})

console = Console(theme=custom_theme)


def get_severity_style(score: float) -> str:
    if score >= 70.0:
        return "critical"
    elif score >= 40.0:
        return "high"
    elif score >= 15.0:
        return "medium"
    return "low"


def get_severity_label(score: float) -> str:
    if score >= 70.0:
        return "CRITICAL"
    elif score >= 40.0:
        return "HIGH"
    elif score >= 15.0:
        return "MEDIUM"
    return "LOW"


def load_stack_from_source(source: str) -> DeploymentStack:
    """Load deployment stack from either a JSON file or a predefined template."""
    if source.endswith(".json"):
        if not os.path.exists(source):
            console.print(f"[error]Error:[/error] File not found at '{source}'")
            sys.exit(1)
        try:
            with open(source, "r", encoding="utf-8") as f:
                data = json.load(f)
            return DeploymentStack.model_validate(data)
        except Exception as e:
            console.print(f"[error]Error parsing Pydantic stack configuration from JSON file:[/error] {e}")
            sys.exit(1)
    else:
        try:
            return templates.load_template(source)
        except ValueError as e:
            console.print(f"[error]Error:[/error] {e}")
            console.print("\nUse `caps list-templates` to see available predefined architectures.")
            sys.exit(1)


def cmd_list_templates(args):
    """List available preconfigured templates."""
    console.print(Panel(
        "[brand]CAPS: Compositional Attack Path Scoring[/brand]\n[info]Preconfigured LLM Deployment Architectures[/info]",
        border_style="purple"
    ))
    
    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Template ID", style="cyan", width=25)
    table.add_column("Architecture Description", style="white")
    
    for t_id, desc in templates.get_templates_list().items():
        table.add_row(t_id, desc)
        
    console.print(table)
    console.print("\nYou can analyze these directly: [bold green]caps analyze <template-id>[/bold green]")


def cmd_analyze(args):
    """Analyze the stack vulnerabilities and list attack paths."""
    stack = load_stack_from_source(args.source)
    engine = AnalysisEngine(stack)
    paths = engine.analyze_paths()
    
    # Header panel
    console.print(Panel(
        f"[brand]CAPS Analysis Summary for: {stack.name}[/brand]\n"
        f"[dim]{stack.description}[/dim]",
        border_style="purple"
    ))
    
    # Overall summary stats
    total_vulns = sum(len(c.vulnerabilities) for c in stack.components)
    total_mits = sum(len(c.mitigations) for c in stack.components)
    max_score = paths[0]["score"] if paths else 0.0
    
    severity_style = get_severity_style(max_score)
    severity_label = get_severity_label(max_score)
    
    summary_table = Table.grid(padding=(0, 2))
    summary_table.add_column(style="cyan")
    summary_table.add_column(style="bold white")
    summary_table.add_row("Total Components:", str(len(stack.components)))
    summary_table.add_row("Total Data Flows:", str(len(stack.connections)))
    summary_table.add_row("Vulnerabilities:", str(total_vulns))
    summary_table.add_row("Active Mitigations:", str(total_mits))
    summary_table.add_row(
        "Maximum Attack Path Score:", 
        f"[{severity_style}]{max_score:.1f} ({severity_label} RISK)[/{severity_style}]"
    )
    
    console.print(Panel(summary_table, title="Topology Metadata", border_style="cyan"))
    
    if not paths:
        console.print("[success]No attack paths detected in this topology![/success]")
        return

    # Visual Critical Path Tree
    console.print("\n[brand]⚡ Critical Attack Path Map:[/brand]")
    critical_path = paths[0]
    
    tree = Tree(f"[bold magenta]Start: {critical_path['path'][0]}[/bold magenta]")
    current_tree = tree
    for i, node_id in enumerate(critical_path["path"][1:]):
        comp = stack.get_component(node_id)
        vuln = critical_path["vulnerabilities"][i+1] # node 0 has index 0
        
        lbl = f"[bold white]{comp.name}[/bold white] [dim]({comp.type})[/dim]"
        if vuln:
            lbl += f"\n  ┗━ [bold red]⚠️ Exploits: {vuln.name}[/bold red] [dim](Eff. Exploitability: {comp.get_effective_exploitability(vuln.id):.2f})[/dim]"
            
        if i == len(critical_path["path"]) - 2: # Last node
            lbl += f" ➜ [bold red][Target: Score {critical_path['score']:.1f}][/bold red]"
            
        current_tree = current_tree.add(lbl)
        
    console.print(tree)
    console.print("")

    # Detailed Path List Table
    paths_table = Table(show_header=True, header_style="bold magenta", expand=True)
    paths_table.add_column("Rank", justify="center", style="cyan", width=6)
    paths_table.add_column("Path Chain", style="white")
    paths_table.add_column("Joint Likelihood", justify="right", style="yellow")
    paths_table.add_column("Target Value", justify="right", style="cyan")
    paths_table.add_column("CAPS Score", justify="right")
    
    for idx, path_info in enumerate(paths):
        chain_str = " ➜ ".join(path_info["path"])
        score_val = path_info["score"]
        sev_style = get_severity_style(score_val)
        
        paths_table.add_row(
            str(idx + 1),
            chain_str,
            f"{path_info['likelihood']:.3f}",
            f"{path_info['target_impact']:.1f}",
            f"[{sev_style}]{score_val:.1f}[/{sev_style}]"
        )
        
    console.print(paths_table)


def cmd_recommend(args):
    """Analyze the stack and generate prioritized mitigation recommendations."""
    stack = load_stack_from_source(args.source)
    engine = AnalysisEngine(stack)
    recommendations = engine.recommend_mitigations()
    
    console.print(Panel(
        f"[brand]Mitigation ROI Recommendations for: {stack.name}[/brand]",
        border_style="purple"
    ))
    
    if not recommendations:
        console.print("[info]No mitigation recommendations generated for this stack configuration.[/info]")
        return
        
    table = Table(show_header=True, header_style="bold magenta", expand=True)
    table.add_column("Priority", justify="center", style="cyan", width=8)
    table.add_column("Target Component", style="white")
    table.add_column("Proposed Mitigation", style="bold green")
    table.add_column("Security Impact Description", style="dim")
    table.add_column("Risk Reduction", justify="right", style="bold green")
    
    for idx, rec in enumerate(recommendations):
        table.add_row(
            str(idx + 1),
            rec["component_name"],
            rec["mitigation_name"],
            rec["description"],
            f"-{rec['percentage_reduction']:.1f}%"
        )
        
    console.print(table)
    console.print("\nMitigation effects can be simulated by updating the stack YAML/JSON configuration files with active mitigations.")


def cmd_export(args):
    """Export the stack analysis to a high-fidelity HTML report."""
    stack = load_stack_from_source(args.source)
    engine = AnalysisEngine(stack)
    paths = engine.analyze_paths()
    recommendations = engine.recommend_mitigations()
    
    html = generate_html_report(stack, paths, recommendations)
    
    try:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(html)
        console.print(f"[success]Successfully exported gorgeous HTML report to: [bold white]{args.output}[/bold white][/success]")
    except Exception as e:
        console.print(f"[error]Error exporting report:[/error] {e}")
        sys.exit(1)


def cmd_save_template(args):
    """Save a preconfigured template to a JSON file for custom editing."""
    try:
        stack = templates.load_template(args.template)
    except ValueError as e:
        console.print(f"[error]Error:[/error] {e}")
        sys.exit(1)
        
    try:
        # Pydantic JSON dumping
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(stack.model_dump(), f, indent=4)
        console.print(f"[success]Template '{args.template}' successfully written to: [bold white]{args.output}[/bold white][/success]")
        console.print("You can now edit this JSON file to customize components, vulnerabilities, and connections.")
    except Exception as e:
        console.print(f"[error]Error writing JSON file:[/error] {e}")
        sys.exit(1)


def app():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="CAPS: Compositional Attack Path Scoring for LLM Deployment Stacks"
    )
    subparsers = parser.add_subparsers(dest="command", required=True, help="Subcommands")
    
    # list-templates
    subparsers.add_parser("list-templates", help="List predefined stack templates")
    
    # analyze
    parser_analyze = subparsers.add_parser("analyze", help="Analyze and score attack paths in a stack")
    parser_analyze.add_argument(
        "source", 
        help="Target configuration. Either a template ID (e.g. 'rag-chatbot') or path to a JSON stack configuration file (e.g. 'stack.json')"
    )
    
    # recommend
    parser_rec = subparsers.add_parser("recommend", help="Recommend security mitigations based on path analysis")
    parser_rec.add_argument(
        "source",
        help="Target configuration. Either a template ID or path to a JSON file."
    )
    
    # export
    parser_export = subparsers.add_parser("export", help="Export stack analysis to a high-fidelity HTML report")
    parser_export.add_argument(
        "source",
        help="Target configuration. Either a template ID or path to a JSON file."
    )
    parser_export.add_argument(
        "--output", "-o",
        required=True,
        help="Path to save the generated HTML file (e.g. 'report.html')"
    )
    
    # save-template
    parser_save = subparsers.add_parser("save-template", help="Export a predefined template configuration to JSON file for editing")
    parser_save.add_argument(
        "template",
        help="Name of the template (e.g. 'rag-chatbot')"
    )
    parser_save.add_argument(
        "--output", "-o",
        required=True,
        help="Path to write the JSON configuration file"
    )
    
    args = parser.parse_args()
    
    if args.command == "list-templates":
        cmd_list_templates(args)
    elif args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "recommend":
        cmd_recommend(args)
    elif args.command == "export":
        cmd_export(args)
    elif args.command == "save-template":
        cmd_save_template(args)


if __name__ == "__main__":
    app()
