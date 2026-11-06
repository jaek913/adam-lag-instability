"""D.5 suite verdict run, statistical cells (DESIGN D.5 as amended by Amendments 7-10).
For each cell x replicate of the selected kinds, generates the series (analysis/synth.py, child index =
cell child_first + rep) and runs the E2 chain with joint resampling and the D.3 label (analysis/pipeline.py),
or the unequal-memory chain (scripts/suite/umem.py). One JSON line per replicate. Resumable.
Grading is separate: scripts/suite/grade_suite.py.

Resampling inside a replicate uses a fresh default_rng(20261030), exactly as the E2 run on A1 will
(Amendment 7.4); the replicate's data come from its own SeedSequence child (Amendment 8.2(14)).

Usage:
  python scripts/suite/run_suite.py --workers 16                      (all runnable kinds)
  python scripts/suite/run_suite.py --cells 25 --workers 1 --out-suffix _single   (item-14 identity check)"""
import argparse
import json
import os
import sys
from multiprocessing import Pool

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [os.path.join(ROOT, "analysis"), os.path.join(ROOT, "scripts", "suite")]
OUTDIR = os.path.join(ROOT, "scripts", "outputs", "suite_v1")
RUN_KINDS = {"planted_effect", "regime_span", "planted_null", "surge_null", "surge_effect", "t3_null",
             "decision_flip", "t3_decision_flip", "unequal_memory_null", "null_pulse_sweep", "step_characterization",
             "realised_count_null", "realised_count_flip", "realised_count_effect"}
CALIB = os.path.join(ROOT, "scripts", "outputs", "calibration_pulse.json")


def series_kwargs(c, calib):
    kw = dict(phi=c["phi"], n_events=c["n_events"], L=c.get("L"), A=c.get("A", 0.0),
              innov=c.get("innov", "gauss"), surge_on=c.get("surge", False))
    if c["kind"] == "null_pulse_sweep":
        kw["pulse_h"] = float(calib["phi"][str(c["phi"])]["chosen"][c["pulse_for"]])
    if c["kind"] == "step_characterization":
        kw["step_h"] = float(c["step_h"])
    return kw


def task(args):
    import pipeline
    import synth
    import umem
    cell, rep = args
    c = CELLS[cell]
    kw = series_kwargs(c, CAL)
    blocks, events = synth.make_series(c["child_first"] + rep, **kw)
    if c["kind"] == "unequal_memory_null":
        r = umem.run(blocks, events)
        row = {"label": r["label"], "C_min": r["C_min"], "p05": r["p05"], "C": r["C"], "nstar": r["nstar"],
               "mean_lead": r["mean_lead"]}
    else:
        o = pipeline.run(blocks, events, grid=1, scan=128, coverage_stop=None, n_draws=1000, seed=20261030)
        row = {"label": o["label"], "C_min": o.get("C_min"), "p05": o.get("p05"), "C": o.get("C"),
               "nstar": o["nstar"], "N_out": o["N_out"], "argmax": o.get("argmax"),
               "coverage": {d: o["detectors"][d]["coverage"] for d in o["detectors"]},
               "per_detector": o.get("per_detector")}
    if "pulse_h" in kw:
        row["pulse_h"] = kw["pulse_h"]
    return cell, rep, row


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
    cal = json.load(open(CALIB))
    sel = ([int(x) for x in a.cells.split(",")] if a.cells else
           [c["cell"] for c in table if c["kind"] in RUN_KINDS and "superseded" not in c and "pending" not in c])
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
    print(f"{len(sel)} cells, {len(todo)} replicates to run, {a.workers} workers", flush=True)
    handles = {ci: open(p, "a", newline="\n") for ci, p in files.items()}
    with Pool(a.workers, initializer=_init, initargs=(table, cal)) as pool:
        for k, (ci, rep, row) in enumerate(pool.imap_unordered(task, todo, chunksize=1), 1):
            handles[ci].write(json.dumps({"cell": ci, "rep": rep, **row}, sort_keys=True) + "\n")
            handles[ci].flush()
            if k % 100 == 0 or k == len(todo):
                print(f"{k}/{len(todo)} done", flush=True)
    for h in handles.values():
        h.close()
    print("DONE; grade with: python scripts/suite/grade_suite.py")


if __name__ == "__main__":
    main()
