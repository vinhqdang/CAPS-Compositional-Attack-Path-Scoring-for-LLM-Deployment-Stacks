import matplotlib.pyplot as plt
import numpy as np
import os

# Figures belong to paper 1; resolve the path relative to the repository root so
# this script can be run from any working directory.
REPO_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
FIGURES_DIR = os.path.join(REPO_ROOT, "papers", "paper1-caps-jdsis", "figures")
os.makedirs(FIGURES_DIR, exist_ok=True)

# 1. Baseline Comparison Bar Chart
labels = ['RAG Chatbot', 'Autonomous Agent', 'Model Router']
b1_scores = [71.2, 85.0, 85.0]
b3_scores = [42.4, 58.1, 56.0]
caps_scores = [34.3, 51.3, 47.6]

x = np.arange(len(labels))
width = 0.25

fig, ax = plt.subplots(figsize=(8, 5))
rects1 = ax.bar(x - width, b1_scores, width, label='B1 (OWASP/CVSS)', color='#ff6b6b')
rects2 = ax.bar(x, b3_scores, width, label='B3 (ADTree No Decay)', color='#feca57')
rects3 = ax.bar(x + width, caps_scores, width, label='CAPS (Proposed)', color='#48dbfb')

ax.set_ylabel('Critical Path Risk Score (0-100)')
ax.set_title('Risk Score Comparison Across Evaluation Topologies')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()
ax.grid(axis='y', linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "baseline_comparison.pdf"))
plt.close()

# 2. Decay Effect Line Chart
hops = np.arange(1, 6)
alphas = [1.0, 0.95, 0.85, 0.70]
base_prob = 0.8  # Assume each node has 0.8 exploitability

fig, ax = plt.subplots(figsize=(8, 5))

for alpha in alphas:
    # P = alpha^(k-1) * prod(E)
    probs = [ (alpha**(k-1)) * (base_prob**k) for k in hops ]
    ax.plot(hops, probs, marker='o', label=f'$\\alpha$ = {alpha}')

ax.set_xlabel('Number of Path Hops ($k$)')
ax.set_ylabel('Cumulative Path Exploitability ($P_{exploit}$)')
ax.set_title('Effect of Chaining Decay Factor over Multi-Hop Attacks')
ax.set_xticks(hops)
ax.legend()
ax.grid(linestyle='--', alpha=0.7)

plt.tight_layout()
plt.savefig(os.path.join(FIGURES_DIR, "decay_effect.pdf"))
plt.close()
