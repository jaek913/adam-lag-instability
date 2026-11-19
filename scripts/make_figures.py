"""Build the manuscript figures (OUTLINE v0.8 §5 and §9) from committed outputs only; no new analysis.
FIG-1 schematic; FIG-2 one A1 event; FIG-3 FA-grid frontier (also IMG-01, stand-alone); FIG-4 headline detection
outcomes; FIG-5 E5; FIG-8 X1 event-locked curve (EXPLORATORY). Writes paper/figures/*.png and
paper/figures/MANIFEST.json (SHA-256 of each image and of every input it read).
FIG-2 reads the hashed A1 store (PRV check first) and recomputes each detector's headline alarm state with the E2
operators at the thetas recorded in e2_result.json; it HALTS unless the recomputed onsets equal the recorded ones.
FIG-2 event (display rule, DECISIONS 68): eligible events sorted by (D_div headline lead, t_e); index (n-1)//2.
Palette: reference categorical slots 1-5 (validated, dataviz skill), D_div slot 1. Static images: identity is carried
by direct labels and a legend, never colour alone.
Usage: python scripts/make_figures.py <store_root>"""
import glob
import hashlib
import json
import math
import os
import subprocess
import sys

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyBboxPatch  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, "analysis"), os.path.join(ROOT, "scripts")]
import a1_loader  # noqa: E402
import ops  # noqa: E402

OUT = os.path.join(ROOT, "paper", "figures")
DET = ["D_div", "B1", "B2", "B3", "B4"]
COL = {"D_div": "#2a78d6", "B1": "#eb6834", "B2": "#1baf7a", "B3": "#eda100", "B4": "#e87ba4"}
MARK = {"D_div": "o", "B1": "s", "B2": "^", "B3": "D", "B4": "v"}
INK, INK2, MUTED, GRID, AXIS, SURF = "#0b0b0b", "#52514e", "#898781", "#e1e0d9", "#c3c2b7", "#fcfcfb"
E2 = "scripts/outputs/e2/e2_result.json"
XD = "analysis/outputs/post/x_diag.json"
E5 = "analysis/outputs/post/e5_result.json"
READ = set()

plt.rcParams.update({"font.size": 9, "axes.edgecolor": AXIS, "axes.labelcolor": INK2, "xtick.color": INK2,
                     "ytick.color": INK2, "axes.titlesize": 10, "axes.titlecolor": INK, "figure.facecolor": SURF,
                     "axes.facecolor": SURF, "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.6,
                     "axes.spines.top": False, "axes.spines.right": False, "legend.frameon": False,
                     "savefig.dpi": 200, "lines.linewidth": 2})


def load(rel):
    READ.add(rel)
    return json.load(open(os.path.join(ROOT, rel), encoding="utf-8"))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def save(fig, name):
    p = os.path.join(OUT, name)
    fig.savefig(p, facecolor=SURF, bbox_inches="tight", metadata={"Software": None})
    plt.close(fig)
    return p


def fig1():
    fig, ax = plt.subplots(figsize=(6.8, 2.6))
    ax.axis("off")
    W, Y0, H = 0.22, 0.48, 0.26
    boxes = [(0.00, "parameters θ"), (0.26, "gradient $g_t$"),
             (0.52, "second moment\n$v_t=\\beta_2 v_{t-1}+(1-\\beta_2)g_t^2$"), (0.78, "step $\\eta/\\sqrt{v_t}$")]
    for x, t in boxes:
        ax.add_patch(FancyBboxPatch((x, Y0), W, H, boxstyle="round,pad=0.01", fc="white", ec=AXIS, lw=1))
        ax.text(x + W / 2, Y0 + H / 2, t, ha="center", va="center", color=INK, fontsize=7.5)
    for a, b in [(0.22, 0.26), (0.48, 0.52), (0.74, 0.78)]:
        ax.annotate("", (b, Y0 + H / 2), (a, Y0 + H / 2), arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2))
    ax.annotate("", (W / 2, Y0 - 0.02), (0.78 + W / 2, Y0 - 0.02),
                arrowprops=dict(arrowstyle="->", color=INK2, lw=1.2, connectionstyle="arc3,rad=-0.22"))
    ax.text(0.5, 0.02, "feedback: each update changes the gradients that the average is measuring", ha="center",
            color=INK2, fontsize=8)
    ax.text(0.37, 0.90, "logged scalar: $y=\\ln g$  →  $D=\\mathrm{SMA}_{32}(y)-\\mathrm{SMA}_{128}(y)$  →  "
            "expanding-percentile score (D_div)", ha="center", color=COL["D_div"], fontsize=8)
    ax.annotate("", (0.37, 0.84), (0.37, Y0 + H + 0.02), arrowprops=dict(arrowstyle="->", color=COL["D_div"], lw=1))
    ax.set_xlim(-0.01, 1.01)
    ax.set_ylim(0, 1)
    return save(fig, "fig1_loop.png")


