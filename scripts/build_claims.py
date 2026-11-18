"""Build claims.lock (Phase 3, Research-to-Publication Standard). claims.lock is NEVER hand-edited: change this
builder or verification/cic_signoff.json and rebuild.

One row per load-bearing number. Each row wires the value to: the committed output it is read from (path + SHA-256),
the JSON pointer inside it, the generating script (path + SHA-256), the input-data group (SOURCES.md rows, SHA-256),
the expected value and its tolerance, the re-execution mode verify.py uses, and the 7-point CIC sign-off for the
generating script (from verification/cic_signoff.json; unsigned until signed there).

Re-execution modes (read by scripts/verify.py):
  rerun     - the script is re-run to a scratch folder and the same pointer is compared.
  rerun_long- as rerun, but only under verify.py --full (hours; run on JAE's machine).
  reproduce - E2 rows. run_e2.py is NEVER re-invoked (one real run, DECISIONS 47). The value is compared with the
              independent recomputation E4 V0 (analysis/outputs/post/e4/V0.json, same pipeline, DECISIONS 53-54),
              and C_b / C_min / mean and median leads are re-derived from the per-event leads in e2_result.json.
  regrade   - the D.5 suite grader is re-run over the committed suite outputs (the suite itself is not re-run).
  static    - value fixed by a §K rule applied to another ledger row (no script of its own).
Usage: python scripts/build_claims.py [--out claims.lock]"""
import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
from prv_hash_check import listed  # noqa: E402

DETS = ["D_div", "B1", "B2", "B3", "B4"]
BASES = ["B1", "B2", "B3", "B4"]
E2 = "scripts/outputs/e2/e2_result.json"
A1E = "scripts/outputs/a1_events.json"
XD = "analysis/outputs/post/x_diag.json"
E1 = "analysis/outputs/post/e1_result.json"
E5 = "analysis/outputs/post/e5_result.json"
E4D = "analysis/outputs/post/e4"
SUITE = "verification/suite_verdict.md"
K_RULE = {"REFUTE": "STOP"}          # DESIGN §K: REFUTE stops the project. Other labels never reached; refuse them.
E4_VARIANTS = ["V0", "W16_64", "W64_256", "W4_16", "B1_25", "B1_100", "B3_adj", "B4_2s", "B4_g"]

SCRIPTS = {
    "e2": "scripts/run_e2.py", "a1": "scripts/a1_events.py", "x": "analysis/post/x_diag.py",
    "e1": "analysis/post/e1.py", "e5": "analysis/post/e5.py", "e4": "analysis/post/e4.py",
    "suite": "scripts/suite/grade_suite.py",
}
REEXEC = {"e2": "reproduce", "a1": "rerun", "x": "rerun", "e1": "rerun", "e5": "rerun", "e4": "rerun_long",
          "suite": "regrade"}


