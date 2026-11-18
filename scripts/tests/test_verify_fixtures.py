"""verify.py must be GREEN on a good fixture and RED on each deliberately broken one (Phase 3 box:
value drift, unsigned CIC, missing citation, surviving stub, missing section, orphan figure, dangling
cross-reference, dropped limit-of-claim, missing artifact; plus unknown ledger id and un-quoted finding)."""
import copy
import json
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import verify  # noqa: E402

OUTLINE = """# OUTLINE fixture
## 3. Citations
| Key | Reference | Role | Where | Status |
|---|---|---|---|---|
| Kim-2026a | Kim (2026a) | foundation | 3 | NEW |
| Old-1999 | Old | dropped | 2 | DROPPED - fixture |
## 4. Load-bearing findings
| LB-id | Finding | Supports | Status |
|---|---|---|---|
| LB-T-one | test value | ARG-01 | LANDED |
| LB-T-gone | not run | ARG-01 | NOT RUN - fixture |
## 5. Figures, tables & equations
| ID | What | § | Referenced by | Status |
|---|---|---|---|---|
| FIG-1 | a figure | 5 | 5 | NEW |
| EQ-1 | an equation | 3 | 3 | NEW |
## 6. Assumptions & scope conditions
| ID | Statement | Anchor | Status |
|---|---|---|---|
| S1 | causal | 4 | NEW |
## 7. Conclusions & limits-of-claim
| ID | Text | Anchor | Status |
|---|---|---|---|
| C-01 | verdict | 7 | NEW |
| L-01 | not a mechanism | 6 | NEW |
## 8. Internal cross-references
| From | To | Purpose | Status |
|---|---|---|---|
| 3 | EQ-1, 5 | link | NEW |
"""

PAPER = """# Abstract
The value is {{LB-T-one}} [@Kim-2026a].

**Keywords:** fixture

# 1 Introduction
Intro. {#L-01}

# 2 Related Work
Prior work [@Kim-2026a].

# 3 Methods {#sec-3}
Equation @EQ-1 holds. $$x$$ {#EQ-1} Scope {#S1}. Code in `scripts/verify.py`.

# 4 Results
See @FIG-1 and @sec-5. Figure {#FIG-1}

## 5 More results {#sec-5}
Rendered {{LB-T-one:.2f}}.

# 6 Discussion
Discussion.

# 7 Conclusion
Done. {#C-01}

# References
[Kim-2026a] Kim, J. (2026).
"""


def lock_fixture():
    root = tempfile.mkdtemp(prefix="vfix_")
    os.makedirs(os.path.join(root, "out"))
    out = os.path.join(root, "out", "r.json")
    json.dump({"a": {"b": 1.5}}, open(out, "w"))
    scr = os.path.join(root, "s.py")
    open(scr, "w").write("# fixture script\n")
    flags = {str(i): {"pass": True, "evidence": "fixture"} for i in range(1, 8)}
    row = {"id": "LB-T-one", "lb_id": "LB-T-one", "exploratory": False, "value": 1.5, "kind": "float", "tol_abs": 1e-12,
           "output": {"path": "out/r.json", "sha256": verify.sha256_file(out)}, "pointer": ["a", "b"],
           "script": {"path": "s.py", "sha256": verify.sha256_file(scr)}, "inputs": "A1", "reexec": "rerun",
           "cic": flags, "cic_signed": "fixture-signer 2026-11-18", "note": None}
    return root, {"rows": [row], "inputs": {"A1": {"files": [], "sources_md_sha256": ""}}}


def paper_check(paper, outline=OUTLINE):
    d = tempfile.mkdtemp(prefix="vpap_")
    pp, op = os.path.join(d, "paper.md"), os.path.join(d, "OUTLINE.md")
    open(pp, "w").write(paper)
    open(op, "w").write(outline)
    _, lock = lock_fixture()
    red, _ = verify.check_paper(lock, op, pp, root=ROOT)
    return red


