"""A1 loader: kept-series grid blocks (y = ln g, g) per DESIGN Amendment 2 ownership and the
A1.12 structural report, plus the public event list (DECISIONS entry 13). Reads `_step` and
`optim/total_grad_norm` only. Runs on real data ONLY after the D.5 suite passes.

A grid observation is dropped (A1.1) if g is null, non-finite or <= 0; prepare_block carries it
forward and starts each block at its first non-dropped reading (Amendment 5.2).
"""
import glob
import json
import os

import numpy as np
import pyarrow.parquet as pq

import ops

GN = "optim/total_grad_norm"
GRID = 10


def _owner_map(report):
    return [(iv["range"][0], iv["range"][1], iv["owner"]) for iv in report["owner_intervals"]]


def load_blocks(report_path, store, rung="4.0", events_path=None):
    rep = json.load(open(report_path, encoding="utf-8"))
    owners = _owner_map(rep)
    cache = {}

    def gn_of(seg):
        if seg not in cache:
            sid = next(s["id"] for s in rep["segments"] if s["seg"] == seg)
            f = glob.glob(os.path.join(store, "A1", f"{seg}_{sid}_history-*_0000.parquet"))
            if len(f) != 1:
                raise SystemExit(f"{seg}: expected one route-1 file, found {f}")
            t = pq.read_table(f[0], columns=["_step", GN])
            st = [int(x) for x in t.column("_step").to_pylist()]
            cache[seg] = dict(zip(st, t.column(GN).to_pylist()))
        return cache[seg]

    blocks, report = [], []
    for kb in rep["kept_blocks"]:
        a, b = kb["range"]
        first_grid = (a + GRID - 1) // GRID * GRID
        steps = np.arange(first_grid, b + 1, GRID)
        g = np.empty(len(steps))
        for i, s in enumerate(steps):
            seg = next(o for lo, hi, o in owners if lo <= s <= hi)
            v = gn_of(seg).get(int(s))
            g[i] = np.nan if v is None else float(v)
        dropped = ~np.isfinite(g) | (g <= 0)
        gcf, off = ops.prepare_block(np.where(dropped, np.nan, g), dropped)
        blocks.append({"first_step": int(steps[off]) if off < len(steps) else None,
                       "y": np.log(gcf), "g": gcf})
        report.append({"kept_block": [a, b], "first_grid_step": int(steps[0]), "n_obs": int(len(steps)),
                       "leading_dropped": int(off), "dropped_total": int(dropped.sum())})
    events = None
    if events_path:
        ev = json.load(open(events_path, encoding="utf-8"))
        events = [{"t_e": e["t_e"], "eligible": e["eligible"], "series": e["series"]}
                  for e in ev["rungs"][rung]["events"]]
    return blocks, events, report
