"""S-3 measurement (2026-11-06): alternative construction, a step of height h from a uniform offset u in [1, scan]
before each event through t_e; detection rate and mean lead per detector at headline FA. Calibration seeds.
Usage: python scripts/suite/probe_null3050_step.py <phi> <reps> <h1,h2,...>"""
import sys, numpy as np
import os; sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'analysis')); import synth, pipeline
phi=float(sys.argv[1]); reps=int(sys.argv[2]); hs=[float(x) for x in sys.argv[3].split(',')]
for h in hs:
    rates={d:[] for d in pipeline.DET}; leads={d:[] for d in pipeline.DET}
    for r in range(reps):
        rng=synth.child_rng(10_500_000+r)
        b,e=synth.make_series(10_000_000+r, phi=phi, n_events=20)
        y=b[0]["y"].copy()
        for ev in e:
            u=int(rng.integers(1,129)); t=ev["t_e"]; y[t-u:t+1]+=h      # step from t_e-u through t_e
        b=[{"first_step":0,"y":y,"g":np.exp(y)}]
        o=pipeline.run(b,e,grid=1,scan=128,resample=False,coverage_stop=None)
        for d in pipeline.DET: rates[d].append(o["per_detector"][d]["detection_rate"]); leads[d].append(o["per_detector"][d]["mean_lead"])
    print("phi",phi,"step h",h,"rate",{d: round(float(np.mean(v)),2) for d,v in rates.items()},"lead",{d: round(float(np.mean(v)),1) for d,v in leads.items()}, flush=True)
