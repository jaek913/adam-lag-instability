"""Read ledger values from the machine-written markdown reports (claims.lock rows whose pointer is {"md": [...]}).
Shared by scripts/build_claims.py and scripts/verify.py so both read the same way. Supported pointers:
  ["suite_summary", "verdict"|"cells_pass"|"cells_fail"]  suite_verdict.md: ALL PASS banner and PASS/FAIL row counts
  ["suite_sir", cell, i]              suite_verdict.md: SUPPORT/INCONCL/REFUTE rate i (0, 1, 2) of a cell
  ["suite_none", kind]                suite_verdict.md: sorted phi values of `kind` cells reporting "no construction found"
  ["suite_refute_range", kinds, phis, "min"|"max"]  min/max REFUTE rate over cells of those kinds (phis: list or null = all)
  ["dyn_det", grid, phi, L]           suite_verdict.md dyn-range row: D_div detection rate at L (25, 75 or 125 obs)
  ["chance", cell]                    chance_leads_15_17.md: "max - min mean lead" of a cell
  ["chance_largest", "value"|"cell"]  chance_leads_15_17.md: the stated largest difference and its cell
  ["ddiv_b", grid, phi, L, det, "matched"|"fixed"]  ddiv_response_15_8.md (b): [p10, p90] of per-replicate mean lead
  ["ddiv_c", grid, phi, L, "slope"|"r2"]            ddiv_response_15_8.md (c): D_div regression on history length"""
import re

DETS = ["D_div", "B1", "B2", "B3", "B4"]


def _phi(s):
    return float(s)


def _suite_rows(text):
    rows = {}
    for ln in text.splitlines():
        m = re.match(r"^\| (\d+) \| (\w+) \((.*?)\) \|(.*)$", ln)
        if m:
            args = dict(kv.split("=", 1) for kv in m.group(3).split(", ") if "=" in kv)
            rows[int(m.group(1))] = {"kind": m.group(2), "args": args, "rest": m.group(4)}
    return rows


def _sir(rest):
    m = re.search(r"SUPPORT/INCONCL/REFUTE ([0-9.]+)/([0-9.]+)/([0-9.]+)", rest)
    if not m:
        raise KeyError("no SUPPORT/INCONCL/REFUTE")
    return [float(x) for x in m.groups()]


def extract(text, ptr):
    op = ptr[0]
    if op == "suite_summary":
        if ptr[1] == "verdict":
            return "ALL PASS" if "**ALL PASS**" in text else "NOT ALL PASS"
        pat = r"\| PASS \|$" if ptr[1] == "cells_pass" else r"\| FAIL \|$"
        return len(re.findall(pat, text, re.M))
    if op == "suite_sir":
        return _sir(_suite_rows(text)[int(ptr[1])]["rest"])[int(ptr[2])]
    if op == "suite_none":
        return sorted(_phi(r["args"]["phi"]) for r in _suite_rows(text).values()
                      if r["kind"] == ptr[1] and "no construction found" in r["rest"])
    if op == "suite_refute_range":
        kinds, phis, which = ptr[1], ptr[2], ptr[3]
        v = [_sir(r["rest"])[2] for r in _suite_rows(text).values()
             if r["kind"] in kinds and (phis is None or _phi(r["args"]["phi"]) in phis)]
        if not v:
            raise KeyError("no cells")
        return min(v) if which == "min" else max(v)
    if op == "dyn_det":
        grid, phi, L = int(ptr[1]), float(ptr[2]), int(ptr[3])
        name = "dr2_grid10" if grid == 10 else "dr2_step"
        for ln in text.splitlines():
            if ln.startswith(f"| dyn-range | {name} phi={phi:g} "):
                cols = [c.strip() for c in ln.strip("|").split("|")]
                # cols[2] = pair (25, 75); cols[3] = pair (75, 125); each "D_div det a/b": a at the lower L, b at the upper
                pair, j = {25: (cols[2], 1), 75: (cols[2], 2), 125: (cols[3], 2)}[L]
                return float(re.search(r"D_div det ([0-9.]+)/([0-9.]+)", pair).group(j))
        raise KeyError("dyn-range row not found")
    if op == "chance":
        for ln in text.splitlines():
            cols = [c.strip() for c in ln.strip("|").split("|")]
            if cols and cols[0] == str(ptr[1]):
                return float(cols[-1])
        raise KeyError("chance cell not found")
    if op == "chance_largest":
        m = re.search(r"Largest between-detector difference in mean chance lead: ([0-9.]+) steps \(cell (\d+)\)", text)
        return float(m.group(1)) if ptr[1] == "value" else int(m.group(2))
    if op in ("ddiv_b", "ddiv_c"):
        sec = text.split("## (c)")[0] if op == "ddiv_b" else text.split("## (c)")[1]
        if op == "ddiv_b":
            sec = sec.split("## Fixed")[0]
        grid, phi, L = str(ptr[1]), float(ptr[2]), str(ptr[3])
        for ln in sec.splitlines():
            cols = [c.strip() for c in ln.strip("|").split("|")]
            if len(cols) > 3 and cols[0] == grid and re.match(r"^[0-9.]+$", cols[1]) and float(cols[1]) == phi and cols[2] == L:
                if op == "ddiv_c":
                    s, r2 = [float(x) for x in cols[3].split(",")]
                    return s if ptr[4] == "slope" else r2
                cell = cols[3 + DETS.index(ptr[4])]
                m = re.match(r"\[(\d+),(\d+)\] → \[(\d+),(\d+)\]", cell)
                a, b, c, d = (int(x) for x in m.groups())
                return [a, b] if ptr[5] == "matched" else [c, d]
        raise KeyError("ddiv row not found")
    raise KeyError(f"unknown md pointer {op}")
