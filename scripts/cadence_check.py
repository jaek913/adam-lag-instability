"""Logging-cadence check for a staged W&B history parquet (Phase 2, pre-amendment).

Reads the step index and the per-row NULL MASK of two columns only.
No metric value is printed, saved or summarised. Usage:
    python scripts/cadence_check.py <parquet> <label> <out_json>
"""
import hashlib, json, sys
from collections import Counter
from datetime import datetime, timezone

import pyarrow.parquet as pq

G, L = "optim/total_grad_norm", "train/CrossEntropyLoss"


def digest(path, algo):
    h = hashlib.new(algo)
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def runs(steps):
    out, st, prev = [], steps[0], steps[0]
    for x in steps[1:]:
        if x != prev + 1:
            out.append((st, prev)); st = x
        prev = x
    out.append((st, prev))
    return out


def main(path, label, out):
    pf = pq.ParquetFile(path)
    names = set(pf.schema_arrow.names)
    cols = [c for c in ("_step", G, L) if c in names]
    t = pf.read(columns=cols)
    steps = [int(x) for x in t.column("_step").to_pylist()]
    order = sorted(range(len(steps)), key=steps.__getitem__)
    steps = [steps[i] for i in order]
    mask = {c: [t.column(c).is_valid().to_pylist()[i] for i in order] for c in (G, L) if c in names}
    blocks = runs(steps)
    big = max(blocks, key=lambda b: b[1] - b[0])
    in_big = [(s, {c: mask[c][i] for c in mask}) for i, s in enumerate(steps) if big[0] <= s <= big[1]]
    gsteps = [s for s, m in in_big if m.get(G)]
    res = {
        "label": label, "file": path,
        "checked_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "bytes_md5": digest(path, "md5"), "sha256": digest(path, "sha256"),
        "required_present": {G: G in names, L: L in names},
        "rows": len(steps), "first_step": steps[0], "last_step": steps[-1],
        "unique_steps": len(set(steps)),
        "contiguous_whole_file": len(steps) == steps[-1] - steps[0] + 1 and len(set(steps)) == len(steps),
        "n_contiguous_blocks": len(blocks),
        "largest_block": {"first": big[0], "last": big[1], "rows": len(in_big)},
        "loss_every_row_in_largest_block": all(m.get(L) for _, m in in_big) if L in names else None,
        "grad_norm_rows_in_largest_block": len(gsteps),
        "grad_norm_spacing_counts": dict(Counter(b - a for a, b in zip(gsteps, gsteps[1:])).most_common(5)),
        "grad_norm_every_row_in_largest_block": len(gsteps) == len(in_big),
        "grad_norm_only_on_step_mod_10_eq_0": all(s % 10 == 0 for s in gsteps) if gsteps else None,
        "note": "step index and null mask only; no metric value printed or saved",
    }
    with open(out, "w", encoding="utf-8", newline="\n") as f:
        json.dump(res, f, indent=2); f.write("\n")
    print(json.dumps(res, indent=2))


if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3])
