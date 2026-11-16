"""E4 operator gate: two-sided B4 fast == loop (scores, onsets, alarm) on random series and thresholds; one-sided
reduction check; B3-adjusted equals ops.score_b3 when no z exceeds 2.5 and differs when one does; B4-on-g equals
b4_z(exp(y)). Usage: python scripts/tests/test_e4_ops.py"""
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [os.path.join(ROOT, "analysis"), os.path.join(ROOT, "analysis", "post")]
import e4_ops  # noqa: E402
import ops  # noqa: E402

C = []


def ok(n, c):
    C.append((n, bool(c)))


rng = np.random.default_rng(11)
allok = True
for trial in range(12):
    y = np.cumsum(rng.standard_normal(3000)) * 0.05 + rng.standard_normal(3000)
    z = ops.b4_z(y)
    _, sc = e4_ops.b4_free_state_2s(z)
    vals = sc[np.isfinite(sc)]
    for th in np.quantile(vals, [0.5, 0.9, 0.99]):
        a = e4_ops.b4_alarm_2s(z, th)
        b = e4_ops.b4_alarm_2s_loop(z, th)
        same = (np.array_equal(np.nan_to_num(a[0], nan=-1), np.nan_to_num(b[0], nan=-1))
                and np.array_equal(a[1], b[1]) and np.array_equal(a[2], b[2]))
        allok &= same
ok("two-sided B4: fast == loop (36 cases)", allok)
y = rng.standard_normal(3000)
z = ops.b4_z(y)
a = e4_ops.b4_alarm_2s_loop(z, 1e9)
ok("two-sided score >= one-sided score everywhere", np.all(np.nan_to_num(a[0], nan=0) >= np.nan_to_num(ops.b4_alarm_loop(z, 1e9)[0], nan=0) - 1e-12))
g = np.exp(0.01 * rng.standard_normal(2000))
_mh = ops.MIN_HIST
ops.MIN_HIST = 0                                          # ungated scores for this check only
b3 = ops.score_b3(g)
first = int(np.nonzero(np.nan_to_num(b3) > 2.5)[0][0])     # identical up to and including the first z > 2.5
ok("B3-adjusted == B3 up to the first z > 2.5, differs after it",
   np.allclose(np.nan_to_num(e4_ops.score_b3_adjusted(g)[:first + 1]), np.nan_to_num(b3[:first + 1]))
   and not np.allclose(np.nan_to_num(e4_ops.score_b3_adjusted(g)[first + 1:]), np.nan_to_num(b3[first + 1:])))
ops.MIN_HIST = _mh
g2 = g.copy()
g2[1500] = 50.0
ok("B3-adjusted != B3 after a spike", not np.allclose(np.nan_to_num(e4_ops.score_b3_adjusted(g2)[1501:]), np.nan_to_num(ops.score_b3(g2)[1501:])))
yy = rng.standard_normal(1500)
ok("B4 on g == b4_z(exp(y))", np.array_equal(np.nan_to_num(e4_ops.b4_z_on_g(yy)), np.nan_to_num(ops.b4_z(np.exp(yy)))))
for n, c in C:
    print(("PASS " if c else "FAIL ") + n)
print("ALL PASS" if all(c for _, c in C) else "FAILED")
sys.exit(0 if all(c for _, c in C) else 1)
