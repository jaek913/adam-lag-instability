"""Watch-to-fail for scripts/suite/grade_suite.py on fabricated outputs: an all-passing set grades ALL PASS;
each single violation (null false-SUPPORT 0.06, flip REFUTE 0.94, unequal-memory invariance 0.94 or median 1.5,
a missing replicate) grades FAIL. Usage: python scripts/tests/test_grade_suite.py"""
import json
import os
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GRADER = os.path.join(ROOT, "scripts", "suite", "grade_suite.py")
sys.path.insert(0, os.path.join(ROOT, "scripts", "suite"))
import grade_suite as G  # noqa: E402

CHECKS = []
DET = ["D_div", "B1", "B2", "B3", "B4"]


def ok(n, c):
    CHECKS.append((n, bool(c)))


def rows_for(c, mutate=None):
    out = []
    for r in range(c["reps"]):
        k = c["kind"]
        row = {"cell": c["cell"], "rep": r, "per_detector": {d: {"mean_lead": 1.0} for d in DET}}
        if k in G.DR:                                  # separated leads, full detection
            lo = c.get("L_obs", c.get("L"))
            row["per_detector"] = {d: {"mean_lead": float(lo + (r % 10)), "detection_rate": 1.0} for d in DET}
        if k in G.NULLS:
            row["label"] = "SUPPORT" if r < 5 else "INCONCLUSIVE"        # 5/200 = 0.025
        elif k in G.FLIPS:
            row["label"] = "SUPPORT" if r < 5 else ("REFUTE" if r < 170 else "INCONCLUSIVE")   # SUPPORT 0.025
        elif k == "unequal_memory_null":
            row["label"] = "REFUTE"
            row["C"] = {"S1": 0.0, "S40": 0.0 if r < 196 else 3.0}       # invariance 0.98
        else:
            row["label"] = "INCONCLUSIVE"
        if k in G.E2E:
            row["events_match"] = True
            row["residues"] = list(range(10))
        if k in G.A1S:
            row.update(eligibility_match=True, n_eligible=57, ineligible_by_block=[2, 1, 1],
                       predicted_ineligible_by_block=[2, 1, 1])
        out.append(row)
    return mutate(out) if mutate else out


def run(table, muts):
    d = tempfile.mkdtemp()
    for c in table:
        rows = rows_for(c, muts.get(c["cell"]))
        with open(os.path.join(d, f"cell_{c['cell']:03d}.jsonl"), "w") as f:
            f.write("".join(json.dumps(x) + "\n" for x in rows))
    p = subprocess.run([sys.executable, GRADER, "--dir", d, "--out", os.path.join(d, "v.md"), "--skip-licence"],
                       capture_output=True, text=True)
    return p.returncode, p.stdout.strip()


