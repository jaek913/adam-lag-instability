"""Amendment 8.2(14) check: one cell run single-process must equal its multi-process output, row for row.
Usage: python scripts/suite/check_identity.py <cell>   (after run_suite.py --cells <cell> --workers 1 --out-suffix _single)"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
D = os.path.join(ROOT, "scripts", "outputs", "suite_v1")
cell = int(sys.argv[1])
load = lambda s: {json.loads(l)["rep"]: json.loads(l) for l in open(os.path.join(D, f"cell_{cell:03d}{s}.jsonl"))}  # noqa: E731
multi, single = load(""), load("_single")
same = multi.keys() == single.keys() and all(multi[r] == single[r] for r in multi)
print(f"cell {cell}: {len(multi)} multi-process rows, {len(single)} single-process rows ->",
      "IDENTICAL" if same else "DIFFERENT")
sys.exit(0 if same else 1)
