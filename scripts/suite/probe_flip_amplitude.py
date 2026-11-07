"""S-4 measurement (2026-11-06): decision-flip ramp amplitude. L = 8 observations, A in a list, 20 events,
headline FA, full E2 chain with resampling and label. Seeds: child indices 40,000,000+ (never used by any
evaluation, calibration or measurement run). Usage: python scripts/suite/probe_flip_amplitude.py <phi> <reps> <A1,A2,..> [innov] [L]"""
import os
import sys

import numpy as np

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "analysis"))
import pipeline  # noqa: E402
import synth  # noqa: E402

phi, reps, As = float(sys.argv[1]), int(sys.argv[2]), [float(x) for x in sys.argv[3].split(",")]
innov = sys.argv[4] if len(sys.argv) > 4 else "gauss"
L = int(sys.argv[5]) if len(sys.argv) > 5 else 8
for A in As:
    labs, dr = [], {d: [] for d in pipeline.DET}
    for r in range(reps):
        b, e = synth.make_series(40_000_000 + r, phi=phi, n_events=20, L=L, A=A, innov=innov)
        o = pipeline.run(b, e, grid=1, scan=128, coverage_stop=None)
        labs.append(o["label"])
        for d in pipeline.DET:
            dr[d].append(o["per_detector"][d]["detection_rate"])
    print(f"phi {phi} {innov} L={L} A={A}: REFUTE {labs.count('REFUTE') / reps:.3f} INCONCL {labs.count('INCONCLUSIVE') / reps:.3f} "
          f"SUPPORT {labs.count('SUPPORT') / reps:.3f} | det rate " +
          ", ".join(f"{d} {np.mean(v):.2f}" for d, v in dr.items()), flush=True)
