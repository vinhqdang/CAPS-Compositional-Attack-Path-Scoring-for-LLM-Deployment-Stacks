from typing import Dict
from caps.models import DeploymentStack, Component, Connection, Vulnerability, Mitigation


def get_rag_chatbot() -> DeploymentStack:
    """Pre-configured RAG Chatbot Deployment Stack template."""
    return DeploymentStack(
        name="RAG Chatbot Stack",
        description="A standard corporate customer service chatbot connected to a Pinecone vector DB and internal SQL client.",
        components=[
            Component(
                id="attacker",
                name="External Attacker / Web Client",
                type="attacker",
                asset_value=1.0,
                vulnerabilities=[],
                mitigations=[]
            ),
            Component(
                id="chat_ui",
                name="Chat UI Frontend",
                type="user",
                asset_value=2.0,
                vulnerabilities=[
                    Vulnerability(
                        id="xss",
                        name="Stored Cross-Site Scripting (XSS)",
                        description="Chat UI does not sanitize chatbot markdown outputs, allowing code execution in client browser.",
                        exploitability=0.65,
                        impact=5.0
                    )
                ],
                mitigations=[]
            ),
            Component(
                id="prompt_gateway",
                name="LLM Prompt Gateway (Orchestrator)",
                type="orchestrator",
                asset_value=5.0,
                vulnerabilities=[
                    Vulnerability(
                        id="indirect_prompt_injection",
                        name="Indirect Prompt Injection",
                        description="Gateway dynamically concatenates external RAG outputs into model prompt without safety envelopes.",
                        exploitability=0.85,
                        impact=7.0
                    )
                ],
                mitigations=[
                    Mitigation(
                        id="weak_regex_filter",
                        name="Regex Input Filtering",
                        description="A basic regex-based prompt filter that attempts to block common injection keywords.",
                        effectiveness=0.30
                    )
                ]
            ),
            Component(
                id="vector_db",
                name="Pinecone Vector Database (RAG)",
                type="vector_db",
                asset_value=7.5,
                vulnerabilities=[
                    Vulnerability(
                        id="data_poisoning",
                        name="RAG Document Poisoning",
                        description="External attackers can upload feedback or documentation to website that is scraped and embedded in the vector DB.",
                        exploitability=0.80,
                        impact=6.0
                    )
                ],
                mitigations=[]
            ),
            Component(
                id="customer_db",
                name="Confidential Customer DB (SQL)",
                type="database",
                asset_value=9.5,
                vulnerabilities=[
                    Vulnerability(
                        id="sql_injection",
                        name="SQL Injection via SQL Agent Tool",
                        description="SQL tool takes natural language queries from orchestrator and translates them into SQL without parameterization.",
                        exploitability=0.75,
                        impact=9.5
                    )
                ],
                mitigations=[]
            )
        ],
        connections=[
            Connection(source="attacker", destination="chat_ui", description="Attacker sends chat message"),
            Connection(source="chat_ui", destination="prompt_gateway", description="Frontend forwards message to LLM gateway"),
            Connection(source="prompt_gateway", destination="vector_db", description="Gateway queries embeddings to enrich prompt context"),
            Connection(source="prompt_gateway", destination="customer_db", description="Gateway calls SQL Tool to query user details"),
            Connection(source="vector_db", destination="prompt_gateway", description="Returns injected/poisoned context"),
            Connection(source="customer_db", destination="chat_ui", description="Exfiltrates data back to UI output")
        ],
        chaining_decay=0.9
    )


def get_autonomous_coding_agent() -> DeploymentStack:
    """Pre-configured Autonomous Developer Coding Agent template."""
    return DeploymentStack(
        name="Autonomous Coding Agent Stack",
        description="A developer agent (built with LangGraph/CrewAI) that scans GitHub pull requests and executes bash scripts in a terminal.",
        components=[
            Component(
                id="malicious_repo",
                name="Untrusted GitHub Repository (Attacker)",
                type="attacker",
                asset_value=1.0,
                vulnerabilities=[],
                mitigations=[]
            ),
            Component(
                id="agent_orchestrator",
                name="DevAgent Core Orchestrator (LangGraph)",
                type="orchestrator",
                asset_value=6.0,
                vulnerabilities=[
                    Vulnerability(
                        id="indirect_prompt_injection_repo",
                        name="Indirect Prompt Injection via Repo Code",
                        description="Agent scans files (like README or config) containing injection commands telling the agent to ignore user instructions and run shell scripts.",
                        exploitability=0.90,
                        impact=8.0
                    )
                ],
                mitigations=[]
            ),
            Component(
                id="file_writer",
                name="File Writer Tool",
                type="tool",
                asset_value=4.0,
                vulnerabilities=[
                    Vulnerability(
                        id="path_traversal",
                        name="Path Traversal",
                        description="File writer tool does not restrict directories, enabling writing files to system startup folder.",
                        exploitability=0.70,
                        impact=8.5
                    )
                ],
                mitigations=[]
            ),
            Component(
                id="bash_executor",
                name="Bash Command Execution Tool",
                type="tool",
                asset_value=8.0,
                vulnerabilities=[
                    Vulnerability(
                        id="arbitrary_code_exec",
                        name="Arbitrary Shell Execution",
                        description="Bash tool executes any generated command directly on the host machine without containment.",
                        exploitability=0.95,
                        impact=9.5
                    )
                ],
                mitigations=[
                    Mitigation(
                        id="read_only_workspace",
                        name="Read-Only Workspace Directory Limitation",
                        description="Restricts basic file tools to the workspace, but bash execution remains unconstrained.",
                        effectiveness=0.20
                    )
                ]
            ),
            Component(
                id="production_host",
                name="Host Operating System & Cloud Node",
                type="database",
                asset_value=10.0,
                vulnerabilities=[
                    Vulnerability(
                        id="host_compromise",
                        name="Full Host Control / Privilege Escalation",
                        description="Attacker executing root commands on the cloud VM can exfiltrate credentials and take over production cluster.",
                        exploitability=0.85,
                        impact=10.0
                    )
                ],
                mitigations=[]
            )
        ],
        connections=[
            Connection(source="malicious_repo", destination="agent_orchestrator", description="Agent reads and parses repository files"),
            Connection(source="agent_orchestrator", destination="file_writer", description="Agent requests file write"),
            Connection(source="agent_orchestrator", destination="bash_executor", description="Agent requests bash command execution"),
            Connection(source="bash_executor", destination="production_host", description="Commands execute on host system environment")
        ],
        chaining_decay=0.95
    )


