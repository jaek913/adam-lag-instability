"""D.5 assembly probes (DESIGN D.5 "Assembly probes"; Amendment 12.2 E2 gate), run through the REAL A1 scripts:
scripts/a1_d1_check.py (D.1 completeness, as a subprocess), analysis/a1_loader.py (A1.1 dropped observations)
and scripts/a1_events.py (gaps). Expected outcomes are taken from the frozen text:
  D.1 / A1.1: rows contiguous first..last, no duplicate steps, loss every step, optim/total_grad_norm present by
  NAME and required on grid steps only; a missing step inside a segment fails D.1;
  A1.1 G6: a grid step present with null, non-positive or non-finite g is a DROPPED observation - counted, carried
  forward, not a gap and not a D.1 failure;
  D.2 / A1.1 G4: a gap resets state; the loss spike baseline restarts at every gap.
The rewind (overlap with a superseded tail containing a spike) and P-SEG ownership probes are in
scripts/tests/test_a1_events.py (Amendment 3 case iii) and test_a1_loader.py and are re-run by the gate.
Usage: python scripts/tests/test_assembly_probes.py <scratch_dir>"""
import json
import os
import subprocess
import sys

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [os.path.join(ROOT, "analysis"), os.path.join(ROOT, "scripts")]
import a1_events  # noqa: E402
import a1_loader  # noqa: E402

D1 = os.path.join(ROOT, "scripts", "a1_d1_check.py")
LOSS, GN = "train/CrossEntropyLoss", "optim/total_grad_norm"
CHECKS = []


def ok(n, c):
    CHECKS.append((n, bool(c)))


def write(path, steps, loss=None, gn=None, drop_gn_col=False, step_float=False):
    n = len(steps)
    loss = [2.5] * n if loss is None else loss
    gn = [(1.0 if s % 10 == 0 else None) for s in steps] if gn is None else gn
    cols = {"_step": pa.array([float(s) for s in steps] if step_float else steps,
                              pa.float64() if step_float else pa.int64()),
            LOSS: pa.array(loss, pa.float64())}
    if not drop_gn_col:
        cols[GN] = pa.array(gn, pa.float64())
    pq.write_table(pa.table(cols), path)


def d1(path, scratch, label):
    out = os.path.join(scratch, label + ".json")
    md5 = subprocess.run([sys.executable, "-c", f"import hashlib;print(hashlib.md5(open(r'{path}','rb').read()).hexdigest())"],
                         capture_output=True, text=True).stdout.strip()
    r = subprocess.run([sys.executable, D1, path, label, "0", md5, out], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr)
    return json.load(open(out))


