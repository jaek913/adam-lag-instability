"""Seed paper/paper.md from OUTLINE.md (Phase 4 box "Skeleton seeded from OUTLINE.md"). Deterministic; run once at
Phase 4 open, then the manuscript is drafted by hand over the seeds. Refuses to overwrite an existing manuscript.

Seeding rules:
- Headings, in order, from the §1 IMRaD map; numbered subsections from each row's Content ("3.1 Title; 3.2 ...");
  anchors {#sec-N}, {#sec-N.M}, {#app-X}; Keywords line after the Abstract.
- Each active ARG node is seeded (claim text, its citations as [@Key], each LB-id as one ledger marker) at the first
  section in its § column; a §4 finding not named in any ARG support is seeded at the section of the ARG it supports; FIG/TBL/EQ are defined ({#ID}) at their § and referenced (@ID); S/C/L anchors at their
  anchor section; §8 cross-references become "See @target" lines in the From section.
- §3.5 quotes the §K kill rule verbatim from DESIGN.md at the prereg-v1 tag, with the registration DOI.
- References: every active citation key, "[Key] reference".
Seed lines are marked "> seed:" so drafting can replace them; they are not placeholders for verify.py.
Usage: python scripts/seed_paper.py [--out paper/paper.md]"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import verify  # noqa: E402

KEYWORDS = "loss spikes; training instability; early warning; Adam; gradient norm; pre-registration; negative result"
INACTIVE = re.compile(r"DROPPED|NOT RUN|N/A")


def tables(text):
    out = {}
    for s in re.split(r"^## ", text, flags=re.M):
        head = s.split("\n", 1)[0]
        rows = [ln for ln in s.split("\n") if ln.startswith("| ") and not ln.startswith("|---")][1:]
        out[head] = [[c.strip() for c in ln.strip("|").split("|")] for ln in rows]
    return out


def first_sec(col):
    col = re.sub(r"\b[A-Z]+-\d+\b", "", col)          # ignore node ids such as ARG-01
    m = re.search(r"(App\.\s*[A-Z]|\d+(?:\.\d+)?)", col)
    return None if not m else (("app-" + m.group(1)[-1]) if m.group(1).startswith("App") else "sec-" + m.group(1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(ROOT, "paper", "paper.md"))
    a = ap.parse_args()
    if os.path.exists(a.out):
        sys.exit(f"REFUSED: {a.out} exists (seed once; draft by hand)")
    T = tables(open(os.path.join(ROOT, "OUTLINE.md"), encoding="utf-8").read())
    lock = json.load(open(os.path.join(ROOT, "claims.lock"), encoding="utf-8"))
    first_row = {}
    for r in lock["rows"]:
        first_row.setdefault(r["lb_id"], r["id"])
    get = lambda h: next(v for k, v in T.items() if k.startswith(h))  # noqa: E731
    imrad, args_, cites = get("1. IMRaD"), get("2. Argument"), get("3. Citations")
    disp, scope, concl, xref = get("5. Figures"), get("6. Assumptions"), get("7. Conclusions"), get("8. Internal")
    active_cites = [c for c in cites if not INACTIVE.search(c[-1])]
    keys = [c[0] for c in active_cites]              # table order (deterministic)

    body = {}                                         # anchor -> list of seed lines

    def put(anchor, line):
        body.setdefault(anchor, []).append(line)

    for r in args_:
        if INACTIVE.search(r[-1]):
            continue
        sec = first_sec(r[2]) or "sec-1"
        sup = r[4]
        cits = " ".join(f"[@{k}]" for k in keys if re.search(rf"\b{re.escape(k)}\b", sup))
        lbs = " ".join("{{" + first_row[lb] + "}}" for lb in re.findall(r"LB-[A-Za-z0-9-]+", sup) if lb in first_row)
        refs = " ".join(f"@{d}" for d in re.findall(r"\b(?:FIG|TBL|EQ)-\d+\b", sup))
        put(sec, f"> seed: **{r[0]}.** {r[1]} {cits} {refs} {lbs}".rstrip())
    for r in disp:
        if INACTIVE.search(r[-1]):
            continue
        sec = first_sec(r[2]) or "sec-1"
        kind = {"FIG": "Figure", "TBL": "Table", "EQ": "Equation"}[r[0].split("-")[0]]
        put(sec, f"> seed: {kind} @{r[0]} — {r[1]} {{#{r[0]}}}")
    for r in scope + concl:
        if INACTIVE.search(r[-1]):
            continue
        sec = first_sec(r[2]) or "sec-6"
        put(sec, f"> seed: `{r[0]}` {r[1]} {{#{r[0]}}}")
    for r in xref:
        if INACTIVE.search(r[-1]):
            continue
        tg = " ".join("@" + verify._anchor(t) for t in re.split(r",\s*", r[1]))
        put(first_sec(r[0]) or "sec-1", f"> seed: See {tg} ({r[2]}).")
    lbt = get("4. Load-bearing")
    arg_sec = {r[0]: first_sec(r[2]) for r in args_}
    placed = " ".join(ln for v in body.values() for ln in v)
    for r in lbt:                                     # findings not named in any ARG support: seed at their ARG's section
        if INACTIVE.search(r[-1]) or r[0] not in first_row or "{{" + first_row[r[0]] + "}}" in placed:
            continue
        put(arg_sec.get(r[2]) or "sec-4", f"> seed: **{r[0]}** ({r[2]}). {r[1]} {{{{{first_row[r[0]]}}}}}")
    for c in active_cites:                            # any citation not yet used by an ARG node: seed at its section
        if not any(f"[@{c[0]}]" in ln for v in body.values() for ln in v):
            put(first_sec(c[3]) or "sec-2", f"> seed: [@{c[0]}] {c[2]}.")

    k = subprocess.run(["git", "-C", ROOT, "show", "prereg-v1:DESIGN.md"], capture_output=True, text=True).stdout
    ksec = k.split("### §K — Kill rule (pre-registered)", 1)[1].split("\n## ", 1)[0].strip()
    put("sec-3.5", "> seed: Registered kill rule and grading day, verbatim from `prereg-v1` "
                   "(DOI 10.5281/zenodo.23825294); the grading day was later re-set once (Amendments 16–17, @sec-3.8):")
    put("sec-3.5", "\n".join("> " + ln if ln else ">" for ln in ksec.split("\n")))

    out = []
    for row in imrad:
        sec, name, content = row[0], row[1], row[2]
        if name == "References":
            continue
        if sec in ("—", ""):
            anchor, title = "sec-abstract", name
            out += [f"# {name}", ""]
        elif sec.isalpha():
            anchor = f"app-{sec}"
            out += [f"# {name} {{#{anchor}}}", ""]
        else:
            anchor = f"sec-{sec}"
            out += [f"# {sec} {name} {{#{anchor}}}", ""]
        out += [f"> seed (map): {content}", ""]
        out += body.pop(anchor, []) + [""]
        if name == "Abstract":
            out += [f"**Keywords:** {KEYWORDS}", ""]
        segs = re.split(r";\s*(?=\d+\.\d+ )", content) if sec[:1].isdigit() else []
        for sg in segs:
            m = re.match(r"(\d+\.\d+) (.+)$", sg.strip())
            if not m:
                continue
            sub = f"sec-{m.group(1)}"
            title = m.group(2).split(" (")[0].strip().rstrip(".")
            out += [f"## {m.group(1)} {title} {{#{sub}}}", ""]
            out += body.pop(sub, []) + [""]
    out += ["# References", ""]
    out += [f"[{c[0]}] {c[1]}" for c in sorted(active_cites, key=lambda c: c[0].lower())] + [""]
    if body:
        sys.exit(f"HALT: seeds with no section in the map: {sorted(body)}")
    os.makedirs(os.path.dirname(a.out), exist_ok=True)
    with open(a.out, "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out).replace("\n\n\n", "\n\n"))
    print("seeded", a.out)


if __name__ == "__main__":
    main()
