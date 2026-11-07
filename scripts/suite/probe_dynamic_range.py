"""Dynamic-range measurement (D.5 "lead distributions separate at planted L differences of 50 steps").
Per-step cells, 20 events, headline FA, ramps L in a list at amplitude A; per detector: detection rate,
median and mean of per-replicate mean lead. Seeds: child indices 43,000,000+ (never used elsewhere).
Usage: python scripts/suite/probe_dynamic_range.py <phi> <reps> <A> <L1,L2,...>"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "analysis"))
import pipeline  # noqa: E402
import synth  # noqa: E402

phi, reps, A, Ls = float(sys.argv[1]), int(sys.argv[2]), float(sys.argv[3]), [int(x) for x in sys.argv[4].split(",")]
for L in Ls:
    ml = {d: [] for d in pipeline.DET}
    dr = {d: [] for d in pipeline.DET}
    for r in range(reps):
        b, e = synth.make_series(43_000_000 + r, phi=phi, n_events=20, L=L, A=A)
        o = pipeline.run(b, e, grid=1, scan=128, resample=False, coverage_stop=None)
        for d in pipeline.DET:
            ml[d].append(o["per_detector"][d]["mean_lead"])
            dr[d].append(o["per_detector"][d]["detection_rate"])
    print(f"phi {phi} A {A} L {L}: " + "; ".join(f"{d} det {np.mean(dr[d]):.2f} meanlead {np.mean(ml[d]):.1f} "
                                                f"[{np.percentile(ml[d], 10):.1f},{np.percentile(ml[d], 90):.1f}]"
                                                for d in pipeline.DET), flush=True)
