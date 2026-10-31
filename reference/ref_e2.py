"""Independent reference implementation of the E2 chain (DESIGN.md D.0-D.3, D.5, D.7,
Amendments 1-9), written from DESIGN.md (MD5 92d33da52ad20b4c25f9ceb12e00d36f) only.

Plain per-observation loops by design. Every interpretation is listed in NOTES.md
(cited here as [Nk]).

Units: one "observation" is one grid point of a block. Windows, hold, minimum history
and B1/B3/B4 windows are counted in observations (Amendment 1 A1.2, Amendment 5.2).
Scan window and leads are in steps (A1.4).
"""

import math
from bisect import bisect_right, insort
from fractions import Fraction

import numpy as np

DETECTORS = ["D_div", "B1", "B2", "B3", "B4"]
BASELINES = ["B1", "B2", "B3", "B4"]

# Frozen constants (D.2, D.7, Amendment 1 A1.2, Amendment 5.2).
FROZEN = {
    "min_hist": 1000,      # Amendment 5.2 "Minimum history"
    "w_f": 32,             # D.2 fast SMA
    "w_s": 128,            # D.2 slow SMA
    "b1_win": 50,          # P-B1
    "b3_alpha": 0.97,      # D.2 B3 / Amendment 5.2
    "b3_warm": 25,         # D.2 B3 / Amendment 5.2
    "b3_eps": 1e-6,        # Amendment 5.2 B3
    "b4_win": 200,         # D.2 B4
    "b4_minobs": 30,       # D.2 B4 / Amendment 5.2
    "b4_k": 1.0,           # D.2 B4
    "b4_mad_c": 1.4826,    # D.2 B4
    "b4_floor": 1e-12,     # Amendment 5.2 B4
    "b4_warm_after_reset": False,  # Amendment 9.1: no warm-up after a reset [N12]
    "headline_fa": 1.0,    # D.2 / A1.2
}


# ----------------------------------------------------------------------------------
# Block preparation (D.2 Observable, F15; Amendment 1 A1.1 G6; Amendment 5.2 j rule)
# ----------------------------------------------------------------------------------

def is_dropped(v):
    """A reading is dropped if null, non-finite or <= 0 (D.2, A1.1 G6) [N2]."""
    if v is None:
        return True
    try:
        x = float(v)
    except (TypeError, ValueError):
        return True
    if not math.isfinite(x):
        return True
    return x <= 0.0


def prepare_block(block, grid):
    """Return the series of one gap-free block, or None if every reading is dropped.

    The series starts at the first non-dropped reading (j = 0); leading dropped readings
    are not part of the series [N3]. Later dropped readings are carried forward (g and y)
    and count toward j (Amendment 5.2) [N4].
    """
    first_step = int(block["first_step"])
    raw = list(block["g"])
    start = None
    for i in range(len(raw)):
        if not is_dropped(raw[i]):
            start = i
            break
    if start is None:
        return None
    steps, g, y, dropped = [], [], [], []
    last_g = None
    last_y = None
    for i in range(start, len(raw)):
        if is_dropped(raw[i]):
            gi = last_g
            yi = last_y
            d = True
        else:
            gi = float(raw[i])
            yi = math.log(gi)
            d = False
        steps.append(first_step + i * grid)
        g.append(gi)
        y.append(yi)
        dropped.append(d)
        last_g = gi
        last_y = yi
    return {"steps": steps, "g": g, "y": y, "dropped": dropped, "n": len(steps)}


# ----------------------------------------------------------------------------------
# Detector scores. Each returns a list, one entry per observation j; None = undefined.
# A score is defined only at j >= min_hist (Amendment 5.2), whatever the warm-up.
# ----------------------------------------------------------------------------------

def mean_exact(xs):
    return math.fsum(xs) / len(xs)  # [N7]


def score_ddiv(y, w_f, w_s, min_hist):
    """Amendment 5.2 D_div: SMAs include the current observation; D defined j >= w_s-1;
    P_D(j) = #{s in [w_s-1, j]: D(s) <= D(j)} / #{s in [w_s-1, j]} (ties count)."""
    n = len(y)
    out = [None] * n
    history = []  # sorted D(s), s = w_s-1 .. j  (history includes j < min_hist) [N8]
    for j in range(n):
        if j < w_s - 1:
            continue
        sma_f = mean_exact(y[j - w_f + 1: j + 1])
        sma_s = mean_exact(y[j - w_s + 1: j + 1])
        d = sma_f - sma_s
        insort(history, d)
        count_le = bisect_right(history, d)
        p = count_le / len(history)
        if j >= min_hist:
            out[j] = p
    return out


