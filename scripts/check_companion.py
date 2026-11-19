"""Mechanical QA for paper/companion.md against the Companion Standard (ClickUp doc 2kydc08j-754, page 2kydc08j-614,
BINDING). Checks: H1 form; verbatim preamble and footer; required sections in order (claim first, takeaway last);
banned elements; banned jargon (unless built: listed in BUILT with the section that builds it); sentences <= 40 words;
dry-honesty phrases; RECORD never named; every marker renders; number trace: every number in the source outside a
{{marker}} must be in ALLOWED with its source. The comprehension walk and honesty check are human steps (QA gate 2, 4).
Usage: python scripts/check_companion.py [--companion paper/companion.md] [--lock claims.lock]"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "scripts"))
import render_paper  # noqa: E402

PREAMBLE = ("Companion to the research paper of the same title. This is education, not investment advice. Nothing here "
            "tells you what to buy, sell, or predict. It explains what the paper found, how the checking worked, and "
            "what the results do and do not mean.")
FOOTER = ("This companion is licensed CC BY-NC 4.0. The research paper it accompanies is licensed CC BY-NC-ND 4.0, "
          "and the analysis and verification code is MIT-licensed. Education, not advice: nothing in this document is "
          "financial advice, an investment recommendation, or a forecast.")
JARGON = ["autocorrelation", "ACF", "parametric", "anti-conservative", "data vintage", "significance", "subsampling",
          "estimator", "stochastic", "heteroskedasticity", "p-value", "percentile", "Mann", "bootstrap", "null hypothesis",
          "CUSUM", "z-score", "EMA", "preconditioner", "Hessian", "covariance", "variance"]
DRY = ["what makes this series", "richer casualty", "best-guarded", "process works", "brave", "earned trust",
       "kill switch", "By rule.", "honest", "integrity"]
BANNED = ["Where to dig", "©"]
# design constants and plain facts typed by hand, each with its source (number trace)
ALLOWED = {"7": "OLMo 7B model size (paper §3.3)", "10": "gradient-norm logging interval (Amendment 1; paper §3.3)",
           "32": "fast window (DESIGN D.2)", "128": "slow window (DESIGN D.2)",
           "10,000": "FA denominator (DESIGN D.2)", "1": "headline FA (DESIGN D.2)",
           "5": "FA grid point (DESIGN D.2)", "15": "E2 run date, 15 November 2026 (DECISIONS 47)",
           "2026": "E2 run date year (DECISIONS 47)", "14,000": "approx. start of uncovered range 14,211 (paper S14)",
           "52,000": "approx. end of uncovered range 52,300 (paper S14)", "8": "eight ball (analogy)",
           "4.0": "licence version (verbatim footer)"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--companion", default=os.path.join(ROOT, "paper", "companion.md"))
    ap.add_argument("--lock", default=os.path.join(ROOT, "claims.lock"))
    a = ap.parse_args()
    src = open(a.companion, encoding="utf-8").read()
    rows = {r["id"]: r for r in json.load(open(a.lock, encoding="utf-8"))["rows"]}
    red, notes = [], []
    lines = src.splitlines()
    if not re.match(r"^# .+ — the plain-English companion$", lines[0]):
        red.append("H1 is not '# «Full paper title» — the plain-English companion'")
    if f"*{PREAMBLE}*" not in src:
        red.append("preamble not verbatim")
    if f"*{FOOTER}*" not in src.strip().splitlines()[-1]:
        red.append("footer not verbatim / not last")
    heads = re.findall(r"^## (.+)$", src, re.M)
    if not heads or heads[0] != "The claim in one sentence":
        red.append("first section is not 'The claim in one sentence'")
    if not heads or heads[-1] != "The takeaway":
        red.append("last section is not 'The takeaway'")
    for h in ("What the checking caught in this paper", "What this cannot do"):
        if h not in heads:
            red.append(f"missing section: {h}")
    if heads.index("What the checking caught in this paper") > heads.index("What this cannot do"):
        red.append("'What the checking caught' must precede 'What this cannot do'")
    claim = src.split("## The claim in one sentence", 1)[1].split("\n## ", 1)[0].strip()
    if len(re.findall(r"[.!?](\s|$)", claim)) != 1:
        red.append("claim-in-one-sentence is not exactly one sentence")
    body = src.replace(f"*{PREAMBLE}*", "").replace(f"*{FOOTER}*", "")
    for b in BANNED:
        if b in body:
            red.append(f"banned element: {b}")
    for j in JARGON:
        for m in re.finditer(rf"\b{re.escape(j)}\b", body, re.I if j.islower() else 0):
            red.append(f"jargon '{j}' at offset {m.start()} (build it or remove it)")
    for d in DRY:
        if re.search(re.escape(d), body, re.I):
            red.append(f"dry-honesty: '{d}'")
    if re.search(r"RECORD|reasonofrecord", src):
        red.append("RECORD named")
    rendered, missing = render_paper.render(src, rows)
    if missing or "{{" in rendered:
        red.append(f"unrendered markers: {missing}")
    text = re.sub(r"^#.*$", "", rendered, flags=re.M)
    sents = [s_.strip() for s_ in re.split(r"(?<=[.!?])[\"”’]?\s+", re.sub(r"\s+", " ", text)) if s_.strip()]
    long_ = [s_ for s_ in sents if len(s_.split()) > 40 and PREAMBLE[:40] not in s_ and FOOTER[:40] not in s_]
    for s_ in long_:
        red.append(f"sentence over 40 words ({len(s_.split())}): {s_[:80]}...")
    # number trace
    plain = re.sub(r"\{\{[^}]+\}\}", "", body)
    plain = re.sub(r"`[^`]*`", "", plain)
    nums = re.findall(r"(?<![\w.])\d[\d,]*(?:\.\d+)?(?![\w])", plain)
    untraced = sorted({n for n in nums if n not in ALLOWED})
    for n in untraced:
        red.append(f"number '{n}' typed by hand and not traced (use a ledger marker or add it to ALLOWED with its source)")
    n_mark = len(re.findall(r"\{\{[^}]+\}\}", src))
    notes.append(f"number trace: {n_mark} ledger markers + {len(nums)} typed design constants/facts, "
                 f"{len(nums) - sum(n in untraced for n in nums)}/{len(nums)} typed traced")
    notes.append(f"{len(sents)} sentences, longest {max(len(s_.split()) for s_ in sents)} words; "
                 f"{len(rendered.split())} words rendered")
    print("\n".join(notes))
    print("\n".join("RED " + r for r in red) if red else "COMPANION MECHANICAL QA: GREEN")
    sys.exit(1 if red else 0)


if __name__ == "__main__":
    main()
