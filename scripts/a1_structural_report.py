"""A1 structural report (DESIGN Amendment 1 A1.12; Amendment 2 P-SEG; DECISIONS Addendum C item 5(i)).

Inputs: step index and per-row non-null masks of `train/CrossEntropyLoss` and
`optim/total_grad_norm` from the seven used route-1 files, plus run metadata (resume steps).
NO metric value is read, printed or saved. Runs before any loss event is enumerated.

Usage:
  python scripts/a1_structural_report.py <segment_metadata_json> <store_root> <out_json> <out_md>
"""
import glob
import json
import math
import os
import sys
from datetime import datetime, timezone

import pyarrow.parquet as pq

LOSS = "train/CrossEntropyLoss"
GN = "optim/total_grad_norm"
MIN_HIST_OBS = 1000          # Amendment 1 A1.4
SCAN_STEPS = 1280            # Amendment 1 A1.4 (129 grid obs, [t - 1280, t])
GRID = 10
FA_GRID = [0.5, 1, 2, 5]
# Last logged step of the run: run-025's last served row (DECISIONS Addendum B item 8).
RUN_LAST_STEP = 543360
# Served (sparse) last steps of UNUSED segments, from the 2026-10-30 browser query recorded in
# DECISIONS Addendum B item 8. These are LOWER BOUNDS on each segment's true last step.
UNUSED_SERVED_LAST = {"run-002": 14900, "run-003": 39360, "run-004": 41410, "run-005": 42210,
                      "run-006": 51460, "run-007": 52310, "run-009": 73378, "run-011": 160599,
                      "run-012": 160855, "run-014": None, "run-015": None, "run-019": 505560,
                      "run-020": 507010, "run-021": 508510, "run-022": 509210, "run-023": 511360,
                      "run-024": 521010, "run-025": 543360}


def half_up(x):
    return int(math.floor(x + 0.5))


def blocks_of(sorted_steps):
    out = []
    for s in sorted_steps:
        if out and s == out[-1][1] + 1:
            out[-1][1] = s
        else:
            out.append([s, s])
    return out


def subtract(span, cut):
    """[a,b] minus [c,d] -> list of ranges."""
    (a, b), (c, d) = span, cut
    res = []
    if c > b or d < a:
        return [[a, b]]
    if a < c:
        res.append([a, c - 1])
    if d < b:
        res.append([d + 1, b])
    return res


