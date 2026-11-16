"""E4 — sensitivity on A1, no verdict (DESIGN D.3 E4, Amendment 1 E4 row; scope approved by JAE, DECISIONS 53).
Every variant re-matches all thresholds at headline FA (1 per 10,000) with the E2 pipeline; one variable at a time.
Variants: V0 (E2 reproduction), D_div windows (16,64) (64,256) (4,16), P-B1 window 25 / 100, P-B3 adjusted update,
P-B4 two-sided, P-B4 on g. Derived from V0: P-CENS (lead 0; excluded), rewind events excluded, event-block resampling
(blocks of 3 consecutive eligible events). Not run: P-SEG keep-earlier (needs a rebuilt assembly; JAE 2026-11-16).
Resumable: one JSON per variant in the output folder. Usage: python analysis/post/e4.py <store_root> [--only NAME] [--sources F --out DIR (test use)]"""
import json
import math
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path[:0] = [os.path.join(ROOT, "analysis"), os.path.join(ROOT, "analysis", "post")]
import a1_loader  # noqa: E402
import e2stat  # noqa: E402
import e4_ops  # noqa: E402
import ops  # noqa: E402
import pipeline  # noqa: E402

ORIG = {k: getattr(ops, k) for k in ("score_div", "score_b1", "score_b3", "b4_z", "b4_free_state", "b4_alarm")}


def patch(name):
    for k, v in ORIG.items():
        setattr(ops, k, v)
    if name.startswith("W"):
        wf, ws = map(int, name[1:].split("_"))
        ops.score_div = lambda y, wf=wf, ws=ws: ORIG["score_div"](y, wf, ws)
    elif name.startswith("B1_"):
        w = int(name[3:])
        ops.score_b1 = lambda y, w=w: ORIG["score_b1"](y, w)
    elif name == "B3_adj":
        ops.score_b3 = e4_ops.score_b3_adjusted
    elif name == "B4_2s":
        ops.b4_free_state = e4_ops.b4_free_state_2s
        ops.b4_alarm = e4_ops.b4_alarm_2s
    elif name == "B4_g":
        ops.b4_z = e4_ops.b4_z_on_g


VARIANTS = ["V0", "W16_64", "W64_256", "W4_16", "B1_25", "B1_100", "B3_adj", "B4_2s", "B4_g"]


def summary(o):
    s = {"label_point": o.get("label"), "nstar": o.get("nstar"), "C": o.get("C"), "C_min": o.get("C_min")}
    s["detectors"] = {d: {"matchable": v["matchable"], "theta": v["theta"] if math.isfinite(v["theta"]) else "inf",
                          "realised": v["realised"], "coverage": v["coverage"]} for d, v in o["detectors"].items()}
    if "per_detector" in o:
        s["per_detector"] = o["per_detector"]
        s["leads"] = o["leads"]
        s["flags"] = o["flags"]
    return s


def main():
    store = sys.argv[1]
    sources = sys.argv[sys.argv.index("--sources") + 1] if "--sources" in sys.argv else os.path.join(ROOT, "SOURCES.md")
    outdir = (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv
              else os.path.join(ROOT, "analysis", "outputs", "post", "e4"))
    os.makedirs(outdir, exist_ok=True)
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "prv_hash_check.py"), store, "--sources", sources],
                       capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1], flush=True)
    if r.returncode:
        sys.exit("HALT: PRV hash check failed")
    blocks, events, _ = a1_loader.load_blocks(os.path.join(ROOT, "scripts", "outputs", "a1_structural_report.json"),
                                              store, rung="4.0",
                                              events_path=os.path.join(ROOT, "scripts", "outputs", "a1_events.json"))
    todo = [sys.argv[sys.argv.index("--only") + 1]] if "--only" in sys.argv else VARIANTS
    for v in todo:
        p = os.path.join(outdir, f"{v}.json")
        if os.path.exists(p):
            print(v, "done already", flush=True)
            continue
        patch(v)
        o = pipeline.run(blocks, events, fa=1.0, grid=10, scan=1280, resample=False)
        patch("V0")
        json.dump(summary(o), open(p, "w", encoding="utf-8", newline="\n"), indent=1)
        print(v, o.get("label"), "C_min", o.get("C_min"),
              {d: (o["detectors"][d]["matchable"], o.get("per_detector", {}).get(d, {}).get("mean_lead")) for d in o["detectors"]},
              flush=True)
    # derived from V0
    v0 = json.load(open(os.path.join(outdir, "V0.json")))
    if "leads" in v0:
        L = {d: np.array(v0["leads"][d], float) for d in v0["leads"]}
        cens = {d: np.array(v0["flags"][d]["censored"], bool) for d in L}
        lead0 = {d: np.where(cens[d], 0.0, L[d]) for d in L}
        anyc = np.any(np.stack([cens[d] for d in L]), axis=0)
        excl = {d: L[d][~anyc] for d in L}
        der = {"P_CENS_lead0": {"C_min": e2stat.contrasts(lead0)[1], "n_censored": {d: int(cens[d].sum()) for d in L}},
               "P_CENS_excluded": {"C_min": e2stat.contrasts(excl)[1] if (~anyc).sum() else None, "n_kept": int((~anyc).sum())},
               "rewind_excluded": {"n_rewind_events": sum(1 for e in events if e["series"] != "kept"),
                                   "note": "all events lie on the kept series; identical to V0"}}
        rng = np.random.default_rng(np.random.SeedSequence(20261030, spawn_key=(4,)))
        n = len(L["D_div"])
        nb = math.ceil(n / 3)
        cm = []
        for _ in range(1000):
            starts = rng.integers(0, n - 2, size=nb)
            idx = np.concatenate([np.arange(s, s + 3) for s in starts])[:n]
            cm.append(e2stat.contrasts(L, idx)[1])
        der["event_block3_resampling"] = {"C_min_point": e2stat.contrasts(L)[1],
                                          "C_min_p05_p95": [float(np.percentile(cm, 5)), float(np.percentile(cm, 95))]}
        json.dump(der, open(os.path.join(outdir, "derived.json"), "w", encoding="utf-8", newline="\n"), indent=1)
        print("derived:", der, flush=True)


if __name__ == "__main__":
    main()
