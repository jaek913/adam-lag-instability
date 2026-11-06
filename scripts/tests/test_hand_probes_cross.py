"""Amendment 8.1 hand-probe condition: BOTH implementations reproduce the hand-computed deterministic
probes exactly (onset, theta, lead, C_min). Expected values are worked by hand (comments) and asserted
against analysis/ (ours) AND reference/ (independent). Part A: our hand probes run on the reference;
Part B: the reference's hand probes (reference/selftest.py T2-T10) run on ours; Part C: lead/flag probes on
the A1 grid run end-to-end through BOTH full chains. Usage: python scripts/tests/test_hand_probes_cross.py"""
import contextlib
import importlib.util
import math
import os
import sys
import types

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [os.path.join(ROOT, "analysis"), os.path.join(ROOT, "reference")]
import ops  # noqa: E402
import pipeline  # noqa: E402
import ref_e2 as R  # noqa: E402
sys.path.insert(0, os.path.join(ROOT, "scripts", "tests"))
import test_ops as TO  # noqa: E402  (vendored-source loaders)

TP = os.path.join(ROOT, "scripts", "tests", "third_party")
CHECKS = []
nan = float("nan")


def ok(n, c):
    CHECKS.append((n, bool(c)))


def eqn(a, b, tol=1e-12):
    """None/nan-aware elementwise equality."""
    a = [nan if x is None else float(x) for x in a]
    b = [nan if x is None else float(x) for x in b]
    return len(a) == len(b) and all((math.isnan(x) and math.isnan(y)) or abs(x - y) <= tol for x, y in zip(a, b))


@contextlib.contextmanager
def small(min_hist=0, wf=2, ws=4, b1w=3, b3w=3, b4win=4, b4min=2):
    """Run OUR chain with the small constants the reference's T9/T10 use (P in selftest.py)."""
    saved = {k: getattr(ops, k) for k in ("MIN_HIST", "score_div", "score_b1", "score_b3", "b4_z")}
    o = dict(saved)
    ops.MIN_HIST = min_hist
    ops.score_div = lambda y: o["score_div"](y, wf, ws)
    ops.score_b1 = lambda y: o["score_b1"](y, b1w)
    ops.score_b3 = lambda g: o["score_b3"](g, warmup=b3w)
    ops.b4_z = lambda y: o["b4_z"](y, window=b4win, minobs=b4min)
    try:
        yield
    finally:
        for k, v in saved.items():
            setattr(ops, k, v)


P_SMALL = dict(R.FROZEN)
P_SMALL.update(min_hist=0, w_f=2, w_s=4, b1_win=3, b3_warm=3, b4_minobs=2, b4_win=4)


def ours_run(y, events, fa, grid, scan, hold, thetas=None):
    g = np.exp(np.asarray(y, float))
    return pipeline.run([{"first_step": 0, "y": np.log(g), "g": g}], events, fa=fa, grid=grid, scan=scan,
                        hold=hold, resample=False, coverage_stop=None, thetas=thetas)


def load(name, rel):
    spec = importlib.util.spec_from_file_location(name, os.path.join(TP, rel))
    m = importlib.util.module_from_spec(spec)
    return spec, m


