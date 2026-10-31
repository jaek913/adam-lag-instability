"""Loss-spike events on A1 (DESIGN D.2 spike rule; Amendment 1 A1.3-A1.4; Amendment 2 P-SEG;
Amendment 3 construction details; P-KLAD k ladder). Runs BEFORE any detector score.

Reads `_step` and `train/CrossEntropyLoss` only. Prints counts and event times; never prints a
loss value.

Usage:
  python scripts/a1_events.py <structural_report_json> <segment_metadata_json> <store_root> <out_json> <out_md>
"""
import glob
import json
import math
import os
import sys
from datetime import datetime, timezone

import numpy as np
import pyarrow.parquet as pq

LOSS = "train/CrossEntropyLoss"
W = 128                 # D.2 trailing window
MIN_FINITE = 64         # Amendment 3 (2)
DEDUP_A1 = 2000         # Amendment 1 A1.3 (inclusive, Amendment 3 (3))
GRID = 10
MIN_HIST_OBS = 1000     # Amendment 1 A1.4
SCAN = 1280             # Amendment 1 A1.4
K_LADDER = [4.0, 3.0]   # P-KLAD
MIN_EVENTS = 5


# ---------------------------------------------------------------- core (series-level)
def blocks_from_steps(steps):
    """Indices [i0, i1) of contiguous step runs in a sorted step array."""
    if len(steps) == 0:
        return []
    br = np.nonzero(np.diff(steps) != 1)[0] + 1
    starts = np.concatenate([[0], br])
    ends = np.concatenate([br, [len(steps)]])
    return list(zip(starts.tolist(), ends.tolist()))


def spikes_in_block(x, k):
    """x: loss values of ONE contiguous block (np.float64, non-finite allowed).
    Returns (spike_mask, tested_mask, untested_a, untested_b). Amendment 3 (1)-(2)."""
    n = len(x)
    fin = np.isfinite(x)
    tested = np.zeros(n, bool)
    spike = np.zeros(n, bool)
    if n <= W:
        return spike, tested, n, 0
    off = np.nanmedian(np.where(fin, x, np.nan)) if fin.any() else 0.0
    xv = np.where(fin, x - off, 0.0)
    c = np.concatenate([[0], np.cumsum(fin)])
    s1 = np.concatenate([[0.0], np.cumsum(xv)])
    s2 = np.concatenate([[0.0], np.cumsum(xv * xv)])
    t = np.arange(W, n)                       # trailing window t-W .. t-1 lies in block
    cnt = c[t] - c[t - W]
    ok = cnt >= MIN_FINITE
    untested_a = W
    untested_b = int((~ok).sum())
    tested[t[ok]] = True
    sm = s1[t] - s1[t - W]
    sq = s2[t] - s2[t - W]
    with np.errstate(invalid="ignore", divide="ignore"):
        mean = sm / cnt
        var = (sq - sm * sm / cnt) / (cnt - 1)
    sd = np.sqrt(np.maximum(var, 0.0))
    for kk, tt in enumerate(t):
        if not ok[kk]:
            continue
        if not fin[tt]:
            spike[tt] = True                  # NaN/inf counts as exceeding (D.2)
            continue
        thr = mean[kk] + k * sd[kk]
        val = x[tt] - off
        tol = 1e-6 * (abs(thr) + 1.0)
        if val > thr + tol:
            spike[tt] = True
        elif val > thr - tol:                 # borderline: exact two-pass recomputation
            w = x[tt - W:tt]
            w = w[np.isfinite(w)]
            spike[tt] = bool(x[tt] > w.mean() + k * w.std(ddof=1))
    return spike, tested, untested_a, untested_b


def chain_events(spike_steps, nan_steps, dedup):
    """Chained dedup within ONE block (Amendment 3 (3)-(4)): inclusive distance."""
    events = []
    for s in spike_steps:
        if events and s - events[-1]["last"] <= dedup:
            e = events[-1]
            e["last"] = s
            e["n_spikes"] += 1
            e["any_nan"] = e["any_nan"] or (s in nan_steps)
        else:
            events.append({"t_e": int(s), "last": int(s), "n_spikes": 1, "any_nan": s in nan_steps})
    return events


