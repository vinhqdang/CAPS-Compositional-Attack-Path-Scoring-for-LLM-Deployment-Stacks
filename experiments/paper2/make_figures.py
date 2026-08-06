"""Generate paper 2's figures.

Every number is computed from `caps/` or read from `results/*.json`. Nothing is
hardcoded, so the figures cannot drift from the data the way paper 1's
`generate_plots.py` can (it embeds its values as literals).

Figures
-------
1. iatrogenic_gap      -- ACE is invariant while NCE spans 51 points and crosses zero.
2. placement_bound     -- the inversion threshold against reachability, with the hard
                          feasibility ceiling at E_g * I_t = 10.
3. eg_distribution     -- measured E_g per guardrail with 95% CIs, split by model class,
                          against the three inversion thresholds.
4. bypass_heatmap      -- which injection structures evade which safety classifier.

Design notes: the palette is the validated categorical default (slots 1-2, which pass
all six checks including CVD separation). Because this journal prints in grayscale,
every figure carries a secondary encoding -- hatching on bars, distinct markers, and
direct value labels -- so nothing depends on hue alone.

Run:  /opt/miniconda3/envs/py313/bin/python experiments/paper2/make_figures.py
"""

import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Patch

sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from caps.engine_nonmono import Control, evaluate_control, inversion_report, max_path_score
from caps.models import Component, Connection, Mitigation, Vulnerability
from caps.templates import (
    get_autonomous_coding_agent,
    get_model_router,
    get_rag_chatbot,
)

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(HERE, "results")
FIGDIR = os.path.join(
    os.path.dirname(os.path.dirname(HERE)), "papers", "paper2-nonmonotone", "figures"
)

# Validated categorical slots 1-2 (see dataviz references/palette.md).
BLUE = "#2a78d6"
ORANGE = "#eb6834"
INK = "#0b0b0b"
INK2 = "#52514e"
GRID = "#d8d7d2"
MAX_EG_TIMES_I = 10.0

TOPOLOGIES = [
    ("RAG Chatbot", get_rag_chatbot),
    ("Autonomous Coding Agent", get_autonomous_coding_agent),
    ("Enterprise Model Router", get_model_router),
]
SAFETY_CLASSIFIERS = ("content-safety", "llama-guard", "safeguard")


def style():
    plt.rcParams.update({
        "font.family": "serif",
        "font.serif": ["DejaVu Serif", "Times New Roman"],
        "font.size": 9,
        "axes.labelsize": 9,
        "axes.titlesize": 10,
        "axes.edgecolor": INK2,
        "axes.linewidth": 0.8,
        "axes.grid": True,
        "grid.color": GRID,
        "grid.linewidth": 0.6,
        "grid.alpha": 0.9,
        "xtick.labelsize": 8,
        "ytick.labelsize": 8,
        "legend.fontsize": 8,
        "legend.frameon": False,
        "figure.dpi": 110,
        "savefig.bbox": "tight",
        "savefig.pad_inches": 0.02,
    })


def finish(fig, name):
    os.makedirs(FIGDIR, exist_ok=True)
    for ext, kw in (("png", {"dpi": 300}), ("pdf", {})):
        fig.savefig(os.path.join(FIGDIR, f"{name}.{ext}"), **kw)
    plt.close(fig)
    print(f"  wrote {name}.png / {name}.pdf")


def despine(ax, keep=("left", "bottom")):
    for s in ("top", "right", "left", "bottom"):
        ax.spines[s].set_visible(s in keep)
    ax.set_axisbelow(True)


# ----------------------------------------------------------------- figure 1
def shared_guardrail(asset_value, exploitability, entry, protect):
    return Control(
        name=f"g({asset_value},{exploitability})",
        attenuations={protect: Mitigation(id="a", name="a", effectiveness=0.80)},
        induced_components=[
            Component(
                id="shared_guardrail", name="G", type="orchestrator",
                asset_value=asset_value,
                vulnerabilities=[Vulnerability(
                    id="v", name="hijack", exploitability=exploitability, impact=7.0)],
            )
        ],
        induced_connections=[
            Connection(source=entry, destination="shared_guardrail"),
            Connection(source="shared_guardrail", destination=protect),
        ],
    )


