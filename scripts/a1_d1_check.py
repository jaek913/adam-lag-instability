"""D.1 completeness check for one A1 route-1 history artifact (DECISIONS Addendum D item 1).

Reads ONLY the `_step` column and the non-null masks of `train/CrossEntropyLoss`
and `optim/total_grad_norm` (DESIGN Amendment 1, A1.1). No metric value is printed or saved.

Usage:
  python scripts/a1_d1_check.py <parquet> <label> <server_historyLineCount> <expected_md5> <out_json>
"""
import hashlib
import json
import sys
from datetime import datetime, timezone

import pyarrow.parquet as pq

LOSS = "train/CrossEntropyLoss"
GN = "optim/total_grad_norm"


def digest(path, algo):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


BOOKKEEPING = {"_step", "_runtime", "_timestamp"}


def is_bookkeeping(col):
    """Columns allowed on a bookkeeping-only row (DECISIONS entry 7)."""
    return col in BOOKKEEPING or col.startswith("System/")


def bookkeeping_only_steps(path, steps_without_loss):
    """Of the rows with no loss, return the steps whose ONLY non-null columns are bookkeeping."""
    if not steps_without_loss:
        return [], []
    import pyarrow.compute as pc
    full = pq.read_table(path)
    sub = full.filter(pc.is_null(full.column(LOSS)))
    ok, other = [], []
    for i in range(sub.num_rows):
        s = sub.column("_step")[i].as_py()
        s = None if s is None else int(s)
        nonnull = [c for c in sub.column_names if sub.column(c)[i].is_valid]
        (ok if all(is_bookkeeping(c) for c in nonnull) else other).append(s)
    return sorted(x for x in ok if x is not None), sorted(x for x in other if x is not None)


def runs_of(sorted_steps):
    """Contiguous blocks [first, last] in a sorted list of unique ints."""
    blocks = []
    for s in sorted_steps:
        if blocks and s == blocks[-1][1] + 1:
            blocks[-1][1] = s
        else:
            blocks.append([s, s])
    return blocks


