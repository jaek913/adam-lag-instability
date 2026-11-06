"""Amendment 8.1 reference agreement across the D.5 suite (DECISIONS entry 20: full rerun after
Amendment 9). For every E2-chain cell x replicate, runs analysis/ (pipeline) and reference/ (independent
implementation) on the same series and records whether theta, realised count, every lead, N_out, n* and
C_min agree (compare_ref.compare). Resumable: replicates already in the output file are skipped.

Usage:
  python scripts/suite/run_ref_agreement.py --workers 16            (all eligible cells)
  python scripts/suite/run_ref_agreement.py --cells 25 --workers 1 --out-suffix _single   (item-14 check)
Cells excluded: unequal_memory_null (S1/S40 baselines are not part of the E2 chain; Amendment 9.3(16))
and null_30_50 (superseded by the Amendment 10.2 pulse-sweep cells). Series are built by
run_suite.series_kwargs, so pulse-sweep, step and realised-count cells use exactly the suite's construction.
Cells already on disk (v2: cells 0-99, 105-114) are skipped by the resume logic."""
import argparse
import json
import os
import sys
from multiprocessing import Pool

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts", "suite"))
OUTDIR = os.path.join(ROOT, "scripts", "outputs", "ref_agreement_v2")   # v2: onsets + flags compared (Amendment 8.1)
EXCLUDE = {"unequal_memory_null", "null_30_50"}    # S1/S40 are not the E2 chain; null_30_50 superseded (10.2)
CAL = None


def task(args):
    cell, rep = args
    import compare_ref  # noqa: E402  (imports pipeline, synth, ref_e2)
    import synth
    import run_suite
    c = CELLS[cell]
    kw = run_suite.series_kwargs(c, CAL)               # same construction as the suite verdict run
    blocks, events = synth.make_series(c["child_first"] + rep, **kw)
    d = compare_ref.compare(blocks, events, 1, 128)
    return cell, rep, [list(map(str, x)) for x in d]


def _init(cells, cal):
    global CELLS, CAL
    CELLS, CAL = cells, cal


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--cells", type=str, default="")
    ap.add_argument("--reps", type=int, default=None)
    ap.add_argument("--out-suffix", type=str, default="")
    a = ap.parse_args()
    table = json.load(open(os.path.join(ROOT, "scripts", "suite", "cells.json")))["cells"]
    sel = ([int(x) for x in a.cells.split(",")] if a.cells else
           [c["cell"] for c in table if c["kind"] not in EXCLUDE and "superseded" not in c])
    os.makedirs(OUTDIR, exist_ok=True)
    todo, files = [], {}
    for ci in sel:
        path = os.path.join(OUTDIR, f"cell_{ci:03d}{a.out_suffix}.jsonl")
        files[ci] = path
        done = set()
        if os.path.exists(path):
            with open(path) as f:
                done = {json.loads(l)["rep"] for l in f if l.strip()}
        n = a.reps or table[ci]["reps"]
        todo += [(ci, r) for r in range(n) if r not in done]
    print(f"{len(sel)} cells, {len(todo)} replicate comparisons to run, {a.workers} workers", flush=True)
    handles = {ci: open(p, "a", newline="\n") for ci, p in files.items()}
    n_diff = 0
    cal = json.load(open(os.path.join(ROOT, "scripts", "outputs", "calibration_pulse.json")))
    with Pool(a.workers, initializer=_init, initargs=(table, cal)) as pool:
        for k, (ci, rep, d) in enumerate(pool.imap_unordered(task, todo, chunksize=1), 1):
            handles[ci].write(json.dumps({"cell": ci, "rep": rep, "identical": not d, "diffs": d}) + "\n")
            handles[ci].flush()
            n_diff += bool(d)
            if k % 50 == 0 or k == len(todo):
                print(f"{k}/{len(todo)} done; {n_diff} differing so far", flush=True)
    for h in handles.values():
        h.close()
    # summary over everything on disk
    tot = bad = 0
    for ci, p in files.items():
        with open(p) as f:
            for l in f:
                r = json.loads(l)
                tot += 1
                bad += not r["identical"]
    print(f"SUMMARY: {tot} replicate comparisons on disk, {bad} differ ->", "ALL IDENTICAL" if bad == 0 else "DIFFERENCES FOUND")


if __name__ == "__main__":
    main()
