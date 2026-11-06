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
        if k in G.NULLS:
            row["label"] = "SUPPORT" if r < 5 else "INCONCLUSIVE"        # 5/200 = 0.025
        elif k in G.FLIPS:
            row["label"] = "REFUTE" if r < 196 else "INCONCLUSIVE"       # 0.98
        elif k == "unequal_memory_null":
            row["label"] = "REFUTE"
            row["C"] = {"S1": 0.0, "S40": 0.0 if r < 196 else 3.0}       # invariance 0.98
        else:
            row["label"] = "INCONCLUSIVE"
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

    def flip94(rows):
        for i in range(188, 200):
            rows[i]["label"] = "INCONCLUSIVE"
        return rows
    rc, out = run(table, {flip: flip94})                                  # 188/200 = 0.94
    ok("WATCH-FAIL flip REFUTE 0.94 -> FAIL", rc == 1)

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