def sha256(rel):
    return hashlib.sha256(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()


def md5(rel):
    return hashlib.md5(open(os.path.join(ROOT, rel), "rb").read()).hexdigest()


def load(rel):
    return json.load(open(os.path.join(ROOT, rel)))


def get(obj, ptr):
    for k in ptr:
        obj = obj[k]
    return obj


def norm(v):
    if isinstance(v, str) and v.lower() in ("inf", "infinity"):
        return "inf"
    if isinstance(v, float) and math.isinf(v):
        return "inf"
    return v


def kind_tol(v):
    if isinstance(v, bool) or isinstance(v, str) or v is None:
        return type(v).__name__, 0
    if isinstance(v, int):
        return "int", 0
    if isinstance(v, float):
        return "float", 1e-12
    if isinstance(v, list):
        return "list", 1e-12
    raise TypeError(v)


def suite_summary():
    txt = open(os.path.join(ROOT, SUITE), encoding="utf-8").read()
    verdict = "ALL PASS" if "**ALL PASS**" in txt else "NOT ALL PASS"
    return {"verdict": verdict, "cells_pass": len(re.findall(r"\| PASS \|$", txt, re.M)),
            "cells_fail": len(re.findall(r"\| FAIL \|$", txt, re.M))}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "claims.lock"))
    a = ap.parse_args()
    sign = load("verification/cic_signoff.json")["scripts"] if os.path.exists(
        os.path.join(ROOT, "verification/cic_signoff.json")) else {}

    rows = []

    def add(rid, lb, sk, out, ptr, value=None, exploratory=False, note=None):
        v = norm(get(load(out), ptr) if value is None else value)
        k, tol = kind_tol(v)
        cic = sign.get(SCRIPTS[sk]) if sk in SCRIPTS else None
        rows.append({"id": rid, "lb_id": lb, "exploratory": exploratory, "value": v, "kind": k, "tol_abs": tol,
                     "output": {"path": out, "sha256": sha256(out)}, "pointer": ptr,
                     "script": ({"path": SCRIPTS[sk], "sha256": sha256(SCRIPTS[sk])} if sk in SCRIPTS else None),
                     "inputs": "A1", "reexec": REEXEC.get(sk, "static"),
                     "cic": cic["flags"] if cic else {str(i): None for i in range(1, 8)},
                     "cic_signed": cic.get("signed") if cic else None, "note": note})

    # --- A1 event stage (entry 13)
    r4 = ["rungs", "4.0"]
    add("LB-A1-nevents-k4", "LB-A1-nevents-k4", "a1", A1E, ["k_ladder_resolution", "eligible_k4"])
    add("LB-A1-nevents-k3", "LB-A1-nevents-k3", "a1", A1E, ["k_ladder_resolution", "eligible_k3"])
    add("LB-A1-rung", "LB-A1-rung", "a1", A1E, ["k_ladder_resolution", "resolved"])
    add("LB-A1-events-kept", "LB-A1-nevents-k4", "a1", A1E, r4 + ["events_kept"])
    add("LB-A1-ineligible.min_history", "LB-A1-ineligible", "a1", A1E, r4 + ["ineligible_min_history"])
    add("LB-A1-ineligible.crosses_gap", "LB-A1-ineligible", "a1", A1E, r4 + ["ineligible_window_crosses_gap"])
    add("LB-A1-rewind", "LB-A1-rewind", "a1", A1E, r4 + ["rewind_events"])

    # --- E2 (entry 47)
    h = ["headline"]
    add("LB-E2-verdict", "LB-E2-verdict", "e2", E2, h + ["label"])
    add("LB-E2-Cmin", "LB-E2-Cmin", "e2", E2, h + ["C_min"])
    for b in BASES:
        add(f"LB-E2-Cb.{b}", "LB-E2-Cb", "e2", E2, h + ["C", b])
    for d in DETS:
        add(f"LB-E2-lead-det.{d}.mean", "LB-E2-lead-det", "e2", E2, h + ["per_detector", d, "mean_lead"])
        add(f"LB-E2-lead-det.{d}.median", "LB-E2-lead-det", "e2", E2, h + ["per_detector", d, "median_lead"])
        for f in ("detection_rate", "misses", "censored", "concurrent"):
            add(f"LB-E2-miss-det.{d}.{f}", "LB-E2-miss-det", "e2", E2, h + ["per_detector", d, f])
        for f in ("matchable", "realised", "coverage", "theta"):
            add(f"LB-E2-nstar.{d}.{f}", "LB-E2-nstar", "e2", E2, h + ["detectors", d, f])
        add(f"LB-E2-argmax.{d}", "LB-E2-argmax", "e2", E2, h + ["argmax", d])
    add("LB-E2-nstar", "LB-E2-nstar", "e2", E2, h + ["nstar"])
    add("LB-E2-nstar.N_out", "LB-E2-nstar", "e2", E2, h + ["N_out"])
    add("LB-E2-nstar.n_eligible", "LB-E2-nstar", "e2", E2, h + ["n_eligible"])
    add("LB-E2-nstar.n_events", "LB-E2-nstar", "e2", E2, ["n_events"])
    add("LB-suite-cell.phi_hat_y", "LB-suite-cell", "e2", E2, ["phi_hat_y"])
    add("LB-suite-cell.selected_phi", "LB-suite-cell", "e2", E2, ["selected_cell_phi"])
    lab = get(load(E2), h + ["label"])
    if lab not in K_RULE:
        sys.exit(f"HALT: E2 label {lab!r} has no §K mapping in this builder")
    add("LB-K-verdict", "LB-K-verdict", "static", E2, h + ["label"], value=K_RULE[lab],
        note="§K: REFUTE -> STOP; applied to LB-E2-verdict")

    # --- D.5 suite (e7abad6)
    s = suite_summary()
    for k in ("verdict", "cells_pass", "cells_fail"):
        add(f"LB-suite-null.{k}", "LB-suite-null", "suite", SUITE, [k], value=s[k])

    # --- E1 (entry 51)
    p = ["primary"]
    add("LB-E1-label", "LB-E1-label", "e1", E1, p + ["label"])
    add("LB-E1-predsign", "LB-E1-predsign", "e1", E1, p + ["predicted_sign"])
    add("LB-E1-predsign.criterion", "LB-E1-predsign", "e1", E1, p + ["criterion"])
    add("LB-E1-rho", "LB-E1-rho", "e1", E1, p + ["rho"])
    add("LB-E1-rho.n_pairs", "LB-E1-rho", "e1", E1, p + ["n_pairs"])
    add("LB-E1-p", "LB-E1-p", "e1", E1, p + ["p_one_sided_predicted"])
    add("LB-E1-label.sensitivity", "LB-E1-label", "e1", E1, ["sensitivity_rng_7_4", "label"])

    # --- E5 (entry 52)
    add("LB-E5-aor-real.rate", "LB-E5-aor-real", "e5", E5, p + ["real_rate"])
    add("LB-E5-aor-real.mean_lead", "LB-E5-aor-real", "e5", E5, p + ["real_mean_lead"])
    add("LB-E5-aor-real.n_alarm_steps", "LB-E5-aor-real", "e5", E5, p + ["n_alarm_steps"])
    add("LB-E5-aor-shifted.rate_median", "LB-E5-aor-shifted", "e5", E5, p + ["shift_rate_median"])
    add("LB-E5-aor-shifted.rate_p05_p95", "LB-E5-aor-shifted", "e5", E5, p + ["shift_rate_p05_p95"])
    add("LB-E5-aor-shifted.block_shuffle_matchable", "LB-E5-aor-shifted", "e5", E5,
        ["block_shuffle", "D_div_matchable"])
    add("LB-E5-flag", "LB-E5-flag", "e5", E5, p + ["flag_tripped"])

    # --- E4 (entry 54): sensitivity, never rescue
    for v in E4_VARIANTS:
        out = f"{E4D}/{v}.json"
        add(f"LB-E4-variants.{v}.C_min", "LB-E4-variants", "e4", out, ["C_min"])
        add(f"LB-E4-variants.{v}.D_div_matchable", "LB-E4-variants", "e4", out, ["detectors", "D_div", "matchable"])
    dv = f"{E4D}/derived.json"
    add("LB-E4-variants.P_CENS_lead0.C_min", "LB-E4-variants", "e4", dv, ["P_CENS_lead0", "C_min"])
    add("LB-E4-variants.P_CENS_excluded.C_min", "LB-E4-variants", "e4", dv, ["P_CENS_excluded", "C_min"])
    add("LB-E4-variants.rewind_excluded.n", "LB-E4-variants", "e4", dv, ["rewind_excluded", "n_rewind_events"])
    add("LB-E4-variants.event_block3.C_min", "LB-E4-variants", "e4", dv, ["event_block3_resampling", "C_min_point"])
    add("LB-E4-variants.event_block3.p05_p95", "LB-E4-variants", "e4", dv,
        ["event_block3_resampling", "C_min_p05_p95"])

    # --- X1-X3 (entry 49): EXPLORATORY
    x = dict(exploratory=True)
    for f in ("event_rise_median", "control_rise_median", "event_share_gt2", "control_share_gt2",
              "mannwhitney_p_one_sided", "n_events", "n_control", "n_tiles_excluded_clearance"):
        add(f"LB-X1-precursor.{f}", "LB-X1-precursor", "x", XD, ["X1", f], **x)
    for sub in ("whole", "block_1", "block_2", "longest_first_half", "longest_second_half"):
        for f in ("onsets_at_top", "nstar_headline", "unmatchable"):
            add(f"LB-X2-matchability.{sub}.{f}", "LB-X2-matchability", "x", XD, ["X2", sub, f], **x)
    add("LB-X2-matchability.whole.rate_per_10k", "LB-X2-matchability", "x", XD, ["X2", "whole", "rate_per_10k"], **x)
    for f in ("added_grid_obs_if_route3", "nstar_full_approx", "unmatchable_at_full_nstar"):
        add(f"LB-X2-matchability.projection.{f}", "LB-X2-matchability", "x", XD, ["X2", "projection", f], **x)
    for blk in ("block_0", "block_1", "block_2"):
        for f in ("eligible_events", "events_per_10k_obs", "median_rise"):
            add(f"LB-X3-events.{blk}.{f}", "LB-X3-events", "x", XD, ["X3", blk, f], **x)

    ids = [r["id"] for r in rows]
    if len(ids) != len(set(ids)):
        sys.exit("HALT: duplicate row id")
    inputs = {"A1": {"sources_md_sha256": sha256("SOURCES.md"),
                     "files": [{"path": p_, "sha256": s_} for p_, s_ in listed(os.path.join(ROOT, "SOURCES.md"))
                               if p_.startswith("A1/")]}}
    not_landed = {
        "LB-E2-Cmin-p05": "N/A - REFUTE: p05 not computed (Amendment 7.5)",
        "LB-E2-power": "N/A - INCONCLUSIVE branch not reached",
        "LB-E3-verdict": "NOT RUN - §K stop; A2-A6 not staged (DECISIONS 48)",
        "LB-E3-nruns": "NOT RUN - as LB-E3-verdict",
        "LB-A-included": "NOT RUN - A2-A6 not staged (DECISIONS 48)",
        "LB-E6-table": "DROPPED - Leg B (OUTLINE v0.6)", "LB-E6-spearman": "DROPPED - Leg B",
        "LB-E7-tau": "DROPPED - Leg B", "LB-B-noisecell": "DROPPED - Leg B", "LB-B-replicates": "DROPPED - Leg B",
        "LB-E8-Cmin": "DROPPED - Leg B", "LB-E8-Nout": "DROPPED - Leg B",
    }
    head = subprocess.run(["git", "-C", ROOT, "rev-parse", "HEAD"], capture_output=True, text=True).stdout.strip()
    lock = {"schema": "claims.lock v1", "builder": {"path": "scripts/build_claims.py",
                                                    "sha256": sha256("scripts/build_claims.py")},
            "built_at_head": head, "theorem_rows": [],
            "theorem_note": "No original theorem is relied on (Phase 3 theorem box N/A; see verification/no_original_theorem.md).",
            "inputs": inputs, "not_landed": not_landed, "rows": rows}
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(lock, f, indent=1, sort_keys=False)
        f.write("\n")
    print(f"claims.lock: {len(rows)} rows, {len(set(r['lb_id'] for r in rows))} LB-ids, "
          f"{len(inputs['A1']['files'])} A1 input files; md5 {md5(os.path.relpath(a.out, ROOT))}")


if __name__ == "__main__":
    main()
