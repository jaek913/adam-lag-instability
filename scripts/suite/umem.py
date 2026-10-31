"""Unequal-memory null (DESIGN D.5 fix round N1; Amendment 9.3(16)): D_div against two synthetic
baselines S1(j) = y(j) and S40(j) = max(y(j-39..j)), each matched by P-FA top scan (Amendment 6.1)
with hold (P-HOLD); leads (A1.4, Amendment 7.6); C_b, C_min over {S1, S40}; joint resampling and the
D.3 label. Theta-independent scores only, so alarm_from_scores applies to all three.
Usage (item-17 measurement): python scripts/suite/umem.py <phi> <first_index> <n_reps>"""
import json
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
import ops  # noqa: E402
import e2stat  # noqa: E402
import pipeline  # noqa: E402
import synth  # noqa: E402

DETS = ["D_div", "S1", "S40"]
BASES = ["S1", "S40"]


def s40(y):
    out = np.full(len(y), np.nan)
    win = np.lib.stride_tricks.sliding_window_view(y, 40).max(axis=1)
    out[39:] = win
    return out


def run(blocks, events, grid=1, scan=128, hold=ops.HOLD, fa=1.0, n_draws=1000, seed=20261030):
    b = blocks[0]
    y = np.asarray(b["y"], float)
    st = b["first_step"] + grid * np.arange(len(y))
    oos = ~pipeline.scan_mask(st, events, grid, scan) & (np.arange(len(y)) >= ops.MIN_HIST)
    n_out = int(oos.sum())
    nstar = ops.round_half_up(fa * n_out / 10000.0)
    scores = {"D_div": ops.score_div(y), "S1": ops._gate(y), "S40": ops._gate(s40(y))}
    alarms, thetas = {}, {}
    oidx = np.nonzero(oos)[0]
    for d in DETS:
        s = scores[d]
        cnt = lambda v, s=s: int(np.isin(ops.alarm_from_scores(s, v, hold)[0], oidx).sum())
        c = s[oos]
        m = ops.match_threshold(cnt, c[~np.isnan(c)], nstar)
        thetas[d] = m["theta"]
        _, al = ops.alarm_from_scores(s, m["theta"], hold)
        alarms[d] = {"kept": [(b["first_step"], al)]}
    elig = [{"t_e": e["t_e"], "series": "kept"} for e in events if e["eligible"]]
    lt = e2stat.leads_table(alarms, elig, grid, scan)
    leads = {d: lt[d][0] for d in DETS}
    C = {bb: float(leads["D_div"].mean() - leads[bb].mean()) for bb in BASES}
    cmin = min(C.values())
    rng = np.random.default_rng(seed)
    n = len(elig)
    cmins = np.empty(n_draws)
    for r in range(n_draws):
        idx = rng.integers(0, n, size=n)
        md = leads["D_div"][idx].mean()
        cmins[r] = min(md - leads[bb][idx].mean() for bb in BASES)
    lab, p05 = e2stat.label(cmin, cmins)
    return {"nstar": nstar, "C": C, "C_min": cmin, "label": lab, "p05": p05, "thetas": thetas,
            "mean_lead": {d: float(leads[d].mean()) for d in DETS}}


def main():
    phi, first, n = float(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    for i in range(first, first + n):
        blocks, events = synth.make_series(i, phi=phi, n_events=20)
        r = run(blocks, events)
        print(json.dumps({"index": i, "phi": phi, **{k: r[k] for k in ("nstar", "C", "C_min", "label", "p05", "mean_lead")}}), flush=True)


if __name__ == "__main__":
    main()