def main():
    table = [c for c in json.load(open(os.path.join(ROOT, "scripts", "suite", "cells.json")))["cells"]
             if "superseded" not in c and "pending" not in c]
    null = next(c["cell"] for c in table if c["kind"] == "planted_null")
    flip = next(c["cell"] for c in table if c["kind"] == "decision_flip")
    um = next(c["cell"] for c in table if c["kind"] == "unequal_memory_null")
    rc, out = run(table, {})
    ok("fabricated all-passing set -> ALL PASS", rc == 0 and out == "ALL PASS")

    def sup(rows, n=12):
        for i in range(n):
            rows[i]["label"] = "SUPPORT"
        return rows
    rc, out = run(table, {null: lambda r: sup(r, 12)})                   # 12/200 = 0.06
    ok("WATCH-FAIL null false-SUPPORT 0.06 -> FAIL", rc == 1 and out.startswith("FAIL"))

    rc, out = run(table, {flip: lambda r: sup(r, 11)})                    # SUPPORT 11/200 = 0.055
    ok("WATCH-FAIL flip SUPPORT 0.055 -> FAIL (Amendment 12.1)", rc == 1)
    def norefute(rows):
        for r_ in rows[5:]:
            r_["label"] = "INCONCLUSIVE"
        return rows
    rc, out = run(table, {flip: norefute})                                 # REFUTE 0, SUPPORT 0.025
    ok("flip with REFUTE 0 but SUPPORT 0.025 passes (REFUTE is reported, not binding)", rc == 0)

    def inv94(rows):
        for i in range(188, 200):
            rows[i]["C"]["S40"] = 3.0
        return rows
    rc, out = run(table, {um: inv94})
    ok("WATCH-FAIL unequal-memory invariance 0.94 -> FAIL", rc == 1)

    def med15(rows):
        for r in rows:
            r["C"]["S1"] = 1.5
            r["C"]["S40"] = 1.5
        return rows
    rc, out = run(table, {um: med15})
    ok("WATCH-FAIL unequal-memory |median C_b| 1.5 -> FAIL", rc == 1)
    g10 = next(c["cell"] for c in table if c["kind"] == "grid10_null")
    def badmatch(rows):
        rows[7]["events_match"] = False
        return rows
    rc, out = run(table, {g10: badmatch})
    ok("WATCH-FAIL grid-10 cell with one replicate's events not recovered -> FAIL", rc == 1)
    def badres(rows):
        rows[3]["residues"] = list(range(9))
        return rows
    rc, out = run(table, {g10: badres})
    ok("WATCH-FAIL grid-10 cell missing a t_e mod 10 residue -> FAIL", rc == 1)
    a1n = next(c["cell"] for c in table if c["kind"] == "a1s_null")
    def badel(rows):
        rows[9]["ineligible_by_block"] = [2, 2, 0]
        return rows
    rc, out = run(table, {a1n: badel})
    ok("WATCH-FAIL A1-structure cell with ineligible events in the wrong blocks -> FAIL", rc == 1)
    drc = [c for c in table if c["kind"] == "dr2_step" and c["phi"] == 0.9]
    mid = next(c["cell"] for c in drc if c["L"] == 75)
    def overlap(rows):
        for r_ in rows:
            for d in DET:
                r_["per_detector"][d]["mean_lead"] = 25.0 + (r_["rep"] % 10)   # same as L=25 -> overlap
        return rows
    rc, out = run(table, {mid: overlap})
    ok("WATCH-FAIL dynamic range: a qualifying baseline overlapping at L=25 vs 75 -> FAIL", rc == 1)
    def ddiv_weak(rows):
        for r_ in rows:
            r_["per_detector"]["D_div"]["detection_rate"] = 0.5
            r_["per_detector"]["D_div"]["mean_lead"] = 25.0 + (r_["rep"] % 10)
        return rows
    rc, out = run(table, {mid: ddiv_weak})
    ok("15.7: D_div weak/overlapping does NOT fail the instrument check (reported only)", rc == 0)
    def base_only_div(rows):
        for r_ in rows:
            for d in ("B1", "B2", "B3", "B4"):
                r_["per_detector"][d]["detection_rate"] = 0.1
        return rows
    rc, out = run(table, {mid: base_only_div})
    ok("WATCH-FAIL dynamic range: no baseline at >= 80% -> FAIL (no vacuous pass)", rc == 1)
    rc, out = run(table, {null: lambda r: r[:-1]})
    ok("WATCH-FAIL a missing replicate -> FAIL (INCOMPLETE)", rc == 1)
    rc, out = run(table, {null: lambda r: sup(r, 10)})                   # exactly 0.05 -> passes
    ok("boundary: false-SUPPORT exactly 0.05 passes", rc == 0)
    p = subprocess.run([sys.executable, GRADER, "--dir", tempfile.mkdtemp(), "--out", os.path.join(tempfile.mkdtemp(), "v.md")],
                       capture_output=True, text=True)
    ok("licence check runs against the agreement commit (empty dir -> FAIL on completeness, not a crash)",
       p.returncode == 1 and "Traceback" not in p.stderr)
    for n, c in CHECKS:
        print(("PASS " if c else "FAIL ") + n)
    print("ALL PASS" if all(c for _, c in CHECKS) else "SOME FAILED")
    sys.exit(0 if all(c for _, c in CHECKS) else 1)


if __name__ == "__main__":
    main()