def main():
    path, label, server_lines, expected_md5, out_json = sys.argv[1:6]
    server_lines = int(server_lines)
    md5 = digest(path, "md5")
    sha256 = digest(path, "sha256")

    pf = pq.ParquetFile(path)
    names = pf.schema_arrow.names
    present = {c: (c in names) for c in ("_step", LOSS, GN)}
    if not all(present.values()):
        rep = {"label": label, "file": path, "md5": md5, "sha256": sha256,
               "md5_matches_manifest": md5 == expected_md5.lower(),
               "required_present": present, "D1_pass": False,
               "reason": "required column missing by name"}
    else:
        t = pq.read_table(path, columns=["_step", LOSS, GN])
        step_type = str(t.schema.field("_step").type)
        raw_steps = t.column("_step").to_pylist()
        # `_step` may be stored as float64 in W&B history parquet; it must be integral.
        non_integral = sum(1 for s in raw_steps
                           if s is not None and (s != s or float(s) != int(s)))
        steps = [None if (s is None or s != s) else int(s) for s in raw_steps]
        loss_ok = t.column(LOSS).is_valid().to_pylist()
        gn_ok = t.column(GN).is_valid().to_pylist()
        n = len(steps)
        null_steps = sum(1 for s in steps if s is None)
        st = [s for s in steps if s is not None]
        uniq = sorted(set(st))
        dup = len(st) - len(uniq)
        first, last = (uniq[0], uniq[-1]) if uniq else (None, None)
        blocks = runs_of(uniq)
        contiguous = (dup == 0 and null_steps == 0 and len(blocks) == 1)

        loss_steps = sorted({s for s, ok in zip(steps, loss_ok) if ok and s is not None})
        loss_blocks = runs_of(loss_steps)
        rows_without_loss = sorted({s for s, ok in zip(steps, loss_ok) if (not ok) and s is not None})

        gn_steps = sorted({s for s, ok in zip(steps, gn_ok) if ok and s is not None})
        off_grid = [s for s in gn_steps if s % 10 != 0]
        if loss_steps:
            lo, hi = loss_steps[0], loss_steps[-1]
            grid_in_span = [g for g in range((lo + 9) // 10 * 10, hi + 1, 10)]
        else:
            grid_in_span = []
        gn_set = set(gn_steps)
        grid_missing = [g for g in grid_in_span if g not in gn_set]

        rep = {
            "label": label,
            "file": path,
            "checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
            "bytes": None,
            "md5": md5,
            "sha256": sha256,
            "md5_matches_manifest": md5 == expected_md5.lower(),
            "n_columns": len(names),
            "required_present": present,
            "step_dtype": step_type,
            "non_integral_steps": non_integral,
            "rows": n,
            "null_step_rows": null_steps,
            "unique_steps": len(uniq),
            "duplicate_steps": dup,
            "first_step": first,
            "last_step": last,
            "n_contiguous_blocks": len(blocks),
            "blocks_first_20": blocks[:20],
            "server_historyLineCount": server_lines,
            "rows_minus_server_lines": n - server_lines,
            "loss_rows": len(loss_steps),
            "loss_first": loss_steps[0] if loss_steps else None,
            "loss_last": loss_steps[-1] if loss_steps else None,
            "loss_n_contiguous_blocks": len(loss_blocks),
            "rows_without_loss_steps_first_20": rows_without_loss[:20],
            "rows_without_loss_count": len(rows_without_loss),
            "gn_rows": len(gn_steps),
            "gn_off_grid_count": len(off_grid),
            "grid_steps_in_loss_span": len(grid_in_span),
            "grid_steps_missing_gn_count": len(grid_missing),
            "grid_steps_missing_gn_first_20": grid_missing[:20],
            # D.1 (Amendment 1 A1.1): step index contiguous, no duplicates; loss every step;
            # grad norm present by name and required on grid steps only.
            "D1_pass": bool(contiguous and non_integral == 0 and len(loss_blocks) == 1
                            and loss_steps and loss_steps[0] == first and loss_steps[-1] == last
                            and len(off_grid) == 0),
            "note": "step index and non-null masks only; no metric value printed or saved",
        }
        # Rule (DECISIONS entry 7): bookkeeping-only rows are removed before the D.1 check.
        bk, other = bookkeeping_only_steps(path, rows_without_loss)
        bk_set = set(bk)
        core = [x for x in uniq if x not in bk_set]
        core_blocks = runs_of(core)
        rep.update({
            "bookkeeping_only_rows": len(bk),
            "bookkeeping_only_steps_first_20": bk[:20],
            "rows_without_loss_not_bookkeeping": len(other),
            "rows_without_loss_not_bookkeeping_first_20": other[:20],
            "core_first_step": core[0] if core else None,
            "core_last_step": core[-1] if core else None,
            "core_n_contiguous_blocks": len(core_blocks),
            "D1_pass_strict": rep["D1_pass"],
            "D1_pass": bool(dup == 0 and null_steps == 0 and non_integral == 0
                            and len(other) == 0 and len(core_blocks) == 1
                            and loss_steps and loss_steps == core
                            and len(off_grid) == 0),
        })
    import os
    rep["bytes"] = os.path.getsize(path)
    with open(out_json, "w", encoding="utf-8", newline="\n") as f:
        json.dump(rep, f, indent=2)
        f.write("\n")
    print(json.dumps({k: rep[k] for k in rep if k not in ("blocks_first_20",
                      "rows_without_loss_steps_first_20", "grid_steps_missing_gn_first_20",
                      "bookkeeping_only_steps_first_20",
                      "rows_without_loss_not_bookkeeping_first_20")}, indent=2))


if __name__ == "__main__":
    main()