def score_b1(y, win, min_hist):
    """Amendment 5.2 B1: mean and sample SD (ddof=1) of y over j-win .. j-1 (current
    excluded); sd = 0 -> undefined [N9]."""
    n = len(y)
    out = [None] * n
    for j in range(n):
        if j < win or j < min_hist:
            continue
        w = y[j - win: j]
        all_equal = True
        for x in w:
            if x != w[0]:
                all_equal = False
                break
        if all_equal:
            continue  # sd = 0 -> undefined, treated as no alarm
        m = mean_exact(w)
        var = math.fsum([(x - m) * (x - m) for x in w]) / (win - 1)
        sd = math.sqrt(var)
        if sd == 0.0:
            continue
        out[j] = (y[j] - m) / sd
    return out


def score_b2(y, min_hist):
    """D.2 / Amendment 5.2 B2: s_2(j) = y(j)."""
    out = [None] * len(y)
    for j in range(len(y)):
        if j >= min_hist:
            out[j] = y[j]
    return out


def score_b3(g, alpha, warm, eps, min_hist):
    """Amendment 5.2 B3 (ZClip 1.0.0 zscore mode, monitor mode) on g (carried-forward g
    at dropped observations). Update weight is the float64 expression (1 - alpha)
    (Amendment 9.2) [N10]."""
    n = len(g)
    out = [None] * n
    buf = []
    mu = None
    v = None
    for j in range(n):
        gj = g[j]
        if mu is None:
            buf.append(gj)
            if len(buf) == warm:
                mu = mean_exact(buf)
                v = math.fsum([(x - mu) * (x - mu) for x in buf]) / len(buf)  # ddof 0
            continue  # warm-up observations (including the 25th) have no score
        s = (gj - mu) / (math.sqrt(v) + eps)  # mu, v before the update
        if j >= min_hist:
            out[j] = s
        mu = alpha * mu + (1.0 - alpha) * gj
        v = alpha * v + (1.0 - alpha) * ((gj - mu) * (gj - mu))  # uses updated mu [N36]
    return out


def b4_robust_z(y, win, minobs, mad_c, floor):
    """Amendment 5.2 / 9.1 B4 robust z. The median/MAD history is never cleared by a reset
    (only by a gap = new block) and every observation is appended, so z(j) does not
    depend on theta; it is computed once [N13]. z[j] is None while the history holds
    fewer than minobs values."""
    n = len(y)
    z = [None] * n
    hist = []
    for j in range(n):
        if len(hist) >= minobs:
            arr = np.array(hist[-win:], dtype=float)
            m = float(np.median(arr))
            mad = float(np.median(np.abs(arr - m)))
            sigma = mad_c * mad
            if sigma < floor:
                sigma = floor
            z[j] = (y[j] - m) / sigma
        hist.append(y[j])
        if len(hist) > win:
            hist = hist[-win:]
    return z


# ----------------------------------------------------------------------------------
# Alarm onset and hold (P-HOLD, D.2; Amendment 7.3)
# ----------------------------------------------------------------------------------

def simulate_alarm(scores, theta, hold):
    """Onset at j iff not in alarm, s(j) defined and >= theta, and s(j-1) < theta or
    undefined/absent. Each onset holds [j, j+hold-1]. Returns (onset indices, alarm)."""
    n = len(scores)
    alarm = [False] * n
    onsets = []
    alarm_end = -1
    for j in range(n):
        s = scores[j]
        s_prev = scores[j - 1] if j > 0 else None
        if j > alarm_end and s is not None and s >= theta and (s_prev is None or s_prev < theta):
            onsets.append(j)
            alarm_end = j + hold - 1
        alarm[j] = j <= alarm_end
    return onsets, alarm