def main():
    meta_path, store, out_json, out_md = sys.argv[1:5]
    meta = json.load(open(meta_path, encoding="utf-8"))
    segs = meta["segments"]
    for s in segs:
        s["resume"] = s["resume_step"] if s["resume_step"] is not None else 0
        s["n"] = int(s["seg"].split("-")[1])

    # --- used segments: step index + null masks only
    used = {}
    for s in segs:
        if not s["used"]:
            continue
        pat = os.path.join(store, "A1", f"{s['seg']}_{s['id']}_history-*_0000.parquet")
        files = glob.glob(pat)
        if len(files) != 1:
            raise SystemExit(f"{s['seg']}: expected one route-1 file, found {files}")
        t = pq.read_table(files[0], columns=["_step", LOSS, GN])
        st = [int(x) for x in t.column("_step").to_pylist()]
        lok = t.column(LOSS).is_valid().to_pylist()
        gok = t.column(GN).is_valid().to_pylist()
        loss_steps = sorted(x for x, ok in zip(st, lok) if ok)
        gn_steps = {x for x, ok in zip(st, gok) if ok}
        lb = blocks_of(loss_steps)
        if len(lb) != 1:
            raise SystemExit(f"{s['seg']}: loss not one contiguous block")
        used[s["seg"]] = {"file": os.path.basename(files[0]), "span": lb[0],
                          "loss_steps": set(loss_steps), "gn_steps": gn_steps,
                          "rows": len(st), "first_row_step": min(st), "last_row_step": max(st)}

    # --- logged span per segment (used: measured loss span; unused: resume+1 .. served last, lower bound)
    for s in segs:
        if s["used"]:
            s["span"] = used[s["seg"]]["span"]
            s["span_basis"] = "measured loss span (route-1 file)"
        else:
            last = UNUSED_SERVED_LAST.get(s["seg"])
            s["span"] = None if last is None else [s["resume"] + 1, last]
            s["span_basis"] = "resume+1 .. served last row (lower bound; Addendum B item 8)"

    # --- ownership (Amendment 2 (a)-(b)): order by (resume, run number); owner of step s = last
    # segment in order with resume < s. Distinct resume values -> owner intervals.
    order = sorted(segs, key=lambda x: (x["resume"], x["n"]))
    distinct = sorted({x["resume"] for x in segs})
    owner_iv = []
    for i, r in enumerate(distinct):
        owner = [x for x in order if x["resume"] == r][-1]
        hi = distinct[i + 1] if i + 1 < len(distinct) else RUN_LAST_STEP
        owner_iv.append({"owner": owner["seg"], "owner_used": owner["used"], "range": [r + 1, hi],
                         "tied_losers": [x["seg"] for x in order if x["resume"] == r][:-1]})
    owned = {iv["owner"]: iv["range"] for iv in owner_iv}

    # --- kept series and gaps
    kept, gaps = [], []
    for iv in owner_iv:
        a, b = iv["range"]
        if iv["owner_used"]:
            ua, ub = used[iv["owner"]]["span"]
            ka, kb = max(a, ua), min(b, ub)
            if ka <= kb:
                kept.append({"range": [ka, kb], "owner": iv["owner"]})
                for g in subtract([a, b], [ka, kb]):
                    gaps.append({"range": g, "cause": f"owner {iv['owner']} (used) not logged here"})
            else:
                gaps.append({"range": [a, b], "cause": f"owner {iv['owner']} (used) not logged here"})
        else:
            gaps.append({"range": [a, b], "cause": f"owner {iv['owner']} unused"})
    # merge adjacent kept / gap ranges
    def merge(lst, key):
        lst = sorted(lst, key=lambda d: d["range"][0])
        out = []
        for d in lst:
            if out and d["range"][0] == out[-1]["range"][1] + 1:
                out[-1]["range"][1] = d["range"][1]
                out[-1][key] = out[-1][key] + "; " + d[key] if d[key] not in out[-1][key] else out[-1][key]
            else:
                out.append({"range": list(d["range"]), key: d[key]})
        return out
    kept_m = merge(kept, "owner")
    gaps_m = merge(gaps, "cause")
    for g in gaps_m:
        a, b = g["range"]
        g["steps"] = b - a + 1
        g["grid_steps"] = len(range((a + GRID - 1) // GRID * GRID, b + 1, GRID))
        g["detector_series_gap"] = g["grid_steps"] > 0
        g["restarts_within"] = sorted(f"{x['seg']}@{x['resume']}" for x in segs if a <= x["resume"] + 1 <= b)

    # --- detector series on the kept blocks
    blocks, N, dropped_total, longest_drop = [], 0, 0, 0
    kept_steps_without_loss = 0
    for k in kept_m:
        a, b = k["range"]
        grid = list(range((a + GRID - 1) // GRID * GRID, b + 1, GRID))
        # owner per grid step within this block (kept_m may merge owners)
        def own(sx):
            for iv in kept:
                if iv["range"][0] <= sx <= iv["range"][1]:
                    return iv["owner"]
        drop = [g for g in grid if g not in used[own(g)]["gn_steps"]]
        run, best = 0, 0
        dset = set(drop)
        for g in grid:
            run = run + 1 if g in dset else 0
            best = max(best, run)
        kept_steps_without_loss += sum(1 for sx in range(a, b + 1) if sx not in used[own(sx)]["loss_steps"])
        first_ok = next((g for g in grid if g not in dset), None)
        earliest = None if first_ok is None else first_ok + GRID * MIN_HIST_OBS + SCAN_STEPS
        last_grid = grid[-1] if grid else None
        span_elig = 0 if (earliest is None or last_grid is None or earliest > last_grid) else last_grid - earliest + GRID
        blocks.append({"range": [a, b], "steps": b - a + 1, "owners": k["owner"], "grid_obs": len(grid),
                       "dropped_grid_obs": len(drop), "longest_dropped_run": best,
                       "earliest_eligible_anchor_t_e_g": earliest, "eligible_anchor_span_steps": span_elig,
                       "longer_than_11280": (b - a + 1) > GRID * MIN_HIST_OBS + SCAN_STEPS})
        N += len(grid)
        dropped_total += len(drop)
        longest_drop = max(longest_drop, best)

    # --- rewind portions (used segments' logged steps they do not own) and unscorable (unused)
    rewind, unscorable = [], []
    for s in segs:
        if s["span"] is None:
            continue
        own_r = owned.get(s["seg"])
        parts = [s["span"]] if own_r is None else subtract(s["span"], own_r)
        for p in parts:
            if p[0] > p[1]:
                continue
            rec = {"seg": s["seg"], "range": p, "steps": p[1] - p[0] + 1,
                   "grid_steps": len(range((p[0] + GRID - 1) // GRID * GRID, p[1] + 1, GRID))}
            (rewind if s["used"] else unscorable).append(rec)

    nstar = {str(fa): half_up(fa * N / 10000) for fa in FA_GRID}
    rep = {
        "generated_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "inputs": {"metadata": os.path.basename(meta_path),
                   "route1_files": {k: v["file"] for k, v in used.items()},
                   "run_last_step": RUN_LAST_STEP, "unused_served_last_lower_bounds": UNUSED_SERVED_LAST},
        "segments": [{"seg": s["seg"], "id": s["id"], "resume_step": s["resume_step"], "used": s["used"],
                      "historyLineCount": s["historyLineCount"], "span": s["span"], "span_basis": s["span_basis"],
                      **({"rows": used[s["seg"]]["rows"], "first_row_step": used[s["seg"]]["first_row_step"],
                          "last_row_step": used[s["seg"]]["last_row_step"]} if s["used"] else {})}
                     for s in sorted(segs, key=lambda x: x["n"])],
        "owner_intervals": owner_iv,
        "kept_blocks": blocks,
        "gaps": gaps_m,
        "detector_series": {"N_grid_obs_kept": N, "dropped_grid_obs": dropped_total,
                            "longest_dropped_run": longest_drop,
                            "kept_steps_without_loss": kept_steps_without_loss},
        "nstar_upper_bounds_before_exclusions": nstar,
        "rewind_portions_used_segments": rewind,
        "unscorable_superseded_unused_segments_lower_bound": unscorable,
        "note": "step index, non-null masks and run metadata only; no metric value read, printed or saved",
    }
    with open(out_json, "w", encoding="utf-8", newline="\n") as f:
        json.dump(rep, f, indent=1)
        f.write("\n")

    # --- markdown
    L = []
    L.append("# A1 structural report (DESIGN Amendment 1 A1.12; Amendment 2)\n")
    L.append(f"Generated {rep['generated_utc']} by scripts/a1_structural_report.py. Step index, non-null masks "
             "and run metadata only; no metric value was read.\n")
    L.append("## Kept series (Amendment 2)\n")
    L.append("| block | steps | owners | grid obs | dropped | longest dropped run | earliest eligible t_e^g | eligible-anchor span (steps) | > 11,280 steps |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    for b in blocks:
        e = b["earliest_eligible_anchor_t_e_g"]
        es = "—" if e is None else f"{e:,}"
        L.append(f"| {b['range'][0]:,}–{b['range'][1]:,} | {b['steps']:,} | {b['owners']} | {b['grid_obs']:,} | "
                 f"{b['dropped_grid_obs']} | {b['longest_dropped_run']} | {es} | "
                 f"{b['eligible_anchor_span_steps']:,} | {'yes' if b['longer_than_11280'] else 'no'} |")
    L.append("\n## Gaps\n")
    L.append("| range | steps | grid steps | detector-series gap | cause | restarts within |")
    L.append("|---|---|---|---|---|---|")
    for g in gaps_m:
        L.append(f"| {g['range'][0]:,}–{g['range'][1]:,} | {g['steps']:,} | {g['grid_steps']:,} | "
                 f"{'yes' if g['detector_series_gap'] else 'no'} | {g['cause']} | {', '.join(g['restarts_within']) or '—'} |")
    d = rep["detector_series"]
    L.append("\n## Detector series and false-alarm budget\n")
    L.append(f"- N (grid observations in the kept series): **{d['N_grid_obs_kept']:,}**")
    L.append(f"- Dropped grid observations: {d['dropped_grid_obs']}; longest consecutive run: {d['longest_dropped_run']}")
    L.append(f"- Kept steps without a loss value: {d['kept_steps_without_loss']}")
    L.append("- n* upper bounds before any exclusion (round-half-up of FA × N / 10,000): " +
             ", ".join(f"FA {k}: {v}" for k, v in nstar.items()))
    L.append("\n## Rewind portions of used segments (scored on their own series)\n")
    L.append("| segment | range | steps | grid steps |")
    L.append("|---|---|---|---|")
    for r in rewind:
        L.append(f"| {r['seg']} | {r['range'][0]:,}–{r['range'][1]:,} | {r['steps']:,} | {r['grid_steps']:,} |")
    L.append("\n## Superseded portions of unused segments (unscorable; lower bounds from served rows)\n")
    L.append("| segment | range | steps |")
    L.append("|---|---|---|")
    for r in unscorable:
        L.append(f"| {r['seg']} | {r['range'][0]:,}–{r['range'][1]:,} | {r['steps']:,} |")
    L.append("\n## Segments\n")
    L.append("| segment | id | resume step | used | server lines | logged span | basis |")
    L.append("|---|---|---|---|---|---|---|")
    for s in rep["segments"]:
        sp = "—" if s["span"] is None else f"{s['span'][0]:,}–{s['span'][1]:,}"
        rs = "—" if s["resume_step"] is None else f"{s['resume_step']:,}"
        L.append(f"| {s['seg']} | {s['id']} | {rs} | "
                 f"{'yes' if s['used'] else 'no'} | {s['historyLineCount']:,} | {sp} | {s['span_basis']} |")
    with open(out_md, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(L) + "\n")
    print(json.dumps({"kept_blocks": [b["range"] for b in blocks], "gaps": [g["range"] for g in gaps_m],
                      **rep["detector_series"], "nstar": nstar,
                      "rewind": [[r["seg"], r["range"]] for r in rewind]}, indent=1))


if __name__ == "__main__":
    main()