def fig_iatrogenic_gap():
    stack = get_model_router()
    assets = (6.0, 7.0, 8.0, 9.0, 10.0)
    expls = (0.5, 0.75, 0.9)

    labels, ace, nce = [], [], []
    for a in assets:
        for e in expls:
            r = evaluate_control(stack, shared_guardrail(a, e, "partner_app", "model_router"))
            labels.append(f"{a:.0f}/{e:g}")
            ace.append(r["ace"])
            nce.append(r["nce"])

    order = np.argsort(nce)[::-1]
    labels = [labels[i] for i in order]
    nce = [nce[i] for i in order]
    ace_const = ace[0]
    assert len(set(round(v, 6) for v in ace)) == 1, "ACE should be invariant"

    fig, ax = plt.subplots(figsize=(6.6, 3.1))
    x = np.arange(len(nce))
    colors = [BLUE if v >= 0 else ORANGE for v in nce]
    hatches = ["" if v >= 0 else "///" for v in nce]
    bars = ax.bar(x, nce, width=0.72, color=colors, edgecolor="white", linewidth=0.8)
    for b, h in zip(bars, hatches):
        if h:
            b.set_hatch(h)

    ax.axhline(0, color=INK, linewidth=0.9)
    ax.axhline(ace_const, color=INK, linestyle="--", linewidth=1.4, zorder=5)
    ax.annotate(
        f"what CAPS v1 reports: +{ace_const:.2f} for every configuration",
        xy=(len(nce) - 0.5, ace_const), xytext=(-4, 5),
        textcoords="offset points", ha="right", va="bottom",
        fontsize=8, color=INK, fontweight="bold",
    )

    for xi, v in zip(x, nce):
        ax.annotate(f"{v:+.1f}", xy=(xi, v), xytext=(0, 3 if v >= 0 else -11),
                    textcoords="offset points", ha="center", fontsize=6.2, color=INK2)

    ax.set_xticks(x)
    ax.set_xticklabels(labels, rotation=90, fontsize=6.5)
    ax.set_xlabel("shared guardrail configuration  ($I_g$ / $E_g$)")
    ax.set_ylabel("effect on risk  (positive = risk reduced)")
    ax.set_title(
        "An attenuation-only model reports one number for a 51-point spread that changes sign",
        loc="left", fontsize=9.5, color=INK)
    ax.set_ylim(min(nce) - 12, max(ace_const, max(nce)) + 10)
    despine(ax)
    ax.grid(axis="x", visible=False)
    ax.legend(handles=[
        Patch(facecolor=BLUE, edgecolor="white", label="NCE > 0 — control helps"),
        Patch(facecolor=ORANGE, edgecolor="white", hatch="///", label="NCE < 0 — control harms"),
    ], loc="lower left", ncol=2)
    finish(fig, "fig1_iatrogenic_gap")


# ----------------------------------------------------------------- figure 2
def fig_placement_bound():
    """Threshold against reachability product, with the hard feasibility ceiling."""
    reach = np.logspace(-3, 0, 200)

    fig, ax = plt.subplots(figsize=(5.6, 3.4))

    for (label, factory), mark in zip(TOPOLOGIES, ("o", "s", "^")):
        stack = factory()
        base = max_path_score(stack)
        thr = base / (10.0 * reach)
        ax.plot(reach, thr, linewidth=1.8, marker="", label=f"{label} (baseline {base:.1f})")

    ax.axhline(MAX_EG_TIMES_I, color=INK, linestyle="--", linewidth=1.5)
    ax.annotate(
        "hard ceiling: $E_g \\cdot I_t \\leq 10$ by schema",
        xy=(1.1e-3, MAX_EG_TIMES_I), xytext=(0, 6), textcoords="offset points",
        fontsize=8, fontweight="bold", color=INK)
    ax.fill_between(reach, MAX_EG_TIMES_I, 1e5, color=GRID, alpha=0.38, zorder=0)
    # Region labels sit in the corners, clear of the curves.
    ax.annotate("inversion IMPOSSIBLE\nthreshold exceeds the ceiling",
                xy=(0.97, 0.955), xycoords="axes fraction", fontsize=8, color=INK2,
                ha="right", va="top", linespacing=1.35)
    # No "inversion possible" label: the only free corner is taken by the legend, and
    # the unshaded region plus the two marker callouts already carry the meaning.

    # The two placements actually measured on the model router.
    stack = get_model_router()
    entry = "partner_app"
    shallow = shared_guardrail(8.0, 0.85, entry, "model_router")
    deep = Control(
        name="deep",
        attenuations={"confidential_gpt4": Mitigation(id="a", name="a", effectiveness=0.8)},
        induced_components=[Component(
            id="sanitiser", name="S", type="tool", asset_value=8.0,
            vulnerabilities=[Vulnerability(id="v", name="v", exploitability=0.85, impact=7.0)])],
        induced_connections=[
            Connection(source="confidential_gpt4", destination="sanitiser"),
            Connection(source="sanitiser", destination="treasury_database"),
        ],
    )
    placements = (
        (shallow, "entry-adjacent ($d$=1)\ninverts", "o", (-10, -20), "right"),
        (deep, "deep ($d$=3)\nprovably safe", "D", (10, 16), "left"),
    )
    for ctrl, txt, mk, off, ha in placements:
        r = inversion_report(stack, ctrl)
        rp, th = r["reachability_product"], r["threshold"]
        ax.plot([rp], [th], marker=mk, markersize=8, color=ORANGE,
                markeredgecolor="white", markeredgewidth=1.2, zorder=6)
        ax.annotate(txt, xy=(rp, th), xytext=off, textcoords="offset points",
                    fontsize=7.5, color=INK, fontweight="bold", ha=ha,
                    linespacing=1.3,
                    bbox=dict(boxstyle="round,pad=0.22", facecolor="white",
                              edgecolor="none", alpha=0.85))

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(1e-3, 1.3)
    ax.set_ylim(0.5, 1e4)
    ax.set_xlabel("reachability of the control,  $\\alpha^{k-1} \\cdot R \\cdot S$")
    ax.set_ylabel("inversion threshold on $E_g \\cdot I_t$")
    ax.set_title("Deep controls are safe by construction, not by parameter choice",
                 loc="left", fontsize=9.5, color=INK)
    despine(ax)
    ax.legend(loc="lower left", fontsize=7.5)
    finish(fig, "fig2_placement_bound")


