"""Amendment 15.4 positive-control calibration (calibration seeds only). Per phi_y (grid + extension), on the
A1-structure layout: a sustained shift of delta x SD over the final 1,000 steps before t_e plus white measurement
noise sigma_m on y. (delta, sigma_m) = the first pair, in order delta ascending then sigma_m ascending on
{0.5, 1, 2} x {1, 2, 4}, at which D_div's population mean lead (mean over R replicates of the per-replicate mean
lead) exceeds EVERY baseline's by >= 100 steps. Seeds: that phi's calibration range, offsets 900..900+R-1.
Output: scripts/outputs/calibration_posctrl.json. Usage: python scripts/suite/calibrate_posctrl.py --workers 16 [--reps 50]"""
import argparse
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
DELTAS, SIGMAS, MARGIN, OFFSET = [0.5, 1.0, 2.0], [1.0, 2.0, 4.0], 100.0, 900


def one(args):
    import pipeline
    import synth_a1layout
    phi, d, s, idx = args
    b, e, m = synth_a1layout.make_a1(idx, phi_obs=phi, shift=d, sigma_m=s)
    o = pipeline.run(b, e, grid=10, scan=1280, resample=False, coverage_stop=None)
    return (phi, d, s), {k: o["per_detector"][k]["mean_lead"] for k in o["per_detector"]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    ap.add_argument("--reps", type=int, default=50)
    a = ap.parse_args()
    calib = json.load(open(os.path.join(ROOT, "scripts", "suite", "cells.json")))["calibration"]
    pairs = [(d, s) for d in DELTAS for s in SIGMAS]
    res = {"grid": pairs, "margin_steps": MARGIN, "reps": a.reps, "offset": OFFSET, "phi": {}}
    with Pool(a.workers) as pool:
        for c in calib:
            phi = c["phi"]
            tasks = [(phi, d, s, c["child_first"] + OFFSET + r) for d, s in pairs for r in range(a.reps)]
            acc = {}
            for key, ml in pool.imap_unordered(one, tasks, chunksize=2):
                acc.setdefault(key, []).append(ml)
            pts, chosen = {}, None
            for d, s in pairs:
                m = {k: float(np.mean([x[k] for x in acc[(phi, d, s)]])) for k in acc[(phi, d, s)][0]}
                adv = m["D_div"] - max(v for k, v in m.items() if k != "D_div")
                pts[f"{d}/{s}"] = {"mean_lead": m, "ddiv_advantage": adv}
                if chosen is None and adv >= MARGIN:
                    chosen = {"shift": d, "sigma_m": s}
            res["phi"][str(phi)] = {"points": pts, "chosen": chosen}
            print(f"phi {phi}: chosen {chosen}; advantages " +
                  ", ".join(f"{k} {v['ddiv_advantage']:.0f}" for k, v in pts.items()), flush=True)
    with open(os.path.join(ROOT, "scripts", "outputs", "calibration_posctrl.json"), "w", newline="\n") as f:
        json.dump(res, f, indent=1)
    none = [p for p, v in res["phi"].items() if v["chosen"] is None]
    print("WROTE scripts/outputs/calibration_posctrl.json |",
          "all calibrated" if not none else f"NO CONSTRUCTION FOUND in which D_div leads at phi {none} (reported per 15.4)")


if __name__ == "__main__":
    main()
