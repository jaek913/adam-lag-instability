"""E1 gate (Amendment 4.1 exact-identity hand probe) for analysis/post/e1.py.
1. R-bar indexing on a hand ACF: half-open and inclusive forms.
2. Exact identity: for any series, sum over t of (SMA_w(y)_t - c) * y_{t+h} equals (1/w) * sum_j sum_t y_{t-j} y_{t+h}
   term by term (checked numerically to 1e-9 on centred data, finite sample, same index set).
3. AR(1) planted: criterion sign positive at phi = 0.9 and the label is CONSISTENT on a long AR(1) series;
   white noise gives INDETERMINATE.
Usage: python scripts/tests/test_e1.py"""
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [os.path.join(ROOT, "analysis"), os.path.join(ROOT, "analysis", "post")]
import e1  # noqa: E402
import ops  # noqa: E402

C = []


def ok(n, c):
    C.append((n, bool(c)))


rho = np.arange(10, dtype=float)
ok("rbar half-open (2,5) = mean of lags 2,3,4", e1.rbar(rho, 2, 5) == 3.0)
ok("rbar inclusive (2,5) = mean of lags 2..5", e1.rbar_incl(rho, 2, 5) == 3.5)

rng = np.random.default_rng(7)
y = rng.standard_normal(500)
w, h = 8, 3
S = ops.sma_incl(y, w)
t = np.arange(w - 1, len(y) - h)
lhs = np.sum(S[t] * y[t + h])
rhs = sum(np.sum(y[t - j] * y[t + h]) for j in range(w)) / w
ok("SMA covariance identity (finite-sample, exact)", abs(lhs - rhs) < 1e-9)

def ar1(n, phi, seed):
    r = np.random.default_rng(seed)
    e = r.standard_normal(n)
    x = np.empty(n)
    x[0] = e[0]
    for i in range(1, n):
        x[i] = phi * x[i - 1] + e[i]
    return x

e1.NPERM = 200
res = e1.run([ar1(20000, 0.9, 1)], np.random.default_rng(1))
ok("AR(1) 0.9: predicted sign +", res["predicted_sign"] == 1)
ok("AR(1) 0.9: CONSISTENT", res["label"] == "CONSISTENT")
res0 = e1.run([np.random.default_rng(2).standard_normal(20000)], np.random.default_rng(2))
ok("white noise: not CONSISTENT", res0["label"] != "CONSISTENT")
for n, c in C:
    print(("PASS " if c else "FAIL ") + n)
print("ALL PASS" if all(c for _, c in C) else "FAILED")
sys.exit(0 if all(c for _, c in C) else 1)
