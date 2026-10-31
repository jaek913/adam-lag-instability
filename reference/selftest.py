"""Hand-computed self-tests for ref_e2.py. Every expected value below was derived by hand
from DESIGN.md text (derivations in comments), not by running the code."""

import math
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np  # noqa: E402

import ref_e2 as R  # noqa: E402

FAILS = []


def check(name, cond, detail=""):
    print(("PASS " if cond else "FAIL ") + name + ("" if cond else "  " + str(detail)))
    if not cond:
        FAILS.append(name)


def close(a, b, tol=1e-12):
    return abs(a - b) <= tol * max(1.0, abs(b))


# T1 block preparation: leading drops excluded; later drops carried forward and counted.
b = R.prepare_block({"first_step": 100, "g": [None, -1, 2.0, float("nan"), 0, 3.0, float("inf")]}, 10)
check("T1 steps", b["steps"] == [120, 130, 140, 150, 160], b["steps"])
check("T1 g carried", b["g"] == [2.0, 2.0, 2.0, 3.0, 3.0], b["g"])
check("T1 y", b["y"][1] == math.log(2.0) and b["y"][4] == math.log(3.0))
check("T1 dropped", b["dropped"] == [False, True, True, False, True])
check("T1 all dropped -> None", R.prepare_block({"first_step": 0, "g": [None, 0, -2]}, 1) is None)

# T2 D_div, w_f=2, w_s=4. y = [0,0,0,4,0,0,8].
# j=3: SMA2=2, SMA4=1, D=1 -> hist{1} P=1
# j=4: SMA2=2, SMA4=1, D=1 -> hist{1,1} P=2/2=1 (tie counts)
# j=5: SMA2=0, SMA4=1, D=-1 -> P=1/3
# j=6: SMA2=4, SMA4=3, D=1 -> hist{-1,1,1,1} P=4/4=1
y = [0, 0, 0, 4, 0, 0, 8]
check("T2 D_div min_hist=0", R.score_ddiv(y, 2, 4, 0) == [None, None, None, 1.0, 1.0, 1 / 3, 1.0])
# min_hist=5: j=3,4 unscored but still in the percentile history.
check("T2 D_div min_hist=5", R.score_ddiv(y, 2, 4, 5) == [None] * 5 + [1 / 3, 1.0])

# T3 B1, win=3, current excluded. y=[1,1,1,5,2,3]
# j=3: window [1,1,1] sd=0 -> undefined
# j=4: window [1,1,5], m=7/3, var=16/3 -> s=(2-7/3)/sqrt(16/3)
# j=5: window [1,5,2], m=8/3, var=13/3 -> s=(3-8/3)/sqrt(13/3)
s1 = R.score_b1([1.0, 1, 1, 5, 2, 3], 3, 0)
check("T3 B1 undefined", s1[:4] == [None] * 4, s1)
check("T3 B1 j4", close(s1[4], (2 - 7 / 3) / math.sqrt(16 / 3)), s1[4])
check("T3 B1 j5", close(s1[5], (3 - 8 / 3) / math.sqrt(13 / 3)), s1[5])

# T4 B3, warm=3, alpha=0.97. g=[1,2,3,10,4]
# init at 3rd obs: mu=2, v=2/3 (ddof 0); j=3: s=8/(sqrt(2/3)+1e-6);
# update weight = float64 (1 - 0.97) (Amendment 9.2), not the literal 0.03:
# mu=0.97*2+(1-0.97)*10 = 2.24 (float 2.24; the literal 0.03 gives 2.2399999999999998);
# v=0.97*(2/3)+(1-0.97)*(10-mu)^2; j=4: s=(4-mu)/(sqrt(v)+1e-6). Exact equality required.
s3 = R.score_b3([1.0, 2, 3, 10, 4], 0.97, 3, 1e-6, 0)
w = 1.0 - 0.97
mu1 = 0.97 * 2.0 + w * 10.0
v1 = 0.97 * (2.0 / 3.0) + w * ((10.0 - mu1) * (10.0 - mu1))
mu1_lit = 0.97 * 2.0 + 0.03 * 10.0
check("T4 B3 warm-up", s3[:3] == [None] * 3)
check("T4 B3 j3", s3[3] == 8.0 / (math.sqrt(2.0 / 3.0) + 1e-6), s3[3])
check("T4 weight readings differ here", mu1 != mu1_lit)
check("T4 B3 j4 uses (1-alpha) exactly", s3[4] == (4.0 - mu1) / (math.sqrt(v1) + 1e-6), s3[4])

