"""E2: the single real run on A1 (DESIGN D.2-D.3 as amended through Amendment 17; §K: one real run).

Order, each step halting on failure:
  1. Guards: the working tree is clean for analysis/, scripts/, reference/ and the DESIGN/DECISIONS files; the
     output file does not exist yet (one real run); HEAD is recorded.
  2. PRV data integrity (D.6 item 7; Amendment 14.2): scripts/prv_hash_check.py on the store.
  3. Load A1's kept grid series (analysis/a1_loader.py; Amendment 2 ownership; A1.1 dropped observations) and the
     committed public event list at rung k = 4 (P-KLAD resolved at k = 4, 57 eligible events; entry 13).
  4. phi_hat_y (15.5): lag-1 sample autocorrelation of y over consecutive grid pairs within blocks, pooled,
     carried-forward observations included, no detrending; cell selection = nearest phi_y grid value, ties up.
  5. Headline E2 (FA = 1 per 10,000, grid 10, scan 1,280, H = 32, joint resampling 1,000 draws,
     default_rng(20261030)): the D.3 label.
  6. FA grid {0.5, 2, 5} (reported, no verdict; G1: n* < 2 -> "not matchable", no contrast).
  7. Writes <out>/e2_result.json and prints its SHA-256. The verdict is recorded in DECISIONS.md and RECORD.md
     by hand, the same day (Amendment 17).

Usage:
  python scripts/run_e2.py --real <store_root>
  python scripts/run_e2.py --dry-run <synthetic_store> --out <scratch> --sources <synthetic SOURCES> (test use)
"""
import argparse
import hashlib
import json
import math
import os
import subprocess
import sys

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
import a1_loader  # noqa: E402
import pipeline  # noqa: E402

PHI_GRID = [0.5, 0.8, 0.9, 0.95, 0.98]                   # the phi_y grid (15.5 selects from it)
FA_HEADLINE, FA_OTHERS = 1.0, [0.5, 2.0, 5.0]
GRID, SCAN, RUNG = 10, 1280, "4.0"
GUARDED = ["analysis", "scripts", "reference", "DESIGN.md", "DECISIONS.md", "SOURCES.md"]


def git(*a):
    return subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True).stdout.strip()


def halt(msg):
    print("HALT:", msg, flush=True)
    sys.exit(1)


def phi_hat(blocks):
    """15.5: lag-1 sample autocorrelation of y, pooled: deviations from the mean of all kept observations;
    numerator over consecutive pairs within blocks only; denominator over all observations."""
    y = np.concatenate([b["y"] for b in blocks])
    mu = y.mean()
    num = sum(float(np.sum((b["y"][1:] - mu) * (b["y"][:-1] - mu))) for b in blocks)
    den = float(np.sum((y - mu) ** 2))
    return num / den


def select_cell(ph):
    """15.5: nearest grid value on the linear scale, ties to the larger; outside [0.5, 0.98] that is the edge
    cell, and the extension cell (0.3 below, 0.99 above) is reported beside it."""
    cell = min(PHI_GRID, key=lambda v: (abs(v - ph), -v))
    ext = 0.3 if ph < PHI_GRID[0] else (0.99 if ph > PHI_GRID[-1] else None)
    return cell, ext


def jsonable(x):
    if isinstance(x, dict):
        return {str(k): jsonable(v) for k, v in x.items()}
    if isinstance(x, (list, tuple)):
        return [jsonable(v) for v in x]
    if isinstance(x, np.ndarray):
        return jsonable(x.tolist())
    if isinstance(x, (np.integer,)):
        return int(x)
    if isinstance(x, (np.floating, float)):
        v = float(x)
        return v if math.isfinite(v) else str(v)
    if isinstance(x, np.bool_):
        return bool(x)
    return x