def enumerate_series(steps, x, k, dedup):
    """steps: sorted int array; x: loss values. Gaps = step jumps. Returns events + counts."""
    out_events, cnt = [], {"steps": len(steps), "tested": 0, "untested_first128": 0,
                          "untested_finite_floor": 0, "nonfinite_steps": int((~np.isfinite(x)).sum()),
                          "spikes": 0, "nonfinite_spikes": 0, "blocks": 0}
    blocks = []
    for i0, i1 in blocks_from_steps(steps):
        st = steps[i0:i1]
        sp, te, ua, ub = spikes_in_block(x[i0:i1], k)
        cnt["blocks"] += 1
        cnt["tested"] += int(te.sum())
        cnt["untested_first128"] += min(ua, len(st))
        cnt["untested_finite_floor"] += ub
        sps = st[sp]
        nan_set = set(st[sp & ~np.isfinite(x[i0:i1])].tolist())
        cnt["spikes"] += len(sps)
        cnt["nonfinite_spikes"] += len(nan_set)
        evs = chain_events(sps.tolist(), nan_set, dedup)
        for e in evs:
            e["block"] = [int(st[0]), int(st[-1])]
        out_events.extend(evs)
        blocks.append([int(st[0]), int(st[-1])])
    return out_events, cnt, blocks


