"""Grade the D.5 statistical cells (DESIGN D.5 as amended through Amendment 10) from scripts/outputs/suite_v1/.
Writes verification/suite_verdict.md and prints ALL PASS / FAIL. Usage:
  python scripts/suite/grade_suite.py [--dir DIR] [--out FILE] [--agreement-commit aad6cf7]
Checks:
  completeness: every graded cell has exactly the replicates 0..reps-1;
  agreement licence (Amendment 8.1, DECISIONS 22): analysis/{ops,pipeline,e2stat}.py and reference/ref_e2.py
    are byte-identical to the commit the reference-agreement v2 run certified, and
    scripts/outputs/ref_agreement_v2/ holds complete, all-identical agreement for every E2-chain cell graded;
  per cell kind:
    planted_null, surge_null, t3_null, null_pulse_sweep, realised_count_null: false-SUPPORT <= 0.05;
    decision_flip, t3_decision_flip, realised_count_flip (fresh seeds, Amendment 12.1): SUPPORT <= 0.05;
      REFUTE reported as the kill rule's power against short precursors;
    unequal_memory_null (10.1): false-SUPPORT <= 0.05, |median C_b| <= 1 for S1, S40,
      share(|C_S1 - C_S40| <= 1) >= 0.95;
    planted_effect, regime_span, surge_effect, realised_count_effect, step_characterization: reported (power);
    grid10_* and e2e_* (A1.7, 7.8): nulls false-SUPPORT <= 0.05, others reported; in every replicate the spike
      rule must recover exactly the planted events, and grid-10 cells must contain all ten residues of t_e mod 10;
    grid10_short (fresh seeds, Amendment 13.2): SUPPORT <= 0.05, REFUTE reported;
    a1s_* (Amendment 13.3): null false-SUPPORT <= 0.05; flip SUPPORT <= 0.05; effect reported; in every replicate
      the A1 eligibility rule reproduces the design (4 ineligible, 2/1/1 by block, 57 eligible)."""
import argparse
import hashlib
import json
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NULLS = {"planted_null", "surge_null", "t3_null", "null_pulse_sweep", "realised_count_null", "grid10_null", "e2e_null",
         "a1s_null"}
FLIPS = {"decision_flip", "t3_decision_flip", "realised_count_flip", "grid10_short", "a1s_flip"}
REPORT = {"planted_effect", "regime_span", "surge_effect", "realised_count_effect", "step_characterization", "flip_long",
          "grid10_effect", "e2e_effect", "a1s_effect"}
E2E = {"grid10_null", "grid10_effect", "grid10_short", "e2e_null", "e2e_effect", "a1s_null", "a1s_flip", "a1s_effect"}
A1S = {"a1s_null", "a1s_flip", "a1s_effect"}
LICENSED = ["analysis/ops.py", "analysis/pipeline.py", "analysis/e2stat.py", "reference/ref_e2.py"]


