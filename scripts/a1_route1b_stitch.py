"""Stitch one A1 segment's route-1b history from raw W&B GraphQL window responses
(DECISIONS entry 2 Addendum D items 2-3) and, where available, test cell identity
against the segment's route-1 artifact parquet.

Each window file is the raw JSON response of ONE GraphQL `sampledHistory` call, saved as
returned, named  A1_<seg>_<id>_route1b_w<NN>_<minStep>-<maxStep>.json  (bounds inclusive).
The call carries one spec per column (W&B returns, per spec, only rows where every key in
that spec is present), in the fixed order of COLS below; each spec = {"keys": ["_step", col],
"samples": 10000, "minStep": lo, "maxStep": hi}.

Asserts (each recorded in the report; any failure -> stitch_pass false):
  (i)   every column list in every window has fewer rows than the 10,000 sampling cap;
  (ii)  every row's step lies inside its window's bounds; windows do not overlap;
  (iii) no step appears twice for a column (within or across windows);
  (iv)  the loss steps are contiguous from first to last;
  (v)   where route 1 is given: identical cells on every shared step, per column
        (null == null; NaN == NaN; floats compared exactly).
No metric value is printed or saved in the report; the stitched parquet holds the data.

Usage:
  python scripts/a1_route1b_stitch.py <label> <windows_dir> <glob> <out_parquet> <out_report_json> [route1_parquet]
"""
import glob
import hashlib
import json
import math
import os
import re
import sys
from datetime import datetime, timezone

import pyarrow as pa
import pyarrow.parquet as pq

COLS = ["train/CrossEntropyLoss", "optim/total_grad_norm",
        "optim/learning_rate_group0", "optim/clipping_rate"]
CAP = 10000
NAME_RE = re.compile(r"_w(\d+)_(\d+)-(\d+)\.json$")


def digests(path):
    m, s = hashlib.md5(), hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            m.update(chunk)
            s.update(chunk)
    return m.hexdigest(), s.hexdigest()


def num(v):
    """JSON value -> float or None. W&B may encode non-finite floats as strings."""
    if v is None:
        return None
    if isinstance(v, str):
        low = v.strip().lower()
        if low == "nan":
            return float("nan")
        if low in ("infinity", "inf"):
            return float("inf")
        if low in ("-infinity", "-inf"):
            return float("-inf")
        return float(v)
    return float(v)


def same(a, b):
    if a is None or b is None:
        return a is None and b is None
    if math.isnan(a) or math.isnan(b):
        return math.isnan(a) and math.isnan(b)
    return a == b


def runs_of(sorted_steps):
    blocks = []
    for s in sorted_steps:
        if blocks and s == blocks[-1][1] + 1:
            blocks[-1][1] = s
        else:
            blocks.append([s, s])
    return blocks


