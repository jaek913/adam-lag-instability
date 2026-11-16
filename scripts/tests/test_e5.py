"""E5 gate (D.5 "Alignment control (E5)") for analysis/post/e5.py: the flag must trip on precursor-free alarms
(alarms placed at random, unrelated to events) and must not trip when alarms precede every event by 100 steps
(planted L = 100). Also: an empty alarm series gives rate 0 and trips the flag.
Usage: python scripts/tests/test_e5.py"""
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [os.path.join(ROOT, "analysis"), os.path.join(ROOT, "analysis", "post")]
import e5  # noqa: E402

C = []


def ok(n, c):
    C.append((n, bool(c)))


e5.NDRAW = 300
n, first = 40000, 10
steps = first + 10 * np.arange(n)
rng = np.random.default_rng(5)
ev_idx = np.sort(rng.choice(np.arange(2000, n - 200), 50, replace=False))
elig = [{"t_e": int(steps[i]), "series": "kept"} for i in ev_idx]
planted = np.zeros(n, bool)
for i in ev_idx:
    planted[i - 10:i - 10 + 32] = True                      # onset 100 steps before every event, held 32 obs
r1 = e5.run_control([(first, planted)], elig, np.random.default_rng(1))
ok("planted L = 100: real rate 1.0", r1["real_rate"] == 1.0)
ok("planted L = 100: flag not tripped", not r1["flag_tripped"])
rand = np.zeros(n, bool)
for i in rng.choice(np.arange(0, n - 32), 50, replace=False):
    rand[i:i + 32] = True
r2 = e5.run_control([(first, rand)], elig, np.random.default_rng(2))
ok("precursor-free alarms: flag tripped", r2["flag_tripped"])
r3 = e5.run_control([(first, np.zeros(n, bool))], elig, np.random.default_rng(3))
ok("empty alarm series: rate 0, flag tripped", r3["real_rate"] == 0.0 and r3["flag_tripped"])
for nm, c in C:
    print(("PASS " if c else "FAIL ") + nm)
print("ALL PASS" if all(c for _, c in C) else "FAILED")
sys.exit(0 if all(c for _, c in C) else 1)