def fig3(standalone=False):
    e2 = load(E2)
    pts = {"0.5": e2["fa_grid"]["0.5"], "1.0": e2["headline"], "2.0": e2["fa_grid"]["2.0"], "5.0": e2["fa_grid"]["5.0"]}
    fas = [0.5, 1.0, 2.0, 5.0]
    fig, axs = plt.subplots(1, 2, figsize=(6.8, 2.8) if not standalone else (8, 3.6))
    for d in DET[1:] + DET[:1]:                         # D_div drawn last, on top
        ml = [pts[str(f) if str(f) in pts else f"{f}"]["per_detector"][d]["mean_lead"] for f in fas]
        dr = [pts[str(f)]["per_detector"][d]["detection_rate"] for f in fas]
        mt = [pts[str(f)]["detectors"][d]["matchable"] for f in fas]
        for ax, v in ((axs[0], ml), (axs[1], dr)):
            ax.plot(fas, v, color=COL[d], lw=2, zorder=2.5 if d == "D_div" else 2)
            for f, val, ok in zip(fas, v, mt):
                ax.plot([f], [val], marker=MARK[d], ms=7 if d != "D_div" else 9, mfc=COL[d] if ok else SURF,
                        mec=COL[d], mew=1.8, ls="none", zorder=4 if d == "D_div" else 3)
        nudge = {"B1": -6, "B2": 6}.get(d, 0)
        axs[0].annotate(d, (fas[-1], ml[-1]), xytext=(7, nudge), textcoords="offset points", color=INK2, fontsize=8,
                        va="center")
    axs[0].set_ylabel("mean lead (steps)")
    axs[1].set_ylabel("detection rate")
    for ax in axs:
        ax.set_xscale("log")
        ax.set_xticks(fas)
        ax.set_xticklabels(["0.5", "1 (headline)", "2", "5"])
        ax.axvline(1.0, color=AXIS, lw=1, ls=":")
    hs = [plt.Line2D([], [], color=COL[d], marker=MARK[d], ms=6, label=d) for d in DET]
    hs.append(plt.Line2D([], [], color=MUTED, marker="o", mfc=SURF, ms=6, ls="none", label="hollow: not matchable"))
    fig.supxlabel("false-alarm rate (onsets per 10,000 out-of-window observations)", fontsize=8.5, color=INK2, y=0.06)
    fig.legend(handles=hs, loc="lower center", ncol=6, bbox_to_anchor=(0.5, -0.06), fontsize=8)
    if standalone:
        fig.suptitle("Pre-registered test on OLMo-0424: at no tested false-alarm rate does the smoothed divergence "
                     "(D_div) lead the best one-step alarm", fontsize=9, color=INK)
    fig.tight_layout()
    return save(fig, "img01_e2_frontier.png" if standalone else "fig3_frontier.png")


def fig4():
    e2 = load(E2)["headline"]
    fig, ax = plt.subplots(figsize=(6.0, 2.5))
    n = len(e2["leads"]["D_div"])
    cats = [("detected (lead > 0)", "detection_rate", 0), ("concurrent (lead 0)", "concurrent", 1), ("missed", "misses", 2)]
    w = 0.26
    for i, d in enumerate(DET):
        pdm = e2["per_detector"][d]
        vals = [round(pdm["detection_rate"] * n), pdm["concurrent"], pdm["misses"]]
        left = 0
        for (lab, _, k), v in zip(cats, vals):
            shade = {0: COL[d], 1: COL[d], 2: GRID}[k]
            ax.barh(i, v, left=left, color=shade, alpha={0: 1, 1: 0.55, 2: 1}[k], edgecolor=SURF, linewidth=2,
                    height=0.62)
            if v:
                ax.text(left + v / 2, i, str(v), ha="center", va="center", fontsize=8,
                        color=INK if k == 2 else "white")
            left += v
    ax.set_yticks(range(len(DET)))
    ax.set_yticklabels(DET)
    ax.invert_yaxis()
    ax.set_xlabel(f"eligible events (of {n}); every headline lead is 0 steps")
    ax.grid(axis="y", visible=False)
    ax.set_xlim(0, n)
    ax.set_title("Coloured: concurrent (alarm at the event's grid step, lead 0). Grey: missed. "
                 "No detector detected any event early.", fontsize=8, color=INK2)
    return save(fig, "fig4_outcomes.png")