# T5 B4, win=4, minobs=2, k=1. y=[0,2,0,5,0,0,0]
# j=2: hist[0,2] med=1 MAD=1 sigma=1.4826 z=-1/1.4826 S=0
# j=3: hist[0,2,0] med=0 MAD=0 -> sigma=1e-12, z=5e12, S=5e12-1
# theta=10, hold=2: onset j=3 (s(2)=0<10), reset S=0; Amendment 9.1: history kept,
# scoring continues at j=4 from S=0:
# j=4: hist[0,2,0,5] med=1 MAD=median(1,1,1,4)=1 z=-1/1.4826 S=max(0,0+z-1)=0
# j=5: hist[2,0,5,0] med=1 MAD=1 z=-1/1.4826 S=0
# j=6: hist[0,5,0,0] med=0 MAD=0 sigma=1e-12 z=0 S=max(0,-1)=0
y5 = [0.0, 2, 0, 5, 0, 0, 0]
z5 = R.b4_robust_z(y5, 4, 2, 1.4826, 1e-12)
check("T5 z j2", close(z5[2], -1 / 1.4826))
check("T5 z j3", z5[3] == 5e12, z5[3])
check("T5 z j4,j5", close(z5[4], -1 / 1.4826) and close(z5[5], -1 / 1.4826))
check("T5 z j6", z5[6] == 0.0)
check("T5 frozen default is 9.1", R.FROZEN["b4_warm_after_reset"] is False)
sc, on, al = R.b4_path(z5, 10.0, 2, 1.0, 2, 0, R.FROZEN["b4_warm_after_reset"])
check("T5 B4 scores", sc == [None, None, 0.0, 5e12 - 1, 0.0, 0.0, 0.0], sc)
check("T5 B4 onsets", on == [3])
check("T5 B4 alarm", al == [False, False, False, True, True, False, False], al)
# reset-free path: j=4 S = (5e12-1) + z4 - 1
sc_free, on_free, _ = R.b4_path(z5, math.inf, 2, 1.0, 2, 0, False)
check("T5 B4 reset-free j4", close(sc_free[4], (5e12 - 1) + (-1 / 1.4826) - 1) and on_free == [])

# T5b B4 accumulation resumes right after a reset (Amendment 9.1), hand z path.
# z = [-, -, 3, 20, 12, 15, -30, 12], k=1, theta=10, hold=2, min_hist=0
# j2: S=2 ; j3: S=21 >=10, prev 2<10 -> onset 3, reset S=0, alarm 3..4
# j4: S=0+12-1=11 (in alarm) ; j5: S=11+15-1=25, prev 11 >= 10 -> no fresh crossing
# j6: S=max(0,25-30-1)=0 ; j7: S=0+12-1=11, prev 0<10 -> onset 7
zb = [None, None, 3.0, 20.0, 12.0, 15.0, -30.0, 12.0]
sc, on, al = R.b4_path(zb, 10.0, 2, 1.0, 2, 0, False)
check("T5b B4 scores", sc == [None, None, 2.0, 21.0, 11.0, 25.0, 0.0, 11.0], sc)
check("T5b B4 onsets", on == [3, 7], on)
check("T5b B4 alarm", al == [False, False, False, True, True, False, False, True], al)

# T6 onset/hold. theta=5, hold=3
sc6 = [None, 5, 5, 5, 5, 5, 1, 5, 5]
on6, al6 = R.simulate_alarm(sc6, 5, 3)
check("T6 onsets", on6 == [1, 7], on6)
check("T6 alarm", al6 == [False, True, True, True, False, False, False, True, True], al6)
# undefined previous score counts as below (Amendment 7.3)
on6b, _ = R.simulate_alarm([5, None, 5, 5], 5, 1)
check("T6 undefined prev", on6b == [0, 2], on6b)

# T7 top scan (Amendment 6.1 / 6.3).
def count_fn_for(scores, hold):
    return lambda v, lim: len(R.simulate_alarm(scores, v, hold)[0])
