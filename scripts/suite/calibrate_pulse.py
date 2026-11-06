"""Amendment 10.2 calibration sweep (calibration seeds only). For each phi_y, a one-observation pulse of
height h at a uniform offset in [1, scan] before each of 20 events; detection rate per detector at headline
FA, averaged over R replicates (child indices = that phi's calibration range in cells.json, first R).
Grid {1,...,120}; per detector, h_{phi,d} = the calibrated h whose rate for d is closest to 0.40 within
[0.30, 0.50]; where no grid point is in band, the bracketing interval is bisected (<= 8 steps) on the same seeds.
Output: scripts/outputs/calibration_pulse.json (every evaluated point + the chosen h per phi x detector).
Usage: python scripts/suite/calibrate_pulse.py --workers 16 [--reps 100]"""
import argparse
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
GRID = [1, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10, 15, 20, 30, 40, 50, 60, 80, 100, 120]
DET = ["D_div", "B1", "B2", "B3", "B4"]
LO, HI, TARGET = 0.30, 0.50, 0.40


def one(args):
    import pipeline
    import synth
    phi, h, idx = args
    b, e = synth.make_series(idx, phi=phi, n_events=20, pulse_h=h)
    o = pipeline.run(b, e, grid=1, scan=128, resample=False, coverage_stop=None)
    return phi, h, idx, {d: o["per_detector"][d]["detection_rate"] for d in DET}


def rates(pool, phi, hs, idxs):
    out = {h: {d: [] for d in DET} for h in hs}
    for _, h, _, r in pool.imap_unordered(one, [(phi, h, i) for h in hs for i in idxs], chunksize=4):
        for d in DET:
            out[h][d].append(r[d])
    return {h: {d: float(np.mean(v)) for d, v in out[h].items()} for h in hs}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--reps", type=int, default=100)
    a = ap.parse_args()
    calib = json.load(open(os.path.join(ROOT, "scripts", "suite", "cells.json")))["calibration"]
    result = {"grid": GRID, "reps": a.reps, "band": [LO, HI], "target": TARGET, "phi": {}}
    with Pool(a.workers) as pool:
        for c in calib:
            phi = c["phi"]
            idxs = list(range(c["child_first"], c["child_first"] + a.reps))
            pts = rates(pool, phi, GRID, idxs)
            print(f"phi {phi}: grid done", flush=True)
            chosen = {}
            for d in DET:
                inb = [h for h in sorted(pts) if LO <= pts[h][d] <= HI]
                it = 0
                while not inb and it < 8:
                    lo = max([h for h in pts if pts[h][d] < LO], default=None)
                    hi = min([h for h in pts if pts[h][d] > HI and (lo is None or h > lo)], default=None)
                    if lo is None or hi is None:
                        break
                    mid = round((lo + hi) / 2.0, 6)
                    pts.update(rates(pool, phi, [mid], idxs))
                    inb = [h for h in sorted(pts) if LO <= pts[h][d] <= HI]
                    it += 1
                chosen[d] = (min(inb, key=lambda h: (abs(pts[h][d] - TARGET), h)) if inb else None)
                print(f"phi {phi} {d}: h = {chosen[d]} (rate {pts[chosen[d]][d] if inb else 'not reached'})", flush=True)
            result["phi"][str(phi)] = {"calib_child_first": c["child_first"],
                                       "points": {str(h): pts[h] for h in sorted(pts)}, "chosen": chosen}
    out = os.path.join(ROOT, "scripts", "outputs", "calibration_pulse.json")
    with open(out, "w", newline="\n") as f:
        json.dump(result, f, indent=1)
    miss = [(p, d) for p, v in result["phi"].items() for d, h in v["chosen"].items() if h is None]
    print("WROTE", out, "| every detector calibrated into band" if not miss else f"| NOT REACHED: {miss}")


if __name__ == "__main__":
    main()
