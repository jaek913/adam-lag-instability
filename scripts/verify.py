"""verify.py (Phase 3; manuscript checks from Phase 4). Exit 0 = GREEN, 1 = RED.

Checks:
  [inputs]   re-hash every A1 input file listed in claims.lock against its SHA-256; SOURCES.md hash matches.
  [ledger]   every row's output file and generating script match their recorded SHA-256; the value at the row's
             JSON pointer equals the recorded value within tolerance.
  [reexec]   re-execute to the claim (modes from scripts/build_claims.py): rerun scripts to a scratch folder and
             compare; E2 'reproduce' (run_e2.py is NEVER invoked: compare with E4 V0 and re-derive from stored
             leads); suite 'regrade'. 'rerun_long' (E4) only with --full.
  [cic]      every non-static row's script carries all 7 CIC flags passed and a signature.
  [paper]    when the manuscript exists: every ledger value present at its {{LB-id}} (rendered by
             scripts/render_paper.py), and the outline reconciliation: required section run (fixed list), keywords,
             citation keys, LB-ids, FIG/TBL/EQ ids defined and referenced, S-/C-/L- anchors, internal
             cross-references resolve, named verification/ (and other repo) paths exist, no STUB/TODO/PLACEHOLDER/
             TBD or un-rendered {{...}}.
Usage: python scripts/verify.py --store <store_root> [--full] [--skip-reexec] [--skip-inputs]
       [--lock claims.lock] [--outline OUTLINE.md] [--paper paper/paper.md]"""
import argparse
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path[:0] = [os.path.join(ROOT, "scripts"), os.path.join(ROOT, "analysis")]
import ledger_md  # noqa: E402

REQUIRED = ["Abstract", "Introduction", "Related Work", "Methods", "Results", "Discussion", "Conclusion", "References"]
PLACEHOLDER = re.compile(r"\b(STUB|TODO|PLACEHOLDER|TBD)\b")
INACTIVE = re.compile(r"DROPPED|NOT RUN|N/A")


