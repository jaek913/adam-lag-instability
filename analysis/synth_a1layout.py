"""A1-structure synthetic series (DESIGN Amendment 13.3). A1's kept-series block/gap layout is read from
scripts/outputs/a1_structural_report.json (step index only). 61 planted loss spikes mirroring A1's realised
enumeration (DECISIONS entry 13): 4 ineligible on minimum history (2/1/1 by block) + 57 eligible (1/13/43);
residues of t_e mod 10 cycle 0..9. Loss and gradient-norm construction as synth_e2e (Amendment 13.1: 19c, 19d);
spike rule = a1_events.enumerate_series (k = 4, dedup 2,000); eligibility = a1_events.eligibility (A1 code)."""
import json
import os

import numpy as np

import synth
import synth_e2e
from synth_e2e import a1_events

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GRID, SCAN, DEDUP, L_MAX = 10, 1280, 2000, 1000
INELIGIBLE = [2, 1, 1]
ELIGIBLE = [1, 13, 43]


def a1_blocks():
    r = json.load(open(os.path.join(ROOT, "scripts", "outputs", "a1_structural_report.json")))
    return [tuple(b["range"]) for b in r["kept_blocks"]]


def _spread(rng, lo, hi, k, gap):
    """k uniform points in [lo, hi] with spacing >= gap (gap transform)."""
    if k == 0:
        return []
    span = hi - lo - (k - 1) * gap
    if span < k:
        raise ValueError("zone too short")
    base = np.sort(rng.choice(span, size=k, replace=False))
    return [int(lo + x + i * gap) for i, x in enumerate(base)]


def place(rng, blocks):
    gap = max(L_MAX + SCAN + GRID, DEDUP + 1)
    planted, designed = [], {}
    for bi, b in enumerate(blocks):
        first_grid = (b[0] + GRID - 1) // GRID * GRID
        elig_from = first_grid + 1000 * GRID + SCAN          # earliest eligible anchor (A1.4)
        # ineligible zone: tested by the spike rule (>= 128 steps after block start), before elig_from - gap
        inel = _spread(rng, b[0] + 300, elig_from - gap - GRID, INELIGIBLE[bi], gap)
        el = _spread(rng, elig_from + GRID, b[1] - 60, ELIGIBLE[bi], gap)
        for t in inel:
            designed[t] = (bi, False)
        for t in el:
            designed[t] = (bi, True)
        planted += inel + el
    planted = sorted(planted)
    out, d2 = [], {}
    for i, t in enumerate(planted):                             # residues cycle 0..9 (A1.7)
        t2 = t - (t % 10) + (i % 10)
        out.append(t2)
        d2[t2] = designed[t]
    return out, d2


def make_a1(index, *, phi_obs, L=None, A=0.0, shift=None, sigma_m=None, shift_len=1000):
    """shift / sigma_m (Amendment 15.4 positive control): a sustained mean shift of `shift` x stationary SD over the
    final `shift_len` steps before each t_e (through t_e), and white measurement noise of SD `sigma_m` added to y at
    every step. Both default to None, which leaves every earlier construction byte-identical (no extra draws)."""
    rng = synth.child_rng(index)
    blocks = a1_blocks()
    t_pl, designed = place(rng, blocks)
    phi_step = phi_obs ** (1.0 / GRID)
    steps_all, loss_all, gblocks = [], [], []
    for b in blocks:
        st = np.arange(b[0], b[1] + 1, dtype=np.int64)
        x = synth.ar1(rng, len(st), phi_step)
        if sigma_m is not None:
            x = x + sigma_m * rng.standard_normal(len(st))
        loss = synth_e2e.LOSS_LEVEL + synth_e2e.LOSS_AMP * synth_e2e.BASE_PATTERN[st % 4]
        for t in t_pl:
            if b[0] <= t <= b[1]:
                i = t - b[0]
                loss[i] += synth_e2e.SPIKE
                if L and A:
                    j0 = max(0, i - L + 1)
                    x[j0:i + 1] += A * np.arange(j0 - i + L, L + 1)[: i + 1 - j0] / L
                if shift is not None:
                    x[max(0, i - shift_len + 1):i + 1] += shift
        steps_all.append(st)
        loss_all.append(loss)
        on = (st % GRID) == 0
        gblocks.append({"first_step": int(st[on][0]), "y": x[on], "g": np.exp(x[on])})
    evs, cnt, bl = a1_events.enumerate_series(np.concatenate(steps_all), np.concatenate(loss_all), 4.0, DEDUP)
    bl = [[b[0], b[1]] for b in blocks]
    events, inel_by_block, pred_by_block = [], [0, 0, 0], [0, 0, 0]
    for e in evs:
        a1_events.eligibility(e, bl)
        events.append({"t_e": e["t_e"], "eligible": bool(e["eligible"])})
    for t, (bi, el) in designed.items():
        pred_by_block[bi] += (not el)
    for e in events:
        bi = next(i for i, b in enumerate(blocks) if b[0] <= e["t_e"] <= b[1])
        inel_by_block[bi] += (not e["eligible"])
    match = sorted(e["t_e"] for e in events) == t_pl
    elig_ok = all(designed.get(e["t_e"], (None, None))[1] == e["eligible"] for e in events)
    return gblocks, events, {"grid": GRID, "scan": SCAN, "planted": t_pl, "events_match": bool(match),
                             "eligibility_match": bool(elig_ok), "n_events": len(events),
                             "n_eligible": sum(e["eligible"] for e in events),
                             "ineligible_by_block": inel_by_block, "predicted_ineligible_by_block": pred_by_block,
                             "residues": sorted({t % 10 for t in t_pl})}
