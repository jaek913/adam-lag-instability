"""E5 — alignment control on A1 (DESIGN D.2 Control, D.3 E5, Amendment 1 G-items, 15.9; pins in DECISIONS entry 51).
Primary: D_div's real headline alarm-state series (from E2's matching, recomputed here with the same code) is shifted
circularly by a uniform offset in [1,000, N - 1,000] grid observations over the concatenated kept series (1,000 draws);
advance-ordering rate (share of eligible events with lead > 0) and mean lead against the real events.
Flag trips if the real rate <= the 95th percentile of the shifted rates.
Second characterization (no flag): one 128-observation block shuffle of y within each block, thresholds re-matched
at headline FA; D_div mean lead, rate and matchability.
Usage: python analysis/post/e5.py <store_root> [--sources F --out DIR]"""
import json
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
import a1_loader  # noqa: E402
import e2stat  # noqa: E402
import pipeline  # noqa: E402

GRID, SCAN, NDRAW = 10, 1280, 1000


def aor_and_mean(alarm_blocks, elig):
    lt = e2stat.leads_table({"D_div": {"kept": alarm_blocks}}, elig, GRID, SCAN)["D_div"]
    return float(np.mean(lt[0] > 0)), float(lt[0].mean())


def shifted(alarm_blocks, off):
    lens = [len(a) for _, a in alarm_blocks]
    cat = np.roll(np.concatenate([a for _, a in alarm_blocks]), off)
    out, i = [], 0
    for (first, _), n in zip(alarm_blocks, lens):
        out.append((first, cat[i:i + n]))
        i += n
    return out


def run_control(alarm_blocks, elig, rng):
    real = aor_and_mean(alarm_blocks, elig)
    N = sum(len(a) for _, a in alarm_blocks)
    offs = rng.integers(1000, N - 1000 + 1, size=NDRAW)
    sh = np.array([aor_and_mean(shifted(alarm_blocks, int(o)), elig) for o in offs])
    p95 = float(np.percentile(sh[:, 0], 95))
    return {"real_rate": real[0], "real_mean_lead": real[1],
            "shift_rate_median": float(np.median(sh[:, 0])), "shift_rate_p05_p95": [float(np.percentile(sh[:, 0], 5)), p95],
            "shift_mean_lead_median": float(np.median(sh[:, 1])),
            "shift_mean_lead_p05_p95": [float(np.percentile(sh[:, 1], 5)), float(np.percentile(sh[:, 1], 95))],
            "flag_tripped": bool(real[0] <= p95), "n_alarm_steps": int(sum(a.sum() for _, a in alarm_blocks))}


def main():
    store = sys.argv[1]
    sources = sys.argv[sys.argv.index("--sources") + 1] if "--sources" in sys.argv else os.path.join(ROOT, "SOURCES.md")
    outdir = sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else os.path.join(ROOT, "analysis", "outputs", "post")
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "prv_hash_check.py"), store, "--sources", sources],
                       capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1])
    if r.returncode:
        sys.exit("HALT: PRV hash check failed")
    blocks, events, _ = a1_loader.load_blocks(os.path.join(ROOT, "scripts", "outputs", "a1_structural_report.json"),
                                              store, rung="4.0",
                                              events_path=os.path.join(ROOT, "scripts", "outputs", "a1_events.json"))
    elig = [{"t_e": e["t_e"], "series": "kept"} for e in events if e["eligible"]]
    # recompute D_div's headline alarm state with the E2 code (pipeline internals are not exposed; same calls)
    import ops
    prep, n_out = [], 0
    for b in blocks:
        st = b["first_step"] + GRID * np.arange(len(b["y"]))
        oos = ~pipeline.scan_mask(st, events, GRID, SCAN) & (np.arange(len(b["y"])) >= ops.MIN_HIST)
        n_out += int(oos.sum())
        prep.append((b, ops.score_div(b["y"]), oos))
    nstar = ops.round_half_up(n_out / 1e4)

    def count(v):
        return sum(int(np.isin(ops.alarm_from_scores(s, v)[0], np.nonzero(o)[0]).sum()) for _, s, o in prep)
    cands = np.concatenate([s[o] for _, s, o in prep])
    m = ops.match_threshold(count, cands[~np.isnan(cands)], nstar)
    alarm_blocks = [(b["first_step"], ops.alarm_from_scores(s, m["theta"])[1]) for b, s, _ in prep]
    primary = run_control(alarm_blocks, elig, np.random.default_rng(np.random.SeedSequence(20261030, spawn_key=(3,))))
    primary.update({"theta": m["theta"], "matchable": m["matchable"], "nstar": nstar})
    sens = run_control(alarm_blocks, elig, np.random.default_rng(20261030))
    # block shuffle (second characterization)
    rng = np.random.default_rng(np.random.SeedSequence(20261030, spawn_key=(3, 1)))
    sb = []
    for b in blocks:
        y = b["y"]
        pieces = [np.arange(i, min(i + 128, len(y))) for i in range(0, len(y), 128)]
        idx = np.concatenate([pieces[j] for j in rng.permutation(len(pieces))])
        sb.append({"first_step": b["first_step"], "y": y[idx], "g": b["g"][idx]})
    o = pipeline.run(sb, events, fa=1.0, grid=GRID, scan=SCAN, resample=False, coverage_stop=None)
    shuffle = {"D_div_matchable": o["detectors"]["D_div"]["matchable"]}
    if "per_detector" in o:
        lt = o["leads"]["D_div"]
        shuffle.update({"D_div_mean_lead": o["per_detector"]["D_div"]["mean_lead"],
                        "D_div_rate": float(np.mean(np.array(lt) > 0))})
    out = {"primary": primary, "sensitivity_rng_7_4": sens, "block_shuffle": shuffle}
    os.makedirs(outdir, exist_ok=True)
    p = os.path.join(outdir, "e5_result.json")
    json.dump(out, open(p, "w", encoding="utf-8", newline="\n"), indent=1, default=float)
    print(json.dumps(out, indent=1, default=str))
    print("WROTE", p)


if __name__ == "__main__":
    main()