def main():
    label, wdir, pattern, out_parquet, out_report = sys.argv[1:6]
    route1 = sys.argv[6] if len(sys.argv) > 6 else None
    files = sorted(glob.glob(os.path.join(wdir, pattern)),
                   key=lambda p: int(NAME_RE.search(p).group(1)))
    rep = {"label": label, "checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
           "columns": COLS, "windows": [], "asserts": {}}
    data = {c: {} for c in COLS}
    dup = {c: 0 for c in COLS}
    out_of_bounds = 0
    over_cap = 0
    bounds = []
    for p in files:
        m = NAME_RE.search(p)
        nn, lo, hi = int(m.group(1)), int(m.group(2)), int(m.group(3))
        bounds.append((lo, hi))
        md5, sha = digests(p)
        with open(p, "r", encoding="utf-8") as f:
            resp = json.load(f)
        if resp.get("errors"):
            raise SystemExit(f"window {nn}: GraphQL errors present")
        lists = resp["data"]["project"]["run"]["sampledHistory"]
        if len(lists) != len(COLS):
            raise SystemExit(f"window {nn}: {len(lists)} spec results, expected {len(COLS)}")
        counts = {}
        for col, rows in zip(COLS, lists):
            counts[col] = len(rows)
            if len(rows) >= CAP:
                over_cap += 1
            for r in rows:
                s = r.get("_step")
                if s is None or col not in r:
                    continue
                s_f = float(s)
                if s_f != int(s_f):
                    raise SystemExit(f"window {nn}: non-integral step")
                s = int(s_f)
                if not (lo <= s <= hi):
                    out_of_bounds += 1
                if s in data[col]:
                    dup[col] += 1
                data[col][s] = num(r[col])
        rep["windows"].append({"file": os.path.basename(p), "n": nn, "minStep": lo, "maxStep": hi,
                               "rows_per_column": counts, "md5": md5, "sha256": sha})
    bounds.sort()
    overlap = any(bounds[i][0] <= bounds[i - 1][1] for i in range(1, len(bounds)))
    loss_steps = sorted(data[COLS[0]])
    blocks = runs_of(loss_steps)
    gn_steps = sorted(data[COLS[1]])
    rep["asserts"] = {
        "i_all_windows_below_cap": over_cap == 0,
        "ii_rows_inside_bounds": out_of_bounds == 0,
        "ii_windows_do_not_overlap": not overlap,
        "iii_no_duplicate_steps": all(v == 0 for v in dup.values()),
        "iv_loss_contiguous": len(blocks) == 1,
    }
    rep["counts"] = {
        "n_windows": len(files),
        "rows_per_column": {c: len(data[c]) for c in COLS},
        "loss_first": loss_steps[0] if loss_steps else None,
        "loss_last": loss_steps[-1] if loss_steps else None,
        "loss_n_blocks": len(blocks),
        "gn_off_grid": sum(1 for s in gn_steps if s % 10 != 0),
        "duplicates_per_column": dup,
    }
    # (v) cell identity against route 1
    if route1:
        t = pq.read_table(route1, columns=["_step"] + COLS)
        r1_steps = [None if s is None else int(s) for s in t.column("_step").to_pylist()]
        cmp = {}
        for c in COLS:
            vals = t.column(c).to_pylist()
            r1 = {s: (None if v is None else float(v)) for s, v in zip(r1_steps, vals)
                  if s is not None and v is not None}
            r1b = {s: v for s, v in data[c].items() if v is not None}
            only_r1 = len(set(r1) - set(r1b))
            only_r1b = len(set(r1b) - set(r1))
            shared = set(r1) & set(r1b)
            mism = sum(1 for s in shared if not same(r1[s], r1b[s]))
            cmp[c] = {"route1_nonnull": len(r1), "route1b_nonnull": len(r1b), "shared": len(shared),
                      "only_route1": only_r1, "only_route1b": only_r1b, "mismatched_cells": mism}
        rep["route1_compare"] = {"route1_file": route1, "md5_sha256": digests(route1), "per_column": cmp}
        rep["asserts"]["v_cells_identical_to_route1"] = all(
            v["mismatched_cells"] == 0 and v["only_route1"] == 0 and v["only_route1b"] == 0
            for v in cmp.values())
    rep["stitch_pass"] = all(rep["asserts"].values())
    # stitched parquet
    steps_all = sorted(set().union(*[set(data[c]) for c in COLS]))
    cols = {"_step": pa.array(steps_all, pa.int64())}
    for c in COLS:
        cols[c] = pa.array([data[c].get(s) for s in steps_all], pa.float64())
    pq.write_table(pa.table(cols), out_parquet)
    rep["stitched_parquet"] = {"file": out_parquet, "rows": len(steps_all),
                               "md5_sha256": digests(out_parquet)}
    rep["note"] = "counts, flags and hashes only; no metric value printed or saved"
    with open(out_report, "w", encoding="utf-8", newline="\n") as f:
        json.dump(rep, f, indent=2)
        f.write("\n")
    print(json.dumps({k: rep[k] for k in ("label", "asserts", "counts", "stitch_pass")}, indent=2))
    if "route1_compare" in rep:
        print(json.dumps(rep["route1_compare"]["per_column"], indent=2))


if __name__ == "__main__":
    main()
