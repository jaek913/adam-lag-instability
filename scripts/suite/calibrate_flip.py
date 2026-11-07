"""Amendment 12.1 calibration of the reported long-ramp flip cells (calibration seeds only).
For each phi_y and L in {16, 24}: A = the smallest value in {3, 4, 5, 6, 8, 10, 12} at which the best
raw-reading baseline (max of B1, B2, B3 detection rate, averaged over R replicates at headline FA, 20 events)
is >= 0.90. Seeds: that phi's calibration range in cells.json, offsets 500..500+R-1 (disjoint from the
pulse calibration, which used offsets 0..99). Output: scripts/outputs/calibration_flip.json.
Usage: python scripts/suite/calibrate_flip.py --workers 16 [--reps 100]"""
import argparse
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
A_GRID = [3, 4, 5, 6, 8, 10, 12]
LS = [16, 24]
RAW = ["B1", "B2", "B3"]
OFFSET = 500


def one(args):
    import pipeline
    import synth
    phi, L, A, idx = args
    b, e = synth.make_series(idx, phi=phi, n_events=20, L=L, A=float(A))
    o = pipeline.run(b, e, grid=1, scan=128, resample=False, coverage_stop=None)
    return phi, L, A, {d: o["per_detector"][d]["detection_rate"] for d in pipeline.DET}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--reps", type=int, default=100)
    a = ap.parse_args()
    calib = json.load(open(os.path.join(ROOT, "scripts", "suite", "cells.json")))["calibration"]
    res = {"A_grid": A_GRID, "reps": a.reps, "offset": OFFSET, "criterion": "max(B1,B2,B3) detection >= 0.90", "phi": {}}
    with Pool(a.workers) as pool:
        for c in calib:
            phi = c["phi"]
            idxs = range(c["child_first"] + OFFSET, c["child_first"] + OFFSET + a.reps)
            tasks = [(phi, L, A, i) for L in LS for A in A_GRID for i in idxs]
            acc = {}
            for _, L, A, r in pool.imap_unordered(one, tasks, chunksize=4):
                acc.setdefault((L, A), []).append(r)
            pts, chosen = {}, {}
            for L in LS:
                for A in A_GRID:
                    m = {d: float(np.mean([r[d] for r in acc[(L, A)]])) for d in acc[(L, A)][0]}
                    pts[f"{L}/{A}"] = m
                ok = [A for A in A_GRID if max(pts[f"{L}/{A}"][d] for d in RAW) >= 0.90]
                chosen[str(L)] = ok[0] if ok else None
                print(f"phi {phi} L {L}: A = {chosen[str(L)]}", flush=True)
            res["phi"][str(phi)] = {"points": pts, "chosen": chosen}
    out = os.path.join(ROOT, "scripts", "outputs", "calibration_flip.json")
    with open(out, "w", newline="\n") as f:
        json.dump(res, f, indent=1)
    miss = [(p, L) for p, v in res["phi"].items() for L, A in v["chosen"].items() if A is None]
    print("WROTE", out, "| all calibrated" if not miss else f"| NOT REACHED: {miss}")


if __name__ == "__main__":
    main()