# ------------------------------------------------------------------ helpers
def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for c in iter(lambda: f.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def value_at(path, ptr):
    """JSON pointer (list) or markdown pointer ({"md": [...]}, scripts/ledger_md.py)."""
    if isinstance(ptr, dict):
        return ledger_md.extract(open(path, encoding="utf-8").read(), ptr["md"])
    return get(json.load(open(path, encoding="utf-8")), ptr)


def get(obj, ptr):
    for k in ptr:
        obj = obj[k]
    return obj


def norm(v):
    if isinstance(v, str) and v.lower() in ("inf", "infinity"):
        return "inf"
    if isinstance(v, float) and math.isinf(v):
        return "inf"
    return v


def same(a, b, tol):
    a, b = norm(a), norm(b)
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(same(x, y, tol) for x, y in zip(a, b))
    if isinstance(a, bool) or isinstance(b, bool) or isinstance(a, str) or isinstance(b, str) or a is None or b is None:
        return a == b
    return abs(float(a) - float(b)) <= tol


# ------------------------------------------------------------------ [inputs]
def check_inputs(lock, store):
    red = []
    grp = lock["inputs"]["A1"]
    if sha256_file(os.path.join(ROOT, "SOURCES.md")) != grp["sources_md_sha256"]:
        red.append("inputs: SOURCES.md SHA-256 differs from claims.lock")
    for f in grp["files"]:
        p = os.path.join(store, *f["path"].split("/"))
        if not os.path.exists(p):
            red.append(f"inputs: MISSING {f['path']}")
        elif sha256_file(p) != f["sha256"]:
            red.append(f"inputs: MISMATCH {f['path']}")
    return red, f"{len(grp['files'])} input files"


# ------------------------------------------------------------------ [ledger]
def check_ledger(lock, root=ROOT):
    red, cache = [], {}
    for r in lock["rows"]:
        op = os.path.join(root, r["output"]["path"])
        if not os.path.exists(op):
            red.append(f"ledger {r['id']}: output missing {r['output']['path']}")
            continue
        if op not in cache:
            cache[op] = (sha256_file(op), open(op, encoding="utf-8").read())
        if cache[op][0] != r["output"]["sha256"]:
            red.append(f"ledger {r['id']}: output SHA-256 drift {r['output']['path']}")
        if r["script"] and sha256_file(os.path.join(root, r["script"]["path"])) != r["script"]["sha256"]:
            red.append(f"ledger {r['id']}: script SHA-256 drift {r['script']['path']}")
        if r["reexec"] not in ("static",) and r["pointer"]:
            try:
                v = value_at(op, r["pointer"])
            except (KeyError, IndexError, TypeError, AttributeError, ValueError):
                red.append(f"ledger {r['id']}: pointer {r['pointer']} not found")
                continue
            if not same(v, r["value"], r["tol_abs"]):
                red.append(f"ledger {r['id']}: value drift ledger={r['value']!r} output={norm(v)!r}")
    return red, f"{len(lock['rows'])} rows"


# ------------------------------------------------------------------ [reexec]
def _cmd(sk, store, scratch):
    py = sys.executable
    if sk == "scripts/a1_events.py":
        return [py, os.path.join(ROOT, sk), os.path.join(ROOT, "scripts/outputs/a1_structural_report.json"),
                os.path.join(ROOT, "scripts/outputs/a1_segment_metadata.json"), store,
                os.path.join(scratch, "a1_events.json"), os.path.join(scratch, "a1_events.md")]
    if sk == "scripts/suite/grade_suite.py":
        return [py, os.path.join(ROOT, sk), "--out", os.path.join(scratch, "suite_verdict.md")]
    if sk == "scripts/suite/report_chance_leads.py":
        return [py, os.path.join(ROOT, sk), "--out", os.path.join(scratch, "chance_leads_15_17.md")]
    if sk == "scripts/suite/check_ddiv_response.py":
        return [py, os.path.join(ROOT, sk), "--workers", str(max(1, (os.cpu_count() or 2) - 2)),
                "--out", os.path.join(scratch, "ddiv_response_15_8.md")]
    return [py, os.path.join(ROOT, sk), store, "--out", scratch]


def _reproduce_e2(lock):
    import numpy as np
    import e2stat
    red = []
    E = json.load(open(os.path.join(ROOT, "scripts/outputs/e2/e2_result.json")))["headline"]
    V = json.load(open(os.path.join(ROOT, "analysis/outputs/post/e4/V0.json")))
    for d in E["detectors"]:
        for k in ("theta", "realised", "matchable", "coverage"):
            if not same(E["detectors"][d][k], V["detectors"][d][k], 1e-12):
                red.append(f"reexec E2: {d}.{k} differs from E4 V0")
    for k in ("leads", "per_detector", "C", "C_min", "nstar"):
        if E[k] != V[k]:
            red.append(f"reexec E2: {k} differs from E4 V0")
    L = {d: np.array(v, float) for d, v in E["leads"].items()}
    C, Cmin = e2stat.contrasts(L)[0], e2stat.contrasts(L)[1]
    for b in C:
        if not same(C[b], float(L["D_div"].mean() - L[b].mean()), 1e-12) or not same(C[b], E["C"][b], 1e-12):
            red.append(f"reexec E2: C_{b} re-derivation differs")
    if not same(Cmin, E["C_min"], 1e-12):
        red.append("reexec E2: C_min re-derivation differs")
    for d in L:
        pd = E["per_detector"][d]
        if not (same(L[d].mean(), pd["mean_lead"], 1e-12) and same(float(np.median(L[d])), pd["median_lead"], 1e-12)
                and same(float(np.mean(E["flags"][d]["detected"])), pd["detection_rate"], 1e-12)):
            red.append(f"reexec E2: {d} lead summary re-derivation differs")
    if (E["C_min"] <= 0) != (E["label"] == "REFUTE"):
        red.append("reexec E2: label rule (REFUTE iff C_min <= 0) violated")
    if int(math.floor(E["N_out"] / 1e4 + 0.5)) != E["nstar"]:
        red.append("reexec E2: n* != round_half_up(N_out / 10,000)")
    # FA-grid frontier (summaries only, no stored leads): internal consistency
    G = json.load(open(os.path.join(ROOT, "scripts/outputs/e2/e2_result.json")))["fa_grid"]
    for fa, g in G.items():
        if int(math.floor(float(fa) * E["N_out"] / 1e4 + 0.5)) != g["nstar"]:
            red.append(f"reexec E2 frontier {fa}: n* != round_half_up(fa x N_out / 10,000)")
        pdm = g["per_detector"]
        for b, cb in g["C"].items():
            if not same(cb, pdm["D_div"]["mean_lead"] - pdm[b]["mean_lead"], 1e-12):
                red.append(f"reexec E2 frontier {fa}: C_{b} != mean lead difference")
        if not same(g["C_min"], min(g["C"].values()), 1e-12):
            red.append(f"reexec E2 frontier {fa}: C_min != min C_b")
        if (g["C_min"] <= 0) != (g["label_point"] == "REFUTE"):
            red.append(f"reexec E2 frontier {fa}: label rule violated")
    return red


def check_reexec(lock, store, full):
    red, done, skipped = [], [], []
    by_script = {}
    for r in lock["rows"]:
        if r["reexec"] in ("rerun", "rerun_long", "regrade"):
            by_script.setdefault(r["script"]["path"], []).append(r)
    for sk, rows in sorted(by_script.items()):
        mode = rows[0]["reexec"]
        if mode == "rerun_long" and not full:
            skipped.append(sk)
            continue
        scratch = tempfile.mkdtemp(prefix="verify_")
        p = subprocess.run(_cmd(sk, store, scratch), capture_output=True, text=True, cwd=ROOT)
        if p.returncode:
            red.append(f"reexec {sk}: exit {p.returncode}: {p.stdout[-300:]} {p.stderr[-300:]}")
            continue
        for r in rows:
            sp = os.path.join(scratch, os.path.relpath(os.path.join(ROOT, r["output"]["path"]),
                                                       os.path.join(ROOT, os.path.dirname(rows[0]["output"]["path"])))
                              if mode == "rerun_long" else os.path.basename(r["output"]["path"]))
            if mode == "regrade":
                if open(sp, "rb").read() != open(os.path.join(ROOT, r["output"]["path"]), "rb").read():
                    red.append(f"reexec {r['id']}: re-graded verdict differs")
                continue
            if not os.path.exists(sp):
                red.append(f"reexec {r['id']}: re-run produced no {os.path.basename(sp)}")
                continue
            v = value_at(sp, r["pointer"])
            if not same(v, r["value"], r["tol_abs"]):
                red.append(f"reexec {r['id']}: re-run value {norm(v)!r} != ledger {r['value']!r}")
        done.append(sk)
    if any(r["reexec"] == "reproduce" for r in lock["rows"]):
        red += _reproduce_e2(lock)
        done.append("E2 reproduce (no re-run)")
    return red, f"re-executed: {done}; skipped (needs --full): {skipped}"


# ------------------------------------------------------------------ [cic]
def check_cic(lock):
    red = []
    seen = set()
    for r in lock["rows"]:
        if r["reexec"] == "static":
            continue
        s = r["script"]["path"]
        if s in seen:
            continue
        seen.add(s)
        flags = r["cic"]
        bad = [k for k in map(str, range(1, 8)) if not (flags.get(k) and flags[k].get("pass") is True)]
        if bad:
            red.append(f"cic {s}: flags not passed: {bad}")
        if not r.get("cic_signed"):
            red.append(f"cic {s}: unsigned")
    return red, f"{len(seen)} scripts"


# ------------------------------------------------------------------ [paper]
def outline_ids(outline_text):
    """Active ids from OUTLINE tables: citation keys (§3), LB-ids (§4), FIG/TBL/EQ (§5), S (§6), C/L (§7),
    cross-reference targets (§8). Rows whose Status says DROPPED / NOT RUN / N/A are inactive."""
    secs = re.split(r"^## ", outline_text, flags=re.M)
    out = {"cite": set(), "lb": set(), "disp": set(), "scope": set(), "concl": set(), "xref": []}
    for s in secs:
        head = s.split("\n", 1)[0]
        rows = [ln for ln in s.split("\n") if ln.startswith("| ") and not ln.startswith("|---")][1:]
        for ln in rows:
            cells = [c.strip() for c in ln.strip("|").split("|")]
            if INACTIVE.search(cells[-1]):
                continue
            if head.startswith("3. Citations"):
                out["cite"].add(cells[0])
            elif head.startswith("4. Load-bearing"):
                out["lb"].add(cells[0])
            elif head.startswith("5. Figures"):
                out["disp"].add(cells[0])
            elif head.startswith("6. Assumptions"):
                out["scope"].add(cells[0])
            elif head.startswith("7. Conclusions"):
                out["concl"].add(cells[0])
            elif head.startswith("8. Internal"):
                for t in re.split(r",\s*", cells[1]):
                    out["xref"].append((cells[0], t.strip()))
    return out


def _anchor(t):
    t = t.strip()
    m = re.match(r"^App\.\s*([A-Z])$", t)
    if m:
        return f"app-{m.group(1)}"
    if re.match(r"^\d+(\.\d+)*$", t):
        return f"sec-{t}"
    return t


def check_paper(lock, outline_path, paper_path, root=ROOT):
    if not os.path.exists(paper_path):
        return [], "no manuscript yet (checks run from Phase 4)"
    import render_paper
    red = []
    src = open(paper_path, encoding="utf-8").read()
    O = outline_ids(open(outline_path, encoding="utf-8").read())
    rows = {r["id"]: r for r in lock["rows"]}
    # required section run (fixed list), in order, plus keywords after the abstract
    heads = [re.sub(r"^\s*(\d+(\.\d+)*\.?\s+)?", "", h).split("{#")[0].strip()
             for h in re.findall(r"^#{1,3}\s+(.+)$", src, re.M)]
    pos = []
    for name in REQUIRED:
        idx = [i for i, h in enumerate(heads) if h.lower() == name.lower()]
        if not idx:
            red.append(f"paper: required section missing: {name}")
        else:
            pos.append(idx[0])
    if pos != sorted(pos):
        red.append("paper: required sections out of order")
    if not re.search(r"^#\s*Abstract.*?\n(?:.*\n)*?\*\*Keywords[:.]?\*\*", src, re.M):
        red.append("paper: keywords line missing after the abstract")
    # placeholders
    for m in PLACEHOLDER.finditer(src):
        red.append(f"paper: placeholder '{m.group(1)}' at offset {m.start()}")
    # LB markers: known ids; every active LB-id appears; all render
    marks = re.findall(r"\{\{([A-Za-z0-9_.\-]+)(?::[^}]*)?\}\}", src)
    for m in marks:
        if m not in rows:
            red.append(f"paper: unknown ledger id {{{{{m}}}}}")
    lb_used = {rows[m]["lb_id"] for m in marks if m in rows}
    for lb in sorted(O["lb"] - lb_used):
        red.append(f"paper: load-bearing finding {lb} never quoted via {{{{...}}}}")
    rendered, missing = render_paper.render(src, rows)
    if missing or "{{" in rendered:
        red.append("paper: un-rendered {{...}} remains after rendering")
    # citations
    cited = set(re.findall(r"\[@([A-Za-z0-9\-]+)(?:,[^\]]*)?\]", src))   # [@Key] or [@Key, locator]
    refs = re.split(r"^#{1,3}\s+References\s*$", src, flags=re.M)
    reflist = set(re.findall(r"^\[([A-Za-z0-9\-]+)\]", refs[1], re.M)) if len(refs) > 1 else set()
    for k in sorted(O["cite"] - cited):
        red.append(f"paper: outline citation {k} not cited")
    for k in sorted(cited - reflist):
        red.append(f"paper: citation {k} has no References entry")
    # anchors and references
    defined = set(re.findall(r"\{#([A-Za-z0-9.\-]+)\}", src))
    refd = set(re.findall(r"@([A-Za-z][A-Za-z0-9.\-]*[A-Za-z0-9])", re.sub(r"\[@[^\]]+\]", "", src)))
    for i in sorted(O["disp"]):
        if i not in defined:
            red.append(f"paper: {i} not defined (missing {{#{i}}})")
        elif i not in refd:
            red.append(f"paper: {i} defined but never referenced in text (orphan)")
    for i in sorted(O["scope"] | O["concl"]):
        if i not in defined:
            red.append(f"paper: scope/limit anchor {i} missing (expected {{#{i}}})")
    for r_ in sorted(refd - defined):
        red.append(f"paper: dangling cross-reference @{r_}")
    for frm, to in O["xref"]:
        a = _anchor(to)
        if a not in defined:
            red.append(f"paper: outline cross-reference {frm} -> {to} does not resolve (no {{#{a}}})")
    # named artifact paths exist
    for pth in set(re.findall(r"`((?:verification|scripts|analysis|paper)/[^`\s]+)`", src)):
        if not os.path.exists(os.path.join(root, pth)):
            red.append(f"paper: named artifact does not exist: {pth}")
    return red, f"{len(marks)} ledger markers; {len(defined)} anchors"


# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--store", required=False)
    ap.add_argument("--full", action="store_true")
    ap.add_argument("--skip-reexec", action="store_true")
    ap.add_argument("--skip-inputs", action="store_true")
    ap.add_argument("--lock", default=os.path.join(ROOT, "claims.lock"))
    ap.add_argument("--outline", default=os.path.join(ROOT, "OUTLINE.md"))
    ap.add_argument("--paper", default=os.path.join(ROOT, "paper", "paper.md"))
    a = ap.parse_args()
    lock = json.load(open(a.lock, encoding="utf-8"))
    if (not a.skip_inputs or not a.skip_reexec) and not a.store:
        sys.exit("--store is required unless --skip-inputs and --skip-reexec")
    report, red_all = [], []
    steps = [("inputs", None if a.skip_inputs else lambda: check_inputs(lock, a.store)),
             ("ledger", lambda: check_ledger(lock)),
             ("reexec", None if a.skip_reexec else lambda: check_reexec(lock, a.store, a.full)),
             ("cic", lambda: check_cic(lock)),
             ("paper", lambda: check_paper(lock, a.outline, a.paper))]
    for name, fn in steps:
        if fn is None:
            print(f"[{name}] SKIPPED")
            continue
        red, info = fn()
        print(f"[{name}] {'GREEN' if not red else 'RED'} — {info}")
        for x in red:
            print("   ", x)
        red_all += red
    print("VERIFY:", "GREEN" if not red_all else f"RED ({len(red_all)} failures)")
    sys.exit(0 if not red_all else 1)


if __name__ == "__main__":
    main()
