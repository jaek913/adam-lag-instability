"""E2 pipeline on prepared blocks: scores -> common N_out -> n* -> P-FA top-scan matching ->
alarm state -> coverage check -> leads -> C_b/C_min -> joint resampling -> label.
DESIGN D.2-D.3 as amended (Amendments 1, 5, 6). Provisional construction items 1-6
(verification/construction_items_pending.md) are marked ITEM n.

blocks: list of dicts {first_step, y, g} on one series ('kept'); y/g carry-forward applied
(ops.prepare_block). Steps of block observation i = first_step + i*grid.
events: list of dicts {t_e, eligible}; ALL events define the FA exclusion (A1.11(b)).
"""
import math

import numpy as np

import ops
import e2stat

DET = e2stat.DETECTORS


def _steps(b, grid):
    return b["first_step"] + grid * np.arange(len(b["y"]))


def scan_mask(steps, events, grid, scan):
    m = np.zeros(len(steps), bool)
    for e in events:
        teg = grid * (e["t_e"] // grid)
        m |= (steps >= teg - scan) & (steps <= teg)
    return m


def run(blocks, events, *, fa=1.0, grid=10, scan=1280, hold=ops.HOLD, n_draws=1000, seed=20261030,
        coverage_stop=0.10, resample=True):
    prep = []
    n_out = 0
    for b in blocks:
        st = _steps(b, grid)
        y = np.asarray(b["y"], float)
        g = np.asarray(b["g"], float)
        out = ~scan_mask(st, events, grid, scan)
        scored = np.arange(len(y)) >= ops.MIN_HIST
        oos = out & scored                              # ITEM 2: common denominator
        n_out += int(oos.sum())
        fixed = {"D_div": ops.score_div(y), "B1": ops.score_b1(y), "B2": ops.score_b2(y), "B3": ops.score_b3(g)}
        z4 = ops.b4_z(y)
        s4_free, _, _ = ops.b4_alarm(z4, None, hold)
        prep.append({"first": b["first_step"], "oos": oos, "fixed": fixed, "z4": z4, "s4_free": s4_free})
    nstar = ops.round_half_up(fa * n_out / 10000.0)

    result = {"N_out": n_out, "nstar": nstar, "fa": fa, "detectors": {}}
    if nstar == 0:                                      # A1.2 guard
        result["label"] = "UNRUN (n* = 0)"
        return result

    alarms = {}
    for d in DET:
        if d == "B4":
            def count(v, d=d):
                return sum(int(np.isin(ops.b4_alarm(p["z4"], v, hold)[1], np.nonzero(p["oos"])[0]).sum()) for p in prep)
            cands = np.concatenate([p["s4_free"][p["oos"]] for p in prep])         # ITEM 1
        else:
            def count(v, d=d):
                return sum(int(np.isin(ops.alarm_from_scores(p["fixed"][d], v, hold)[0],
                                       np.nonzero(p["oos"])[0]).sum()) for p in prep)
            cands = np.concatenate([p["fixed"][d][p["oos"]] for p in prep])
        cands = cands[~np.isnan(cands)]
        m = ops.match_threshold(count, cands, nstar)
        blocks_alarm, cov_num = [], 0
        for p in prep:
            if d == "B4":
                s, _, al = ops.b4_alarm(p["z4"], m["theta"] if m["matchable"] else math.inf, hold)
            else:
                s = p["fixed"][d]
                _, al = ops.alarm_from_scores(s, m["theta"], hold)
            cov_num += int(np.sum(np.where(np.isnan(s), False, s >= m["theta"]) & p["oos"]))
            blocks_alarm.append((p["first"], al))
        coverage = cov_num / n_out if n_out else float("nan")
        result["detectors"][d] = {**m, "coverage": coverage}
        alarms[d] = {"kept": blocks_alarm}

    stops = [d for d in DET if result["detectors"][d]["coverage"] > coverage_stop]
    if stops:                                           # Amendment 6.2 stop-and-report
        result["label"] = "STOP-AND-REPORT (coverage > 10%: " + ", ".join(stops) + ")"
        return result

    elig = [{"t_e": e["t_e"], "series": "kept"} for e in events if e["eligible"]]
    lt = e2stat.leads_table(alarms, elig, grid, scan)
    leads = {d: lt[d][0] for d in DET}
    C, cmin = e2stat.contrasts(leads)
    result.update({"n_eligible": len(elig), "C": C, "C_min": cmin,
                   "per_detector": {d: {"mean_lead": float(leads[d].mean()), "median_lead": float(np.median(leads[d])),
                                        "detection_rate": float(lt[d][2].mean()),     # ITEM 6
                                        "censored": int(lt[d][1].sum()), "misses": int((~lt[d][2]).sum())}
                                    for d in DET}})
    if resample:
        cmins, am = e2stat.resample(leads, n_draws, np.random.default_rng(seed))    # ITEM 4
        lab, p05 = e2stat.label(cmin, cmins)                                        # ITEM 5
        result.update({"label": lab, "p05": p05, "argmax": am})
    else:
        result["label"] = "REFUTE" if cmin <= 0 else "C_min>0"
    result["leads"] = {d: leads[d].tolist() for d in DET}
    return result
