"""D.5 suite cell table (DESIGN D.5 as amended by Amendments 7 and 8). Writes
scripts/suite/cells.json: one row per cell with its parameters and its SeedSequence child-index range
(Amendment 8.2(14)). Calibration ranges are disjoint from every evaluation range.

Cells marked "pending" depend on construction items not yet decided (verification/suite_findings.md)."""
import json
import os

PHI = [0.5, 0.8, 0.9, 0.95, 0.98]
LS = [64, 100, 150, 200]
AS = [1.0, 2.0, 3.0]
NEV = [5, 10, 20, 40]
REPS = 200
CALIB_BASE = 10_000_000          # calibration child indices start here (disjoint from evaluation)
MEASURE_BASE = 20_000_000        # item-17 measurement indices (disjoint from evaluation and calibration)


def build():
    cells = []

    def add(kind, **kw):
        cells.append({"cell": len(cells), "kind": kind, **kw})

    for phi in PHI:
        for L in LS:
            for A in AS:
                add("planted_effect", phi=phi, n_events=20, L=L, A=A)
    for phi in PHI:
        for ne in NEV:
            add("regime_span", phi=phi, n_events=ne, L=100, A=2.0)
    for phi in PHI:
        add("planted_null", phi=phi, n_events=20)
    for phi in PHI:
        add("surge_null", phi=phi, n_events=20, surge=True)
        add("surge_effect", phi=phi, n_events=20, L=100, A=2.0, surge=True)
    for phi in PHI:
        add("t3_null", phi=phi, n_events=20, innov="t3")
    for phi in PHI:
        add("null_30_50", phi=phi, n_events=20, pulse="calibrated")
    for phi in PHI:
        add("decision_flip", phi=phi, n_events=20, L=8, A=3.0)                 # Amendment 9.3(15)
        add("t3_decision_flip", phi=phi, n_events=20, L=8, A=3.0, innov="t3")
    for phi in PHI:
        add("unequal_memory_null", phi=phi, n_events=20, baselines=["S1", "S40"],
            pending="pass criterion: item 17 / S-2")                               # Amendment 9.3(16)
    for c in cells:
        c["reps"] = REPS
        c["child_first"] = c["cell"] * REPS
    calib = [{"calib": i, "phi": phi, "n_events": 20, "child_first": CALIB_BASE + i * 1000, "reps": 1000}
             for i, phi in enumerate(PHI)]
    return {"cells": cells, "calibration": calib}


if __name__ == "__main__":
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cells.json")
    t = build()
    ev = set()
    for c in t["cells"]:
        r = set(range(c["child_first"], c["child_first"] + c["reps"]))
        assert not (r & ev)
        ev |= r
    for c in t["calibration"]:
        assert not (set(range(c["child_first"], c["child_first"] + c["reps"])) & ev)
    with open(out, "w", newline="\n") as f:
        json.dump(t, f, indent=1)
    print(len(t["cells"]), "cells;", len(t["calibration"]), "calibration ranges; disjoint OK ->", out)
