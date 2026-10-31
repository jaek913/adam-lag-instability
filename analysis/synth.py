"""D.5 synthetic series generator (DESIGN D.5 as amended by Amendments 7.7 and 8.2).

Every draw comes from a numpy Generator built from one SeedSequence child (Amendment 8.2(14)).
Units: observations (per-step cells: one observation per step).
"""
import numpy as np

L_MAX = 200


def child_rng(index, root=20261030):
    """Generator for the cell x replicate with fixed child index `index` (Amendment 8.2(14)).
    Equivalent to SeedSequence(root).spawn(N)[index] for any N > index."""
    return np.random.default_rng(np.random.SeedSequence(root, spawn_key=(index,)))   # == spawn(N)[index]


def ar1(rng, n, phi, innov="gauss"):
    """AR(1), mean 0, unit stationary SD (Amendment 8.2(11)). innov: 'gauss' or 't3'
    (Student-t df 3 scaled to unit variance)."""
    sd_e = np.sqrt(1.0 - phi ** 2)
    if innov == "gauss":
        e = rng.standard_normal(n)
    elif innov == "t3":
        e = rng.standard_t(3, n) / np.sqrt(3.0)
    else:
        raise ValueError(innov)
    x = np.empty(n)
    x[0] = e[0]                                         # stationary start: unit SD
    e = e * sd_e
    for i in range(1, n):
        x[i] = phi * x[i - 1] + e[i]
    return x


def place_events(rng, n, n_events, scan, l_max=L_MAX, min_hist=1000):
    """Uniform random event times with consecutive spacing >= scan + l_max + 1 and the first
    t_e >= min_hist + scan + l_max (Amendment 8.2(9)). Exact uniform draw over admissible
    configurations via the gap-transform: choose sorted points in a reduced range, add offsets."""
    gap = scan + l_max + 1
    lo = min_hist + scan + l_max
    hi = n - 1 - 50                                     # room for the 8.2(10) surge after the last event
    span = hi - lo - (n_events - 1) * (gap - 1)
    if span < n_events:
        raise ValueError("series too short for the event count")
    base = np.sort(rng.choice(span, size=n_events, replace=False))
    return [int(lo + b + i * (gap - 1)) for i, b in enumerate(base)]


def ramp(n, t_events, L, A):
    """Linear rise 0 -> A over the L observations ending at t_e (Amendment 7.7)."""
    r = np.zeros(n)
    step = A * np.arange(1, L + 1) / L
    for t in t_events:
        r[t - L + 1:t + 1] += step
    return r


def surge(n, t_events, height=3.0, length=50):
    """+3 SD at t_e decaying linearly to 0 over 50 observations (Amendment 8.2(10))."""
    s = np.zeros(n)
    prof = height * (length - np.arange(length)) / length
    for t in t_events:
        m = min(length, n - t)
        s[t:t + m] += prof[:m]
    return s


def pulses(rng, n, t_events, h, scan):
    """One-observation pulse of height h at a uniform offset in [1, scan] before each event (8.2(13))."""
    p = np.zeros(n)
    for t in t_events:
        p[t - int(rng.integers(1, scan + 1))] += h
    return p


def make_series(index, *, n=50000, phi, n_events, L=None, A=0.0, innov="gauss", surge_on=False,
                pulse_h=None, scan=128):
    """One replicate. Returns (blocks, events) in the pipeline/reference input format, plus meta."""
    rng = child_rng(index)
    x = ar1(rng, n, phi, innov)
    t_ev = place_events(rng, n, n_events, scan)
    y = x.copy()
    if L is not None and A:
        y += ramp(n, t_ev, L, A)
    if surge_on:
        y += surge(n, t_ev)
    if pulse_h is not None:
        y += pulses(rng, n, t_ev, pulse_h, scan)
    g = np.exp(y)
    blocks = [{"first_step": 0, "y": y, "g": g}]
    events = [{"t_e": t, "eligible": True} for t in t_ev]
    return blocks, events
