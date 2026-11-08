"""Build the single-round follow-up review package for DESIGN Amendments 7-14 and suite findings S-1..S-6
(DECISIONS entries 17, 34). Venue: fresh claude.ai incognito chat, no files, web search off. Contents are taken
verbatim, by script, from: DESIGN.md (Amendments 7-14; Amendments 1-6 as context), the public tag prereg-v1
(frozen D.0-D.3 with §K, D.5, D.7), verification/suite_findings.md (S-1..S-6 sections only) and
verification/suite_verdict.md. Never DECISIONS.md, never data, never code.
Usage: python scripts/build_review_package_7_14.py"""
import hashlib
import os
import re
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "verification", "amendments7-14_review_package.md")


def sections(text, level, names):
    """Return the named '## ' sections (heading line startswith any name), verbatim, in file order."""
    pat = re.compile(r"^" + "#" * level + r" ", re.M)
    starts = [m.start() for m in pat.finditer(text)] + [len(text)]
    out = []
    for a, b in zip(starts[:-1], starts[1:]):
        head = text[a:text.index("\n", a)]
        if any(head.startswith("#" * level + " " + n) for n in names):
            out.append(text[a:b].rstrip() + "\n")
    return out


def main():
    design = open(os.path.join(ROOT, "DESIGN.md"), encoding="utf-8").read()
    frozen = subprocess.run(["git", "-C", ROOT, "show", "prereg-v1:DESIGN.md"], capture_output=True).stdout.decode("utf-8")
    findings = open(os.path.join(ROOT, "verification", "suite_findings.md"), encoding="utf-8").read()
    verdict = open(os.path.join(ROOT, "verification", "suite_verdict.md"), encoding="utf-8").read()
    a7 = design.index("## Amendment 7 (")
    a1 = design.index("## Amendment 1 (")
    am_7_14 = design[a7:].rstrip() + "\n"
    am_1_6 = design[a1:a7].rstrip() + "\n"
    head = frozen[: frozen.index("## D.0 ")]
    fz = sections(frozen, 2, ["D.0 ", "D.0a ", "D.2 ", "D.3.0 ", "D.3.1 ", "D.3 ", "D.5 ", "D.7 "])
    sfind = sections(findings, 2, ["S-1 ", "S-2 ", "S-3 ", "Suite verdict run v1", "S-4 ", "S-5 ", "S-6 "])
    md5 = lambda s: hashlib.md5(s.encode("utf-8")).hexdigest()  # noqa: E731
    dmd5 = hashlib.md5(design.encode("utf-8")).hexdigest()
    parts = [
        "# PACKAGE — independent check of DESIGN Amendments 7–14 and suite findings S-1 to S-6\n",
        f"Frozen text verbatim from DESIGN.md at tag prereg-v1 (MD5 {hashlib.md5(frozen.encode('utf-8')).hexdigest()}). "
        f"Amendments verbatim from DESIGN.md (MD5 {dmd5}). Findings verbatim from verification/suite_findings.md "
        f"(S-1..S-6 sections only) and the suite verdict from verification/suite_verdict.md.\n",
        "=== PART 1: Amendments 7–14 (under review) ===\n", am_7_14,
        "=== PART 2: The frozen text they modify (prereg-v1) ===\n", head, *fz,
        "=== PART 3: Suite findings S-1 to S-6, with their evidence (verbatim) ===\n", *sfind,
        "=== PART 4: Suite verdict (grader output, verbatim) ===\n", verdict,
        "=== PART 5: Amendments 1–6 (context only; not under review here — Amendments 2–6 are under a separate review) ===\n",
        am_1_6,
    ]
    pkg = "\n".join(parts)
    with open(OUT, "w", encoding="utf-8", newline="\n") as f:
        f.write(pkg)
    print("WROTE", OUT, "bytes", len(pkg.encode("utf-8")), "md5", md5(pkg))


if __name__ == "__main__":
    main()