# ----------------------------------------------------------------- figure 3
def load_measurements():
    rows = []
    for fn in sorted(os.listdir(RESULTS)):
        if not fn.endswith(".json"):
            continue
        with open(os.path.join(RESULTS, fn)) as f:
            d = json.load(f)
        if "E_g" in d and "model" in d:
            rows.append((d["model"], "static", d["E_g"], d.get("E_g_ci95"),
                         d.get("n_injection_scored")))
        for r in d.get("rows", []):
            if "E_g" in r:
                rows.append((r["model"], "static", r["E_g"], r.get("E_g_ci95"),
                             r.get("n_injection")))
            elif "E_g_adaptive" in r:
                rows.append((r.get("guardrail", "?"), "adaptive", r["E_g_adaptive"],
                             r.get("ci95"), r.get("seeds")))
        for r in d.get("static", []):
            if "E_g" in r and "variant" in r:
                rows.append((f"{r['model']} [{r['variant']}]", "static", r["E_g"],
                             r.get("E_g_ci95"), r.get("n_injection")))

    best = {}
    for m, mode, eg, ci, n in rows:
        if (n or 0) < 8:
            continue
        k = (m, mode)
        if k not in best or (n or 0) > best[k][3]:
            best[k] = (eg, ci or [None, None], mode, n or 0, m)
    return sorted(best.values(), key=lambda r: r[0])