def grade(rows, kind):
    labels = [r["label"] for r in rows]
    n = len(rows)
    rate = {k: labels.count(k) / n for k in ("SUPPORT", "INCONCLUSIVE", "REFUTE")}
    if kind in NULLS:
        return rate["SUPPORT"] <= 0.05, f"false-SUPPORT {rate['SUPPORT']:.3f} (<= 0.05)", rate
    if kind in FLIPS:                                  # Amendment 12.1: SUPPORT binding; REFUTE = reported power
        return rate["SUPPORT"] <= 0.05, (f"SUPPORT {rate['SUPPORT']:.3f} (<= 0.05); reported: REFUTE {rate['REFUTE']:.3f} "
                                         f"(kill-rule power vs short precursor)"), rate
    if kind == "unequal_memory_null":
        c1 = np.array([r["C"]["S1"] for r in rows])
        c40 = np.array([r["C"]["S40"] for r in rows])
        med = max(abs(np.median(c1)), abs(np.median(c40)))
        inv = float(np.mean(np.abs(c1 - c40) <= 1))
        ok = bool(rate["SUPPORT"] <= 0.05 and med <= 1 and inv >= 0.95)   # plain bool: np.bool_ is never `is False`
        cond = {b: float(np.mean(c[c != 0] > 0)) if np.any(c != 0) else float("nan") for b, c in (("S1", c1), ("S40", c40))}
        return ok, (f"false-SUPPORT {rate['SUPPORT']:.3f} (<= 0.05); max|median C_b| {med:.2f} (<= 1); "
                    f"share |C_S1-C_S40|<=1 {inv:.3f} (>= 0.95); reported: false-REFUTE {rate['REFUTE']:.3f}, "
                    f"P(C_b>0|C_b!=0) S1 {cond['S1']:.3f} S40 {cond['S40']:.3f}"), rate
    return None, "reported", rate


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dir", default=os.path.join(ROOT, "scripts", "outputs", "suite_v1"))
    ap.add_argument("--out", default=os.path.join(ROOT, "verification", "suite_verdict.md"))
    ap.add_argument("--agreement-commit", default="aad6cf7")
    ap.add_argument("--skip-licence", action="store_true", help="test use only")
    a = ap.parse_args()
    table = json.load(open(os.path.join(ROOT, "scripts", "suite", "cells.json")))["cells"]
    lines, fails = [], []
    if not a.skip_licence:
        for f in LICENSED:
            cur = hashlib.md5(open(os.path.join(ROOT, f), "rb").read()).hexdigest()
            old = subprocess.run(["git", "-C", ROOT, "show", f"{a.agreement_commit}:{f}"], capture_output=True).stdout
            ok = hashlib.md5(old).hexdigest() == cur and len(old) > 0
            lines.append(f"| licence | {f} | {'unchanged since ' + a.agreement_commit if ok else 'CHANGED - agreement must be re-run'} | {'PASS' if ok else 'FAIL'} |")
            if not ok:
                fails.append(f)
    graded = [c for c in table if c["kind"] in NULLS | FLIPS | REPORT | {"unequal_memory_null"}
              and "superseded" not in c and "pending" not in c]
    if not a.skip_licence:                              # Amendment 8.1: agreement for every E2-chain cell graded
        ag_dir = os.path.join(ROOT, "scripts", "outputs", "ref_agreement_v2")
        missing = []
        for c in graded:
            if c["kind"] == "unequal_memory_null":
                continue
            p = os.path.join(ag_dir, f"cell_{c['cell']:03d}.jsonl")
            rr = [json.loads(l) for l in open(p)] if os.path.exists(p) else []
            if sorted(r["rep"] for r in rr) != list(range(c["reps"])) or not all(r["identical"] for r in rr):
                missing.append(c["cell"])
        lines.append(f"| agreement | reference agreement (8.1) on {sum(c['kind'] != 'unequal_memory_null' for c in graded)} E2-chain cells | "
                     f"{'complete and all identical' if not missing else 'MISSING or DIFFERENT: ' + str(missing[:20])} | {'PASS' if not missing else 'FAIL'} |")
        fails += [f"agreement {m}" for m in missing]
    for c in graded:
        p = os.path.join(a.dir, f"cell_{c['cell']:03d}.jsonl")
        rows = [json.loads(l) for l in open(p)] if os.path.exists(p) else []
        reps = sorted(r["rep"] for r in rows)
        complete = reps == list(range(c["reps"]))
        if not complete:
            lines.append(f"| {c['cell']} | {c['kind']} phi={c['phi']} | INCOMPLETE ({len(rows)} rows) | FAIL |")
            fails.append(c["cell"])
            continue
        ok, text, rate = grade(rows, c["kind"])
        ok = None if ok is None else bool(ok)
        if c["kind"] in E2E:                           # the spike rule must recover exactly the planted events
            em = all(r.get("events_match") is True for r in rows)
            res = (all(r.get("residues") == list(range(10)) for r in rows)
                   if (c.get("grid") == 10 or c["kind"] in A1S) else True)
            text += f"; events recovered exactly in {sum(r.get('events_match') is True for r in rows)}/{len(rows)}"
            if c.get("grid") == 10 or c["kind"] in A1S:
                text += "; all ten residues of t_e mod 10 in every replicate" if res else "; RESIDUES MISSING"
            el = True
            if c["kind"] in A1S:                       # Amendment 13.3 eligibility check
                el = all(r.get("eligibility_match") is True and r.get("n_eligible") == 57
                         and r.get("ineligible_by_block") == r.get("predicted_ineligible_by_block") == [2, 1, 1]
                         for r in rows)
                text += ("; eligibility rule reproduces the design (4 ineligible, 2/1/1 by block; 57 eligible) in every replicate"
                         if el else "; ELIGIBILITY MISMATCH")
            if not (em and res and el):
                ok = False
        tag = "PASS" if ok else ("FAIL" if ok is False else "REPORTED")
        extra = ""
        if c["kind"] in REPORT:
            ml = {d: np.mean([r["per_detector"][d]["mean_lead"] for r in rows]) for d in rows[0]["per_detector"]}
            extra = " | mean lead " + ", ".join(f"{d} {v:.1f}" for d, v in ml.items())
        desc = ", ".join(f"{k}={c[k]}" for k in ("phi", "n_events", "L", "A", "innov", "pulse_for", "step_h") if k in c)
        lines.append(f"| {c['cell']} | {c['kind']} ({desc}) | {text}; SUPPORT/INCONCL/REFUTE "
                     f"{rate['SUPPORT']:.3f}/{rate['INCONCLUSIVE']:.3f}/{rate['REFUTE']:.3f}{extra} | {tag} |")
        if ok is False:
            fails.append(c["cell"])
    verdict = "ALL PASS" if not fails else f"FAIL ({len(fails)}: {fails[:20]})"
    with open(a.out, "w", newline="\n", encoding="utf-8") as f:
        f.write("# D.5 suite verdict — statistical cells\n\n")
        f.write(f"Graded from `{os.path.relpath(a.dir, ROOT).replace(os.sep, '/')}` by `scripts/suite/grade_suite.py`.\n\n**{verdict}**\n\n")
        f.write("| cell | kind | result | verdict |\n|---|---|---|---|\n" + "\n".join(lines) + "\n")
    print(verdict)
    sys.exit(0 if not fails else 1)


if __name__ == "__main__":
    main()
