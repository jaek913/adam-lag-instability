"""A1 first data contact: column names, row count, first/last step only.

Reads parquet METADATA plus the step-index column. No metric value is read,
printed or saved. Usage:
    python scripts/a1_schema_check.py <parquet> <segment_label> <out_json>
"""
import hashlib, json, sys
from datetime import datetime, timezone

import pyarrow.parquet as pq

REQUIRED = ["optim/total_grad_norm", "train/CrossEntropyLoss"]
STEP_CANDIDATES = ["_step", "step", "global_step"]


def digest(path, algo):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main(path, label, out):
    pf = pq.ParquetFile(path)
    names = list(pf.schema_arrow.names)
    rows = pf.metadata.num_rows
    step_col = next((c for c in STEP_CANDIDATES if c in names), None)
    first = last = n_unique = None
    if step_col:
        steps = pf.read(columns=[step_col]).column(0).to_pylist()
        steps = [int(s) for s in steps if s is not None]
        first, last, n_unique = min(steps), max(steps), len(set(steps))
    res = {
        "segment": label,
        "file": path,
        "checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "md5": digest(path, "md5"),
        "sha256": digest(path, "sha256"),
        "n_columns": len(names),
        "columns": names,
        "required_present": {c: (c in names) for c in REQUIRED},
        "lr_columns": [c for c in names if "lr" in c.lower() or "learning_rate" in c.lower()],
        "step_column": step_col,
        "rows": rows,
        "first_step": first,
        "last_step": last,
        "unique_steps": n_unique,
        "contiguous": (None if first is None else (rows == last - first + 1 and n_unique == rows)),
        "note": "metadata + step index only; no metric values read",
    }
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, indent=2)
        f.write("\n")
    show = dict(res)
    print(json.dumps(show, indent=2))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
