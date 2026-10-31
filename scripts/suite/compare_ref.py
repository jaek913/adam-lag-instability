"""Amendment 8.1 oracle check: analysis/ (pipeline) vs reference/ (independent implementation) on the
same series. Usage: python scripts/suite/compare_ref.py <cell> <first_rep> <n_reps>
The reference runs with its own FROZEN constants (as amended through Amendment 9; D-03/D-04 closed)."""
import json
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
sys.path.insert(0, os.path.join(ROOT, "reference"))
import pipeline  # noqa: E402
import synth  # noqa: E402
import ref_e2  # noqa: E402

TOL = 1e-6


def rel_eq(a, b):
    if a is None or b is None:
        return a is b
    if math.isinf(a) or math.isinf(b):
        return a == b
    return abs(a - b) <= TOL * max(1.0, abs(a), abs(b))


def compare(blocks, events, grid, scan):
    a = pipeline.run(blocks, events, grid=grid, scan=scan, resample=False, coverage_stop=None)
    rb = [{"first_step": b["first_step"], "g": list(b["g"])} for b in blocks]
    r = ref_e2.run_reference(rb, events, fa=1.0, grid=grid, scan=scan, hold=32)
    diffs = []
    if a["N_out"] != r["N_out"] or a["nstar"] != r["nstar"]:
        diffs.append(("N_out/nstar", (a["N_out"], a["nstar"]), (r["N_out"], r["nstar"])))
        return diffs
    elig = [e for e in events if e["eligible"]]
    lt_onsets = {}
    for d in pipeline.DET:
        ad, rd = a["detectors"][d], r[d]
        if not rel_eq(ad["theta"], rd["theta"]):
            diffs.append((d + " theta", ad["theta"], rd["theta"]))
        if ad["realised"] != rd["realised"]:
            diffs.append((d + " realised", ad["realised"], rd["realised"]))
        al = a["leads"][d]
        if list(map(float, al)) != list(map(float, rd["leads"])):
            k = [i for i in range(len(al)) if float(al[i]) != float(rd["leads"][i])]
            diffs.append((d + " leads", [al[i] for i in k[:5]], [rd["leads"][i] for i in k[:5]]))
    if not rel_eq(a["C_min"], r["C_min"]) or np.sign(a["C_min"]) != np.sign(r["C_min"]):
        diffs.append(("C_min", a["C_min"], r["C_min"]))
    return diffs


def main():
    cell, first, n = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])
    table = json.load(open(os.path.join(ROOT, "scripts", "suite", "cells.json")))
    c = table["cells"][cell]
    bad = 0
    for rep in range(first, first + n):
        kw = dict(phi=c["phi"], n_events=c["n_events"], L=c.get("L"), A=c.get("A", 0.0),
                  innov=c.get("innov", "gauss"), surge_on=c.get("surge", False))
        blocks, events = synth.make_series(c["child_first"] + rep, **kw)
        d = compare(blocks, events, 1, 128)
        print("cell", cell, "rep", rep, "IDENTICAL" if not d else "DIFF " + repr(d)[:600], flush=True)
        bad += bool(d)
    print("ALL IDENTICAL" if not bad else f"{bad} of {n} replicates differ")


if __name__ == "__main__":
    main()
