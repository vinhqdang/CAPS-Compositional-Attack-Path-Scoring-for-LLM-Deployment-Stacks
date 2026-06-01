import datetime
from jinja2 import Template
from typing import Dict, Any, List
from caps.models import DeploymentStack


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CAPS | Compositional Attack Path Scoring Report</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    
    <style>
        :root {
            --bg-color: #080C14;
            --panel-bg: rgba(17, 24, 39, 0.75);
            --border-color: rgba(255, 255, 255, 0.06);
            --text-primary: #F9FAFB;
            --text-secondary: #9CA3AF;
            --text-muted: #6B7280;
            
            /* Risk Severities */
            --color-critical: #FF3B30;
            --color-high: #FF9500;
            --color-medium: #FFCC00;
            --color-low: #34C759;
            --color-info: #007AFF;
            
            --grad-critical: linear-gradient(135deg, #FF3B30 0%, #FF2D55 100%);
            --grad-high: linear-gradient(135deg, #FF9500 0%, #FFCC00 100%);
            --grad-medium: linear-gradient(135deg, #FFCC00 0%, #FFD60A 100%);
            --grad-low: linear-gradient(135deg, #34C759 0%, #30D158 100%);
            --grad-info: linear-gradient(135deg, #007AFF 0%, #00C7FC 100%);
            --grad-purple: linear-gradient(135deg, #AF52DE 0%, #BF5AF2 100%);
            
            --card-shadow: 0 10px 30px -10px rgba(0, 0, 0, 0.5);
            --glow-shadow: 0 0 25px rgba(255, 59, 48, 0.15);
            
            --font-outfit: 'Outfit', sans-serif;
            --font-inter: 'Inter', sans-serif;
            --font-mono: 'JetBrains Mono', monospace;
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            font-family: var(--font-inter);
            background-color: var(--bg-color);
            color: var(--text-primary);
            min-height: 100vh;
            padding: 2.5rem 1.5rem;
            line-height: 1.6;
            background-image: 
                radial-gradient(circle at 10% 20%, rgba(0, 122, 255, 0.05) 0%, transparent 40%),
                radial-gradient(circle at 90% 80%, rgba(175, 82, 222, 0.05) 0%, transparent 40%);
            background-attachment: fixed;
        }

        .container {
            max-width: 1300px;
            margin: 0 auto;
        }

        /* --- Header --- */
        header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 3rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 2rem;
        }

        .logo-section h1 {
            font-family: var(--font-outfit);
            font-size: 2.5rem;
            font-weight: 800;
            letter-spacing: -0.05em;
            background: linear-gradient(135deg, #FFFFFF 30%, #9CA3AF 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .logo-section h1 span {
            background: var(--grad-critical);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .logo-section p {
            color: var(--text-secondary);
            font-size: 0.95rem;
            margin-top: 0.25rem;
        }

        .meta-tag {
            font-family: var(--font-mono);
            font-size: 0.85rem;
            color: var(--text-muted);
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            padding: 0.5rem 1rem;
            border-radius: 99px;
        }

        /* --- Summary Cards Grid --- */
        .summary-grid {
            display: grid;
            grid-template-columns: 1fr 2.5fr;
            gap: 2rem;
            margin-bottom: 3rem;
        }

        .glass-panel {
            background: var(--panel-bg);
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid var(--border-color);
            border-radius: 18px;
            padding: 2rem;
            box-shadow: var(--card-shadow);
            transition: transform 0.3s ease, border-color 0.3s ease;
        }

        .glass-panel:hover {
            border-color: rgba(255, 255, 255, 0.12);
        }

        /* --- Circular Score Meter --- */
        .score-box {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            position: relative;
            overflow: hidden;
        }

        .score-circle {
            width: 170px;
            height: 170px;
            border-radius: 50%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            margin-bottom: 1.5rem;
            border: 8px solid rgba(255, 255, 255, 0.02);
            position: relative;
            box-shadow: inset 0 0 30px rgba(0, 0, 0, 0.6);
        }

        .score-circle.critical {
            border-top-color: var(--color-critical);
            border-right-color: var(--color-critical);
            box-shadow: 0 0 35px rgba(255, 59, 48, 0.2), inset 0 0 30px rgba(0, 0, 0, 0.6);
        }
        .score-circle.high {
            border-top-color: var(--color-high);
            border-right-color: var(--color-high);
            box-shadow: 0 0 35px rgba(255, 149, 0, 0.2), inset 0 0 30px rgba(0, 0, 0, 0.6);
        }
        .score-circle.medium {
            border-top-color: var(--color-medium);
            border-right-color: var(--color-medium);
            box-shadow: 0 0 35px rgba(255, 204, 0, 0.2), inset 0 0 30px rgba(0, 0, 0, 0.6);
        }
        .score-circle.low {
            border-top-color: var(--color-low);
            border-right-color: var(--color-low);
            box-shadow: 0 0 35px rgba(52, 199, 89, 0.2), inset 0 0 30px rgba(0, 0, 0, 0.6);
        }

        .score-num {
            font-family: var(--font-outfit);
            font-size: 3.5rem;
            font-weight: 800;
            letter-spacing: -0.05em;
            line-height: 1;
        }

        .score-label {
            font-size: 0.85rem;
            text-transform: uppercase;
            letter-spacing: 0.1em;
            font-weight: 600;
            color: var(--text-secondary);
            margin-top: 0.25rem;
        }

        .severity-badge {
            padding: 0.35rem 1rem;
            border-radius: 99px;
            font-size: 0.8rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .severity-badge.critical { background: var(--grad-critical); color: #FFF; }
        .severity-badge.high { background: var(--grad-high); color: #000; }
        .severity-badge.medium { background: var(--grad-medium); color: #000; }
        .severity-badge.low { background: var(--grad-low); color: #FFF; }

        /* --- Metadata and Stack Info --- */
        .info-header {
            font-family: var(--font-outfit);
            font-size: 1.6rem;
            font-weight: 700;
            margin-bottom: 0.75rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .info-desc {
            color: var(--text-secondary);
            font-size: 1rem;
            margin-bottom: 2rem;
            max-width: 800px;
        }

        .info-metrics {
            display: grid;
            grid-template-columns: repeat(4, 1fr);
            gap: 1.5rem;
        }

        .metric-card {
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid rgba(255, 255, 255, 0.04);
            padding: 1.25rem;
            border-radius: 12px;
            text-align: left;
        }

        .metric-val {
            font-family: var(--font-outfit);
            font-size: 2rem;
            font-weight: 700;
            line-height: 1;
            margin-bottom: 0.5rem;
        }

        .metric-lbl {
            font-size: 0.8rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        /* --- Layout Grids --- */
        .section-title {
            font-family: var(--font-outfit);
            font-size: 1.8rem;
            font-weight: 700;
            margin-bottom: 1.5rem;
            margin-top: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .main-layout {
            display: grid;
            grid-template-columns: 1.8fr 1.2fr;
            gap: 2rem;
            margin-bottom: 3rem;
        }

        /* --- Path Cards --- */
        .path-list {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .path-card {
            border-left: 5px solid transparent;
            position: relative;
        }

        .path-card.critical { border-left-color: var(--color-critical); }
        .path-card.high { border-left-color: var(--color-high); }
        .path-card.medium { border-left-color: var(--color-medium); }
        .path-card.low { border-left-color: var(--color-low); }

        .path-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1.25rem;
        }

        .path-title {
            font-family: var(--font-outfit);
            font-size: 1.15rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }

        .path-score-badge {
            font-family: var(--font-mono);
            font-weight: 700;
            font-size: 1rem;
            padding: 0.25rem 0.75rem;
            border-radius: 6px;
            background: rgba(255, 255, 255, 0.05);
            border: 1px solid var(--border-color);
        }
        .path-card.critical .path-score-badge { color: var(--color-critical); background: rgba(255, 59, 48, 0.05); }
        .path-card.high .path-score-badge { color: var(--color-high); background: rgba(255, 149, 0, 0.05); }
        .path-card.medium .path-score-badge { color: var(--color-medium); background: rgba(255, 204, 0, 0.05); }
        .path-card.low .path-score-badge { color: var(--color-low); background: rgba(52, 199, 89, 0.05); }

        /* Attack Chain Visual representation */
        .attack-chain {
            background: rgba(0, 0, 0, 0.25);
            padding: 1.25rem;
            border-radius: 12px;
            display: flex;
            flex-wrap: wrap;
            align-items: center;
            gap: 0.75rem;
            margin-bottom: 1.25rem;
            border: 1px solid rgba(255, 255, 255, 0.02);
        }

        .chain-node {
            padding: 0.4rem 0.8rem;
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            font-size: 0.85rem;
            font-weight: 500;
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
        }

        .chain-node .node-type {
            font-size: 0.65rem;
            text-transform: uppercase;
            color: var(--text-muted);
            letter-spacing: 0.05em;
        }

        .chain-node.attacker-node {
            border-color: rgba(175, 82, 222, 0.4);
            background: rgba(175, 82, 222, 0.03);
        }

        .chain-node.target-node {
            border-color: rgba(255, 59, 48, 0.4);
            background: rgba(255, 59, 48, 0.03);
        }

        .chain-arrow {
            color: var(--text-muted);
            font-weight: bold;
            font-size: 1rem;
        }

        /* Chained Vulnerabilities */
        .vulnerabilities-chain {
            display: flex;
            flex-direction: column;
            gap: 0.75rem;
        }

        .vuln-item {
            background: rgba(255, 255, 255, 0.015);
            border: 1px solid rgba(255, 255, 255, 0.03);
            padding: 1rem;
            border-radius: 10px;
            display: flex;
            align-items: flex-start;
            gap: 0.75rem;
        }

        .vuln-item-icon {
            margin-top: 0.15rem;
            font-size: 1rem;
        }

        .vuln-item-details h5 {
            font-family: var(--font-outfit);
            font-size: 0.95rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 0.15rem;
        }

        .vuln-item-details p {
            font-size: 0.85rem;
            color: var(--text-secondary);
            line-height: 1.4;
        }

        .vuln-metrics {
            margin-top: 0.4rem;
            display: flex;
            gap: 1rem;
            font-size: 0.75rem;
            font-family: var(--font-mono);
            color: var(--text-muted);
        }

        .vuln-metrics span strong {
            color: var(--text-secondary);
        }

        /* --- Recommendation / ROI Cards --- */
        .recommendation-panel {
            display: flex;
            flex-direction: column;
            gap: 1.5rem;
        }

        .roi-card {
            border-left: 4px solid var(--color-low);
            position: relative;
            background: rgba(52, 199, 89, 0.02);
            transition: all 0.3s ease;
        }
        
        .roi-card:hover {
            background: rgba(52, 199, 89, 0.04);
            transform: translateY(-2px);
        }

        .roi-header {
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            margin-bottom: 0.75rem;
        }

        .roi-title {
            font-family: var(--font-outfit);
            font-size: 1.1rem;
            font-weight: 600;
        }

        .roi-badge {
            font-family: var(--font-mono);
            background: rgba(52, 199, 89, 0.12);
            color: #30D158;
            padding: 0.2rem 0.6rem;
            border-radius: 6px;
            font-weight: 700;
            font-size: 0.8rem;
            border: 1px solid rgba(52, 199, 89, 0.2);
        }

        .roi-component {
            font-size: 0.8rem;
            color: var(--text-muted);
            margin-bottom: 0.5rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }

        .roi-desc {
            font-size: 0.88rem;
            color: var(--text-secondary);
            margin-bottom: 1.25rem;
            line-height: 1.5;
        }

        .roi-comparison {
            display: flex;
            align-items: center;
            gap: 1.5rem;
            background: rgba(0, 0, 0, 0.2);
            padding: 0.75rem 1rem;
            border-radius: 8px;
            font-size: 0.8rem;
        }

        .roi-comp-metric {
            display: flex;
            flex-direction: column;
            gap: 0.15rem;
        }

        .roi-comp-metric span {
            color: var(--text-muted);
            font-size: 0.7rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .roi-comp-metric strong {
            font-family: var(--font-mono);
            font-size: 1rem;
        }

        .roi-comp-arrow {
            color: var(--text-muted);
            font-size: 1rem;
        }

        /* --- Component inventory --- */
        .inventory-section {
            margin-bottom: 3rem;
        }

        .inventory-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 1.5rem;
        }

        .inventory-card {
            background: var(--panel-bg);
            border: 1px solid var(--border-color);
            padding: 1.5rem;
            border-radius: 14px;
            position: relative;
        }

        .inventory-card-title {
            font-family: var(--font-outfit);
            font-size: 1.1rem;
            font-weight: 600;
            margin-bottom: 0.25rem;
            display: flex;
            align-items: center;
            justify-content: space-between;
        }

        .inventory-card-type {
            font-family: var(--font-mono);
            font-size: 0.75rem;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 1rem;
            background: rgba(255, 255, 255, 0.02);
            padding: 0.15rem 0.5rem;
            border-radius: 4px;
            display: inline-block;
            border: 1px solid rgba(255, 255, 255, 0.04);
        }

        .inventory-card-metric {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: var(--text-secondary);
            margin-bottom: 0.5rem;
        }

        .inventory-card-metric span strong {
            color: var(--text-primary);
        }

        .inventory-tags {
            margin-top: 1rem;
            display: flex;
            flex-wrap: wrap;
            gap: 0.4rem;
        }

        .inventory-tag {
            font-size: 0.7rem;
            padding: 0.2rem 0.5rem;
            border-radius: 4px;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--border-color);
            color: var(--text-secondary);
        }

        .inventory-tag.vuln {
            background: rgba(255, 59, 48, 0.05);
            border-color: rgba(255, 59, 48, 0.15);
            color: #FF453A;
        }

        .inventory-tag.mit {
            background: rgba(52, 199, 89, 0.05);
            border-color: rgba(52, 199, 89, 0.15);
            color: #30D158;
        }

        footer {
            text-align: center;
            color: var(--text-muted);
            font-size: 0.85rem;
            margin-top: 5rem;
            border-top: 1px solid var(--border-color);
            padding-top: 2rem;
        }

        footer a {
            color: var(--text-secondary);
            text-decoration: none;
        }

        footer a:hover {
            color: var(--text-primary);
        }

        @media (max-width: 1024px) {
            .summary-grid, .main-layout {
                grid-template-columns: 1fr;
            }
            .info-metrics {
                grid-template-columns: repeat(2, 1fr);
            }
        }

        @media (max-width: 640px) {
            .info-metrics {
                grid-template-columns: 1fr;
            }
            header {
                flex-direction: column;
                align-items: flex-start;
                gap: 1rem;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <!-- --- Header --- -->
        <header>
            <div class="logo-section">
                <h1>CAPS <span>//</span> Score Report</h1>
                <p>Compositional Attack Path Scoring for LLM Deployment Stacks</p>
            </div>
            <div class="meta-tag">
                Generated: {{ timestamp }}
            </div>
        </header>

        <!-- --- Summary Cards --- -->
        <div class="summary-grid">
            <!-- Score Meter Panel -->
            <div class="glass-panel score-box">
                {% set max_score = max_score | default(0.0) %}
                {% if max_score >= 70.0 %}
                    {% set score_class = 'critical' %}
                    {% set severity = 'Critical' %}
                {% elif max_score >= 40.0 %}
                    {% set score_class = 'high' %}
                    {% set severity = 'High' %}
                {% elif max_score >= 15.0 %}
                    {% set score_class = 'medium' %}
                    {% set severity = 'Medium' %}
                {% else %}
                    {% set score_class = 'low' %}
                    {% set severity = 'Low' %}
                {% endif %}
                
                <div class="score-circle {{ score_class }}">
                    <div class="score-num" style="color: {% if score_class == 'critical' %}var(--color-critical){% elif score_class == 'high' %}var(--color-high){% elif score_class == 'medium' %}var(--color-medium){% else %}var(--color-low){% endif %};">
                        {{ "%.1f"|format(max_score) }}
                    </div>
                    <div class="score-label">Max Risk</div>
                </div>
                <span class="severity-badge {{ score_class }}">{{ severity }} Risk</span>
            </div>

            <!-- Stack Information & Metrics Panel -->
            <div class="glass-panel">
                <div class="info-header">
                    {{ stack.name }}
                </div>
                <div class="info-desc">
                    {{ stack.description or "No description provided for this deployment configuration." }}
                </div>
                
                <div class="info-metrics">
                    <div class="metric-card">
                        <div class="metric-val" style="color: #AF52DE;">{{ stack.components | length }}</div>
                        <div class="metric-lbl">Components</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-val" style="color: #007AFF;">{{ stack.connections | length }}</div>
                        <div class="metric-lbl">Data Flows</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-val" style="color: #FF9500;">{{ total_vulns }}</div>
                        <div class="metric-lbl">Vulnerabilities</div>
                    </div>
                    <div class="metric-card">
                        <div class="metric-val" style="color: #34C759;">{{ total_mits }}</div>
                        <div class="metric-lbl">Active Mitigations</div>
                    </div>
                </div>
            </div>
        </div>

        <!-- --- Main Layout --- -->
        <div class="main-layout">
            <!-- Left Side: Scored Attack Paths -->
            <div>
                <h2 class="section-title">
                    <span style="color: var(--color-critical);">⚡</span> Scored Attack Paths ({{ paths | length }})
                </h2>
                
                <div class="path-list">
                    {% if not paths %}
                        <div class="glass-panel" style="text-align: center; color: var(--text-secondary); padding: 3rem;">
                            No attack paths identified in this topology. The system is structurally secure or has no entry points.
                        </div>
                    {% endif %}
                    
                    {% for path_info in paths %}
                        {% if path_info.score >= 70.0 %}
                            {% set path_class = 'critical' %}
                        {% elif path_info.score >= 40.0 %}
                            {% set path_class = 'high' %}
                        {% elif path_info.score >= 15.0 %}
                            {% set path_class = 'medium' %}
                        {% else %}
                            {% set path_class = 'low' %}
                        {% endif %}
                        
                        <div class="glass-panel path-card {{ path_class }}">
                            <div class="path-header">
                                <div class="path-title">
                                    Path {{ loop.index }}: {{ path_info.components[0].name }} ➜ {{ path_info.components[-1].name }}
                                </div>
                                <div class="path-score-badge">
                                    Score: {{ "%.1f"|format(path_info.score) }}
                                </div>
                            </div>
                            
                            <!-- Attack Chain Visual -->
                            <div class="attack-chain">
                                {% for comp in path_info.components %}
                                    <div class="chain-node {% if comp.type == 'attacker' %}attacker-node{% elif loop.last %}target-node{% endif %}">
                                        <span class="node-type">{{ comp.type }}</span>
                                        <strong>{{ comp.name }}</strong>
                                    </div>
                                    {% if not loop.last %}
                                        <div class="chain-arrow">➜</div>
                                    {% endif %}
                                {% endfor %}
                            </div>
                            
                            <!-- Chained Vulnerabilities details -->
                            <div class="vulnerabilities-chain">
                                <h4 style="font-size: 0.85rem; text-transform: uppercase; color: var(--text-muted); letter-spacing: 0.05em; margin-bottom: 0.25rem;">Composition Details</h4>
                                {% for vuln in path_info.vulnerabilities %}
                                    {% if vuln %}
                                        <div class="vuln-item">
                                            <div class="vuln-item-icon">⚠️</div>
                                            <div class="vuln-item-details">
                                                <h5>{{ vuln.name }} ({{ path_info.components[loop.index0].name }})</h5>
                                                <p>{{ vuln.description }}</p>
                                                <div class="vuln-metrics">
                                                    <span>Base Exploitability: <strong>{{ vuln.exploitability }}</strong></span>
                                                    <span>Effective Exploitability: <strong>{{ "%.2f"|format(path_info.components[loop.index0].get_effective_exploitability(vuln.id)) }}</strong></span>
                                                    <span>Impact: <strong>{{ vuln.impact }}</strong></span>
                                                </div>
                                            </div>
                                        </div>
                                    {% else %}
                                        <div class="vuln-item">
                                            <div class="vuln-item-icon">ℹ️</div>
                                            <div class="vuln-item-details">
                                                <h5>Baseline Node Surface ({{ path_info.components[loop.index0].name }})</h5>
                                                <p>No declared vulnerability. Scoring models use a minimum baseline vulnerability exploitability (0.1) for complete attack path routing analysis.</p>
                                            </div>
                                        </div>
                                    {% endif %}
                                {% endfor %}
                            </div>
                        </div>
                    {% endfor %}
                </div>
            </div>

            <!-- Right Side: Mitigation ROI Recommendations -->
            <div>
                <h2 class="section-title">
                    <span style="color: var(--color-low);">🛡️</span> Recommended Mitigations (ROI)
                </h2>
                
                <div class="recommendation-panel">
                    {% if not recommendations %}
                        <div class="glass-panel" style="text-align: center; color: var(--text-secondary); padding: 3rem;">
                            No mitigation recommendations. The stack has a low baseline score.
                        </div>
                    {% endif %}
                    
                    {% for rec in recommendations %}
                        <div class="glass-panel roi-card">
                            <div class="roi-header">
                                <div class="roi-title">{{ rec.mitigation_name }}</div>
                                <div class="roi-badge">-{{ rec.percentage_reduction }}% Risk</div>
                            </div>
                            <div class="roi-component">Component: {{ rec.component_name }} ({{ rec.component_id }})</div>
                            <p class="roi-desc">{{ rec.description }}</p>
                            
                            <div class="roi-comparison">
                                <div class="roi-comp-metric">
                                    <span>Current Score</span>
                                    <strong style="color: var(--color-critical);">{{ "%.1f"|format(rec.score_before) }}</strong>
                                </div>
                                <div class="roi-comp-arrow">➜</div>
                                <div class="roi-comp-metric">
                                    <span>Mitigated Score</span>
                                    <strong style="color: {% if rec.score_after >= 40.0 %}var(--color-high){% else %}var(--color-low){% endif %};">{{ "%.1f"|format(rec.score_after) }}</strong>
                                </div>
                                <div class="roi-comp-arrow">|</div>
                                <div class="roi-comp-metric">
                                    <span>Reduction</span>
                                    <strong style="color: var(--color-low);">-{{ "%.1f"|format(rec.score_reduction) }}</strong>
                                </div>
                            </div>
                        </div>
                    {% endfor %}
                </div>
            </div>
        </div>

        <!-- --- Component Inventory Section --- -->
        <div class="inventory-section">
            <h2 class="section-title">
                <span style="color: #AF52DE;">📦</span> Stack Architecture Inventory
            </h2>
            
            <div class="inventory-grid">
                {% for comp in stack.components %}
                    <div class="inventory-card">
                        <div class="inventory-card-title">
                            {{ comp.name }}
                        </div>
                        <span class="inventory-card-type">{{ comp.type }} (ID: {{ comp.id }})</span>
                        
                        <div class="inventory-card-metric">
                            <span>Asset Value (Impact Rating):</span>
                            <span><strong>{{ comp.asset_value }}/10.0</strong></span>
                        </div>
                        
                        <div class="inventory-card-metric">
                            <span>Vulnerabilities:</span>
                            <span><strong>{{ comp.vulnerabilities | length }}</strong></span>
                        </div>
                        
                        <div class="inventory-card-metric">
                            <span>Active Mitigations:</span>
                            <span><strong>{{ comp.mitigations | length }}</strong></span>
                        </div>
                        
                        <div class="inventory-tags">
                            {% for vuln in comp.vulnerabilities %}
                                <span class="inventory-tag vuln">⚠️ {{ vuln.id }}</span>
                            {% endfor %}
                            {% for mit in comp.mitigations %}
                                <span class="inventory-tag mit">🛡️ {{ mit.id }}</span>
                            {% endfor %}
                        </div>
                    </div>
                {% endfor %}
            </div>
        </div>

        <!-- --- Footer --- -->
        <footer>
            <p>CAPS: Compositional Attack Path Scoring Model &copy; 2026. Made with advanced threat intelligence modeling.</p>
        </footer>
    </div>
</body>
</html>
"""


def generate_html_report(stack: DeploymentStack, paths: List[Dict[str, Any]], recommendations: List[Dict[str, Any]]) -> str:
    """Generate high-fidelity HTML report for the deployment stack analysis."""
    # Compute aggregate metadata
    total_vulns = sum(len(comp.vulnerabilities) for comp in stack.components)
    total_mits = sum(len(comp.mitigations) for comp in stack.components)
    max_score = paths[0]["score"] if paths else 0.0

    template = Template(HTML_TEMPLATE)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    return template.render(
        stack=stack,
        paths=paths,
        recommendations=recommendations,
        total_vulns=total_vulns,
        total_mits=total_mits,
        max_score=max_score,
        timestamp=timestamp
    )
