"""Amendment 14.3 measurement run (exploratory; CALIBRATION seeds only) of the dynamic-range cells: same cell
definitions as cells.json (dr_step, dr_grid10), child indices = that phi's calibration range + offset 700 (per-step)
or 800 (grid 10), R replicates (disjoint from the pulse (0-99) and flip (500-599) calibrations and from every
evaluation range). Applies the Amendment 14.3 group criterion and writes scripts/outputs/dynamic_range_measure.json.
Usage: python scripts/suite/measure_dynamic_range.py --workers 16 [--reps 100]"""
import argparse
import json
import os
import sys
from multiprocessing import Pool

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [os.path.join(ROOT, "analysis"), os.path.join(ROOT, "scripts", "suite")]
OFF = {"dr_step": 700, "dr_grid10": 800}


def one(args):
    import pipeline
    import run_suite
    c, idx = args
    cc = dict(c, child_first=idx)
    b, e, grid, scan, _ = run_suite.build(cc, 0, None)
    o = pipeline.run(b, e, grid=grid, scan=scan, resample=False, coverage_stop=None)
    return c["cell"], {"per_detector": {d: {k: o["per_detector"][d][k] for k in ("detection_rate", "mean_lead")}
                                        for d in o["per_detector"]}}


def main():
    import grade_suite
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--reps", type=int, default=100)
    a = ap.parse_args()
    tab = json.load(open(os.path.join(ROOT, "scripts", "suite", "cells.json")))
    calib = {c["phi"]: c["child_first"] for c in tab["calibration"]}
    cells = [c for c in tab["cells"] if c["kind"] in OFF]
    tasks = [(c, calib[c["phi"]] + OFF[c["kind"]] + r) for c in cells for r in range(a.reps)]
    rows = {c["cell"]: [] for c in cells}
    with Pool(a.workers) as pool:
        for k, (ci, row) in enumerate(pool.imap_unordered(one, tasks, chunksize=2), 1):
            rows[ci].append(row)
            if k % 200 == 0:
                print(f"{k}/{len(tasks)}", flush=True)
    out = {"reps": a.reps, "offsets": OFF, "groups": {}}
    for kind in OFF:
        for phi in sorted(calib):
            grp = {c.get("L_obs", c["L"]): rows[c["cell"]] for c in cells if c["kind"] == kind and c["phi"] == phi}
            okd, txt = grade_suite.grade_dr(grp)
            out["groups"][f"{kind} phi={phi}"] = {"pass": okd, "detail": txt}
            print(f"{kind} phi={phi}: {'PASS' if okd else 'FAIL'} | {txt}", flush=True)
    with open(os.path.join(ROOT, "scripts", "outputs", "dynamic_range_measure.json"), "w", newline="\n") as f:
        json.dump(out, f, indent=1)
    print("WROTE scripts/outputs/dynamic_range_measure.json (exploratory; grading is on evaluation seeds)")


if __name__ == "__main__":
    main()
