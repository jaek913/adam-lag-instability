"""Hand-computed probes for analysis/e2stat.py (leads, censoring, contrast, label). Watch-to-fail included.
Usage: python scripts/tests/test_e2stat.py
"""
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
import e2stat as E  # noqa: E402

CHECKS = []


def ok(n, c):
    CHECKS.append((n, bool(c)))


def blk(first, n, on):
    a = np.zeros(n, bool)
    for i in on:
        a[i] = True
    return [(first, a)]


def main():
    G, S = 10, 1280                                    # A1: grid 10, scan 1,280 steps (129 obs)
    # block from step 0, 1,000 obs (steps 0..9,990)
    # event at t_e = 5,007 -> t_e^g = 5,000; window = steps 3,720..5,000
    b = blk(0, 1000, [])
    ok("miss -> lead 0, not detected", E.lead(b, 5007, G, S) == (0, False, False, False))
    b = blk(0, 1000, [495])                            # alarm at step 4,950
    ok("alarm at 4,950 -> lead 50 (t_e^g - step)", E.lead(b, 5007, G, S) == (50, False, True, False))
    b = blk(0, 1000, [500])                            # alarm at t_e^g itself
    ok("alarm first at t_e^g -> lead 0, concurrent, NOT detected (Amendment 7 item 6)", E.lead(b, 5007, G, S) == (0, False, False, True))
    ok("WATCH-FAIL: the superseded rule (lead 0 counted as detected) is rejected", E.lead(b, 5007, G, S)[2] is not True)
    b = blk(0, 1000, [499, 500])                       # alarm at 4,990 and t_e^g
    ok("alarm at t_e^g - 10 -> lead 10, detected, not concurrent", E.lead(b, 5007, G, S) == (10, False, True, False))
    b = blk(0, 1000, [372, 380])                       # alarm at window start 3,720 only
    ok("alarm at window start, not before -> lead 1,280 uncensored", E.lead(b, 5007, G, S) == (1280, False, True, False))
    b = blk(0, 1000, range(371, 373))                  # alarm at 3,710 and 3,720
    ok("alarm at 3,710 and 3,720 -> censored, lead 1,280", E.lead(b, 5007, G, S) == (1280, True, True, False))
    b = blk(0, 1000, [371])                            # alarm only before the window
    ok("alarm only before window -> miss", E.lead(b, 5007, G, S) == (0, False, False, False))
    t_e_anchored = 5007 - 4950                         # what anchoring on t_e instead of t_e^g would give
    ok("WATCH-FAIL: t_e anchoring (57) differs from the t_e^g lead (50)",
       t_e_anchored == 57 and E.lead(blk(0, 1000, [495]), 5007, G, S)[0] == 50)
    # per-step run: grid 1, scan 128
    ok("per-step: alarm at t_e-10 -> lead 10", E.lead(blk(0, 500, [290]), 300, 1, 128) == (10, False, True, False))
    ok("per-step: censored at 128", E.lead(blk(0, 500, [171, 172]), 300, 1, 128) == (128, True, True, False))

    # contrast by hand: 4 events
    la = {"D_div": np.array([100, 50, 0, 30.]), "B1": np.array([20, 50, 0, 10.]), "B2": np.array([0, 0, 0, 0.]),
          "B3": np.array([90, 60, 0, 30.]), "B4": np.array([100, 50, 0, 40.])}
    C, cmin = E.contrasts(la)
    ok("C_b by hand: B1 25, B2 45, B3 0, B4 -2.5", C == {"B1": 25.0, "B2": 45.0, "B3": 0.0, "B4": -2.5})
    ok("C_min = -2.5 (B4 is the best baseline)", cmin == -2.5)
    ok("label REFUTE when C_min <= 0", E.label(cmin, np.array([1.0]))[0] == "REFUTE")
    ok("label REFUTE at exactly 0", E.label(0.0, np.array([1.0]))[0] == "REFUTE")
    ok("SUPPORT when p05 > 0", E.label(3.0, np.linspace(1, 5, 101))[0] == "SUPPORT")
    ok("INCONCLUSIVE when p05 <= 0", E.label(3.0, np.linspace(-1, 5, 101))[0] == "INCONCLUSIVE")
    # resample: identical detectors -> C_min == 0 in every resample
    same = {d: np.array([10, 20, 30, 40.]) for d in E.DETECTORS}
    cm, am = E.resample(same, 200, np.random.default_rng(20261030))
    ok("resample: identical detectors give C_min 0 in every draw", np.all(cm == 0))
    ok("resample: argmax shares tie equally (0.2 each)", all(abs(v - 0.2) < 1e-12 for v in am.values()))
    cm2, _ = E.resample(la, 500, np.random.default_rng(20261030))
    # per-resample C_min is the min over b of resampled C_b, so it can never exceed any resampled C_b;
    # its mean over draws is therefore <= the mean over draws of each single C_b (checked directly)
    rng = np.random.default_rng(7)
    idxs = [rng.integers(0, 4, size=4) for _ in range(300)]
    per = [E.contrasts(la, i) for i in idxs]
    ok("resample: C_min <= every C_b within each draw", all(cm_ <= min(c_.values()) + 1e-12 for c_, cm_ in per))
    ok("WATCH-FAIL: max-over-b would exceed min-over-b in some draw",
       any(max(c_.values()) > cm_ for c_, cm_ in per))
    rng1, rng2 = np.random.default_rng(20261030), np.random.default_rng(20261030)
    ok("resample reproducible under default_rng(20261030)", np.array_equal(E.resample(la, 50, rng1)[0], E.resample(la, 50, rng2)[0]))

    for n, c in CHECKS:
        print(("PASS " if c else "FAIL ") + n)
    print("ALL PASS" if all(c for _, c in CHECKS) else "SOME FAILED")
    sys.exit(0 if all(c for _, c in CHECKS) else 1)


if __name__ == "__main__":
    main()