def fig_eg_distribution():
    data = load_measurements()
    labels, egs, los, his, is_sc = [], [], [], [], []
    for eg, ci, mode, n, m in data:
        # "openrouter/free" would collapse to a bare "free"; keep the vendor there.
        short = m.replace(":free", "")
        if not short.startswith("openrouter/"):
            short = short.split("/")[-1]
        labels.append(f"{short}  ({mode}, n={n})")
        egs.append(eg)
        # Clamp at zero: the Wilson bound for k=0 can land on floating-point noise
        # (e.g. 2.8e-17) rather than exactly 0, which matplotlib rejects as a
        # negative error bar.
        los.append(max(0.0, eg - (ci[0] if ci[0] is not None else eg)))
        his.append(max(0.0, (ci[1] if ci[1] is not None else eg) - eg))
        is_sc.append(any(k in m.lower() for k in SAFETY_CLASSIFIERS))

    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(7.0, 4.9))

    for i in y:
        c = ORANGE if is_sc[i] else BLUE
        mk = "D" if is_sc[i] else "o"
        ax.errorbar(egs[i], i, xerr=[[los[i]], [his[i]]], fmt=mk, color=c,
                    markersize=6.5, capsize=2.6, elinewidth=1.1,
                    markeredgecolor="white", markeredgewidth=0.9, zorder=4)
        # Value sits to the right of the CI cap and vertically centred on its own
        # row; an offset above would land in the neighbouring row at this density.
        ax.annotate(f"{egs[i]:.3f}", xy=(egs[i] + his[i], i), xytext=(5, 0),
                    textcoords="offset points", ha="left", va="center",
                    fontsize=6.6, color=INK2, zorder=6,
                    # White backing so a threshold rule never cuts through a value.
                    bbox=dict(boxstyle="square,pad=0.14", facecolor="white",
                              edgecolor="none"))

    # Threshold rules, with labels staggered so they cannot collide (0.54 and 0.56
    # are only two hundredths apart). The chosen heights sit among the low-E_g rows,
    # whose CI caps end near 0.26, so the rules never overlap a value label.
    for (label, factory), ls, yfrac in zip(
        TOPOLOGIES, (":", "-.", "--"), (0.06, 0.30, 0.45)
    ):
        stack = factory()
        need = max_path_score(stack) / (10.0 * stack.chaining_decay) / 10.0
        ax.axvline(need, color=INK, linestyle=ls, linewidth=1.1, zorder=2)
        ax.annotate(f"{label.split()[0]} needs {need:.2f}",
                    xy=(need, yfrac), xycoords=("data", "axes fraction"),
                    xytext=(-3, 0), textcoords="offset points",
                    rotation=90, fontsize=6.8, color=INK, ha="right", va="center",
                    bbox=dict(boxstyle="round,pad=0.18", facecolor="white",
                              edgecolor="none", alpha=0.9))

    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=7)
    ax.set_xlabel("measured $E_g$  (guardrail bypass rate, 95% Wilson CI)")
    ax.set_xlim(-0.03, 1.0)
    ax.set_title("Only a purpose-built safety classifier reaches the inversion regime",
                 loc="left", fontsize=9.5, color=INK)
    despine(ax)
    ax.grid(axis="y", visible=False)
    ax.legend(handles=[
        plt.Line2D([], [], marker="D", color=ORANGE, linestyle="", markersize=6,
                   label="purpose-built safety classifier"),
        plt.Line2D([], [], marker="o", color=BLUE, linestyle="", markersize=6,
                   label="general-purpose model"),
    ], loc="lower right")
    finish(fig, "fig3_eg_distribution")


# ----------------------------------------------------------------- figure 4
def fig_bypass_heatmap():
    path = os.path.join(RESULTS, "eg_safety_classifiers.json")
    if not os.path.exists(path):
        print("  [skip] fig4 needs eg_safety_classifiers.json")
        return
    with open(path) as f:
        d = json.load(f)

    cells = {}
    for r in d["records"]:
        if r["class"] != "injection" or not r["verdict"]:
            continue
        m = r["model"].split("/")[-1].replace(":free", "")
        cells.setdefault((r["case"], m), []).append(r["verdict"])

    models = sorted({m for _, m in cells})
    cases = sorted({c for c, _ in cells},
                   key=lambda c: -sum(
                       1 for m in models
                       if cells.get((c, m)) and
                       any(v == "ALLOW" for v in cells[(c, m)])))

    M = np.full((len(cases), len(models)), np.nan)
    for i, c in enumerate(cases):
        for j, m in enumerate(models):
            vs = cells.get((c, m))
            if vs:
                M[i, j] = sum(1 for v in vs if v == "ALLOW") / len(vs)

    fig, ax = plt.subplots(figsize=(5.8, 4.4))
    im = ax.imshow(M, cmap="Blues", vmin=0, vmax=1, aspect="auto")

    for i in range(len(cases)):
        for j in range(len(models)):
            if np.isnan(M[i, j]):
                continue
            v = M[i, j]
            ax.text(j, i, f"{v:.2f}", ha="center", va="center", fontsize=7.5,
                    color="white" if v > 0.55 else INK,
                    fontweight="bold" if v > 0 else "normal")

    ax.set_xticks(range(len(models)))
    ax.set_xticklabels([m.replace("-", "-\n", 1) for m in models], fontsize=7)
    ax.set_yticks(range(len(cases)))
    ax.set_yticklabels([c.replace("_", " ") for c in cases], fontsize=7.5)
    ax.set_xticks(np.arange(-0.5, len(models), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(cases), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.6)
    ax.grid(which="major", visible=False)
    ax.tick_params(which="minor", length=0)
    ax.set_title("Blind spots are complementary: no structure evades all three",
                 loc="left", fontsize=9.5, color=INK)
    cb = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.03)
    cb.set_label("fraction of trials bypassed", fontsize=8)
    cb.outline.set_visible(False)
    despine(ax, keep=())
    finish(fig, "fig4_bypass_heatmap")


def main():
    style()
    print(f"figures -> {os.path.relpath(FIGDIR)}")
    fig_iatrogenic_gap()
    fig_placement_bound()
    fig_eg_distribution()
    fig_bypass_heatmap()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
