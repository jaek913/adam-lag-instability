"""E1 — persistence-sign consistency check on A1 (DESIGN D.2, D.3 E1, Amendment 1 A1.2/G14, Amendment 4.1,
15.9; construction pins in DECISIONS entry 50, fixed before computation).
Grid observations throughout: h = 16, (w_f, w_s) = (32, 128), ACF lags 0-256, permutation blocks 128.
Usage: python analysis/post/e1.py <store_root> [--sources F --out DIR]   (--sources/--out: test use)"""
import json
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
import a1_loader  # noqa: E402
import ops  # noqa: E402

H, WF, WS, MAXLAG, PBLK, NPERM = 16, 32, 128, 256, 128, 1000


def acf(blocks, maxlag=MAXLAG):
    """Pooled sample ACF: global mean over all kept observations; lag-k numerator over pairs within blocks;
    normalised by the pooled lag-0 sum, each lag scaled by N / (pairs at that lag)."""
    y_all = np.concatenate([b for b in blocks])
    mu, N = y_all.mean(), len(y_all)
    c0 = np.sum((y_all - mu) ** 2) / N
    rho = np.empty(maxlag + 1)
    for k in range(maxlag + 1):
        num, n = 0.0, 0
        for y in blocks:
            if len(y) > k:
                d = y - mu
                num += float(np.sum(d[:len(y) - k] * d[k:]))
                n += len(y) - k
        rho[k] = (num / n) / c0
    return rho


def rbar(rho, a, b):
    """Amendment 4.1: mean of rho over integer lags a .. b-1 (half-open)."""
    return float(np.mean(rho[a:b]))


def rbar_incl(rho, a, b):
    """Registered inclusive form (sensitivity): lags a .. b."""
    return float(np.mean(rho[a:b + 1]))


def pairs(blocks):
    """(D_t, y_{t+H}) over every t with D defined and t+H inside the same block."""
    dd, yy, owner = [], [], []
    for k, y in enumerate(blocks):
        D = ops.divergence(y, WF, WS)
        t = np.arange(len(y) - H)
        ok = np.isfinite(D[t])
        dd.append(D[t][ok])
        yy.append(y[t + H][ok])
        owner.append(np.full(int(ok.sum()), k))
    return dd, yy


def corr(dd, yy):
    d, y = np.concatenate(dd), np.concatenate(yy)
    return float(np.corrcoef(d, y)[0, 1])


def block_perm(dd, yy, rng):
    """Construction pin (entry 50): within each block, the target series y_{t+H} is cut into consecutive
    128-observation pieces (last piece shorter) and the pieces are permuted; D is held fixed."""
    out = []
    for y in yy:
        pieces = [y[i:i + PBLK] for i in range(0, len(y), PBLK)]
        order = rng.permutation(len(pieces))
        out.append(np.concatenate([pieces[j] for j in order])[:len(y)] if len(pieces) else y)
    return out


def label(pred_sign, rho_real, p_pred, p_opp):
    if pred_sign == 0:
        return "INDETERMINATE (zero predicted criterion)"
    if np.sign(rho_real) == pred_sign and p_pred <= 0.05:
        return "CONSISTENT"
    if np.sign(rho_real) == -pred_sign and p_opp <= 0.05:
        return "INCONSISTENT"
    return "INDETERMINATE"


def run(blocks_y, rng):
    rho = acf(blocks_y)
    crit = rbar(rho, H, H + WF) - rbar(rho, H + WF, H + WS)
    crit_incl = rbar_incl(rho, H, H + WF) - rbar_incl(rho, H + WF, H + WS)
    pred = int(np.sign(crit))
    dd, yy = pairs(blocks_y)
    r = corr(dd, yy)
    null = np.array([corr(dd, block_perm(dd, yy, rng)) for _ in range(NPERM)])
    p_hi = float((1 + np.sum(null >= r)) / (NPERM + 1))
    p_lo = float((1 + np.sum(null <= r)) / (NPERM + 1))
    p_pred = p_hi if pred > 0 else p_lo
    p_opp = p_lo if pred > 0 else p_hi
    z = float((r - null.mean()) / null.std(ddof=1))
    return {"criterion": crit, "criterion_inclusive_sensitivity": crit_incl, "predicted_sign": pred,
            "rho": r, "perm_z": z, "p_one_sided_predicted": p_pred, "p_one_sided_opposite": p_opp,
            "label": label(pred, r, p_pred, p_opp), "acf_lags_0_256": rho.tolist(),
            "n_pairs": int(sum(len(d) for d in dd))}


def main():
    store = sys.argv[1]
    sources = sys.argv[sys.argv.index("--sources") + 1] if "--sources" in sys.argv else os.path.join(ROOT, "SOURCES.md")
    outdir = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "analysis", "outputs", "post")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "prv_hash_check.py"), store, "--sources", sources],
                       capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1])
    if r.returncode:
        sys.exit("HALT: PRV hash check failed")
    blocks, _, _ = a1_loader.load_blocks(os.path.join(ROOT, "scripts", "outputs", "a1_structural_report.json"), store)
    ys = [b["y"] for b in blocks]
    res = run(ys, np.random.default_rng(np.random.SeedSequence(20261030, spawn_key=(2,))))      # 15.9, k = 2
    sens = run(ys, np.random.default_rng(20261030))                                             # 7.4 stream
    drift = []                                                                                   # G14
    for y in ys:
        if len(y) >= 2 * 256:
            m = len(y) // 256
            seg = y[:m * 256].reshape(m, 256).mean(axis=1)
            drift.append(float(np.median(np.abs(np.diff(seg)))))
    out = {"primary": res, "sensitivity_rng_7_4": {k: sens[k] for k in ("p_one_sided_predicted", "p_one_sided_opposite", "perm_z", "label")},
           "drift_median_abs_change_per_2560_steps": drift}
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, "e1_result.json")
    json.dump(out, open(p, "w", encoding="utf-8", newline="\n"), indent=1)
    print(json.dumps({k: v for k, v in res.items() if k != "acf_lags_0_256"}, indent=1))
    print("sensitivity (7.4 stream):", out["sensitivity_rng_7_4"])
    print("drift (median |change| in mean y per 256 obs, per block):", drift)
    print("WROTE", p)


if __name__ == "__main__":
    main()
