"""Amendment 15.8 checks (b) and (c), synthetic only, reported. Seeds: diagnostic range 44,000,000+ (seed map): cell k uses 44,000,000 + k*2000 + {0-19 population, 100-199 L=75, 300-399 L=125}.
(b) theta fixed at its population value: at the 14.3 ramps (L = 75, 125 observations, A = 6), per phi_y and grid
    (per-step; grid 10), the 10-90% range of per-replicate mean lead with each replicate's own P-FA-matched theta, and
    with theta fixed at the cell's population value = median of the finite matched thetas over that cell's 100
    replicates. Reports whether D_div's spread collapses while the baselines' does not.
    The null-series population (R_POP null series per phi_y and grid) is also matched and reported: D_div's matched
    theta is often non-finite there (its divergence percentile reaches its ceiling outside the scan more often than
    the P-FA budget allows), so a null-series population value is undefined for D_div; see the table it writes.
    (v1 of this script fixed theta at the null-series median, which was infinite for D_div; superseded, not reported.)
(c) per-event D_div lead regressed on history length since the series/gap start (observations), matched theta;
    slope and R^2 pooled per cell; B2 alongside for comparison.
Writes verification/ddiv_response_15_8.md. Usage: python scripts/suite/check_ddiv_response.py --workers 16"""
import argparse
import json
import os
import sys
from multiprocessing import Pool

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
PHI = [0.5, 0.8, 0.9, 0.95, 0.98]
DET = ["D_div", "B1", "B2", "B3", "B4"]
BASE = 44_000_000
R_POP, R = 20, 100


def series(grid, idx, phi, L=None, A=0.0):
    import synth
    import synth_e2e
    if grid == 1:
        b, e = synth.make_series(idx, phi=phi, n_events=20, L=L, A=A)
        return b, e, 1, 128
    b, e, m = synth_e2e.make_e2e(idx, grid=10, phi_obs=phi, L=(10 * L if L else None), A=A)
    return b, e, 10, 1280


def run_one(args):
    import pipeline
    grid, idx, phi, L, thetas = args
    b, e, g, sc = series(grid, idx, phi, L, 6.0 if L else 0.0)
    o = pipeline.run(b, e, grid=g, scan=sc, resample=False, coverage_stop=None, thetas=thetas)
    elig = [x for x in e if x["eligible"]]
    hist = []
    for x in elig:
        blk = max((bb for bb in b if bb["first_step"] <= x["t_e"]), key=lambda bb: bb["first_step"])
        hist.append((x["t_e"] - blk["first_step"]) / g)
    return {"thetas": o.get("thetas"), "mean_lead": {d: o["per_detector"][d]["mean_lead"] for d in DET},
            "leads": {d: o["leads"][d] for d in ("D_div", "B2")}, "hist": hist}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    a = ap.parse_args()
    out = ["# D_div lead-response checks (DESIGN Amendment 15.8 (b), (c); synthetic, reported)", "",
           f"Seeds: child indices {BASE:,}+ (diagnostic range; seed map). Ramps A = 6 × SD (14.3). "
           f"Fixed θ = median of the finite matched θ over the cell's replicates (table below); {R} replicates per ramp cell. Leads in steps.", ""]
    res = {}
    with Pool(a.workers) as pool:
        k = 0
        for grid in (1, 10):
            for phi in PHI:
                base = BASE + k * 2000
                k += 1
                pop = pool.map(run_one, [(grid, base + r, phi, None, None) for r in range(R_POP)])
                nfin_null = {d: sum(bool(np.isfinite(p["thetas"][d])) for p in pop) for d in DET}
                cell = {"n_finite_null": nfin_null}
                for L in (75, 125):
                    reps = [(grid, base + (100 if L == 75 else 300) + r, phi, L) for r in range(R)]
                    matched = pool.map(run_one, [x + (None,) for x in reps])
                    theta, nfin = {}, {}
                    for d in DET:
                        v = [m["thetas"][d] for m in matched if np.isfinite(m["thetas"][d])]
                        nfin[d] = len(v)
                        theta[d] = float(np.median(v)) if v else float("inf")
                    fixed = pool.map(run_one, [x + (theta,) for x in reps])
                    rng = lambda rows, d: (float(np.percentile([x["mean_lead"][d] for x in rows], 10)),  # noqa: E731
                                           float(np.percentile([x["mean_lead"][d] for x in rows], 90)))
                    reg = {}
                    for d in ("D_div", "B2"):
                        xs = np.concatenate([np.array(x["hist"]) for x in matched])
                        ys = np.concatenate([np.array(x["leads"][d], float) for x in matched])
                        if len(xs) > 2 and np.std(xs) > 0:
                            sl, ic = np.polyfit(xs, ys, 1)
                            r2 = float(np.corrcoef(xs, ys)[0, 1] ** 2) if np.std(ys) > 0 else 0.0
                        else:
                            sl, r2 = float("nan"), float("nan")
                        reg[d] = (float(sl), r2)
                    cell[L] = {"matched": {d: rng(matched, d) for d in DET}, "fixed": {d: rng(fixed, d) for d in DET},
                               "regression": reg, "theta": theta, "n_finite": nfin}
                res[(grid, phi)] = cell
                print(f"grid {grid} phi {phi} done", flush=True)
    out += ["## (b) 10–90 % range of per-replicate mean lead: matched θ vs fixed population θ", "",
            "| grid | φ_y | L | " + " | ".join(f"{d} matched → fixed" for d in DET) + " |", "|---|---|---|" + "---|" * len(DET)]
    for (grid, phi), cell in res.items():
        for L in (75, 125):
            m, f = cell[L]["matched"], cell[L]["fixed"]
            out.append(f"| {grid} | {phi} | {L} | " + " | ".join(
                f"[{m[d][0]:.0f},{m[d][1]:.0f}] → [{f[d][0]:.0f},{f[d][1]:.0f}]" for d in DET) + " |")
    out += ["", f"## Fixed θ used in (b) (n finite of {R}) and null-series matchability (n finite of {R_POP} null series)", "",
            "| grid | φ_y | L | " + " | ".join(DET) + " | null series, n finite: " + " / ".join(DET) + " |",
            "|---|---|---|" + "---|" * (len(DET) + 1)]
    for (grid, phi), cell in res.items():
        for L in (75, 125):
            t, n = cell[L]["theta"], cell[L]["n_finite"]
            out.append(f"| {grid} | {phi} | {L} | " + " | ".join(
                (f"{t[d]:.4g} ({n[d]})" if np.isfinite(t[d]) else f"— ({n[d]})") for d in DET) + " | "
                + " / ".join(str(cell["n_finite_null"][d]) for d in DET) + " |")
    out += ["", "## (c) per-event lead on history length since the series/gap start (observations), matched θ", "",
            "| grid | φ_y | L | D_div slope (steps/obs), R² | B2 slope, R² |", "|---|---|---|---|---|"]
    for (grid, phi), cell in res.items():
        for L in (75, 125):
            rg = cell[L]["regression"]
            out.append(f"| {grid} | {phi} | {L} | {rg['D_div'][0]:.4f}, {rg['D_div'][1]:.3f} | {rg['B2'][0]:.4f}, {rg['B2'][1]:.3f} |")
    open(os.path.join(ROOT, "verification", "ddiv_response_15_8.md"), "w", encoding="utf-8", newline="\n").write("\n".join(out) + "\n")
    print("WROTE verification/ddiv_response_15_8.md")


if __name__ == "__main__":
    main()
