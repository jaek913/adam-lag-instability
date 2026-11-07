"""End-to-end synthetic series: per-step loss -> spike rule -> events -> gradient-norm grid blocks.
DESIGN D.5 / A1.7 ten-step grid cell (grid = 10, scan 1,280 steps, dedup 2,000) and Amendment 7.8 end-to-end
loss cell (grid = 1, scan 128, dedup 200). The spike rule is the A1 code (scripts/a1_events.py:
enumerate_series at k = 4); eligibility follows Amendment 1 A1.4 with the grid as a parameter.
Construction details are provisional (verification/suite_findings.md items 19a-19f) until decided.
"""
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import a1_events  # noqa: E402

import synth  # noqa: E402

BASE_PATTERN = np.array([0.0, 1.0, 0.0, -1.0])      # period-4 loss base (no spurious spikes; test_a1_events)
LOSS_LEVEL, LOSS_AMP, SPIKE = 2.5, 0.01, 0.1


def geometry(grid):
    """(block step ranges, dedup, scan, n_events). 19a/19b."""
    if grid == 10:
        blocks, s = [], 1
        for _ in range(3):
            blocks.append((s, s + 155_000 - 1))
            s += 155_000 + 5_000                       # 5,000-step gap with no logged steps
        return blocks, 2000, 1280, 57
    return [(1, 50_000)], 200, 128, 20


def eligible(t_e, block, grid, scan, min_hist=1000):
    """Amendment 1 A1.4 with grid as a parameter (== a1_events.eligibility at grid 10)."""
    teg = grid * (t_e // grid)
    ws = teg - scan
    first_grid = (block[0] + grid - 1) // grid * grid
    return ws >= block[0] and (ws - first_grid) // grid >= min_hist


def place(rng, blocks, grid, scan, n_events, l_max, dedup):
    """Uniform random event steps, spacing >= l_max + scan + grid (and > dedup), eligible, residues t_e mod 10
    cycling 0..9 (A1.7). Events are split as evenly as possible across blocks."""
    gap = max(l_max + scan + grid, dedup + 1)
    out = []
    per = [n_events // len(blocks) + (i < n_events % len(blocks)) for i in range(len(blocks))]
    for b, k in zip(blocks, per):
        first_grid = (b[0] + grid - 1) // grid * grid
        lo = first_grid + (1000 * grid) + scan + l_max + grid
        hi = b[1] - 60
        span = hi - lo - (k - 1) * gap
        if span < k:
            raise ValueError("block too short")
        base = np.sort(rng.choice(span, size=k, replace=False))
        out += [int(lo + x + i * gap) for i, x in enumerate(base)]
    out = sorted(out)
    if grid == 10:                                      # force residues 0..9 in turn (A1.7)
        out = [t - (t % 10) + (i % 10) for i, t in enumerate(out)]
    return out


def make_e2e(index, *, grid, phi_obs, L=None, A=0.0, l_max=None):
    rng = synth.child_rng(index)
    blocks, dedup, scan, n_ev = geometry(grid)
    l_max = l_max if l_max is not None else (2000 if grid == 10 else 200)
    t_pl = place(rng, blocks, grid, scan, n_ev, l_max, dedup)
    phi_step = phi_obs ** (1.0 / grid)
    steps_all, loss_all, gblocks = [], [], []
    for b in blocks:
        st = np.arange(b[0], b[1] + 1, dtype=np.int64)
        n = len(st)
        x = synth.ar1(rng, n, phi_step)                 # per-step ln g, unit stationary SD
        loss = LOSS_LEVEL + LOSS_AMP * BASE_PATTERN[st % 4]
        for t in t_pl:
            if b[0] <= t <= b[1]:
                i = t - b[0]
                loss[i] += SPIKE
                if L and A:
                    j0 = max(0, i - L + 1)
                    x[j0:i + 1] += A * np.arange(j0 - i + L, L + 1)[: i + 1 - j0] / L
        steps_all.append(st)
        loss_all.append(loss)
        on = (st % grid) == 0
        y = x[on]
        gblocks.append({"first_step": int(st[on][0]), "y": y, "g": np.exp(y)})
    steps = np.concatenate(steps_all)
    loss = np.concatenate(loss_all)
    evs, cnt, bl = a1_events.enumerate_series(steps, loss, 4.0, dedup)
    events = []
    for e in evs:
        blk = next(bb for bb in blocks if bb[0] <= e["t_e"] <= bb[1])
        events.append({"t_e": e["t_e"], "eligible": bool(eligible(e["t_e"], blk, grid, scan))})
    match = sorted(e["t_e"] for e in events) == t_pl and all(e["eligible"] for e in events)
    return gblocks, events, {"grid": grid, "scan": scan, "planted": t_pl, "events_match": bool(match),
                             "n_events": len(events), "residues": sorted({t % 10 for t in t_pl})}
