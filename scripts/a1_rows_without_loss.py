"""List, for each row of an A1 history parquet that has no train/CrossEntropyLoss,
the NAMES of the columns that are non-null on that row (grouped by prefix).
Column names and counts only; no metric value is printed or saved.

Usage: python scripts/a1_rows_without_loss.py <parquet> <out_json>
"""
import json
import sys
from collections import Counter

import pyarrow.compute as pc
import pyarrow.parquet as pq

LOSS = "train/CrossEntropyLoss"


def main():
    path, out_json = sys.argv[1:3]
    t = pq.read_table(path)
    mask = pc.is_null(t.column(LOSS))
    sub = t.filter(mask)
    rows = []
    for i in range(sub.num_rows):
        step = sub.column("_step")[i].as_py()
        nonnull = [c for c in sub.column_names if sub.column(c)[i].is_valid]
        prefixes = Counter(c.split("/")[0] for c in nonnull)
        rows.append({
            "step": None if step is None else int(step),
            "n_nonnull_columns": len(nonnull),
            "nonnull_by_prefix": dict(sorted(prefixes.items())),
            "nonnull_non_param_columns": sorted(c for c in nonnull
                                                if not c.startswith("optim/param/")
                                                and "/param/" not in c)[:80],
        })
    rep = {"file": path, "rows_without_loss": len(rows), "rows": rows,
           "note": "column names and counts only; no metric value printed or saved"}
    with open(out_json, "w", encoding="utf-8", newline="\n") as f:
        json.dump(rep, f, indent=2)
        f.write("\n")
    print(json.dumps(rep, indent=2))


if __name__ == "__main__":
    main()