def expect(name, red, green=False, must=None):
    ok = (not red) if green else bool(red) and (must is None or any(must in x for x in red))
    print(("PASS " if ok else "FAIL ") + name + ("" if ok else f"  -> {red}"))
    return ok


def main():
    res = []
    root, lock = lock_fixture()
    res.append(expect("good ledger fixture is GREEN", verify.check_ledger(lock, root)[0], green=True))
    bad = copy.deepcopy(lock)
    bad["rows"][0]["value"] = 1.6
    res.append(expect("value drift -> RED", verify.check_ledger(bad, root)[0], must="value drift"))
    md = os.path.join(root, "out", "chance.md")
    open(md, "w").write("**Largest between-detector difference in mean chance lead: 15.5 steps (cell 206).**\n")
    mrow = copy.deepcopy(lock["rows"][0])
    mrow.update({"id": "LB-T-md", "value": 15.5, "pointer": {"md": ["chance_largest", "value"]},
                 "output": {"path": "out/chance.md", "sha256": verify.sha256_file(md)}})
    mlock = {"rows": [mrow], "inputs": lock["inputs"]}
    res.append(expect("good markdown-sourced row is GREEN", verify.check_ledger(mlock, root)[0], green=True))
    bad = copy.deepcopy(mlock)
    bad["rows"][0]["value"] = 15.4
    res.append(expect("markdown-sourced value drift -> RED", verify.check_ledger(bad, root)[0], must="value drift"))
    res.append(expect("good CIC fixture is GREEN", verify.check_cic(lock)[0], green=True))
    bad = copy.deepcopy(lock)
    bad["rows"][0]["cic_signed"] = None
    res.append(expect("unsigned CIC -> RED", verify.check_cic(bad)[0], must="unsigned"))
    bad = copy.deepcopy(lock)
    bad["rows"][0]["cic"]["4"]["pass"] = False
    res.append(expect("failed CIC flag -> RED", verify.check_cic(bad)[0], must="flags not passed"))

    res.append(expect("good manuscript fixture is GREEN", paper_check(PAPER), green=True))
    mut = {
        "missing citation": (PAPER.replace("[@Kim-2026a]", "Kim"), "not cited"),
        "citation without reference entry": (PAPER.replace("[Kim-2026a] Kim, J. (2026).", ""), "no References entry"),
        "surviving stub": (PAPER.replace("Discussion.", "Discussion. TODO"), "placeholder"),
        "missing section": (PAPER.replace("# 2 Related Work", "# 2 Background"), "required section missing: Related Work"),
        "missing keywords": (PAPER.replace("**Keywords:** fixture", ""), "keywords"),
        "orphan figure": (PAPER.replace("See @FIG-1 and", "See"), "orphan"),
        "dangling cross-reference": (PAPER.replace("Done.", "Done, see @TBL-9."), "dangling"),
        "outline cross-reference unresolved": (PAPER.replace("{#sec-5}", ""), "does not resolve"),
        "dropped limit-of-claim": (PAPER.replace("{#L-01}", ""), "L-01"),
        "missing artifact": (PAPER.replace("`scripts/verify.py`", "`verification/no_such_file.md`"), "named artifact"),
        "unknown ledger id": (PAPER.replace("{{LB-T-one:.2f}}", "{{LB-T-nope}}"), "unknown ledger id"),
        "finding never quoted": (PAPER.replace("{{LB-T-one}}", "1.5").replace("{{LB-T-one:.2f}}", "1.50"), "never quoted"),
    }
    for name, (txt, must) in mut.items():
        res.append(expect(f"{name} -> RED", paper_check(txt), must=must))
    print(f"{sum(res)}/{len(res)} passed")
    print("ALL PASS" if all(res) else "FAILURES")
    sys.exit(0 if all(res) else 1)


if __name__ == "__main__":
    main()