def b4_path(z, theta, hold, k, minobs, min_hist, warm_after_reset):
    """B4 score path and alarm state at theta (theta = inf gives the reset-free path).
    S+ <- max(0, S+ + z - k); reset to 0 at each onset (Amendment 9.1: the history is
    kept and scoring continues at the next observation from S+ = 0) [N12].
    warm_after_reset=True reproduces the superseded literal 5.2 reading (not used)."""
    n = len(z)
    scores = [None] * n
    alarm = [False] * n
    onsets = []
    alarm_end = -1
    S = 0.0
    warm_left = 0
    for j in range(n):
        s = None
        if z[j] is not None:
            if warm_left > 0:
                warm_left -= 1
            else:
                S = max(0.0, S + z[j] - k)
                if j >= min_hist:
                    s = S
        scores[j] = s
        s_prev = scores[j - 1] if j > 0 else None
        if j > alarm_end and s is not None and s >= theta and (s_prev is None or s_prev < theta):
            onsets.append(j)
            alarm_end = j + hold - 1
            S = 0.0
            if warm_after_reset:
                warm_left = minobs
        alarm[j] = j <= alarm_end
    return scores, onsets, alarm


# ----------------------------------------------------------------------------------
# Matching helpers (D.2 P-FA as replaced by Amendment 6.1; Amendment 7.1)
# ----------------------------------------------------------------------------------

def nstar_of(fa, n_out):
    """n* = round-half-up(FA x N_out / 10,000) = floor(x + 0.5) (A1.11(a)) [N16]."""
    x = Fraction(str(fa)) * n_out / 10000
    return math.floor(x + Fraction(1, 2))


def top_scan(cands_desc, count_fn, nstar):
    """Amendment 6.1: scan candidates from the highest down; stop at the first with
    c > n*; theta = the candidate immediately above it; if the highest already has
    c > n*, not matchable (theta = inf); if none exceeds, theta = lowest candidate.
    Returns (theta, matchable, n_scanned)."""
    if len(cands_desc) == 0:
        return math.inf, False, 0  # [N19]
    for idx in range(len(cands_desc)):
        c = count_fn(cands_desc[idx], nstar)
        if c > nstar:
            if idx == 0:
                return math.inf, False, 1
            return cands_desc[idx - 1], True, idx + 1
    return cands_desc[-1], True, len(cands_desc)


# ----------------------------------------------------------------------------------
# Main
# ----------------------------------------------------------------------------------

def run_reference(blocks, events, fa=1.0, grid=10, scan=1280, hold=32, thetas=None):
    return _run(blocks, events, fa, grid, scan, hold, thetas, FROZEN)