def get_model_router() -> DeploymentStack:
    """Pre-configured Enterprise Model Router stack."""
    return DeploymentStack(
        name="Enterprise Model Router Stack",
        description="A centralized AI gateway router that forwards user queries to public standard models or private confidential models.",
        components=[
            Component(
                id="partner_app",
                name="Partner SaaS API Integration",
                type="user",
                asset_value=3.0,
                vulnerabilities=[],
                mitigations=[]
            ),
            Component(
                id="model_router",
                name="Enterprise Model Router (API Gateway)",
                type="orchestrator",
                asset_value=7.0,
                vulnerabilities=[
                    Vulnerability(
                        id="routing_hijack",
                        name="Router Configuration/Access Hijack",
                        description="Router accepts query parameters that override the routing logic, enabling redirect to unauthorized private models.",
                        exploitability=0.80,
                        impact=7.5
                    )
                ],
                mitigations=[]
            ),
            Component(
                id="public_llama",
                name="Llama-3 Public API Endpoint",
                type="api",
                asset_value=4.0,
                vulnerabilities=[
                    Vulnerability(
                        id="jailbreak",
                        name="Model Guardrail Bypass (Jailbreak)",
                        description="Model can be easily jailbroken to output unsafe text or malicious instructions.",
                        exploitability=0.90,
                        impact=4.0
                    )
                ],
                mitigations=[]
            ),
            Component(
                id="confidential_gpt4",
                name="GPT-4 Confidential Corporate instance",
                type="api",
                asset_value=8.5,
                vulnerabilities=[
                    Vulnerability(
                        id="data_leakage",
                        name="System Prompt Leak & Private Memorization Extraction",
                        description="Confidential model contains proprietary trade secrets in its system instructions that can be extracted via prompt injection.",
                        exploitability=0.70,
                        impact=8.5
                    )
                ],
                mitigations=[
                    Mitigation(
                        id="system_instruction_guard",
                        name="System Prompt Guardrail",
                        description="Prevents echoing of system prompts and filters out confidential keys.",
                        effectiveness=0.60
                    )
                ]
            ),
            Component(
                id="treasury_database",
                name="Corporate Treasury Database Connection",
                type="database",
                asset_value=10.0,
                vulnerabilities=[
                    Vulnerability(
                        id="unauthenticated_api",
                        name="Unauthenticated Database Tool",
                        description="Database client tool used by confidential model does not validate corporate API signatures.",
                        exploitability=0.85,
                        impact=10.0
                    )
                ],
                mitigations=[]
            )
        ],
        connections=[
            Connection(source="partner_app", destination="model_router", description="Partner app queries AI gateway"),
            Connection(source="model_router", destination="public_llama", description="Gateway routes simple tasks to Llama 3"),
            Connection(source="model_router", destination="confidential_gpt4", description="Gateway routes sensitive tasks to GPT-4"),
            Connection(source="confidential_gpt4", destination="treasury_database", description="GPT-4 queries financial records via tool call")
        ],
        chaining_decay=0.85
    )


def load_template(name: str) -> DeploymentStack:
    """Retrieve template by simplified name."""
    mapping = {
        "rag-chatbot": get_rag_chatbot,
        "autonomous-coding-agent": get_autonomous_coding_agent,
        "model-router": get_model_router
    }
    
    normalized_name = name.lower().replace("_", "-")
    creator = mapping.get(normalized_name)
    if not creator:
        raise ValueError(f"Unknown template: '{name}'. Available templates: {list(mapping.keys())}")
        
    return creator()


def get_templates_list() -> Dict[str, str]:
    """Get list of templates and their descriptions."""
    return {
        "rag-chatbot": "Corporate customer service chatbot connected to Pinecone vector DB and SQL database.",
        "autonomous-coding-agent": "A LangGraph agent with tool write access and direct bash command execution on host OS.",
        "model-router": "API gateway router routing user calls to standard or confidential enterprise databases."
    }
