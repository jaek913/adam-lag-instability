"""Synthetic tests for scripts/a1_events.py (DESIGN Amendment 3 suite cases (i)-(iii), k ladder,
eligibility). Builds synthetic route-1 files on the REAL A1 step structure (entry 11) with a
deterministic period-4 pattern (no spurious spikes), plants events, runs the A1 driver, and asserts.

Usage: python scripts/tests/test_a1_events.py <scratch_dir>
"""
import json
import os
import subprocess
import sys

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
SPANS = {"run-001": ("ucv77bvt", 1, 14210, True), "run-008": ("bnzb4pmk", 52301, 73110, True),
         "run-010": ("wqjq7xzw", 73101, 160851, True), "run-013": ("7lr31kjd", 160601, 212965, True),
         "run-016": ("0g0rjkxo", 212001, 337339, True), "run-017": ("d4g44zcc", 337001, 408923, True),
         "run-018": ("50br7dzw", 408924, 504510, False)}
A = 0.01
BIG, MED = 0.1, 0.025           # k=4 thr ~ 0.0284, k=3 thr ~ 0.0213 for the period-4 pattern


def base(s):
    return 2.5 + A * [0.0, 1.0, 0.0, -1.0][s % 4]


def build(scratch, plants):
    os.makedirs(os.path.join(scratch, "A1"), exist_ok=True)
    for seg, (sid, a, b, bk) in SPANS.items():
        steps = ([0] if bk else []) + list(range(a, b + 1))
        loss = []
        for s in steps:
            if s == 0:
                loss.append(None)
                continue
            v = base(s)
            for (pseg, ps, kind) in plants:
                if pseg == seg and ps == s:
                    v = float("nan") if kind == "nan" else v + (BIG if kind == "big" else MED)
            loss.append(v)
        gn = [1.0 if (s % 10 == 0 and s >= a) else None for s in steps]
        pq.write_table(pa.table({"_step": pa.array([float(s) for s in steps]),
                                 "train/CrossEntropyLoss": pa.array(loss, pa.float64()),
                                 "optim/total_grad_norm": gn}),
                       os.path.join(scratch, "A1", f"{seg}_{sid}_history-v0_0000.parquet"))


def run(scratch, tag):
    out = os.path.join(scratch, f"ev_{tag}.json")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "a1_events.py"),
                        os.path.join(ROOT, "scripts", "outputs", "a1_structural_report.json"),
                        os.path.join(ROOT, "scripts", "outputs", "a1_segment_metadata.json"),
                        scratch, out, os.path.join(scratch, f"ev_{tag}.md")], capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit(r.stderr)
    return json.load(open(out))


def ev_at(R, t, series=None):
    return [e for e in R["events"] if e["t_e"] == t and (series is None or e["series"] == series)]


def main():
    scratch = sys.argv[1]
    nan_run = [("run-016", s, "nan") for s in range(300000, 300070)]
    full = [("run-010", 160400, "big"),      # (ii) chain ending at the 160,501 gap; eligible
            ("run-013", 160700, "big"),      # untested: within the first 128 steps after the gap (Amd 3 (2))
            ("run-013", 160800, "big"),      # (ii) after the gap, <= 2,000 from 160,400: separate event; window crosses gap
            ("run-013", 165000, "big"),      # ineligible: minimum history
            ("run-013", 200000, "big"), ("run-016", 250000, "big"),
            ("run-013", 212001, "big"),      # (iii) rewind event at 013's first superseded step
            ("run-016", 220000, "med"), ("run-016", 230000, "med"), ("run-016", 240000, "med")] + nan_run
    checks = []

    def ok(name, cond):
        checks.append((name, bool(cond)))

    build(scratch, full)
    R = run(scratch, "full")
    k4 = R["rungs"]["4.0"]
    c = k4["kept_series_counts"]
    # (i) NaN run: 65 NaN steps tested -> spikes; steps 300,065..300,133 untested by the finite floor
    ok("(i) untested_finite_floor == 69", c["untested_finite_floor"] == 69)
    ok("(i) non-finite spikes == 65", c["nonfinite_spikes"] == 65)
    e = ev_at(k4, 300000, "kept")
    ok("(i) NaN run is one event at 300,000, eligible", len(e) == 1 and e[0]["any_nan"] and e[0]["eligible"])
    # (ii) chain ending at a gap
    ok("(ii) event at 160,400 eligible", len(ev_at(k4, 160400, "kept")) == 1 and ev_at(k4, 160400, "kept")[0]["eligible"])
    ok("first-128 rule: no event at 160,700", len(ev_at(k4, 160700)) == 0)
    e2 = ev_at(k4, 160800, "kept")
    ok("(ii) separate event at 160,800 (not merged across gap)", len(e2) == 1)
    ok("(ii) 160,800 ineligible: window crosses gap", e2 and e2[0]["reason"].startswith("scan"))
    ok("(ii) chains_closed_at_gap >= 1", k4["chains_closed_at_gap"] >= 1)
    # (iii) rewind event at first superseded step
    e3 = ev_at(k4, 212001)
    ok("(iii) exactly one event at 212,001, on rewind:run-013", len(e3) == 1 and e3[0]["series"] == "rewind:run-013")
    ok("(iii) rewind event eligible", e3 and e3[0]["eligible"])
    ok("(iii) no kept event at 212,001", len(ev_at(k4, 212001, "kept")) == 0)
    # eligibility: min history
    e4 = ev_at(k4, 165000, "kept")
    ok("min-history event ineligible", len(e4) == 1 and e4[0]["reason"].startswith("minimum"))
    # k=4 counts: eligible kept 160,400; 200,000; 250,000; 300,000 + rewind 212,001 = 5
    ok("k=4 eligible_total == 5", k4["eligible_total"] == 5)
    ok("k=4 medium spikes absent", all(len(ev_at(k4, t)) == 0 for t in (220000, 230000, 240000)))
    k3 = R["rungs"]["3.0"]
    ok("k=3 eligible_total == 8", k3["eligible_total"] == 8)
    ok("ladder resolves k=4", R["k_ladder_resolution"]["resolved"] == "k=4")
    ok("no stray events (k=4: 6 kept + 1 rewind)", k4["events_kept"] == 6 and k4["rewind_events"] == 1)

    # ladder -> k=3: drop one big eligible spike (250,000)
    build(scratch, [p for p in full if p[1] != 250000])
    R = run(scratch, "k3")
    ok("ladder resolves k=3 when k=4 has 4", R["k_ladder_resolution"] == {"eligible_k4": 4, "eligible_k3": 7, "resolved": "k=3"})
    # ladder -> INSUFFICIENT: only two eligible bigs, no mediums, no NaN run
    build(scratch, [("run-013", 200000, "big"), ("run-016", 250000, "big")])
    R = run(scratch, "ins")
    ok("ladder INSUFFICIENT EVENTS", R["k_ladder_resolution"]["resolved"] == "INSUFFICIENT EVENTS")
    ok("no spurious spikes from the base pattern", R["rungs"]["3.0"]["kept_series_counts"]["spikes"] == 2)

    for n, c_ in checks:
        print(("PASS " if c_ else "FAIL ") + n)
    print("ALL PASS" if all(c_ for _, c_ in checks) else "SOME FAILED")
    sys.exit(0 if all(c_ for _, c_ in checks) else 1)


if __name__ == "__main__":
    main()
