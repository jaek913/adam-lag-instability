"""Post-verdict exploratory diagnostics X1-X3 (DECISIONS entry 48; fixed before computation).
Reads A1 through analysis/a1_loader.py after the PRV hash check. Writes analysis/outputs/post/x_diag.json.
Usage: python analysis/post/x_diag.py <store_root>   (test use: --sources <file> --out <dir>)"""
import json
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
import a1_loader  # noqa: E402
import ops  # noqa: E402
import pipeline  # noqa: E402

GRID, SCAN = 10, 1280


def mannwhitney_greater(a, b):
    """One-sided Mann-Whitney U (a > b), normal approximation with tie correction (no scipy dependency)."""
    import math
    a, b = np.asarray(a, float), np.asarray(b, float)
    n1, n2 = len(a), len(b)
    allv = np.concatenate([a, b])
    order = np.argsort(allv, kind="mergesort")
    ranks = np.empty(len(allv))
    sv = allv[order]
    i = 0
    while i < len(sv):
        j = i
        while j + 1 < len(sv) and sv[j + 1] == sv[i]:
            j += 1
        ranks[order[i:j + 1]] = (i + j) / 2 + 1
        i = j + 1
    U = ranks[:n1].sum() - n1 * (n1 + 1) / 2
    _, cnt = np.unique(allv, return_counts=True)
    N = n1 + n2
    var = n1 * n2 / 12 * ((N + 1) - np.sum(cnt ** 3 - cnt) / (N * (N - 1)))
    z = (U - n1 * n2 / 2 - 0.5) / math.sqrt(var)
    return float(U), float(0.5 * math.erfc(z / math.sqrt(2)))


def rise_at(b, i):
    """X1 statistic at block index i (= t_e^g): pre = obs i-13..i-1 (steps t-130..t-10); base = 100 obs ending i-128."""
    if i - 128 - 99 < 0 or i >= len(b["y"]):
        return None
    pre = b["y"][i - 13:i]
    base = b["y"][i - 128 - 99:i - 128 + 1]
    sd = base.std(ddof=1)
    return float((pre.mean() - base.mean()) / sd) if sd > 0 else None