def fig5():
    e5 = load(E5)["primary"]
    fig, ax = plt.subplots(figsize=(4.5, 2.2))
    lo, hi = e5["shift_rate_p05_p95"]
    ax.errorbar([1], [e5["shift_rate_median"]], yerr=[[e5["shift_rate_median"] - lo], [hi - e5["shift_rate_median"]]],
                fmt="s", color=MUTED, ms=8, capsize=4, label="circularly shifted (median, 5–95 %)")
    ax.plot([0], [e5["real_rate"]], marker="o", ms=9, color=COL["D_div"], ls="none", label="real alarm series")
    ax.set_xticks([0, 1])
    ax.set_xticklabels(["real", "shifted"])
    ax.set_xlim(-0.6, 1.6)
    ax.set_ylim(-0.05, 1)
    ax.set_ylabel("advance-ordering rate")
    ax.set_title(f"D_div has {e5['n_alarm_steps']} alarm steps at headline FA: degenerate", fontsize=9)
    ax.legend(loc="upper right", fontsize=7)
    return save(fig, "fig5_e5.png")


def fig8():
    x = load(XD)["X1"]
    o = np.array(x["curve_offsets_steps"])
    fig, ax = plt.subplots(figsize=(6.0, 2.6))
    ax.axvline(0, color=AXIS, lw=1, ls=":")
    ax.plot(o, x["curve_events_mean"], color=COL["D_div"], lw=2, label=f"events (n = {x['curve_events_n']})")
    ax.plot(o, x["curve_control_mean"], color=MUTED, lw=2, label=f"controls, disjoint tiles (n = {x['curve_control_n']})")
    ax.set_xlabel("steps relative to the event's grid step (one point per 10-step logging interval)")
    ax.set_ylabel("mean of y minus baseline")
    ax.set_title("EXPLORATORY (X1): the rise sits in the last logging interval", fontsize=9)
    ax.legend(loc="upper left", fontsize=8)
    return save(fig, "fig8_x1_curve.png")


