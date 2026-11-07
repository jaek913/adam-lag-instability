"""D.5 dynamic range, planted-cluster and planted-ties probes (Amendment 12.2 E2 gate), hand-derived, through the
REAL code: scripts/a1_events.py (spike rule, chained dedup, inclusive distance) and analysis/pipeline.py +
reference/ref_e2.py (leads, P-CENS left-censoring) with given thresholds.
Per-step cell: grid 1, scan 128, hold 32, dedup 200 (D.2 frozen per-step values).
Usage: python scripts/tests/test_dynamic_range_cluster.py"""
import math
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [os.path.join(ROOT, "analysis"), os.path.join(ROOT, "scripts"), os.path.join(ROOT, "reference")]
import a1_events  # noqa: E402
import e2stat  # noqa: E402
import pipeline  # noqa: E402
import ref_e2  # noqa: E402

CHECKS = []


def ok(n, c):
    CHECKS.append((n, bool(c)))


def main():
    # ---- (a) planted cluster: loss spikes 200-400 steps apart, dedup 200 inclusive ----
    st = np.arange(1, 6001, dtype=np.int64)
    x = 2.5 + 0.01 * np.array([0, 1, 0, -1])[st % 4]
    sp = [2000, 2200, 2500, 2900, 3100]        # gaps 200 (chain, inclusive), 300, 400, 200 (chain)
    for s in sp:
        x[s - 1] += 0.1
    evs, _, _ = a1_events.enumerate_series(st, x, 4.0, 200)
    te = [e["t_e"] for e in evs]
    # by hand: 2000 & 2200 chain (200 <= 200) -> event 2000 (2 spikes); 2500 new; 2900 & 3100 chain -> event 2900
    ok("cluster: events at 2000, 2500, 2900 (inclusive chaining at exactly 200)", te == [2000, 2500, 2900])
    ok("cluster: spike counts 2, 1, 2", [e["n_spikes"] for e in evs] == [2, 1, 2])
    x2 = x.copy()
    x2[2200 - 1] -= 0.1
    x2[2201 - 1] += 0.1                          # 201 apart -> no chain
    te2 = [e["t_e"] for e in a1_events.enumerate_series(st, x2, 4.0, 200)[0]]
    ok("WATCH-FAIL: at 201 apart the spikes do NOT chain", te2 == [2000, 2201, 2500, 2900])

    # ---- (b) left-censoring through both chains (B2, theta given, hold 32, scan 128) ----
    # obs j = step - 1 (block starts at step 1? use first_step 0). y = 0 except unit-height pulses.
    n = 6000
    y = np.zeros(n)
    pulses = [1840, 2410, 2860]
    for p in pulses:
        y[p] = 2.0
    ev = [{"t_e": t, "eligible": True} for t in (1990, 2500, 2950)]
    # event 1990: window [1862, 1990]; alarm from 1840 holds 1840..1871 -> on at 1862 and 1861 -> censored, lead 128
    # event 2500: window [2372, 2500]; pulse 2410 -> onset 2410 -> lead 90, not censored
    # event 2950: window [2822, 2950]; pulse 2860 -> lead 90; alarm 2860..2891, at 2821 off -> not censored
    th = {"D_div": math.inf, "B1": math.inf, "B2": 1.0, "B3": math.inf, "B4": math.inf}
    g = np.exp(y)
    o = pipeline.run([{"first_step": 0, "y": y, "g": g}], ev, grid=1, scan=128, hold=32, resample=False,
                     coverage_stop=None, thetas=th, fa=100000)
    r = ref_e2.run_reference([{"first_step": 0, "g": list(g)}], ev, fa=100000, grid=1, scan=128, hold=32, thetas=th)
    for tag, L, C in (("ours", o["leads"]["B2"], o["flags"]["B2"]["censored"]), ("ref", r["B2"]["leads"], r["B2"]["censored"])):
        ok(f"censoring: leads [128, 90, 90] ({tag})", list(map(float, L)) == [128.0, 90.0, 90.0])
        ok(f"censoring: censored [T, F, F] ({tag})", list(C) == [True, False, False])
    # ---- (c) planted ties for C_min: two baselines with identical alarm streams ----
    la = {"D_div": np.array([10, 0, 30, 5.]), "B1": np.array([20, 0, 10, 5.]), "B2": np.array([20, 0, 10, 5.]),
          "B3": np.array([0, 0, 0, 0.]), "B4": np.array([20, 0, 10, 5.])}
    C, cmin = e2stat.contrasts(la)
    ok("ties: C_B1 = C_B2 = C_B4 = 11.25 - 8.75 = 2.5 (mean D_div - mean tied baseline)", C["B1"] == C["B2"] == C["B4"] == 2.5)
    ok("ties: C_min = 2.5, attained by three tied baselines", cmin == 2.5)
    cm, am = e2stat.resample(la, 400, np.random.default_rng(20261030))
    ok("ties: argmax share split equally between tied winners in each draw (B1 = B2 = B4)",
       abs(am["B1"] - am["B2"]) < 1e-12 and abs(am["B2"] - am["B4"]) < 1e-12)
    for nme, c in CHECKS:
        print(("PASS " if c else "FAIL ") + nme)
    print(f"{sum(c for _, c in CHECKS)}/{len(CHECKS)}", "ALL PASS" if all(c for _, c in CHECKS) else "SOME FAILED")
    sys.exit(0 if all(c for _, c in CHECKS) else 1)


if __name__ == "__main__":
    main()
