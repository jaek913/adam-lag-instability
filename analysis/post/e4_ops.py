"""E4 sensitivity operators (DESIGN D.3 E4; D.7 pins P-B3, P-B4). Kept outside analysis/ops.py so the E2 code is
unchanged. Each has a loop reference; scripts/tests/test_e4_ops.py asserts equality.
- score_b3_adjusted: ZClip 1.0.0 default (mode "zscore", clip_option "adaptive_scaling", clip_factor 1.0): when
  z > 2.5 the EMA is updated with clip_val = mean + (2.5*std)/(z/2.5) instead of the raw g (vendored
  scripts/tests/third_party/zclip_1_0_0/zclip.py, _compute_clip_val and step; std without eps, as in the source).
- B4 two-sided (trainscope ChangePointDetector @0651b25): S+ = max(0, S+ + z - k), S- = min(0, S- + z + k);
  score = max(S+, |S-|); alarm onset on a fresh crossing; both accumulators reset at each onset (P-B4).
- B4 on g: the same robust z computed on g = exp(y) instead of y."""
import math

import numpy as np

import ops


def score_b3_adjusted(g, alpha=ops.B3_ALPHA, warmup=ops.B3_WARMUP, eps=ops.B3_EPS, z_thresh=2.5):
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
        std = var ** 0.5
        z = (x - mean) / (std + eps)
        out[j] = z
        upd = x
        if z > z_thresh:
            upd = mean + (z_thresh * std) / (z / z_thresh)
        mean = alpha * mean + (1 - alpha) * upd
        var = alpha * var + (1 - alpha) * (upd - mean) ** 2
    return ops._gate(out)


def b4_free_state_2s(z, k=ops.B4_K):
    n = len(z)
    zl = np.asarray(z, dtype=float).tolist()
    st, sc = [(math.nan, math.nan)] * n, [math.nan] * n
    sp, sn = 0.0, 0.0
    for j in range(n):
        zj = zl[j]
        if zj == zj:
            sp = max(0.0, sp + (zj - k))
            sn = min(0.0, sn + (zj + k))
            if j >= ops.MIN_HIST:
                sc[j] = max(sp, -sn)
        st[j] = (sp, sn)
    return st, np.array(sc)


def b4_alarm_2s(z, theta=None, hold=ops.HOLD, k=ops.B4_K, free=None):
    """Two-sided analogue of ops.b4_alarm (same merge-with-free-path construction)."""
    n = len(z)
    st_free, s_free = b4_free_state_2s(z, k) if free is None else free
    if theta is None:
        return s_free.copy(), np.array([], dtype=np.int64), np.zeros(n, bool)
    zl = np.asarray(z, dtype=float).tolist()
    sl = s_free.copy()
    ge = np.where(np.isnan(s_free), False, s_free >= theta)
    cross = np.nonzero(ge & ~np.concatenate([[False], ge[:-1]]))[0]
    onsets, alarm = [], np.zeros(n, bool)
    m, busy = ops.MIN_HIST - 1, -1
    while True:
        start = max(m + 1, busy + 1)
        i = int(np.searchsorted(cross, start))
        if i >= len(cross):
            break
        j = int(cross[i])
        merged_at = None
        while True:
            onsets.append(j)
            busy = j + hold - 1
            alarm[j:min(n, j + hold)] = True
            sp, sn, prev, u, fired = 0.0, 0.0, sl[j], j + 1, None
            while u < n:
                zu = zl[u]
                if zu != zu:
                    u += 1
                    continue
                sp = max(0.0, sp + (zu - k))
                sn = min(0.0, sn + (zu + k))
                s = max(sp, -sn)
                sl[u] = s
                if u > busy and s >= theta and not (prev >= theta):
                    fired = u
                    break
                prev = s
                if (sp, sn) == st_free[u]:
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


def b4_alarm_2s_loop(z, theta=None, hold=ops.HOLD, k=ops.B4_K):
    n = len(z)
    zl = np.asarray(z, dtype=float).tolist()
    sl = [math.nan] * n
    sp = sn = 0.0
    onsets, alarm = [], np.zeros(n, bool)
    busy, prev = -1, math.nan
    for j in range(n):
        zj = zl[j]
        if zj != zj:
            continue
        sp = max(0.0, sp + (zj - k))
        sn = min(0.0, sn + (zj + k))
        if j < ops.MIN_HIST:
            continue
        s = max(sp, -sn)
        sl[j] = s
        if theta is not None and j > busy and s >= theta and not (prev >= theta):
            onsets.append(j)
            busy = j + hold - 1
            alarm[j:min(n, j + hold)] = True
            sp = sn = 0.0
        prev = sl[j]
    return np.array(sl), np.array(onsets, dtype=np.int64), alarm


_B4_Z = ops.b4_z                                         # bound at import, so patching ops.b4_z cannot recurse


def b4_z_on_g(y, *a, **kw):
    return _B4_Z(np.exp(np.asarray(y, dtype=float)), *a, **kw)
