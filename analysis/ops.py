"""Leg A detector operators, alarm state and threshold matching.

Implements DESIGN D.2 as amended (Amendment 1: units = observations; Amendment 5: construction
details; Amendment 6: P-FA top scan). One function per operator; every function works on ONE
gap-free block of observations (gaps reset all state, D.2 "Gaps and state").

Conventions (Amendment 5.2):
  - j = 0 is the first non-dropped observation of the block; dropped observations are carried
    forward BEFORE calling these functions and still count toward j.
  - A score is defined only at j >= MIN_HIST (1,000); np.nan elsewhere. nan = undefined = no alarm.
"""
import math
from collections import deque

import numpy as np

MIN_HIST = 1000
W_F, W_S = 32, 128
B1_W = 50
B3_ALPHA, B3_WARMUP, B3_EPS = 0.97, 25, 1e-6
B4_WINDOW, B4_MINOBS, B4_K, B4_FLOOR = 200, 30, 1.0, 1e-12
HOLD = 32


def _gate(s):
    s = np.asarray(s, dtype=float).copy()
    s[:MIN_HIST] = np.nan
    return s


# ------------------------------------------------------------------ D_div
def sma_incl(y, w):
    """Mean of y[j-w+1 .. j] (current included); nan for j < w-1."""
    y = np.asarray(y, dtype=float)
    out = np.full(len(y), np.nan)
    if len(y) >= w:
        c = np.concatenate([[0.0], np.cumsum(y)])
        out[w - 1:] = (c[w:] - c[:-w]) / w
    return out


def divergence(y, wf=W_F, ws=W_S):
    return sma_incl(y, wf) - sma_incl(y, ws)


def expanding_percentile_le(d, start):
    """P(j) = #{s in [start, j]: d[s] <= d[j]} / (j - start + 1), for j >= start; nan before.
    Exact, O(n log n) via a Fenwick tree over value ranks (ties counted as <=)."""
    n = len(d)
    out = np.full(n, np.nan)
    if n <= start:
        return out
    vals = d[start:]
    uniq = np.unique(vals)
    rank = np.searchsorted(uniq, vals) + 1          # 1-based rank; equal values share a rank
    tree = np.zeros(len(uniq) + 1, dtype=np.int64)
    for i, r in enumerate(rank):
        k = r
        while k <= len(uniq):
            tree[k] += 1
            k += k & -k
        k, cnt = r, 0
        while k > 0:
            cnt += tree[k]
            k -= k & -k
        out[start + i] = cnt / (i + 1)
    return out


def score_div(y, wf=W_F, ws=W_S):
    d = divergence(y, wf, ws)
    return _gate(expanding_percentile_le(d, ws - 1))


# ------------------------------------------------------------------ B1, B2
def score_b1(y, w=B1_W):
    """(y[j] - mean(y[j-w..j-1])) / sd(ddof=1); current EXCLUDED; nan where sd == 0."""
    y = np.asarray(y, dtype=float)
    n = len(y)
    out = np.full(n, np.nan)
    if n > w:
        c1 = np.concatenate([[0.0], np.cumsum(y)])
        c2 = np.concatenate([[0.0], np.cumsum(y * y)])
        j = np.arange(w, n)
        s1 = c1[j] - c1[j - w]
        s2 = c2[j] - c2[j - w]
        mean = s1 / w
        var = (s2 - s1 * s1 / w) / (w - 1)
        # exact recomputation where the fast variance is tiny (cancellation guard)
        small = var <= 1e-12 * (np.abs(mean) + 1.0) ** 2
        for idx in np.nonzero(small)[0]:
            jj = j[idx]
            var[idx] = np.var(y[jj - w:jj], ddof=1)
        sd = np.sqrt(np.maximum(var, 0.0))
        with np.errstate(divide="ignore", invalid="ignore"):
            z = (y[j] - mean) / sd
        z[sd == 0] = np.nan
        out[w:] = z
    return _gate(out)


def b1_sd_zero_count(y, w=B1_W):
    s = score_b1(y, w)
    return int(np.isnan(s[MIN_HIST:]).sum()) if len(y) > MIN_HIST else 0


def score_b2(y):
    return _gate(np.asarray(y, dtype=float))


# ------------------------------------------------------------------ B3 (ZClip 1.0.0, monitor mode)
def score_b3(g, alpha=B3_ALPHA, warmup=B3_WARMUP, eps=B3_EPS):
    g = np.asarray(g, dtype=float)
    out = np.full(len(g), np.nan)
    buf, mean, var = [], None, None
    for j, x in enumerate(g):
        if mean is None:
            buf.append(x)
            if len(buf) >= warmup:
                mean = sum(buf) / len(buf)
                var = sum((b - mean) ** 2 for b in buf) / len(buf)
            continue
        out[j] = (x - mean) / (var ** 0.5 + eps)
        mean = alpha * mean + (1 - alpha) * x
        var = alpha * var + (1 - alpha) * (x - mean) ** 2      # uses the UPDATED mean (as coded)
    return _gate(out)


