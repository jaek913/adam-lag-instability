"""E2 statistic: leads, censoring, contrasts, joint resampling and label (DESIGN D.2-D.3 E2;
Amendment 1 A1.4: scan window of SCAN/grid + 1 observations ending at t_e^g; censored lead = SCAN).

A series is given as a list of blocks; each block is (first_step, alarm) where alarm[i] is the
alarm state at step first_step + i*grid. Units: steps.
"""
import numpy as np

DETECTORS = ["D_div", "B1", "B2", "B3", "B4"]
BASELINES = ["B1", "B2", "B3", "B4"]


def alarm_at(blocks, step, grid):
    for first, alarm in blocks:
        i, r = divmod(step - first, grid)
        if r == 0 and 0 <= i < len(alarm):
            return bool(alarm[i])
    return None                                       # step not on any block


def lead(blocks, t_e, grid, scan):
    """Lead for one event (Amendment 1 A1.4 / G3). Returns (lead, censored, detected)."""
    teg = grid * (t_e // grid)
    ws = teg - scan
    before = alarm_at(blocks, ws - grid, grid)
    if alarm_at(blocks, ws, grid) and before:
        return scan, True, True
    for st in range(ws, teg + 1, grid):
        if alarm_at(blocks, st, grid):
            return teg - st, False, True
    return 0, False, False


def leads_table(alarms_by_detector, events, grid, scan):
    """alarms_by_detector[d][series] -> blocks. events: list of dicts with t_e, series.
    Returns {d: (leads array, censored array, detected array)} over the given events."""
    out = {}
    for d, by_series in alarms_by_detector.items():
        L, C, D = [], [], []
        for e in events:
            l, c, det = lead(by_series[e["series"]], e["t_e"], grid, scan)
            L.append(l)
            C.append(c)
            D.append(det)
        out[d] = (np.array(L, float), np.array(C, bool), np.array(D, bool))
    return out


def contrasts(lead_arrays, idx=None):
    """C_b = mean lead(D_div) - mean lead(B_b); returns (C dict, C_min)."""
    sel = (lambda a: a) if idx is None else (lambda a: a[idx])
    md = sel(lead_arrays["D_div"]).mean()
    C = {b: float(md - sel(lead_arrays[b]).mean()) for b in BASELINES}
    return C, min(C.values())


def resample(lead_arrays, n_draws, rng):
    """Joint resamples of events with replacement; C_min within each resample; argmax counts."""
    n = len(lead_arrays["D_div"])
    cmins = np.empty(n_draws)
    argmax = {d: 0 for d in DETECTORS}
    for r in range(n_draws):
        idx = rng.integers(0, n, size=n)
        _, cmins[r] = contrasts(lead_arrays, idx)
        means = {d: lead_arrays[d][idx].mean() for d in DETECTORS}
        top = max(means.values())
        winners = [d for d in DETECTORS if means[d] == top]
        for w in winners:
            argmax[w] += 1.0 / len(winners)
    return cmins, {d: argmax[d] / n_draws for d in DETECTORS}


def label(cmin_point, cmins):
    """D.3 E2 outcome partition (INSUFFICIENT EVENTS is decided before this, by P-KLAD)."""
    if cmin_point <= 0:
        return "REFUTE", None
    p05 = float(np.percentile(cmins, 5))              # numpy default (linear); construction item 5
    return ("SUPPORT" if p05 > 0 else "INCONCLUSIVE"), p05