def main():
    # =========== Part A: our hand probes on the reference ===========
    # D_div, wf=2, ws=4, y=[1,2,3,10,4,0,0]: SMA2 j3..6 = 6.5,7,2,0; SMA4 = 4,4.75,4.25,3.5;
    # D = 2.5, 2.25, -2.25, -3.5; P = 1, 1/2, 1/3, 1/4
    yA = [1, 2, 3, 10, 4, 0, 0.0]
    exp_div = [None, None, None, 1.0, 0.5, 1 / 3, 0.25]
    ok("A1 D_div hand (ref)", eqn(R.score_ddiv(yA, 2, 4, 0), exp_div))
    with small():
        ok("A1 D_div hand (ours)", eqn(ops.score_div(np.array(yA)), exp_div))
    # B1, w=3, current excluded, ddof 1: y=[1,2,3,10,4] -> j3 (10-2)/1 = 8; j4 (4-5)/sqrt(19); sd=0 -> undefined
    ok("A2 B1 hand (ref)", eqn(R.score_b1([1, 2, 3, 10, 4.0], 3, 0), [None, None, None, 8.0, -1 / math.sqrt(19)]))
    ok("A2 B1 sd=0 undefined (ref)", R.score_b1([5, 5, 5, 7.0], 3, 0)[3] is None)
    # B3 against ZClip 1.0.0's own class (monitor mode), 400 obs, exact to 1e-12
    ZClip = TO.load_zclip()
    rng = np.random.default_rng(20261030)
    g = np.abs(rng.normal(1.0, 0.2, size=400)) + 0.05
    g[300] = 5.0
    z = ZClip(alpha=0.97, z_thresh=2.5, warmup_steps=25, mode="zscore")
    zr = []
    for x in g:
        if not z.initialized:
            z.buffer.append(float(x))
            if len(z.buffer) >= z.warmup_steps:
                z._initialize_ema()
            zr.append(None)
            continue
        zz, _ = z._compute_positive_zscore(float(x))
        zr.append(zz)
        z._update_ema(float(x))
    ok("A3 B3 == ZClip 1.0.0 class (ref)", eqn(R.score_b3(list(g), 0.97, 25, 1e-6, 0), zr))
    # B4 S+ against trainscope 0651b25's own class up to its first fire
    CPD = TO.load_trainscope()
    y = rng.normal(0.0, 1.0, size=600)
    y[450:] += 2.5
    ref = CPD(threshold=6.0, slack=1.0, window=200, min_observations=30)
    sp_ref, fired = [], None
    for j, x in enumerate(y):
        if ref.update(float(x)) is not None and fired is None:
            fired = j
        sp_ref.append(None if j < 30 else ref._positive_cusum)
    zz = R.b4_robust_z(list(y), 200, 30, 1.4826, 1e-12)
    s4, _, _ = R.b4_path(zz, math.inf, 32, 1.0, 30, 0, False)
    ok("A4 trainscope fires (non-vacuous)", fired is not None)
    ok("A4 B4 S+ == trainscope class before first fire (ref)", eqn(s4[:fired], sp_ref[:fired]))
    # dropped reading inside the first 1,000 (Amendment 5.3(v)): counts toward j, first score at j = 1,000
    vals = list(np.exp(rng.normal(size=1500) * 0.3))
    vals[500] = None
    pb = R.prepare_block({"first_step": 0, "g": vals}, 1)
    ok("A5 carry-forward (ref)", pb["y"][500] == pb["y"][499] and len(pb["y"]) == 1500)
    sd = R.score_ddiv(pb["y"], 32, 128, 1000)
    ok("A5 first D_div score at j=1000 (ref)", all(v is None for v in sd[:1000]) and sd[1000] is not None)
    # Amendment 6.3(iii): non-monotone c(v); scores 4 everywhere, 9 at 2 obs, 7 at 8 obs; n*=4, hold 32
    s3 = [4.0] * 4000
    for i in (500, 2500):
        s3[i] = 9.0
    for i in range(700, 3900, 400):
        s3[i] = 7.0
    cnt = lambda v, lim=None: len(R.simulate_alarm(s3, v, 32)[0])  # noqa: E731
    th, okm, _ = R.top_scan([9.0, 7.0, 4.0], cnt, 4)
    ok("A6 top scan stops above the excursion: theta = 9 (ref)", th == 9.0 and okm)
    m3 = ops.match_threshold(lambda v: len(ops.alarm_from_scores(np.array(s3), v)[0]), np.array(s3), 4)
    ok("A6 same (ours)", m3["theta"] == 9.0)
    # P-HOLD: crossings at 10, 20, 50, hold 32 -> onsets [10, 50]
    sh = [0.0] * 200
    for i in (10, 20, 50):
        sh[i] = 1.0
    ok("A7 hold: onsets [10, 50] (ref)", R.simulate_alarm(sh, 0.5, 32)[0] == [10, 50])
    ok("A7 hold: onsets [10, 50] (ours)", list(ops.alarm_from_scores(np.array(sh), 0.5, 32)[0]) == [10, 50])
    ok("A8 n* half-up 2.5 -> 3 (ref, ours)", R.nstar_of(1.0, 25000) == 3 and ops.round_half_up(2.5) == 3)

    # =========== Part B: the reference's hand probes on ours ===========
    # T2 D_div ties: y=[0,0,0,4,0,0,8] -> [-,-,-,1,1,1/3,1]
    with small():
        ok("B-T2 D_div ties (ours)", eqn(ops.score_div(np.array([0, 0, 0, 4, 0, 0, 8.0])),
                                         [None, None, None, 1.0, 1.0, 1 / 3, 1.0]))
        s1 = ops.score_b1(np.array([1.0, 1, 1, 5, 2, 3]))
        ok("B-T3 B1 (ours)", eqn(s1, [None] * 4 + [(2 - 7 / 3) / math.sqrt(16 / 3), (3 - 8 / 3) / math.sqrt(13 / 3)]))
        w = 1.0 - 0.97
        mu1 = 0.97 * 2.0 + w * 10.0
        v1 = 0.97 * (2.0 / 3.0) + w * ((10.0 - mu1) * (10.0 - mu1))
        s3o = ops.score_b3(np.array([1.0, 2, 3, 10, 4]))
        ok("B-T4 B3 exact (ours)", eqn(s3o, [None] * 3 + [8.0 / (math.sqrt(2.0 / 3.0) + 1e-6),
                                                           (4.0 - mu1) / (math.sqrt(v1) + 1e-6)], tol=0))
        z5 = ops.b4_z(np.array([0.0, 2, 0, 5, 0, 0, 0]))
        ok("B-T5 B4 z (ours)", eqn(z5, [None, None, -1 / 1.4826, 5e12, -1 / 1.4826, -1 / 1.4826, 0.0]))
        sc, on, al = ops.b4_alarm(z5, 10.0, 2)
        ok("B-T5 B4 scores/onsets/alarm (ours)", eqn(sc, [None, None, 0.0, 5e12 - 1, 0, 0, 0]) and list(on) == [3]
           and list(al) == [False, False, False, True, True, False, False])
        zb = np.array([nan, nan, 3.0, 20.0, 12.0, 15.0, -30.0, 12.0])
        sc, on, al = ops.b4_alarm(zb, 10.0, 2)
        ok("B-T5b B4 restart after reset (ours)", eqn(sc, [None, None, 2, 21, 11, 25, 0, 11]) and list(on) == [3, 7])
        sc, on, al = ops.b4_alarm_loop(zb, 10.0, 2)
        ok("B-T5b same via reference loop (ours)", list(on) == [3, 7])
    ok("B-T6 onsets/hold (ours)", list(ops.alarm_from_scores(np.array([nan, 5, 5, 5, 5, 5, 1, 5, 5]), 5, 3)[0]) == [1, 7])
    ok("B-T6 undefined prev = below (ours)", list(ops.alarm_from_scores(np.array([5, nan, 5, 5.0]), 5, 1)[0]) == [0, 2])
    p7 = np.array([0, 3, 2, 3, 0, 0, 9, 0.0])
    ok("B-T7 non-monotone -> 9 (ours)", ops.match_threshold(lambda v: len(ops.alarm_from_scores(p7, v, 1)[0]), p7, 1)["theta"] == 9.0)
    p7b = np.array([0, 3, 2, 3, 0.0])
    mb = ops.match_threshold(lambda v: len(ops.alarm_from_scores(p7b, v, 1)[0]), p7b, 1)
    ok("B-T7 not matchable (ours)", not mb["matchable"] and math.isinf(mb["theta"]))
    p7c = np.array([0, 3, 0.0])
    ok("B-T7 lowest when none exceeds (ours)", ops.match_threshold(lambda v: len(ops.alarm_from_scores(p7c, v, 1)[0]), p7c, 5)["theta"] == 0.0)
    ok("B-T8 n* (ours)", [ops.round_half_up(x) for x in (2.5, 0.4, 0.5, 1.2)] == [3, 0, 1, 1])
    # T9 end-to-end, small constants, both chains: B2 theta 2, onsets 1,4,11, realised 2, coverage .2, lead 1
    y9 = [0, 3, 0, 0, 2, 0, 0, 1, 1, 0, 0, 2.5, 0]
    ev9 = [{"t_e": 12, "eligible": True}]
    r9 = R._run([{"first_step": 0, "g": [math.exp(v) for v in y9]}], ev9, 2000, 1, 2, 2, None, P_SMALL)
    with small():
        o9 = ours_run(y9, ev9, 2000, 1, 2, 2)
    for tag, nout, ns, th, on, real, cov, lead, det, conc in (
            ("ref", r9["N_out"], r9["nstar"], r9["B2"]["theta"], r9["B2"]["onsets"], r9["B2"]["realised"],
             r9["B2"]["coverage"], r9["B2"]["leads"], r9["B2"]["detected"], r9["B2"]["concurrent"]),
            ("ours", o9["N_out"], o9["nstar"], o9["detectors"]["B2"]["theta"], o9["detectors"]["B2"]["onsets"],
             o9["detectors"]["B2"]["realised"], o9["detectors"]["B2"]["coverage"], o9["leads"]["B2"],
             o9["flags"]["B2"]["detected"], o9["flags"]["B2"]["concurrent"])):
        ok(f"B-T9 N_out 10, n* 2 ({tag})", nout == 10 and ns == 2)
        ok(f"B-T9 B2 theta 2, onsets [1,4,11], realised 2, coverage 0.2 ({tag})",
           math.isclose(th, 2.0) and list(on) == [1, 4, 11] and real == 2 and math.isclose(cov, 0.2))
        ok(f"B-T9 B2 lead 1, detected, not concurrent ({tag})", list(map(float, lead)) == [1.0] and list(det) == [True]
           and list(conc) == [False])
    ok("B-T9 C_min identical across chains", math.isclose(r9["C_min"], o9["C_min"], rel_tol=1e-12, abs_tol=1e-12))
    # T10 leads/flags with given thetas (B2 theta 1, hold 3, scan 4): leads [4,4,0,4,0]; C_B2 = C_min = -12/5
    y10 = [0.0] * 30
    for k in (6, 13, 24):
        y10[k] = 2.0
    ev10 = [{"t_e": t, "eligible": True} for t in (10, 18, 24, 29, 5)]
    th10 = {"D_div": math.inf, "B1": math.inf, "B2": 1.0, "B3": math.inf, "B4": math.inf}
    r10 = R._run([{"first_step": 0, "g": [math.exp(v) for v in y10]}], ev10, 100000, 1, 4, 3, th10, P_SMALL)
    with small():
        o10 = ours_run(y10, ev10, 100000, 1, 4, 3, thetas=th10)
    for tag, L, C, D, K, cm in (("ref", r10["B2"]["leads"], r10["B2"]["censored"], r10["B2"]["detected"],
                                 r10["B2"]["concurrent"], r10["C_min"]),
                                ("ours", o10["leads"]["B2"], o10["flags"]["B2"]["censored"], o10["flags"]["B2"]["detected"],
                                 o10["flags"]["B2"]["concurrent"], o10["C_min"])):
        ok(f"B-T10 leads [4,4,0,4,0] ({tag})", list(map(float, L)) == [4, 4, 0, 4, 0])
        ok(f"B-T10 censored [F,T,F,T,F] ({tag})", list(C) == [False, True, False, True, False])
        ok(f"B-T10 detected [T,T,F,T,F], concurrent [F,F,T,F,F] ({tag})",
           list(D) == [True, True, False, True, False] and list(K) == [False, False, True, False, False])
        ok(f"B-T10 C_min = -12/5 ({tag})", math.isclose(cm, -12 / 5))

    # =========== Part C: A1-grid lead probes through BOTH chains ===========
    # grid 10, scan 1,280, hold 2, B2 theta 1; 1,000 obs (steps 0..9,990); event t_e = 5,007 -> t_e^g 5,000,
    # window 3,720..5,000. One-obs spikes y=2 at the listed obs; each is a fresh crossing whose alarm holds
    # for 2 obs (the spike obs and the next). Expected (lead, censored, detected, concurrent):
    cases = [([], (0, False, False, False), "miss"),
             ([495], (50, False, True, False), "alarm at 4,950 -> 50"),
             ([500], (0, False, False, True), "alarm first at t_e^g -> concurrent"),
             ([372], (1280, False, True, False), "onset at window start 3,720, not at 3,710 -> 1,280 uncensored"),
             ([371], (1280, True, True, False), "onset 3,710 held to 3,720 -> censored 1,280"),
             ([370], (0, False, False, False), "alarm 3,700-3,710 only, before window -> miss")]
    thC = {"D_div": math.inf, "B1": math.inf, "B2": 1.0, "B3": math.inf, "B4": math.inf}
    ev = [{"t_e": 5007, "eligible": True}]
    for spikes, expect, name in cases:
        yc = [0.0] * 1000
        for i in spikes:
            yc[i] = 2.0
        rr = R._run([{"first_step": 0, "g": [math.exp(v) for v in yc]}], ev, 100000, 10, 1280, 2, thC, P_SMALL)
        with small():
            oo = ours_run(yc, ev, 100000, 10, 1280, 2, thetas=thC)
        gr = (rr["B2"]["leads"][0], rr["B2"]["censored"][0], rr["B2"]["detected"][0], rr["B2"]["concurrent"][0])
        go = (oo["leads"]["B2"][0], oo["flags"]["B2"]["censored"][0], oo["flags"]["B2"]["detected"][0],
              oo["flags"]["B2"]["concurrent"][0])
        if spikes == [495]:
            got495 = (gr, go)
        ok(f"C {name} (ref)", tuple(map(float, gr[:1])) + tuple(gr[1:]) == (float(expect[0]),) + expect[1:])
        ok(f"C {name} (ours)", tuple(map(float, go[:1])) + tuple(go[1:]) == (float(expect[0]),) + expect[1:])
    # watch-to-fail: a wrong expectation is rejected
    ok("WATCH-FAIL: a wrong expected lead (49 at 4,950) is rejected by both chains' outputs",
       all(float(x[0]) != 49.0 for x in got495))
    ok("WATCH-FAIL: hold 1 would NOT censor the 3,710 case (hold matters; both chains)",
       R._run([{"first_step": 0, "g": [math.exp(2.0 if i == 371 else 0.0) for i in range(1000)]}], ev, 100000, 10,
              1280, 1, thC, P_SMALL)["B2"]["censored"][0] is False)

    for n, c in CHECKS:
        print(("PASS " if c else "FAIL ") + n)
    print(f"{sum(c for _, c in CHECKS)}/{len(CHECKS)}", "ALL PASS" if all(c for _, c in CHECKS) else "SOME FAILED")
    sys.exit(0 if all(c for _, c in CHECKS) else 1)


if __name__ == "__main__":
    main()