# ------------------------------------------------------------------ alarm state (P-HOLD)
def alarm_from_scores(s, theta, hold=HOLD):
    """Onsets and alarm state for a score path that does not depend on theta (D_div, B1-B3).
    Onset at j: not in alarm, s[j] >= theta, and s[j-1] < theta (an undefined s[j-1], incl. the
    first scored observation, counts as below theta). Each onset holds the alarm for `hold`
    observations; no onset is counted while in alarm."""
    n = len(s)
    above = np.where(np.isnan(s), False, s >= theta)
    prev_above = np.concatenate([[False], above[:-1]])
    cross = np.nonzero(above & ~prev_above)[0]
    onsets, alarm = [], np.zeros(n, bool)
    busy_until = -1
    for j in cross:
        if j <= busy_until:
            continue
        onsets.append(int(j))
        busy_until = j + hold - 1
        alarm[j:min(n, j + hold)] = True
    return np.array(onsets, dtype=np.int64), alarm


def b4_z(y, window=B4_WINDOW, minobs=B4_MINOBS, floor=B4_FLOOR, chunk=4096):
    """trainscope ChangePointDetector @0651b25 robust z (theta-independent: a P-B4 reset clears
    S+ only, never the median/MAD history). z[j] = nan during the warm-up (j < minobs).
    Vectorised form of b4_z_loop (bit-identical; asserted in scripts/tests/test_ops.py): for
    j >= window the history is exactly y[j-window:j]; for minobs <= j < window it is y[:j]."""
    y = np.asarray(y, dtype=float)
    n = len(y)
    z = np.full(n, np.nan)
    for j in range(minobs, min(n, window)):
        h = y[:j]
        med = float(np.median(h))
        sd = max(float(np.median(np.abs(h - med))) * 1.4826, floor)
        z[j] = (y[j] - med) / sd
    if n > window:
        win = np.lib.stride_tricks.sliding_window_view(y[:-1], window)   # row r = y[r : r+window]
        for a in range(0, n - window, chunk):
            h = win[a:a + chunk]
            med = np.median(h, axis=1)
            sd = np.maximum(np.median(np.abs(h - med[:, None]), axis=1) * 1.4826, floor)
            z[window + a: window + a + len(h)] = (y[window + a: window + a + len(h)] - med) / sd
    return z


def b4_z_loop(y, window=B4_WINDOW, minobs=B4_MINOBS, floor=B4_FLOOR):
    """Reference loop transcription of trainscope's per-reading update (kept for the equality test)."""
    y = np.asarray(y, dtype=float)
    n = len(y)
    z = np.full(n, np.nan)
    hist = deque()
    for j in range(n):
        x = y[j]
        if len(hist) < minobs:
            hist.append(x)
            continue
        h = np.fromiter(hist, dtype=float, count=len(hist))
        med = float(np.median(h))
        mad = float(np.median(np.abs(h - med)))
        sd = mad * 1.4826
        if sd < floor:
            sd = floor
        z[j] = (x - med) / sd
        hist.append(x)
        if len(hist) > window:
            hist.popleft()
    return z


def b4_free_state(z, k=B4_K):
    """Reset-free S+: (state after each observation, gated score array). Same float arithmetic as
    b4_alarm_loop with theta=None."""
    n = len(z)
    zl = np.asarray(z, dtype=float).tolist()
    st, sc = [math.nan] * n, [math.nan] * n
    sp = 0.0
    for j in range(n):
        zj = zl[j]
        if zj == zj:
            sp = max(0.0, sp + (zj - k))
            if j >= MIN_HIST:
                sc[j] = sp
        st[j] = sp
    return np.array(st), np.array(sc)