def main():
    store = sys.argv[1]
    sources = sys.argv[sys.argv.index("--sources") + 1] if "--sources" in sys.argv else os.path.join(ROOT, "SOURCES.md")
    outdir = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "analysis", "outputs", "post")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "prv_hash_check.py"), store, "--sources", sources],
                       capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1])
    if r.returncode:
        sys.exit("HALT: PRV hash check failed")
    blocks, events, _ = a1_loader.load_blocks(os.path.join(ROOT, "scripts", "outputs", "a1_structural_report.json"),
                                              store, rung="4.0",
                                              events_path=os.path.join(ROOT, "scripts", "outputs", "a1_events.json"))

    def loc(step):
        for k, b in enumerate(blocks):
            i, rr = divmod(step - b["first_step"], GRID)
            if rr == 0 and 0 <= i < len(b["y"]):
                return k, i
        return None

    elig = [e for e in events if e["eligible"]]
    out = {}
    # ---------------- X1
    ev_rise, ev_block = [], []
    for e in elig:
        k, i = loc(GRID * (e["t_e"] // GRID))
        ev_rise.append(rise_at(blocks[k], i))
        ev_block.append(k)
    # control anchors: out-of-window grid steps, history >= 1,000 + 228 obs, uniform over all such
    pool = []
    for k, b in enumerate(blocks):
        st = b["first_step"] + GRID * np.arange(len(b["y"]))
        oos = ~pipeline.scan_mask(st, events, GRID, SCAN)
        idx = np.nonzero(oos & (np.arange(len(b["y"])) >= ops.MIN_HIST + 228))[0]
        pool += [(k, int(i)) for i in idx]
    rng = np.random.default_rng(20261030)
    pick = rng.choice(len(pool), size=2000, replace=False)
    ctl = [rise_at(blocks[pool[j][0]], pool[j][1]) for j in pick]
    ctl = [c for c in ctl if c is not None]
    evr = [x for x in ev_rise if x is not None]
    mw_U, mw_p = mannwhitney_greater(evr, ctl)

    def curve(points):
        offs = np.arange(-128, 21)
        acc = []
        for k, i in points:
            y = blocks[k]["y"]
            if i - 128 >= 0 and i + 20 < len(y):
                acc.append(y[i + offs] - y[i - 128 - 99:i - 128 + 1].mean())
        return (offs * GRID).tolist(), np.mean(acc, axis=0).tolist(), len(acc)

    ev_pts = [loc(GRID * (e["t_e"] // GRID)) for e in elig]
    o_e, c_e, n_e = curve(ev_pts)
    o_c, c_c, n_c = curve([pool[j] for j in pick])
    out["X1"] = {"n_events": len(evr), "n_control": len(ctl),
                 "event_rise_median": float(np.median(evr)), "control_rise_median": float(np.median(ctl)),
                 "event_share_gt2": float(np.mean(np.array(evr) > 2)), "control_share_gt2": float(np.mean(np.array(ctl) > 2)),
                 "mannwhitney_U": mw_U, "mannwhitney_p_one_sided": mw_p,
                 "event_rises": evr, "event_block": ev_block,
                 "curve_offsets_steps": o_e, "curve_events_mean": c_e, "curve_events_n": n_e,
                 "curve_control_mean": c_c, "curve_control_n": n_c,
                 "reading": ("precursor present (p < 0.05)" if mw_p < 0.05 else
                             "no gradient-norm precursor at 10-130 steps (p >= 0.05)")}
    # ---------------- X2
    def top_rate(sub_blocks):
        n_out, ons = 0, 0
        for b in sub_blocks:
            s = ops.score_div(b["y"])
            st = b["first_step"] + GRID * np.arange(len(b["y"]))
            oos = ~pipeline.scan_mask(st, events, GRID, SCAN) & (np.arange(len(b["y"])) >= ops.MIN_HIST)
            # onsets at D_div's top value P = 1.0 (the percentile's ceiling)
            on, _ = ops.alarm_from_scores(s, 1.0)
            ons += int(np.sum(oos[on])) if len(on) else 0
            n_out += int(oos.sum())
        ns = ops.round_half_up(n_out / 1e4)
        return {"n_out": n_out, "onsets_at_top": ons, "rate_per_10k": 1e4 * ons / n_out if n_out else None,
                "nstar_headline": ns, "unmatchable": (ons > ns) if ns >= 1 else None}

    x2 = {"whole": top_rate(blocks)}
    for k, b in enumerate(blocks):
        x2[f"block_{k}"] = top_rate([b])
    L = max(range(len(blocks)), key=lambda k: len(blocks[k]["y"]))
    b = blocks[L]
    h = len(b["y"]) // 2
    x2["longest_first_half"] = top_rate([{"first_step": b["first_step"], "y": b["y"][:h], "g": b["g"][:h]}])
    x2["longest_second_half"] = top_rate([{"first_step": b["first_step"] + GRID * h, "y": b["y"][h:], "g": b["g"][h:]}])
    n_add = (52300 - 14211 + 1 + 543360 - 504511 + 1) // GRID
    x2["projection"] = {"added_grid_obs_if_route3": n_add,
                        "nstar_full_approx": ops.round_half_up((x2["whole"]["n_out"] + n_add) / 1e4)}
    subs = [v["unmatchable"] for kk, v in x2.items() if kk not in ("projection", "whole") and v["unmatchable"] is not None]
    x2["projection"]["unmatchable_at_full_nstar"] = x2["whole"]["onsets_at_top"] > x2["projection"]["nstar_full_approx"]
    x2["reading"] = ("unmatchable in every sub-series with n* >= 1: detector property, not data coverage"
                     if subs and all(subs) else "matchable in some sub-series with n* >= 1: depends on available data")
    out["X2"] = x2
    # ---------------- X3
    x3 = {}
    for k, b in enumerate(blocks):
        ne = sum(1 for kk in ev_block if kk == k)
        rr = [x for x, kk in zip(ev_rise, ev_block) if kk == k and x is not None]
        x3[f"block_{k}"] = {"first_step": b["first_step"], "n_obs": len(b["y"]), "eligible_events": ne,
                            "events_per_10k_obs": 1e4 * ne / len(b["y"]),
                            "median_rise": float(np.median(rr)) if rr else None}
    out["X3"] = x3
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, "x_diag.json")
    json.dump(out, open(p, "w", encoding="utf-8", newline="\n"), indent=1)
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if not isinstance(vv, list)} if isinstance(v, dict) else v
                      for k, v in out.items()}, indent=1, default=str)[:6000])
    print("WROTE", p)


if __name__ == "__main__":
    main()