def _run(blocks, events, fa, grid, scan, hold, thetas, P):
    min_hist = P["min_hist"]

    # --- block preparation -------------------------------------------------------
    series = []
    for b in blocks:
        s = prepare_block(b, grid)
        if s is not None:
            series.append(s)

    # --- scan windows of ALL events (eligible or not) (D.2 F18, A1.4, A1.11(b)) ----
    windows = []
    for ev in events:
        teg = grid * math.floor(int(ev["t_e"]) / grid)  # A1.4 anchor [N25]
        windows.append((teg - scan, teg))

    # --- N_out (Amendment 7.2): j >= min_hist and outside every scan window -------
    N_out = 0
    for s in series:
        out_mask = [False] * s["n"]
        for j in range(s["n"]):
            if j < min_hist:
                continue
            st = s["steps"][j]
            inside = False
            for (lo, hi) in windows:
                if lo <= st <= hi:
                    inside = True
                    break
            if not inside:
                out_mask[j] = True
                N_out += 1
        s["out_mask"] = out_mask

    nstar = nstar_of(fa, N_out)
    if nstar == 0:
        return {"N_out": N_out, "nstar": nstar, "label": "UNRUN (n* = 0)"}

    # --- scores ------------------------------------------------------------------
    for s in series:
        y, g = s["y"], s["g"]
        s["score"] = {
            "D_div": score_ddiv(y, P["w_f"], P["w_s"], min_hist),
            "B1": score_b1(y, P["b1_win"], min_hist),
            "B2": score_b2(y, min_hist),
            "B3": score_b3(g, P["b3_alpha"], P["b3_warm"], P["b3_eps"], min_hist),
        }
        s["b4_z"] = b4_robust_z(y, P["b4_win"], P["b4_minobs"], P["b4_mad_c"], P["b4_floor"])

    def path_at(s, det, theta):
        """(scores, onset indices, alarm) of detector det on series s at theta."""
        if det == "B4":
            return b4_path(s["b4_z"], theta, hold, P["b4_k"], P["b4_minobs"], min_hist,
                           P["b4_warm_after_reset"])
        sc = s["score"][det]
        on, al = simulate_alarm(sc, theta, hold)
        return sc, on, al

    def out_onsets(det, theta, limit=None):
        """Out-of-window onset count at theta; stops early once count > limit."""
        c = 0
        for s in series:
            _, on, _ = path_at(s, det, theta)
            for j in on:
                if s["out_mask"][j]:
                    c += 1
                    if limit is not None and c > limit:
                        return c
        return c

    # step -> (series index, j) lookup for leads
    where = {}
    for si in range(len(series)):
        for j in range(series[si]["n"]):
            where[series[si]["steps"][j]] = (si, j)

    eligible_events = [ev for ev in events if bool(ev["eligible"])]

    # eligibility re-check (A1.4 equivalent form) - reported, not enforced [N26]
    elig_check = []
    for ev in eligible_events:
        teg = grid * math.floor(int(ev["t_e"]) / grid)
        lo = teg - scan
        ok = lo in where and teg in where
        if ok:
            si_lo, j_lo = where[lo]
            si_hi, _ = where[teg]
            ok = (si_lo == si_hi) and j_lo >= min_hist
        elig_check.append(ok)

    result = {"N_out": N_out, "nstar": nstar}
    fa_not_matchable = (Fraction(str(fa)) != Fraction(str(P["headline_fa"]))) and nstar < 2
    result["fa_point_not_matchable_G1"] = fa_not_matchable
    result["eligibility_check"] = elig_check

    mean_leads = {}
    for det in DETECTORS:
        # ---- theta ----
        if thetas is not None:
            theta = float(thetas[det])
            n_scanned = None
        else:
            # candidates: distinct values on out-of-window scored observations;
            # B4 from its reset-free path (Amendment 7.1)
            cand_set = set()
            for s in series:
                sc, _, _ = path_at(s, det, math.inf)
                for j in range(s["n"]):
                    if s["out_mask"][j] and sc[j] is not None:
                        cand_set.add(sc[j])
            cands_desc = sorted(cand_set, reverse=True)
            theta, _, n_scanned = top_scan(
                cands_desc, lambda v, lim, d=det: out_onsets(d, v, lim), nstar)
        matchable = math.isfinite(theta)

        # ---- path at theta: onsets, realised count, coverage ----
        onset_steps = []
        realised = 0
        cover_num = 0
        alarms = []
        for s in series:
            sc, on, al = path_at(s, det, theta)
            alarms.append(al)
            for j in on:
                onset_steps.append(s["steps"][j])
                if s["out_mask"][j]:
                    realised += 1
            for j in range(s["n"]):
                if s["out_mask"][j] and sc[j] is not None and sc[j] >= theta:
                    cover_num += 1
        onset_steps.sort()
        coverage = cover_num / N_out

        # ---- leads (D.2 P-MISS/P-CENS, A1.4, Amendment 7.6) ----
        leads, censored, detected, concurrent, miss = [], [], [], [], []
        for ev in eligible_events:
            teg = grid * math.floor(int(ev["t_e"]) / grid)
            lo = teg - scan
            first = None
            st = lo
            while st <= teg:
                if st in where:
                    si, j = where[st]
                    if alarms[si][j]:
                        first = st
                        break
                st += grid
            cens = False
            if first is None:
                lead = 0
            else:
                lead = teg - first
                if first == lo:
                    prev = lo - grid
                    if prev in where:
                        si, j = where[prev]
                        if alarms[si][j]:
                            cens = True
                    lead = scan  # = teg - lo
            leads.append(lead)
            censored.append(cens)
            detected.append(lead > 0)
            concurrent.append(first is not None and first == teg)
            miss.append(first is None)
        mean_leads[det] = (math.fsum(leads) / len(leads)) if leads else None

        result[det] = {
            "theta": theta,
            "realised": realised,
            "shortfall": nstar - realised,
            "matchable": matchable,
            "coverage": coverage,
            "coverage_stop": coverage > 0.10,  # Amendment 6.2 (meaningful at headline FA)
            "candidates_scanned": n_scanned,
            "onsets": onset_steps,
            "leads": leads,
            "censored": censored,
            "detected": detected,
            "concurrent": concurrent,
            "miss": miss,
        }

    # ---- C_b and C_min (D.3 E2) ----
    C = {}
    if fa_not_matchable or mean_leads["D_div"] is None:
        for b in BASELINES:
            C[b] = None
        C_min = None
    else:
        for b in BASELINES:
            C[b] = mean_leads["D_div"] - mean_leads[b]
        C_min = min(C[b] for b in BASELINES)
    result["C"] = C
    result["C_min"] = C_min
    return result
