"""Dry run of scripts/run_e2.py on a SYNTHETIC store with A1's real step structure (test_a1_loader SPANS):
g = exp(AR(1) noise) on every grid step, seeds = synth.child_rng(45,000,000 + segment number) (seed map).
Checks: the run completes and writes a result; label is one of the D.3 labels; 57 eligible events; phi_hat_y
is reported with a cell; the one-run guard halts a second invocation; a one-byte corruption halts PRV; a --real
run with an overridden --sources halts. No A1 value is read.
Usage: python scripts/tests/test_run_e2_dryrun.py <scratch_dir>"""
import hashlib
import json
import os
import subprocess
import sys

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [os.path.join(ROOT, "analysis"), os.path.join(ROOT, "scripts", "tests")]
import synth  # noqa: E402
from test_a1_loader import SPANS, SEGNUM  # noqa: E402

RUN = os.path.join(ROOT, "scripts", "run_e2.py")
CHECKS = []


def ok(n, c):
    CHECKS.append((n, bool(c)))


def call(*a):
    r = subprocess.run([sys.executable, RUN, *a], capture_output=True, text=True)
    return r.returncode, r.stdout + r.stderr


def main():
    scratch = sys.argv[1]
    store = os.path.join(scratch, "store")
    os.makedirs(os.path.join(store, "A1"), exist_ok=True)
    rows = []
    for seg, (sid, a, b, bk) in SPANS.items():
        steps = ([0] if bk else []) + list(range(a, b + 1))
        rng = synth.child_rng(45_000_000 + SEGNUM[seg])
        e = rng.standard_normal(len(steps))
        y = np.empty(len(steps))
        y[0] = e[0]
        for i in range(1, len(steps)):
            y[i] = 0.9 * y[i - 1] + e[i]
        g = [float(np.exp(0.1 * v)) if (s % 10 == 0 and s >= a) else None for s, v in zip(steps, y)]
        rel = f"A1/{seg}_{sid}_history-v0_0000.parquet"
        p = os.path.join(store, *rel.split("/"))
        pq.write_table(pa.table({"_step": pa.array([float(s) for s in steps]), "optim/total_grad_norm": g}), p)
        rows.append((rel, hashlib.sha256(open(p, "rb").read()).hexdigest()))
    src = os.path.join(scratch, "SOURCES_synth.md")
    with open(src, "w", encoding="utf-8") as f:
        f.write("| file | note | sha256 |\n|---|---|---|\n")
        for rel, h in rows:
            f.write(f"| `{rel}` | synthetic | {h} |\n")
    out = os.path.join(scratch, "e2out")
    rc, txt = call("--dry-run", store, "--out", out, "--sources", src)
    res_p = os.path.join(out, "e2_result.json")
    ok("dry run exits 0 and writes e2_result.json", rc == 0 and os.path.exists(res_p))
    if os.path.exists(res_p):
        r = json.load(open(res_p))
        ok("mode recorded as DRY-RUN", r["mode"] == "DRY-RUN")
        ok("57 eligible of 61 events", r["n_eligible"] == 57 and r["n_events"] == 61)
        lab = r["headline"]["label"]
        ok("headline label is a D.3 label or a pre-registered stop", lab in ("SUPPORT", "INCONCLUSIVE", "REFUTE")
           or lab.startswith("STOP-AND-REPORT") or lab.startswith("UNRUN"))
        ok("phi_hat_y in (-1, 1) with a grid cell", -1 < r["phi_hat_y"] < 1 and r["selected_cell_phi"] in
           (0.5, 0.8, 0.9, 0.95, 0.98))
        ok("FA grid has 0.5, 2 and 5", sorted(r["fa_grid"]) == ["0.5", "2.0", "5.0"])
    rc2, txt2 = call("--dry-run", store, "--out", out, "--sources", src)
    ok("second invocation halts (one real run)", rc2 != 0 and "already run" in txt2)
    victim = os.path.join(store, *rows[0][0].split("/"))
    data = bytearray(open(victim, "rb").read())
    data[len(data) // 2] ^= 0xFF
    open(victim, "wb").write(bytes(data))
    rc3, txt3 = call("--dry-run", store, "--out", os.path.join(scratch, "e2out_corrupt"), "--sources", src)
    ok("one flipped byte halts at PRV", rc3 != 0 and "PRV hash check failed" in txt3)
    rc4, txt4 = call("--real", store, "--out", os.path.join(scratch, "e2out_real"), "--sources", src)
    ok("--real halts at the first guard (date window, sign-off, or sources override)", rc4 != 0 and "HALT" in txt4
       and not os.path.exists(os.path.join(scratch, "e2out_real")))
    import datetime
    if not datetime.date(2026, 11, 14) <= datetime.date.today() <= datetime.date(2026, 12, 3):
        ok("--real outside 2026-11-14..2026-12-03 halts on the date guard", "a real run is allowed only" in txt4)
    rc5, txt5 = call("--real", store, "--out", os.path.join(scratch, "e2out_real2"), "--signoff-entry", "1")
    ok("--real never reaches PRV or the store without a valid sign-off", rc5 != 0 and "PRV" not in txt5
       and not os.path.exists(os.path.join(scratch, "e2out_real2")))
    for n, c in CHECKS:
        print(("PASS " if c else "FAIL ") + n)
    print("ALL PASS" if all(c for _, c in CHECKS) else "FAILED")
    sys.exit(0 if all(c for _, c in CHECKS) else 1)


if __name__ == "__main__":
    main()
