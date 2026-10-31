"""Hand-computed probes for analysis/ops.py (DESIGN Amendment 5.3 (i)-(v); Amendment 6.3 (i)-(iii)).
Every check is also watched to FAIL by a perturbation (Phase 2 validation gate (c)).
Usage: python scripts/tests/test_ops.py
"""
import importlib.util
import math
import os
import sys
import types

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
import ops  # noqa: E402

TP = os.path.join(ROOT, "scripts", "tests", "third_party")
CHECKS = []


def ok(name, cond):
    CHECKS.append((name, bool(cond)))


def close(a, b, tol=1e-12):
    a, b = np.asarray(a, float), np.asarray(b, float)
    return a.shape == b.shape and np.all((np.isnan(a) & np.isnan(b)) | (np.abs(a - b) <= tol))


def with_hist(h, fn):
    old = ops.MIN_HIST
    ops.MIN_HIST = h
    try:
        return fn()
    finally:
        ops.MIN_HIST = old


def load_zclip():
    torch = types.ModuleType("torch")
    dist = types.ModuleType("torch.distributed")
    fsdp = types.ModuleType("torch.distributed.fsdp")
    fsdp.FullyShardedDataParallel = type("FSDP", (), {})
    torch.distributed = dist
    dist.fsdp = fsdp
    sys.modules.update({"torch": torch, "torch.distributed": dist, "torch.distributed.fsdp": fsdp})
    spec = importlib.util.spec_from_file_location("zclip_ref", os.path.join(TP, "zclip_1_0_0", "zclip.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.ZClip


def load_trainscope():
    for name in ("trainscope", "trainscope.core", "trainscope.core.detectors"):
        sys.modules.setdefault(name, types.ModuleType(name))
    spec_b = importlib.util.spec_from_file_location("trainscope.core.detectors.base",
                                                    os.path.join(TP, "trainscope_0651b25", "base.py"))
    b = importlib.util.module_from_spec(spec_b)
    spec_b.loader.exec_module(b)
    sys.modules["trainscope.core.detectors.base"] = b
    sys.modules["ruptures"] = None                      # PELT absent (Amendment 5.2)
    spec = importlib.util.spec_from_file_location("cp_ref", os.path.join(TP, "trainscope_0651b25", "changepoint.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m.ChangePointDetector


def main():
    nan = float("nan")
    # ---------------- (i) D_div by hand
    ok("sma_incl [1,2,3,4], w=2", close(ops.sma_incl([1, 2, 3, 4], 2), [nan, 1.5, 2.5, 3.5]))
    ok("divergence wf=2, ws=4", close(ops.divergence(np.arange(1, 7.0), 2, 4), [nan, nan, nan, 1, 1, 1]))
    p = ops.expanding_percentile_le(np.array([nan, nan, 3, 1, 3, 2.0]), 2)
    ok("percentile ties <= : [1, .5, 1, .5]", close(p, [nan, nan, 1.0, 0.5, 1.0, 0.5]))
    ok("WATCH-FAIL: strict < would give 2/3 at the tie", not close(p[4], 2 / 3))
    rng = np.random.default_rng(20261030)
    d = rng.normal(size=400)
    brute = np.array([np.nan if j < 5 else np.mean(d[5:j + 1] <= d[j]) for j in range(400)])
    ok("percentile Fenwick == brute force (n=400)", close(ops.expanding_percentile_le(d, 5), brute))

    # ---------------- (ii) B1 by hand (current excluded, ddof=1)
    s1 = with_hist(0, lambda: ops.score_b1(np.array([1, 2, 3, 10, 4.0]), 3))
    ok("B1 j=3: (10-2)/1 = 8", math.isclose(s1[3], 8.0, abs_tol=1e-12))
    ok("B1 j=4: (4-5)/sqrt(19)", math.isclose(s1[4], -1 / math.sqrt(19), abs_tol=1e-12))
    ok("B1 j<w undefined", np.isnan(s1[:3]).all())
    s1z = with_hist(0, lambda: ops.score_b1(np.array([5, 5, 5, 7.0]), 3))
    ok("B1 sd==0 -> undefined", np.isnan(s1z[3]))
    ok("WATCH-FAIL: current-included would give (10-4)/sd([1,2,3,10]) != 8",
       not math.isclose((10 - np.mean([1, 2, 3, 10])) / np.std([1, 2, 3, 10], ddof=1), 8.0))

    # ---------------- (iii) B3 vs ZClip 1.0.0's own class
    ZClip = load_zclip()
    g = np.abs(rng.normal(1.0, 0.2, size=400)) + 0.05
    g[300] = 5.0
    ref = ZClip(alpha=0.97, z_thresh=2.5, warmup_steps=25, mode="zscore")
    zr = []
    for x in g:
        if not ref.initialized:
            ref.buffer.append(float(x))
            if len(ref.buffer) >= ref.warmup_steps:
                ref._initialize_ema()
            zr.append(nan)
            continue
        z, _ = ref._compute_positive_zscore(float(x))
        zr.append(z)
        ref._update_ema(float(x))                      # monitor mode: raw g (P-B3)
    ours = with_hist(0, lambda: ops.score_b3(g))
    ok("B3 == ZClip 1.0.0 code (400 obs, 1e-12)", close(ours, zr))
    ok("B3 first score at obs 26 (index 25)", np.isnan(ours[:25]).all() and not np.isnan(ours[25]))
    bad = g.copy()
    bad[100] += 1e-6
    ok("WATCH-FAIL: perturbed input differs", not close(with_hist(0, lambda: ops.score_b3(bad)), zr))

    # ---------------- (iv) B4 vs trainscope 0651b25's own class (S+ up to its first fire)
    CPD = load_trainscope()
    y = rng.normal(0.0, 1.0, size=600)
    y[450:] += 2.5                                     # drift > slack k so the reference fires
    ref = CPD(threshold=6.0, slack=1.0, window=200, min_observations=30)
    sp_ref, fired_at = [], None
    for j, x in enumerate(y):
        r = ref.update(float(x))
        if r is not None and fired_at is None:
            fired_at = j
        sp_ref.append(nan if j < 30 else ref._positive_cusum)
    s4, _, _ = with_hist(0, lambda: ops.b4_path(y, theta=None))
    upto = fired_at if fired_at is not None else len(y)
    ok("reference fires somewhere (test is non-vacuous)", fired_at is not None)
    ok("B4 S+ == trainscope code before its first fire (1e-12)", close(s4[:upto], sp_ref[:upto]))
    ok("B4 warm-up: undefined for j < 30", np.isnan(s4[:30]).all() and not np.isnan(s4[30]))
    # a variant whose median/MAD baseline INCLUDES the current reading must disagree with the code
    from collections import deque
    hist, sp, alt = deque(), 0.0, []
    for j, x in enumerate(y):
        if len(hist) < 30:
            hist.append(x)
            alt.append(nan)
            continue
        hist.append(x)
        if len(hist) > 200:
            hist.popleft()
        h = np.array(hist)
        med = np.median(h)
        sd = max(np.median(np.abs(h - med)) * 1.4826, 1e-12)
        sp = max(0.0, sp + (x - med) / sd - 1.0)
        alt.append(sp)
    ok("WATCH-FAIL: current-INCLUDED baseline variant disagrees with trainscope", not close(alt[:upto], sp_ref[:upto]))

    # ---------------- (v) dropped reading inside the first 1,000 (JAE)
    vals = rng.normal(size=1500)
    dropped = np.zeros(1500, bool)
    dropped[500] = True
    v, off = ops.prepare_block(vals, dropped)
    ok("(v) no leading drop: offset 0, length 1,500", off == 0 and len(v) == 1500)
    ok("(v) dropped obs carried forward", v[500] == v[499] and v[501] == vals[501])
    for name, fn in (("D_div", ops.score_div), ("B1", ops.score_b1), ("B2", ops.score_b2), ("B3", ops.score_b3)):
        sc = fn(np.abs(v) + 0.1 if name == "B3" else v)
        ok(f"(v) {name}: first defined score at j = 1,000", np.isnan(sc[:1000]).all() and not np.isnan(sc[1000]))
    s4v, _, _ = ops.b4_path(v, theta=None)
    ok("(v) B4: first defined score at j = 1,000", np.isnan(s4v[:1000]).all() and not np.isnan(s4v[1000]))
    d2 = dropped.copy()
    d2[:3] = True
    v2, off2 = ops.prepare_block(vals, d2)
    ok("(v) leading dropped readings: block starts at first non-dropped", off2 == 3 and v2[0] == vals[3])

    # ---------------- Amendment 6.3 (i)-(iii): P-FA top scan
    def count(s):
        return lambda v: len(ops.alarm_from_scores(s, v)[0])
    s = rng.normal(size=5000)
    c_min = count(s)(s.min())
    m = ops.match_threshold(count(s), s, 4)
    ok("6.3(i) minimum candidate satisfies c <= n* (the defect's precondition)", c_min <= 4)
    ok("6.3(i) top scan does NOT select the minimum", m["theta"] > s.min() and m["matchable"])
    ok("6.3(i) coverage small (< 1%)", np.mean(s >= m["theta"]) < 0.01)
    ok("6.3(i) realised <= n*", m["realised"] <= 4)
    frozen = min(v for v in np.unique(s) if count(s)(v) <= 4)
    ok("WATCH-FAIL: frozen smallest-candidate rule picks the minimum", frozen == s.min())
    s2 = rng.normal(size=3000)
    s2[np.arange(100, 3000, 60)] = 10.0               # ~49 isolated ties at the maximum
    m2 = ops.match_threshold(count(s2), s2, 4)
    ok("6.3(ii) tied top with c > n*: not matchable, never alarms",
       (not m2["matchable"]) and math.isinf(m2["theta"]) and len(ops.alarm_from_scores(s2, m2["theta"])[0]) == 0)
    s3 = np.full(4000, 4.0)
    s3[[500, 2500]] = 9.0
    s3[np.arange(700, 3900, 400)] = 7.0               # 8 isolated values at 7
    c9, c7, c4 = count(s3)(9.0), count(s3)(7.0), count(s3)(4.0)
    m3 = ops.match_threshold(count(s3), s3, 4)
    ok("6.3(iii) non-monotone c: c(9)<=4 < c(7), c(4)<=4", c9 <= 4 < c7 and c4 <= 4)
    ok("6.3(iii) top scan stops above the excursion: theta = 9", m3["theta"] == 9.0)

    # ---------------- P-HOLD basics
    sh = np.zeros(200)
    sh[10:120] = 1.0
    on, al = ops.alarm_from_scores(sh, 0.5, hold=32)
    ok("P-HOLD: standing score -> one onset, 32 alarm obs", list(on) == [10] and al.sum() == 32)
    sh2 = np.zeros(200)
    sh2[[10, 20, 50]] = 1.0
    on2, _ = ops.alarm_from_scores(sh2, 0.5, hold=32)
    ok("P-HOLD: crossing inside hold ignored; next after hold counts", list(on2) == [10, 50])
    ok("round_half_up(2.5) == 3 (not banker's)", ops.round_half_up(2.5) == 3 and round(2.5) == 2)

    # Vectorised b4_z and list-based b4_alarm must be bit-identical to the reference loop
    rng = np.random.default_rng(5)
    same = True
    for n in (10, 31, 150, 200, 201, 5000):
        yy = np.cumsum(rng.standard_normal(n)) * 0.1
        yy[n // 3:n // 3 + 5] = 3.0                    # ties in the history
        zv, zl = ops.b4_z(yy), ops.b4_z_loop(yy)
        same = same and np.array_equal(zv, zl, equal_nan=True)
    ok("b4_z (vectorised) == b4_z_loop (reference) bit-for-bit, n in {10..5000}", same)
    yy = np.cumsum(rng.standard_normal(3000)) * 0.1
    zz = ops.b4_z_loop(yy)
    yy2 = yy.copy()
    yy2[2500] += 1e-9
    # Fast b4_alarm (merge-with-free-path) must be bit-identical to b4_alarm_loop
    mism, cases = 0, 0
    for trial in range(12):
        n = int(rng.integers(1300, 4000))
        yb = np.cumsum(rng.standard_normal(n)) * 0.2 + rng.standard_normal(n)
        zb = ops.b4_z(yb)
        sf = ops.b4_alarm_loop(zb, None)[0]
        vals = np.unique(sf[~np.isnan(sf)])
        for th in list(rng.choice(vals, 5)) + [float(vals.max()), float(vals.max()) + 1.0]:
            for hh in (1, 32):
                fa_, lo_ = ops.b4_alarm(zb, th, hh), ops.b4_alarm_loop(zb, th, hh)
                cases += 1
                mism += not (np.array_equal(fa_[0], lo_[0], equal_nan=True) and np.array_equal(fa_[1], lo_[1])
                             and np.array_equal(fa_[2], lo_[2]))
    ok(f"b4_alarm (fast) == b4_alarm_loop bit-for-bit on {cases} randomised cases", mism == 0)
    ok("WATCH-FAIL: a 1e-9 perturbation is detected by the equality check",
       not np.array_equal(ops.b4_z(yy2), zz, equal_nan=True))

    for n, c in CHECKS:
        print(("PASS " if c else "FAIL ") + n)
    print("ALL PASS" if all(c for _, c in CHECKS) else "SOME FAILED")
    sys.exit(0 if all(c for _, c in CHECKS) else 1)


if __name__ == "__main__":
    main()
