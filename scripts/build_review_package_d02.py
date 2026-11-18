"""Second-focused-review package for Discrepancy Register D-02, built verbatim from committed files.
Writes verification/d02_review_prompt.md and verification/d02_review_package.md."""
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(p):
    return open(os.path.join(ROOT, p), encoding="utf-8").read()


def entry(dec, head):
    m = re.search(rf"^## {re.escape(head)}.*?(?=^## |\Z)", dec, re.S | re.M)
    return m.group(0).rstrip()


dec, reg = read("DECISIONS.md"), read("verification/Discrepancy_Register.md")
rows = [l for l in reg.splitlines() if l.startswith("| id ") or l.startswith("|---") or l.startswith("| D-02")]
parts = ["# Package — second focused review of discrepancy D-02", "",
         "Verbatim excerpts from the project's committed files. Nothing else is provided.", "",
         "## 1. The dossier row (verification/Discrepancy_Register.md)", "", *rows, "",
         "## 2. DECISIONS.md entry 5 (where D-02 was found)", "", entry(dec, "Entry 5 "), "",
         "## 3. DECISIONS.md entry 2, Addendum B", "", entry(dec, "Entry 2 — Addendum B ("), "",
         "## 4. DECISIONS.md entry 2, Addendum B item 8", "", entry(dec, "Entry 2 — Addendum B, item 8"), "",
         "## 5. DECISIONS.md entry 2, Addendum C", "", entry(dec, "Entry 2 — Addendum C"), "",
         "## 6. DECISIONS.md entry 9 (the seven complete segments)", "", entry(dec, "Entry 9 "), "",
         "## 7. DECISIONS.md entry 44 (route 3 did not arrive)", "", entry(dec, "Entry 44 "), "",
         "## 8. DECISIONS.md entry 45 (D-02 closed)", "", entry(dec, "Entry 45 "), "",
         "## 9. DECISIONS.md entry 49 (X1-X3; bears on what the missing data could change)", "", entry(dec, "Entry 49 "), ""]
prompt = """# Second focused review — discrepancy D-02

You are an independent reviewer. You have no other context about this project and must not assume any. The attached
package contains verbatim excerpts from a pre-registered study's committed files.

Review the dossier in isolation:
1. Restate the discrepancy in one sentence.
2. Check the cascade: is the stated blast radius complete? Name anything missing.
3. Check the method that answered and its grade (ground truth / consistent-with / new-construction).
4. Check the adjudication "original unrecoverable from public sources": is every recovery route in the package exhausted
   or closed with a recorded reason? Is the gap correctly scoped as a coverage limitation rather than a correctness
   problem, and does any reported quantity depend on it?
5. Verdict: CONFIRMED (possibly with corrections you state) or WITHDRAWN (with reasoning).

Answer in plain text, under 450 words. Do not propose new analyses beyond what the verdict needs."""
open(os.path.join(ROOT, "verification", "d02_review_package.md"), "w", encoding="utf-8", newline="\n").write("\n".join(parts) + "\n")
open(os.path.join(ROOT, "verification", "d02_review_prompt.md"), "w", encoding="utf-8", newline="\n").write(prompt + "\n")
print("WROTE")