# (iii) non-monotone: scores [0,3,2,3,0,0,9,0], hold 1, n*=1.
# c(9)=1, c(3)=3 (j=1,3,6) -> stop -> theta=9 (old rule would give 0: c(0)=1).
p7 = [0, 3, 2, 3, 0, 0, 9, 0]
th, ok, _ = R.top_scan([9, 3, 2, 0], count_fn_for(p7, 1), 1)
check("T7 non-monotone stops above", th == 9 and ok, th)
check("T7 old rule would pick 0", len(R.simulate_alarm(p7, 0, 1)[0]) == 1)
# (ii) top candidate already exceeds: [0,3,2,3,0] -> c(3)=2 > 1 -> not matchable
th, ok, _ = R.top_scan([3, 2, 0], count_fn_for([0, 3, 2, 3, 0], 1), 1)
check("T7 not matchable", th == math.inf and not ok)
# (i) none exceeds -> lowest candidate
th, ok, _ = R.top_scan([3, 0], count_fn_for([0, 3, 0], 1), 5)
check("T7 lowest when none exceeds", th == 0 and ok)

# T8 n* round-half-up (A1.11(a)); Python round(2.5)=2 would be wrong.
check("T8 half-up 2.5->3", R.nstar_of(1.0, 25000) == 3)
check("T8 0.4->0", R.nstar_of(1.0, 4000) == 0)
check("T8 0.5->1", R.nstar_of(0.5, 10000) == 1)
check("T8 1.2->1", R.nstar_of(1.0, 12000) == 1)

# T9 end-to-end with small parameters (B2 checked by hand). grid=1, scan=2, hold=2,
# min_hist=0. 13 obs, event t_e=12 -> window [10,12]; out obs j=0..9 -> N_out=10;
# fa=2000 -> n*=2.
# y: 0 3 0 0 2 0 0 1 1 0 | 0 2.5 0
# B2 cands {3,2,1,0}: c(3)=1 (j1); c(2)=2 (j1,j4); c(1)=3 (j1,j4,j7) > 2 -> theta=2.
# onsets at theta=2: 1, 4, 11 (in window); realised (out) = 2; coverage = 2/10.
# lead: first alarm in [10,12] at 11 -> lead 1, detected, not concurrent.
P = dict(R.FROZEN)
P.update(min_hist=0, w_f=2, w_s=4, b1_win=3, b3_warm=3, b4_minobs=2, b4_win=4)
y9 = [0, 3, 0, 0, 2, 0, 0, 1, 1, 0, 0, 2.5, 0]
blk = {"first_step": 0, "g": [math.exp(v) for v in y9]}
r9 = R._run([blk], [{"t_e": 12, "eligible": True}], 2000, 1, 2, 2, None, P)
B2 = r9["B2"]
check("T9 N_out, n*", r9["N_out"] == 10 and r9["nstar"] == 2, (r9["N_out"], r9["nstar"]))
check("T9 B2 theta", close(B2["theta"], 2.0), B2["theta"])
check("T9 B2 onsets", B2["onsets"] == [1, 4, 11], B2["onsets"])
check("T9 B2 realised/coverage", B2["realised"] == 2 and close(B2["coverage"], 0.2))
check("T9 B2 lead flags", B2["leads"] == [1] and B2["detected"] == [True]
      and B2["concurrent"] == [False] and B2["censored"] == [False])
check("T9 C consistency", all(close(r9["C"][b], r9["D_div"]["leads"][0] - r9[b]["leads"][0])
                              for b in R.BASELINES) and r9["C_min"] == min(r9["C"].values()))

# T10 leads: concurrent, censored, onset exactly at window start, miss (thetas given).
# grid=1, scan=4, hold=3, min_hist=0, B2 theta=1. Block y (steps 0..29):
# spike at 6 -> alarm 6..8; event A t_e=10 window [6,10]: alarm at 6, alarm at 5? no
#   -> lead 4, not censored.
# spike at 13 -> alarm 13..15; event B t_e=18 window [14,18]: alarm at 14 and 13
#   -> censored, lead 4.
# spike at 24 -> event C t_e=24 window [20,24]: first alarm at 24 -> lead 0, concurrent.
# event D t_e=29 window [25,29]: alarm 24..26 -> first at 25, alarm at 24 -> censored 4.
# event E t_e=5 window [1,5]: no alarm -> miss.
y10 = [0.0] * 30
for k in (6, 13, 24):
    y10[k] = 2.0
blk10 = {"first_step": 0, "g": [math.exp(v) for v in y10]}
evs = [{"t_e": t, "eligible": True} for t in (10, 18, 24, 29, 5)]
P10 = dict(P)
r10 = R._run([blk10], evs, 100000, 1, 4, 3,
             {"D_div": math.inf, "B1": math.inf, "B2": 1.0, "B3": math.inf, "B4": math.inf}, P10)