def eligibility(e, blocks):
    """Amendment 1 A1.4 on grid observations (no dropped grid observations on A1: entry 11)."""
    teg = GRID * (e["t_e"] // GRID)
    ws = teg - SCAN
    b = next(bb for bb in blocks if bb[0] <= e["t_e"] <= bb[1])
    first_grid = (b[0] + GRID - 1) // GRID * GRID
    e["t_e_g"] = teg
    e["scan_window_steps"] = [ws, teg]
    if ws < b[0]:
        e["eligible"], e["reason"] = False, "scan window crosses series start/gap"
    elif (ws - first_grid) // GRID < MIN_HIST_OBS:
        e["eligible"], e["reason"] = False, "minimum history (1,000 grid obs) not met"
    else:
        e["eligible"], e["reason"] = True, ""
    return e


# ---------------------------------------------------------------- A1 driver
def load_loss(store, seg, sid):
    f = glob.glob(os.path.join(store, "A1", f"{seg}_{sid}_history-*_0000.parquet"))
    if len(f) != 1:
        raise SystemExit(f"{seg}: expected one route-1 file, found {f}")
    t = pq.read_table(f[0], columns=["_step", LOSS])
    st = np.array([int(s) for s in t.column("_step").to_pylist()], dtype=np.int64)
    lv = np.array([np.nan if v is None else float(v) for v in t.column(LOSS).to_pylist()], dtype=np.float64)
    has = np.array([v is not None for v in t.column(LOSS).to_pylist()])
    return {int(s): float(v) for s, v, h in zip(st, lv, has) if h}, os.path.basename(f[0])


def main():
    rep_path, meta_path, store, out_json, out_md = sys.argv[1:6]
    rep = json.load(open(rep_path, encoding="utf-8"))
    meta = json.load(open(meta_path, encoding="utf-8"))
    segs = {s["seg"]: s for s in meta["segments"]}
    loss = {}
    files = {}
    for seg, s in segs.items():
        if s["used"]:
            loss[seg], files[seg] = load_loss(store, seg, s["id"])

    def owner_of(step):
        for iv in rep["owner_intervals"]:
            if iv["range"][0] <= step <= iv["range"][1]:
                return iv["owner"]

    # kept series
    kept_steps = []
    for b in rep["kept_blocks"]:
        kept_steps.extend(range(b["range"][0], b["range"][1] + 1))
    kept_steps = np.array(kept_steps, dtype=np.int64)
    kept_x = np.array([loss[owner_of(int(s))][int(s)] for s in kept_steps])

    # rewind series (Amendment 3 (5))
    rewind_series = []
    for rw in rep["rewind_portions_used_segments"]:
        seg = rw["seg"]
        r = segs[seg]["resume_step"] or 0
        pre = kept_steps[kept_steps <= r]
        own = np.array(sorted(s for s in loss[seg] if s > r), dtype=np.int64)
        st = np.concatenate([pre, own])
        x = np.concatenate([kept_x[kept_steps <= r], np.array([loss[seg][int(s)] for s in own])])
        rewind_series.append({"seg": seg, "portion": rw["range"], "steps": st, "x": x})

    result = {"generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
              "inputs": {"structural_report": os.path.basename(rep_path), "route1_files": files},
              "rules": {"W": W, "min_finite": MIN_FINITE, "sigma_ddof": 1, "dedup_inclusive": DEDUP_A1,
                        "min_hist_grid_obs": MIN_HIST_OBS, "scan_steps": SCAN, "k_ladder": K_LADDER},
              "rungs": {}}
    for k in K_LADDER:
        ev, cnt, blocks = enumerate_series(kept_steps, kept_x, k, DEDUP_A1)
        for e in ev:
            e["series"] = "kept"
            eligibility(e, blocks)
        rws = []
        rcounts = {}
        for rs in rewind_series:
            evr, cr, br = enumerate_series(rs["steps"], rs["x"], k, DEDUP_A1)
            a, b = rs["portion"]
            sel = [e for e in evr if a <= e["t_e"] <= b]
            for e in sel:
                e["series"] = f"rewind:{rs['seg']}"
                eligibility(e, br)
            rws.extend(sel)
            rcounts[rs["seg"]] = {"rewind_events": len(sel), "eligible": sum(e["eligible"] for e in sel)}
        allev = ev + rws
        n_el = sum(e["eligible"] for e in allev)
        result["rungs"][str(k)] = {
            "kept_series_counts": cnt,
            "events_kept": len(ev), "eligible_kept": sum(e["eligible"] for e in ev),
            "spikes_merged_by_dedup_kept": cnt["spikes"] - len(ev),
            "ineligible_min_history": sum(1 for e in allev if e["reason"].startswith("minimum")),
            "ineligible_window_crosses_gap": sum(1 for e in allev if e["reason"].startswith("scan")),
            "rewind": rcounts, "rewind_events": len(rws), "eligible_rewind": sum(e["eligible"] for e in rws),
            "eligible_total": n_el,
            "chains_closed_at_gap": sum(1 for e in ev if e["block"][1] - e["last"] <= DEDUP_A1
                                        and e["block"][1] != int(kept_steps[-1])),
            "events": allev,
        }
    r4 = result["rungs"]["4.0"]["eligible_total"]
    r3 = result["rungs"]["3.0"]["eligible_total"]
    if r4 >= MIN_EVENTS:
        resolved = "k=4"
    elif r3 >= MIN_EVENTS:
        resolved = "k=3"
    else:
        resolved = "INSUFFICIENT EVENTS"
    result["k_ladder_resolution"] = {"eligible_k4": r4, "eligible_k3": r3, "resolved": resolved}
    result["note"] = "event times and counts only; no loss value printed or saved"
    with open(out_json, "w", encoding="utf-8", newline="\n") as f:
        json.dump(result, f, indent=1)
        f.write("\n")

    L = ["# A1 loss-spike events (D.2; Amendments 1-3; P-KLAD)\n",
         f"Generated {result['generated_utc']} by scripts/a1_events.py. Loss values were read to test spikes; "
         "none is printed or saved. No detector score has been computed.\n",
         f"**k ladder:** eligible events at k = 4: **{r4}**; at k = 3: **{r3}**; resolved: **{resolved}**.\n"]
    for k in K_LADDER:
        R = result["rungs"][str(k)]
        c = R["kept_series_counts"]
        L.append(f"## k = {k:g}\n")
        L.append(f"- Kept series: {c['steps']:,} steps in {c['blocks']} blocks; tested {c['tested']:,}; untested "
                 f"(first 128 after a start/gap) {c['untested_first128']:,}; untested (finite floor < 64) "
                 f"{c['untested_finite_floor']:,}; non-finite loss steps {c['nonfinite_steps']:,}.")
        L.append(f"- Spikes {c['spikes']:,} (non-finite {c['nonfinite_spikes']:,}); events {R['events_kept']:,}; "
                 f"spikes merged by the 2,000-step dedup {R['spikes_merged_by_dedup_kept']:,}; chains closed at a gap "
                 f"{R['chains_closed_at_gap']}.")
        L.append(f"- Eligible: kept {R['eligible_kept']}, rewind {R['eligible_rewind']} (of {R['rewind_events']} rewind "
                 f"events), total **{R['eligible_total']}**. Ineligible: minimum history {R['ineligible_min_history']}, "
                 f"scan window crosses a start/gap {R['ineligible_window_crosses_gap']}.\n")
        L.append("| series | t_e | t_e^g | last spike | spikes | non-finite | eligible | reason |")
        L.append("|---|---|---|---|---|---|---|---|")
        for e in sorted(R["events"], key=lambda d: d["t_e"]):
            L.append(f"| {e['series']} | {e['t_e']:,} | {e['t_e_g']:,} | {e['last']:,} | {e['n_spikes']} | "
                     f"{'yes' if e['any_nan'] else 'no'} | {'yes' if e['eligible'] else 'no'} | {e['reason'] or '—'} |")
        L.append("")
    with open(out_md, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    print(json.dumps({"k_ladder_resolution": result["k_ladder_resolution"],
                      **{f"k={k:g}": {kk: result['rungs'][str(k)][kk] for kk in
                         ("events_kept", "eligible_kept", "rewind_events", "eligible_rewind", "eligible_total",
                          "ineligible_min_history", "ineligible_window_crosses_gap", "spikes_merged_by_dedup_kept")}
                         for k in K_LADDER}}, indent=1))


if __name__ == "__main__":
    main()
