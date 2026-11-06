"""S-3 measurement (2026-11-06): one-observation pulse of height h at a uniform offset in [1, scan] before each event
(Amendment 8.2(13)); detection rate per detector at headline FA. Calibration seed range 10,000,000+ (cells.json).
Usage: python scripts/suite/probe_null3050_pulse.py <phi> <reps> <h1,h2,...>"""
import sys, numpy as np
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'analysis')); import synth, pipeline
phi=float(sys.argv[1]); reps=int(sys.argv[2]); hs=[float(x) for x in sys.argv[3].split(',')]
for h in hs:
    rates={d:[] for d in pipeline.DET}
    for r in range(reps):
        b,e=synth.make_series(10_000_000+r, phi=phi, n_events=20, pulse_h=h)
        o=pipeline.run(b,e,grid=1,scan=128,resample=False,coverage_stop=None)
        for d in pipeline.DET: rates[d].append(o["per_detector"][d]["detection_rate"])
    print("phi",phi,"h",h, {d: round(float(np.mean(v)),3) for d,v in rates.items()}, flush=True)
