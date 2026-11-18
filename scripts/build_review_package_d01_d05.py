"""Builds the second-focused-review package for Discrepancy Register D-01 and D-05 from committed files
(verbatim excerpts). Writes verification/d01_d05_review_prompt.md and verification/d01_d05_review_package.md."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(p):
    return open(os.path.join(ROOT, p), encoding="utf-8").read()


def entry(dec, n):
    m = re.search(rf"^## Entry {n} .*?(?=^## |\Z)", dec, re.S | re.M)
    return m.group(0).rstrip()


def design_block(des, start, stop):
    i = des.index(start)
    j = des.index(stop, i)
    return des[i:j].rstrip()


dec, des, reg = read("DECISIONS.md"), read("DESIGN.md"), read("verification/Discrepancy_Register.md")
rows = [l for l in reg.splitlines() if l.startswith("| id ") or l.startswith("|---") or l.startswith("| D-01") or l.startswith("| D-05")]
parts = ["# Package — second focused review of discrepancies D-01 and D-05", "",
         "Verbatim excerpts from the project's committed files. Nothing else is provided.", "",
         "## 1. The two dossier rows (verification/Discrepancy_Register.md)", "", *rows, "",
         "## 2. DECISIONS.md entry 5 (first data contact; source of D-01)", "", entry(dec, 5), "",
         "## 3. DECISIONS.md entry 40 (the recorded commit is the copy job's, not training's)", "", entry(dec, 40), "",
         "## 4. scripts/outputs/prv_item3_metadata.json", "", "```json", read("scripts/outputs/prv_item3_metadata.json").rstrip(), "```", "",
         "## 5. DESIGN.md Amendment 7.4 (P-RNG streams)", "",
         design_block(des, "**7.4 P-RNG streams.**", "\n**7.5"), "",
         "## 6. DESIGN.md 15.9 (RNG)", "", design_block(des, "**15.9 RNG", "\n**15.10"), "",
         "## 7. DECISIONS.md entry 50 (D-05 found)", "", entry(dec, 50), "",
         "## 8. The E2 resampling and label code (analysis/e2stat.py, lines as committed)", "", "```python",
         "def contrasts" + read("analysis/e2stat.py").split("def contrasts", 1)[1].rstrip(), "```", ""]
prompt = """# Second focused review — discrepancies D-01 and D-05

You are an independent reviewer. You have no other context about this project and must not assume any. The attached
package contains verbatim excerpts from a pre-registered study's committed files.

Review each dossier IN ISOLATION (D-01 first, then D-05). For each one:
1. Restate the discrepancy in one sentence.
2. Check the cascade: is the stated blast radius complete? Name anything missing.
3. Check the method and its grade (ground truth / consistent-with / new-construction). D-01 cites "code at the run's
   recorded training commit"; section 3 shows that the recorded commit is AI2's copy job. Does the finding (gradient norm
   logged every 10 steps) still stand, on what evidence, and what grade does that evidence support?
4. Check the adjudication: is it supported? Does any reported quantity change?
5. Verdict: CONFIRMED (the dossier stands, possibly with a corrected method/grade you state) or WITHDRAWN (with reasoning).

Answer in plain text, one section per dossier, under 600 words in total. Do not propose new analyses beyond what the
verdict needs."""
open(os.path.join(ROOT, "verification", "d01_d05_review_package.md"), "w", encoding="utf-8", newline="\n").write("\n".join(parts) + "\n")
open(os.path.join(ROOT, "verification", "d01_d05_review_prompt.md"), "w", encoding="utf-8", newline="\n").write(prompt + "\n")
print("WROTE package and prompt")