B2 = r10["B2"]
check("T10 leads", B2["leads"] == [4, 4, 0, 4, 0], B2["leads"])
check("T10 censored", B2["censored"] == [False, True, False, True, False], B2["censored"])
check("T10 detected", B2["detected"] == [True, True, False, True, False])
check("T10 concurrent", B2["concurrent"] == [False, False, True, False, False])
check("T10 miss", B2["miss"] == [False, False, False, False, True])
check("T10 inf never alarms", r10["D_div"]["onsets"] == [] and r10["D_div"]["leads"] == [0] * 5)
# C_B2 = mean(D_div)=0 - mean(B2)=12/5
check("T10 C_B2", close(r10["C"]["B2"], -12 / 5) and close(r10["C_min"], -12 / 5))

# T11 event anchor t_e^g = 10*floor(t_e/10) and window exclusion with grid 10 (A1.4).
# Block steps 0..990 (100 obs), min_hist=0; event t_e=507 -> anchor 500, scan 40
# -> window steps 460..500 = 5 obs excluded -> N_out = 95.
blk11 = {"first_step": 0, "g": [1.0 + 0.01 * (i % 7) for i in range(100)]}
r11 = R._run([blk11], [{"t_e": 507, "eligible": False}], 10000 / 95 * 1, 10, 40, 3, None, P)
check("T11 N_out with anchor", r11["N_out"] == 95, r11["N_out"])

# T12 n* = 0 guard returns UNRUN.
r12 = R._run([blk11], [], 1.0, 10, 40, 3, None, P)
check("T12 UNRUN", r12.get("label") == "UNRUN (n* = 0)" and r12["nstar"] == 0, r12)

# T13 frozen constants: a dropped reading inside the first 1,000 observations counts
# toward j and the first defined score is at j=1000 (Amendment 5.3(v)); a dropped first
# reading shifts the series start by one.
rng = np.random.default_rng(1)
n = 1200
gs = list(np.exp(rng.standard_normal(n) * 0.3))
gs[0] = None      # dropped first reading -> series starts at index 1
gs[500] = float("nan")
blk13 = {"first_step": 0, "g": gs}
s13 = R.prepare_block(blk13, 10)
d13 = R.score_ddiv(s13["y"], 32, 128, 1000)
first_def = min(j for j in range(len(d13)) if d13[j] is not None)
check("T13 first score at j=1000 (step 10010)", first_def == 1000 and s13["steps"][1000] == 10010)
check("T13 carry-forward at dropped", s13["y"][499] == s13["y"][498])

# T14 frozen-constant end-to-end smoke test: 2 blocks, 20k obs, invariants only.
rng = np.random.default_rng(7)
def ar1(n, phi):
    out = np.zeros(n)
    e = rng.standard_normal(n) * math.sqrt(1 - phi * phi)
    for i in range(1, n):
        out[i] = phi * out[i - 1] + e[i]
    return out
y1 = ar1(12000, 0.9)
y2 = ar1(9000, 0.9)
evs14 = []
for t in (3000, 6000, 9000, 11500):  # obs index -> step = 10*i (+ offset 7 to test anchor)
    y1[t - 100: t] += np.linspace(0, 2, 100)
    evs14.append({"t_e": t * 10 + 7, "eligible": True})
blocks14 = [{"first_step": 0, "g": list(np.exp(y1))},
            {"first_step": 200000, "g": list(np.exp(y2))}]
evs14.append({"t_e": 200000 + 500 * 10, "eligible": False})  # in min-history: excluded anyway
t0 = time.time()
r14 = R.run_reference(blocks14, evs14, fa=5.0)
dt = time.time() - t0
check("T14 n* matches N_out", r14["nstar"] == R.nstar_of(5.0, r14["N_out"]))
check("T14 realised <= n*", all(r14[d]["realised"] <= r14["nstar"] for d in R.DETECTORS),
      {d: r14[d]["realised"] for d in R.DETECTORS})
check("T14 eligibility check", r14["eligibility_check"] == [True] * 4)
check("T14 leads range", all(0 <= L <= 1280 and L % 10 == 0 for d in R.DETECTORS for L in r14[d]["leads"]))
print("T14 summary: N_out=%d n*=%d time=%.1fs" % (r14["N_out"], r14["nstar"], dt))
for d in R.DETECTORS:
    print("   %-5s theta=%r realised=%d cov=%.5f leads=%s" % (
        d, r14[d]["theta"], r14[d]["realised"], r14[d]["coverage"], r14[d]["leads"]))
print("   C=%r C_min=%r" % (r14["C"], r14["C_min"]))

print()
print("ALL PASS" if not FAILS else "FAILURES: %s" % FAILS)
sys.exit(0 if not FAILS else 1)
