"""Amendment 15.17 (reported): from every planted-null cell's suite outputs (scripts/outputs/suite_v1), per detector:
the share of events with at least one in-window alarm (1 - misses / eligible events), and the mean in-window chance
lead (mean of per-replicate mean lead). The largest between-detector difference in mean chance lead is the measured
size of D.2 P-HOLD note (i)'s second-order effect. Writes verification/chance_leads_15_17.md.
Usage: python scripts/suite/report_chance_leads.py"""
import json
import os

import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
NULL_KINDS = ["planted_null", "surge_null", "t3_null", "realised_count_null", "grid10_null", "e2e_null", "a1s_null"]
DET = ["D_div", "B1", "B2", "B3", "B4"]


def n_elig(c, row):
    if "n_eligible" in row:
        return row["n_eligible"]
    if c["kind"].startswith(("grid10", "a1s")):
        return 57                                      # synth_e2e grid 10 (19b) / A1 layout (13.3): 57 eligible
    if c["kind"].startswith("e2e"):
        return 20                                      # synth_e2e grid 1 (19b)
    return c["n_events"]


def main():
    tab = json.load(open(os.path.join(ROOT, "scripts", "suite", "cells.json")))["cells"]
    L = ["# Chance-lead asymmetry under the planted null (DESIGN Amendment 15.17; reported)", "",
         "Per cell: share of eligible events with ≥ 1 in-window alarm, and mean in-window lead (all chance under the null). "
         "Lead units: steps.", "",
         "| cell | kind | φ_y | " + " | ".join(f"{d} share / lead" for d in DET) + " | max − min mean lead |",
         "|---|---|---|" + "---|" * len(DET) + "---|"]
    worst = (0.0, None)
    for c in tab:
        if c["kind"] not in NULL_KINDS or "superseded" in c:
            continue
        p = os.path.join(ROOT, "scripts", "outputs", "suite_v1", f"cell_{c['cell']:03d}.jsonl")
        if not os.path.exists(p):
            L.append(f"| {c['cell']} | {c['kind']} | {c['phi']} | " + " | ".join("—" for _ in DET) + " | NOT RUN |")
            continue
        rows = [json.loads(l) for l in open(p)]
        share = {d: float(np.mean([1 - r["per_detector"][d]["misses"] / n_elig(c, r) for r in rows])) for d in DET}
        lead = {d: float(np.mean([r["per_detector"][d]["mean_lead"] for r in rows])) for d in DET}
        spread = max(lead.values()) - min(lead.values())
        if spread > worst[0]:
            worst = (spread, c["cell"])
        L.append(f"| {c['cell']} | {c['kind']} | {c['phi']} | " +
                 " | ".join(f"{share[d]:.3f} / {lead[d]:.1f}" for d in DET) + f" | {spread:.1f} |")
    L += ["", f"**Largest between-detector difference in mean chance lead: {worst[0]:.1f} steps (cell {worst[1]}).** "
              "Stated in the Methods as the measured size of note (i)'s second-order effect (15.17)."]
    open(os.path.join(ROOT, "verification", "chance_leads_15_17.md"), "w", encoding="utf-8", newline="\n").write("\n".join(L) + "\n")
    print(f"WROTE verification/chance_leads_15_17.md; largest difference {worst[0]:.1f} steps (cell {worst[1]})")


if __name__ == "__main__":
    main()
