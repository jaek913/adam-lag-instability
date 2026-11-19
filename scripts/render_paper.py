"""Render paper/paper.md -> paper/paper_rendered.md by substituting {{ROW-ID}} or {{ROW-ID:fmt}} markers with
claims.lock values. Numbers are never typed by hand in the manuscript. fmt is a Python format spec (e.g. .3f, ,d, .1e);
fmt "yn" renders booleans yes/no; "inf" renders as ∞; a spec on a list applies to each element;
without a spec: ints get thousands separators, floats 4 significant digits, others str(). Unknown ids are an error.
Usage: python scripts/render_paper.py [--paper paper/paper.md] [--lock claims.lock] [--out paper/paper_rendered.md]"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MARK = re.compile(r"\{\{([A-Za-z0-9_.\-]+)(?::([^}]*))?\}\}")


def fmt(v, spec):
    if v == "inf":
        return "∞"
    if spec == "yn":
        return "yes" if v else "no"
    if isinstance(v, list) and spec:
        return "[" + ", ".join(format(x, spec) for x in v) + "]"
    if spec:
        return format(v, spec)
    if isinstance(v, bool) or isinstance(v, str):
        return str(v)
    if isinstance(v, int):
        return f"{v:,}"
    if isinstance(v, float):
        return f"{v:.4g}"
    if isinstance(v, list):
        return "[" + ", ".join(fmt(x, None) for x in v) + "]"
    return str(v)


def render(text, rows):
    missing = []

    def sub(m):
        rid, spec = m.group(1), m.group(2)
        if rid not in rows:
            missing.append(rid)
            return m.group(0)
        return fmt(rows[rid]["value"], spec)
    return MARK.sub(sub, text), missing


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--paper", default=os.path.join(ROOT, "paper", "paper.md"))
    ap.add_argument("--lock", default=os.path.join(ROOT, "claims.lock"))
    ap.add_argument("--out", default=os.path.join(ROOT, "paper", "paper_rendered.md"))
    a = ap.parse_args()
    rows = {r["id"]: r for r in json.load(open(a.lock, encoding="utf-8"))["rows"]}
    out, missing = render(open(a.paper, encoding="utf-8").read(), rows)
    if missing:
        sys.exit(f"RED: unknown ledger ids in manuscript: {sorted(set(missing))}")
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write(out)
    print("rendered", a.out)


if __name__ == "__main__":
    main()