def fig2(store):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "prv_hash_check.py"), store],
                       capture_output=True, text=True)
    if r.returncode:
        sys.exit("HALT: PRV hash check failed")
    e2 = load(E2)["headline"]
    rep = "scripts/outputs/a1_structural_report.json"
    READ.update({rep, "scripts/outputs/a1_events.json"})
    blocks, events, _ = a1_loader.load_blocks(os.path.join(ROOT, rep), store, rung="4.0",
                                              events_path=os.path.join(ROOT, "scripts", "outputs", "a1_events.json"))
    elig = [e for e in events if e["eligible"]]
    order = sorted(range(len(elig)), key=lambda i: (e2["leads"]["D_div"][i], elig[i]["t_e"]))
    ev = elig[order[(len(elig) - 1) // 2]]
    teg = 10 * (ev["t_e"] // 10)
    # recompute headline alarm state per block; HALT unless onsets equal e2_result's
    onsets, states = {d: [] for d in DET}, {d: [] for d in DET}
    for b in blocks:
        y, g = np.asarray(b["y"], float), np.asarray(b["g"], float)
        sc = {"D_div": ops.score_div(y), "B1": ops.score_b1(y), "B2": ops.score_b2(y), "B3": ops.score_b3(g)}
        z4 = ops.b4_z(y)
        fr4 = ops.b4_free_state(z4)
        for d in DET:
            th = e2["thetas"][d]
            th = math.inf if th == "inf" else float(th)
            if d == "B4":
                _, on, al = ops.b4_alarm(z4, th, ops.HOLD, free=fr4)
            else:
                on, al = ops.alarm_from_scores(sc[d], th, ops.HOLD)
            onsets[d] += [int(b["first_step"] + 10 * j) for j in on]
            states[d].append((b["first_step"], al))
    full = load(E2)
    for d in DET:
        if sorted(onsets[d]) != sorted(full["headline"]["detectors"][d]["onsets"]):
            sys.exit(f"HALT: recomputed {d} onsets differ from e2_result.json")
    b = next(bb for bb in blocks if bb["first_step"] <= teg <= bb["first_step"] + 10 * (len(bb["y"]) - 1))
    i0 = (teg - b["first_step"]) // 10
    lo, hi = max(0, i0 - 256), min(len(b["y"]), i0 + 50)
    st = b["first_step"] + 10 * np.arange(lo, hi)
    y = np.asarray(b["y"], float)
    D = ops.divergence(y)
    # loss: per-step, from the owning route-1 file (a1_events.load_loss)
    import a1_events
    meta = load("scripts/outputs/a1_segment_metadata.json")
    srep = load(rep)
    owner = next(iv["owner"] for iv in srep["owner_intervals"] if iv["range"][0] <= teg <= iv["range"][1])
    sid = next(s["id"] for s in meta["segments"] if s["seg"] == owner)
    loss, _ = a1_events.load_loss(store, owner, sid)
    ls = np.arange(st[0], st[-1] + 1)
    lv = np.array([loss.get(int(t), np.nan) for t in ls])
    fig, axs = plt.subplots(4, 1, figsize=(6.5, 5.4), sharex=True, gridspec_kw={"height_ratios": [1, 1, 1, 1.1]})
    rel = lambda t: np.asarray(t) - teg  # noqa: E731
    for ax in axs:
        ax.axvspan(-1280, 0, color=GRID, alpha=0.5, lw=0)
        ax.axvline(0, color=INK2, lw=1, ls=":")
    axs[0].plot(rel(st), y[lo:hi], color=INK2, lw=1.2)
    axs[0].set_ylabel("y = ln g")
    axs[1].plot(rel(st), D[lo:hi], color=COL["D_div"], lw=1.5)
    axs[1].set_ylabel("D")
    axs[2].plot(rel(ls), lv, color=INK, lw=0.8)
    axs[2].set_ylabel("loss")
    for k, d in enumerate(DET):
        al = next(a for f, a in states[d] if f == b["first_step"])[lo:hi]
        axs[3].fill_between(rel(st), k + 0.1, k + 0.9, where=al, color=COL[d], step="mid", lw=0)
        axs[3].text(rel(st)[0], k + 0.5, f"{d} " + ("(θ = ∞, never alarms)" if d == "D_div" else ""), fontsize=7,
                    va="center", color=INK2)
    if not any(next(a for f, a in states[d] if f == b["first_step"])[lo:hi].any() for d in DET):
        axs[3].text(rel(st)[len(st) // 2], len(DET) / 2, "no detector is in alarm anywhere in this window",
                    ha="center", va="center", fontsize=8, color=INK2)
    axs[3].set_ylim(len(DET), 0)
    axs[3].set_yticks([])
    axs[3].set_ylabel("alarm")
    axs[3].set_xlabel("steps relative to t_e^g (shaded: 1,280-step scan window)")
    axs[0].set_title("One A1 event (display rule fixed in DECISIONS 68); headline thresholds", fontsize=9)
    fig.tight_layout()
    return save(fig, "fig2_event.png"), ev["t_e"]


def main():
    store = sys.argv[1]
    os.makedirs(OUT, exist_ok=True)
    made = {"fig1_loop.png": fig1()}
    p, t_e = fig2(store)
    made["fig2_event.png"] = p
    made["fig3_frontier.png"] = fig3()
    made["img01_e2_frontier.png"] = fig3(standalone=True)
    made["fig4_outcomes.png"] = fig4()
    made["fig5_e5.png"] = fig5()
    made["fig8_x1_curve.png"] = fig8()
    man = {"script_sha256": sha(os.path.abspath(__file__)), "fig2_event_t_e": t_e,
           "inputs": {r: sha(os.path.join(ROOT, r)) for r in sorted(READ)},
           "images": {k: sha(v) for k, v in made.items()}}
    json.dump(man, open(os.path.join(OUT, "MANIFEST.json"), "w", encoding="utf-8", newline="\n"), indent=1)
    print(json.dumps(man, indent=1))


if __name__ == "__main__":
    main()