def main():
    ap = argparse.ArgumentParser()
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--real", metavar="STORE")
    mode.add_argument("--dry-run", metavar="SYNTH_STORE")
    ap.add_argument("--out", default=os.path.join(ROOT, "scripts", "outputs", "e2"))
    ap.add_argument("--sources", default=os.path.join(ROOT, "SOURCES.md"))
    a = ap.parse_args()
    store = a.real or a.dry_run
    out_json = os.path.join(a.out, "e2_result.json")

    # 1. guards
    head = git("rev-parse", "HEAD")
    if a.real:
        if os.path.abspath(a.sources) != os.path.join(ROOT, "SOURCES.md"):
            halt("--sources may not be overridden in a real run")
        dirty = git("status", "--porcelain", "--", *GUARDED)
        if dirty:
            halt("uncommitted changes in guarded paths:\n" + dirty)
    if os.path.exists(out_json):
        halt(f"{out_json} exists: E2 has already run (one real run, §K)")
    print(f"mode {'REAL' if a.real else 'DRY-RUN'}; HEAD {head}", flush=True)

    # 2. PRV data integrity
    r = subprocess.run([sys.executable, os.path.join(ROOT, "scripts", "prv_hash_check.py"), store,
                        "--sources", a.sources], capture_output=True, text=True)
    print(r.stdout.strip().splitlines()[-1] if r.stdout.strip() else r.stderr.strip()[-300:], flush=True)
    if r.returncode != 0:
        halt("PRV hash check failed")

    # 3. load
    blocks, events, load_rep = a1_loader.load_blocks(
        os.path.join(ROOT, "scripts", "outputs", "a1_structural_report.json"), store, rung=RUNG,
        events_path=os.path.join(ROOT, "scripts", "outputs", "a1_events.json"))
    n_elig = sum(e["eligible"] for e in events)
    if n_elig < 5:
        halt(f"{n_elig} eligible events at k = 4: P-KLAD must be resolved before E2 (it was resolved at k = 4)")
    print(f"loaded {len(blocks)} blocks, {sum(len(b['y']) for b in blocks)} grid observations, "
          f"{len(events)} events ({n_elig} eligible)", flush=True)

    # 4. phi_hat_y and cell selection
    ph = phi_hat(blocks)
    cell, ext = select_cell(ph)

    # 5. headline
    res = pipeline.run(blocks, events, fa=FA_HEADLINE, grid=GRID, scan=SCAN, resample=True)

    # 6. FA grid (reported)
    grid_rep = {}
    for fa in FA_OTHERS:
        g = pipeline.run(blocks, events, fa=fa, grid=GRID, scan=SCAN, resample=False)
        if g.get("nstar", 0) < 2:
            grid_rep[str(fa)] = {"nstar": g.get("nstar"), "status": "not matchable (G1)"}
        else:
            grid_rep[str(fa)] = {"nstar": g["nstar"], "label_point": g.get("label"), "C": g.get("C"),
                                 "C_min": g.get("C_min"), "detectors": g.get("detectors"),
                                 "per_detector": g.get("per_detector")}

    out = {"mode": "REAL" if a.real else "DRY-RUN", "head": head, "store": store,
           "load_report": load_rep, "n_events": len(events), "n_eligible": n_elig,
           "phi_hat_y": ph, "selected_cell_phi": cell, "extension_cell_phi": ext, "headline": res, "fa_grid": grid_rep}
    os.makedirs(a.out, exist_ok=True)
    with open(out_json, "w", encoding="utf-8", newline="\n") as f:
        json.dump(jsonable(out), f, indent=1, sort_keys=True)
    sha = hashlib.sha256(open(out_json, "rb").read()).hexdigest()
    print(f"phi_hat_y = {ph:.4f} -> cell phi_y = {cell}" + (f" (outside [0.5, 0.98]; extension cell {ext})" if ext else ""), flush=True)
    print(f"E2 LABEL: {res['label']}  (C_min {res.get('C_min')}, p05 {res.get('p05')})", flush=True)
    print(f"WROTE {out_json} SHA-256 {sha}", flush=True)


if __name__ == "__main__":
    main()
