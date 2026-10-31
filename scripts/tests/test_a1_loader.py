"""Synthetic test for analysis/a1_loader.py on the REAL A1 step structure (entry 11), with planted
grad-norm values whose ln is the step number, so ownership and alignment are checkable exactly.
Usage: python scripts/tests/test_a1_loader.py <scratch_dir>
"""
import os
import sys

import numpy as np
import pyarrow as pa
import pyarrow.parquet as pq

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "analysis"))
import a1_loader  # noqa: E402

SPANS = {"run-001": ("ucv77bvt", 1, 14210, True), "run-008": ("bnzb4pmk", 52301, 73110, True),
         "run-010": ("wqjq7xzw", 73101, 160851, True), "run-013": ("7lr31kjd", 160601, 212965, True),
         "run-016": ("0g0rjkxo", 212001, 337339, True), "run-017": ("d4g44zcc", 337001, 408923, True),
         "run-018": ("50br7dzw", 408924, 504510, False)}
SEGNUM = {k: int(k.split("-")[1]) for k in SPANS}
CHECKS = []


def ok(n, c):
    CHECKS.append((n, bool(c)))


def main():
    scratch = sys.argv[1]
    os.makedirs(os.path.join(scratch, "A1"), exist_ok=True)
    for seg, (sid, a, b, bk) in SPANS.items():
        steps = ([0] if bk else []) + list(range(a, b + 1))
        # g = exp(step/1e6 + segment number) on grid steps -> ln g identifies step AND owner
        g = [float(np.exp(s / 1e6 + SEGNUM[seg])) if (s % 10 == 0 and s >= a) else None for s in steps]
        if seg == "run-016":
            g[steps.index(300000)] = None                 # one dropped grid reading
        pq.write_table(pa.table({"_step": pa.array([float(s) for s in steps]), "optim/total_grad_norm": g}),
                       os.path.join(scratch, "A1", f"{seg}_{sid}_history-v0_0000.parquet"))
    blocks, events, rep = a1_loader.load_blocks(os.path.join(ROOT, "scripts", "outputs", "a1_structural_report.json"),
                                                scratch, events_path=os.path.join(ROOT, "scripts", "outputs", "a1_events.json"))
    ok("three kept blocks", len(blocks) == 3)
    ok("block grid starts 10, 52310, 160610", [b["first_step"] for b in blocks] == [10, 52310, 160610])
    ok("obs counts 1,420 / 10,820 / 34,390", [r["n_obs"] for r in rep] == [1420, 10820, 34390])
    ok("N = 46,630", sum(len(b["y"]) for b in blocks) == 46630)

    def owner_at(block, step):
        i = (step - block["first_step"]) // 10
        return round(block["y"][i] - step / 1e6)

    b2, b3 = blocks[1], blocks[2]
    ok("73,100 owned by run-008 (resume of 010 is 73,100)", owner_at(b2, 73100) == 8)
    ok("73,110 owned by run-010 (008's 73,101-73,110 is a rewind portion)", owner_at(b2, 73110) == 10)
    ok("160,500 owned by run-010", owner_at(b2, 160500) == 10)
    ok("212,000 owned by run-013; 212,010 by run-016", owner_at(b3, 212000) == 13 and owner_at(b3, 212010) == 16)
    ok("337,010 owned by run-017", owner_at(b3, 337010) == 17)
    ok("408,930 owned by run-018", owner_at(b3, 408930) == 18)
    i = (300000 - b3["first_step"]) // 10
    ok("dropped reading at 300,000 carried forward", b3["y"][i] == b3["y"][i - 1] and rep[2]["dropped_total"] == 1)
    ok("y = ln g exactly", np.allclose(np.exp(b3["y"]), b3["g"]))
    ok("73,110 is not owned by run-008 (negative form of the ownership check)", owner_at(b2, 73110) != 8)
    ok("events loaded: 61 at k = 4, 57 eligible", len(events) == 61 and sum(e["eligible"] for e in events) == 57)
    for n, c in CHECKS:
        print(("PASS " if c else "FAIL ") + n)
    print("ALL PASS" if all(c for _, c in CHECKS) else "SOME FAILED")
    sys.exit(0 if all(c for _, c in CHECKS) else 1)


if __name__ == "__main__":
    main()
