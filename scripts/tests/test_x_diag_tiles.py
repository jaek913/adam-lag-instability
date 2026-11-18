"""DECISIONS 62: control tiles for X1 are disjoint, have the history floor, and clear every event window."""
import os
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
sys.path.insert(0, os.path.join(ROOT, "analysis", "post"))
import ops  # noqa: E402
import x_diag  # noqa: E402


def _blocks():
    return [{"first_step": 10, "y": np.zeros(5000), "g": np.zeros(5000)},
            {"first_step": 100010, "y": np.zeros(700), "g": np.zeros(700)}]


def test_disjoint_floor_and_clearance():
    ev = [{"t_e": 10 + 10 * 2500, "eligible": True}, {"t_e": 10 + 10 * 4000 + 3, "eligible": False}]
    pts, n_excl = x_diag.control_tiles(_blocks(), ev)
    assert pts and all(k == 0 for k, _ in pts)           # block 1 too short for the history floor
    a = sorted(i for _, i in pts)
    assert all(b - c >= x_diag.TILE for c, b in zip(a, a[1:]))          # disjoint windows
    assert all(i >= ops.MIN_HIST + 228 for i in a)                       # history floor
    for i in a:
        s0, s1 = 10 + 10 * (i - x_diag.TILE + 1), 10 + 10 * i
        for e in ev:
            t = 10 * (e["t_e"] // 10)
            assert s1 < t - x_diag.SCAN or s0 > t + x_diag.POST          # clear of scan + aftermath
    assert n_excl > 0


def test_tile_boundary_exact():
    # an event whose aftermath ends exactly one step before a tile starts leaves that tile in
    b = [{"first_step": 0, "y": np.zeros(3000), "g": np.zeros(3000)}]
    j = 10                                                # tile 10 = obs 2280..2507 -> steps 22800..25070
    t = 22800 - x_diag.POST - 10
    pts, _ = x_diag.control_tiles(b, [{"t_e": t, "eligible": True}])
    assert (0, j * x_diag.TILE + x_diag.TILE - 1) in pts
    pts2, _ = x_diag.control_tiles(b, [{"t_e": t + 10, "eligible": True}])
    assert (0, j * x_diag.TILE + x_diag.TILE - 1) not in pts2


if __name__ == "__main__":
    test_disjoint_floor_and_clearance()
    test_tile_boundary_exact()
    print("test_x_diag_tiles: 2 passed")