def main():
    sc = sys.argv[1]
    os.makedirs(sc, exist_ok=True)
    S = list(range(1, 3001))
    # 1. clean segment -> D.1 PASS
    p = os.path.join(sc, "clean.parquet"); write(p, S); r = d1(p, sc, "clean")
    ok("clean contiguous segment: D.1 PASS", r["D1_pass"] and r["duplicate_steps"] == 0)
    # 2. duplicate step -> D.1 FAIL
    p = os.path.join(sc, "dup.parquet"); write(p, S[:500] + [500] + S[500:]); r = d1(p, sc, "dup")
    ok("duplicate step: D.1 FAIL, duplicate_steps = 1", (not r["D1_pass"]) and r["duplicate_steps"] == 1)
    # 3. missing grad-norm column -> D.1 FAIL by name
    p = os.path.join(sc, "nogn.parquet"); write(p, S, drop_gn_col=True); r = d1(p, sc, "nogn")
    ok("missing optim/total_grad_norm column: D.1 FAIL (required column missing by name)",
       (not r["D1_pass"]) and r["required_present"][GN] is False)
    # 3b. column present under another name only -> still FAIL (resolution by NAME, D.6 item 1)
    p = os.path.join(sc, "renamed.parquet")
    pq.write_table(pa.table({"_step": pa.array(S, pa.int64()), LOSS: pa.array([2.5] * len(S)),
                             "optim/grad_norm": pa.array([1.0] * len(S))}), p)
    r = d1(p, sc, "renamed")
    ok("grad norm under a different column name: D.1 FAIL (by NAME, never position)", not r["D1_pass"])
    # 4. point-sampled (incomplete) segment: every 100th step -> D.1 FAIL
    P = list(range(100, 30001, 100))
    p = os.path.join(sc, "sampled.parquet"); write(p, P); r = d1(p, sc, "sampled")
    ok("point-sampled segment (every 100th step): D.1 FAIL, many blocks", (not r["D1_pass"]) and r["n_contiguous_blocks"] > 1)
    # 5. missing step inside a segment -> D.1 FAIL (A1.1)
    p = os.path.join(sc, "hole.parquet"); write(p, S[:1000] + S[1001:]); r = d1(p, sc, "hole")
    ok("missing step inside a segment: D.1 FAIL", not r["D1_pass"])
    # 6. null grad norm at a grid step -> D.1 PASS (grid-only requirement is a dropped obs, A1.1 G6), counted
    g = [(1.0 if s % 10 == 0 else None) for s in S]; g[S.index(1500)] = None
    p = os.path.join(sc, "nullgn.parquet"); write(p, S, gn=g); r = d1(p, sc, "nullgn")
    ok("null g at one grid step: D.1 PASS and counted (grid_steps_missing_gn = 1)",
       r["D1_pass"] and r["grid_steps_missing_gn_count"] == 1)
    # 7. loss missing on one step (not bookkeeping) -> D.1 FAIL (loss every step)
    L_ = [2.5] * len(S); L_[S.index(2000)] = None
    p = os.path.join(sc, "noloss.parquet"); write(p, S, loss=L_); r = d1(p, sc, "noloss")
    ok("loss missing on one step: D.1 FAIL", not r["D1_pass"])
    # 8. float _step (as W&B stores it) -> integral check passes
    p = os.path.join(sc, "floatstep.parquet"); write(p, S, step_float=True); r = d1(p, sc, "floatstep")
    ok("float64 _step with integral values: D.1 PASS", r["D1_pass"] and r["non_integral_steps"] == 0)

    # 9. loader: dropped observations (null, NaN, inf, 0, negative) carried forward, counted, not a gap
    os.makedirs(os.path.join(sc, "store", "A1"), exist_ok=True)
    steps = list(range(1, 20001))
    gvals = {s: float(np.exp(s / 1e4)) for s in steps if s % 10 == 0}
    bad = {5000: None, 5010: float("nan"), 5020: float("inf"), 5030: 0.0, 5040: -1.0}
    gcol = [(bad[s] if s in bad else gvals.get(s)) for s in steps]
    pq.write_table(pa.table({"_step": pa.array(steps, pa.int64()), LOSS: pa.array([2.5] * len(steps)),
                             GN: pa.array(gcol, pa.float64())}), os.path.join(sc, "store", "A1", "run-001_x_history-v0_0000.parquet"))
    rep = {"segments": [{"seg": "run-001", "id": "x"}], "owner_intervals": [{"owner": "run-001", "range": [1, 20000]}],
           "kept_blocks": [{"range": [1, 20000]}]}
    rp = os.path.join(sc, "rep.json"); json.dump(rep, open(rp, "w"))
    blocks, _, lrep = a1_loader.load_blocks(rp, os.path.join(sc, "store"))
    y = blocks[0]["y"]; i0 = 5000 // 10 - 1                      # obs index of step 5000 (first grid step 10)
    ok("loader: one block (dropped obs are not a gap)", len(blocks) == 1 and blocks[0]["first_step"] == 10)
    ok("loader: 5 dropped observations counted", lrep[0]["dropped_total"] == 5)
    ok("loader: null/NaN/inf/0/negative all carried forward from step 4,990",
       all(y[i0 + k] == y[i0 - 1] for k in range(5)) and y[i0 + 5] == np.log(gvals[5050]))
    ok("WATCH-FAIL: a carried value differs from the raw (dropped) value it replaces", np.isfinite(y[i0 + 2]))

    # 10. gaps: spike baseline restarts at a gap (loss series, D.2); events never chain across a gap
    st = np.array(list(range(1, 5001)) + list(range(5101, 10001)), np.int64)
    x = 2.5 + 0.01 * np.array([0, 1, 0, -1])[st % 4]
    x[np.searchsorted(st, 4999)] += 0.1                           # spike just before the gap
    x[np.searchsorted(st, 5101 + 50)] += 0.1                      # within 128 steps after the gap: untested
    x[np.searchsorted(st, 5101 + 300)] += 0.1                     # tested; within dedup 2,000 of 4,999 but across the gap
    evs, cnt, bl = a1_events.enumerate_series(st, x, 4.0, 2000)
    ok("gap: two blocks", len(bl) == 2)
    ok("gap: spike within 128 steps after the gap is untested (baseline restarts)", 5151 not in [e["t_e"] for e in evs])
    ok("gap: spike after the gap opens a new event, not chained to 4,999", sorted(e["t_e"] for e in evs) == [4999, 5401])

    for n, c in CHECKS:
        print(("PASS " if c else "FAIL ") + n)
    print(f"{sum(c for _, c in CHECKS)}/{len(CHECKS)}", "ALL PASS" if all(c for _, c in CHECKS) else "SOME FAILED")
    sys.exit(0 if all(c for _, c in CHECKS) else 1)


if __name__ == "__main__":
    main()