def b4_alarm(z, theta=None, hold=HOLD, k=B4_K, free=None):
    """S+ recursion with P-B4 resets on a precomputed z. Returns (scores, onsets, alarm).
    Exact fast form of b4_alarm_loop (bit-identical; asserted in scripts/tests/test_ops.py).
    Up to the first onset the path IS the reset-free path. After each reset the restarted path is
    iterated with the same float arithmetic until its state equals the reset-free state exactly;
    from there the two recursions coincide, so the next onset is located on the reset-free path.
    free: optional precomputed b4_free_state(z, k)."""
    n = len(z)
    st_free, s_free = b4_free_state(z, k) if free is None else free
    if theta is None:
        return s_free.copy(), np.array([], dtype=np.int64), np.zeros(n, bool)
    zl = np.asarray(z, dtype=float).tolist()
    stl = st_free.tolist()
    sl = s_free.copy()
    ge = np.where(np.isnan(s_free), False, s_free >= theta)
    cross = np.nonzero(ge & ~np.concatenate([[False], ge[:-1]]))[0]   # fresh crossings on the free path
    onsets, alarm = [], np.zeros(n, bool)
    m, busy = MIN_HIST - 1, -1                         # path == free at every index >= m
    while True:
        start = max(m + 1, busy + 1)
        i = int(np.searchsorted(cross, start))
        if i >= len(cross):
            break
        j = int(cross[i])
        merged_at = None
        while True:                                    # onset at j, then the divergent stretch
            onsets.append(j)
            busy = j + hold - 1
            alarm[j:min(n, j + hold)] = True
            sp, prev, u, fired = 0.0, sl[j], j + 1, None
            while u < n:
                zu = zl[u]
                if zu != zu:
                    u += 1
                    continue
                sp = max(0.0, sp + (zu - k))
                sl[u] = sp
                if u > busy and sp >= theta and not (prev >= theta):
                    fired = u
                    break
                prev = sp
                if sp == stl[u]:
                    merged_at = u
                    break
                u += 1
            if fired is None:
                break
            j = fired
        if merged_at is None:
            break
        m = merged_at
    return sl, np.array(onsets, dtype=np.int64), alarm


def b4_alarm_loop(z, theta=None, hold=HOLD, k=B4_K):
    """Reference loop transcription (kept for the equality test). Returns (scores, onsets, alarm)."""
    n = len(z)
    zl = np.asarray(z, dtype=float).tolist()           # plain floats: same IEEE arithmetic, faster loop
    sl = [math.nan] * n
    sp = 0.0
    onsets, alarm = [], np.zeros(n, bool)
    busy_until, prev = -1, math.nan
    for j in range(n):
        zj = zl[j]
        if zj != zj:                                   # nan
            continue
        sp = max(0.0, sp + (zj - k))
        if j < MIN_HIST:
            continue                                   # score gated (Amendment 5.2)
        sl[j] = sp
        if theta is not None and j > busy_until and sp >= theta and not (prev >= theta):
            onsets.append(j)
            busy_until = j + hold - 1
            alarm[j:min(n, j + hold)] = True
            sp = 0.0                                   # P-B4: reset at each alarm onset
        prev = sl[j]
    return np.array(sl, dtype=float), np.array(onsets, dtype=np.int64), alarm


def b4_path(y, theta=None, hold=HOLD, k=B4_K, window=B4_WINDOW, minobs=B4_MINOBS, floor=B4_FLOOR):
    """trainscope ChangePointDetector @0651b25 (upward accumulator), with P-B4 resets.
    Returns (scores, onsets, alarm). theta=None -> no alarms, no resets (the reset-free path)."""
    return b4_alarm(b4_z(y, window, minobs, floor), theta, hold, k)


# ------------------------------------------------------------------ P-FA top scan (Amendment 6)
def match_threshold(onset_count, candidates, nstar):
    """Amendment 6.1: theta = smallest candidate v such that EVERY candidate u >= v has
    c(u) <= nstar. Scans candidates from the highest down; stops at the first c > nstar.
    onset_count(v) -> int. Returns dict(theta, realised, evaluated, matchable)."""
    cand = np.unique(np.asarray(candidates, dtype=float))[::-1]
    best, best_c, evaluated = None, None, 0
    for v in cand:
        c = onset_count(v)
        evaluated += 1
        if c > nstar:
            break
        best, best_c = v, c
    if best is None:
        return {"theta": math.inf, "realised": 0, "evaluated": evaluated, "matchable": False}
    return {"theta": float(best), "realised": int(best_c), "evaluated": evaluated, "matchable": True}


def round_half_up(x):
    return int(math.floor(x + 0.5))


# ------------------------------------------------------------------ block preparation (A1.1, Amendment 5.2)
def prepare_block(values, dropped):
    """Start the block at its first non-dropped reading (j = 0 there); carry every later dropped
    reading forward from the previous observation (it still counts toward j). Returns
    (values_cf, offset) where offset = number of leading dropped readings removed."""
    v = np.asarray(values, dtype=float)
    d = np.asarray(dropped, dtype=bool)
    ok = np.nonzero(~d)[0]
    if len(ok) == 0:
        return np.array([], dtype=float), len(v)
    off = int(ok[0])
    v = v[off:].copy()
    d = d[off:]
    for i in range(1, len(v)):
        if d[i]:
            v[i] = v[i - 1]
    return v, off
