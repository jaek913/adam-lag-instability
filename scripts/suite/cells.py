"""D.5 suite cell table (DESIGN D.5 as amended by Amendments 7 and 8). Writes
scripts/suite/cells.json: one row per cell with its parameters and its SeedSequence child-index range
(Amendment 8.2(14)). Calibration ranges are disjoint from every evaluation range.

Cells marked "pending" depend on construction items not yet decided (verification/suite_findings.md)."""
import json
import os

PHI = [0.5, 0.8, 0.9, 0.95, 0.98]
EXT_PHI = [0.3, 0.99]                     # Amendment 15.5 extension cells
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
        add("null_30_50", phi=phi, n_events=20, pulse="calibrated",
            superseded="Amendment 10.2: replaced by the null_pulse_sweep cells")
    for phi in PHI:
        add("decision_flip", phi=phi, n_events=20, L=8, A=3.0)                 # Amendment 9.3(15)
        add("t3_decision_flip", phi=phi, n_events=20, L=8, A=3.0, innov="t3")
    for phi in PHI:
        add("unequal_memory_null", phi=phi, n_events=20, baselines=["S1", "S40"])  # Amendment 9.3(16); criterion 10.1
    # ---- appended 2026-11-06 (Amendment 10); earlier indices and seed ranges unchanged ----
    for phi in PHI:
        for d in ["D_div", "B1", "B2", "B3", "B4"]:
            add("null_pulse_sweep", phi=phi, n_events=20, pulse_for=d,
                pulse_h="from scripts/outputs/calibration_pulse.json [phi][detector]")   # Amendment 10.2
    for phi in PHI:
        for h in [1.5, 2.0, 2.5]:
            add("step_characterization", phi=phi, n_events=20, step_h=h, report_only=True)  # Amendment 10.3
    # ---- appended 2026-11-06 (Amendment 11): A1's realised event count ----
    for phi in PHI:
        add("realised_count_null", phi=phi, n_events=57)
        add("realised_count_flip", phi=phi, n_events=57, L=8, A=3.0)
        add("realised_count_effect", phi=phi, n_events=57, L=100, A=2.0)
    # ---- appended 2026-11-06 (Amendment 12.1): decision flip re-graded on fresh seeds; long-ramp flips reported ----
    for c in list(cells):
        if c["kind"] in ("decision_flip", "t3_decision_flip", "realised_count_flip") and "superseded" not in c:
            c["superseded"] = "Amendment 12.1: v1 record of the failed REFUTE >= 0.95 bar; re-graded on fresh seeds"
            fresh = {k: v for k, v in c.items() if k not in ("cell", "superseded")}
            add(c["kind"], **{k: v for k, v in fresh.items() if k != "kind"}, fresh_of=c["cell"])
    for phi in PHI:
        for L in (16, 24):
            add("flip_long", phi=phi, n_events=20, L=L, A="from scripts/outputs/calibration_flip.json [phi][L]",
                report_only=True)
    # ---- appended 2026-11-06 (Amendment 12.2 E2 gate): ten-step grid cell (A1.7) and end-to-end loss cell (7.8);
    #      construction provisional (suite_findings items 19a-19f) ----
    for phi in PHI:
        add("grid10_null", phi=phi, grid=10)
        for L in (640, 1000, 1500, 2000):
            add("grid10_effect", phi=phi, grid=10, L=L, A=2.0, report_only=True)
        add("grid10_short", phi=phi, grid=10, L=200, A=2.0, report_only=True)
    for phi in PHI:
        add("e2e_null", phi=phi, grid=1)
        add("e2e_effect", phi=phi, grid=1, L=100, A=2.0, report_only=True)
    # ---- appended 2026-11-07 (Amendment 13): short ramp re-graded on fresh seeds; A1-structure cells ----
    for c in list(cells):
        if c["kind"] == "grid10_short" and "superseded" not in c:
            c["superseded"] = "Amendment 13.2: measured before the bar; re-graded on fresh seeds"
            add("grid10_short", **{k: v for k, v in c.items() if k not in ("cell", "kind", "superseded", "report_only")},
                fresh_of=c["cell"])
    for phi in PHI:
        add("a1s_null", phi=phi)
        add("a1s_flip", phi=phi, L=80, A=3.0)
        add("a1s_effect", phi=phi, L=1000, A=2.0, report_only=True)
    # ---- appended 2026-11-07 (Amendment 14.3): graded dynamic range ----
    for phi in PHI:
        for L in (25, 75, 125):
            add("dr_step", phi=phi, n_events=20, L=L, A=6.0)
        for L in (25, 75, 125):
            add("dr_grid10", phi=phi, grid=10, L=10 * L, A=6.0, L_obs=L)
    # ---- appended 2026-11-08 (Amendment 15): 15.7 instrument check (fresh seeds), 15.4 positive control,
    #      15.5 extension cells phi in {0.3, 0.99} ----
    for c in list(cells):
        if c["kind"] in ("dr_step", "dr_grid10") and "superseded" not in c:
            c["superseded"] = "Amendment 15.7: 14.3 grading replaced; re-graded as an instrument check on fresh seeds"
    for phi in PHI:
        for L in (25, 75, 125):
            add("dr2_step", phi=phi, n_events=20, L=L, A=6.0)
        for L in (25, 75, 125):
            add("dr2_grid10", phi=phi, grid=10, L=10 * L, A=6.0, L_obs=L)
    for phi in PHI + EXT_PHI:
        add("pos_ctrl", phi=phi, shift="from scripts/outputs/calibration_posctrl.json", report_only=True)  # 15.4
    for phi in EXT_PHI:                                                                                 # 15.5
        add("a1s_null", phi=phi, extension=True)
        add("a1s_flip", phi=phi, L=80, A=3.0, extension=True)
        add("a1s_effect", phi=phi, L=1000, A=2.0, report_only=True, extension=True)
    for c in cells:
        c["reps"] = REPS
        c["child_first"] = c["cell"] * REPS
    calib = [{"calib": i, "phi": phi, "n_events": 20, "child_first": CALIB_BASE + i * 1000, "reps": 1000}
             for i, phi in enumerate(PHI + EXT_PHI)]       # EXT_PHI ranges appended 2026-11-08 (Amendment 15.5)
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
