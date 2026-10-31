# Independent check of DESIGN Amendments 2–6 — prompt (paste as the ONLY message of a fresh session, followed by the package)

You are an adversarial reviewer of five amendments to a public pre-registration. Below this prompt the package has three parts:

1. **Amendments 2–6**, verbatim as appended to DESIGN.md.
2. **The frozen text they modify**, verbatim from the public tag `prereg-v1`: the DESIGN header and §D.1, §D.2, §D.3 (with §K), §D.4, §D.5 and §D.7.
3. **Amendment 1**, already in force and independently reviewed. It is context only, not under review. Amendments 2–6 refer to it (grid observations, 2,000-step dedup, scan window, minimum history).

No data, code, results or decision log exist for you. Judge only what is written. Do not browse the web.

**Background, stated once.**
- **The design.** A fast–slow moving-average divergence detector (D_div) is compared with four baseline alarms (B1–B4) on how early they warn of loss spikes, at a matched false-alarm rate. The comparison is made on a public training log (A1), and its result (E2) decides a kill rule (§K).
- **What was read when each amendment was made.** This bears on the frozen header rule: "No amendment to §K's thresholds, windows, spike definition, or FA grid is permitted after A1 is touched."
  - **Before Amendment 2:** A1's step index, per-row null masks and run metadata (resume checkpoints). Cell-equality checks between two copies of the same files were done by script, with no value displayed.
  - **Before Amendment 3:** the same.
  - **Before Amendments 4–6:** additionally, A1's loss values were read to enumerate loss-spike events under Amendments 1–3. The events are fixed and public: 61 events at k = 4, 57 eligible.
  - **No gradient-norm value has entered any computation** other than the cell-equality check. No detector score, threshold or lead has been computed.
- **What each amendment changes.**
  - **Amendment 2:** how segments are assembled (P-SEG).
  - **Amendment 3:** construction details of the spike rule.
  - **Amendment 4:** E1's discrete autocorrelation estimator and a Leg B persistence input, after a check against the published theorems.
  - **Amendment 5:** detector construction details. Two baselines are re-specified from their tools' source code.
  - **Amendment 6:** fixes a threshold-matching rule. The author found that, under the hold rule, the frozen rule always selects the minimum score, which would decide E2 regardless of the data.

**This is a single-round check.** There is no follow-up message and no fix round. Your reply is final.

## Five passes, one concern each — keep them separate

**Pass 1 — Permissibility.** For each amendment, given what had been read when it was made (above), judge whether it is permitted under the frozen header rule.
- The rule covers §K's thresholds, windows, spike definition and FA grid "after A1 is touched".
- Say whether each amendment changes any of those four things, or only construction details the frozen text left unstated.
- Say whether any could have been chosen with knowledge that favours one E2 outcome.

**Pass 2 — Can every rule still return each of its outcomes?**
- Cover E1 (CONSISTENT / INCONSISTENT / INDETERMINATE), E2 (SUPPORT / INCONCLUSIVE / REFUTE; INSUFFICIENT EVENTS is now known not to occur on A1), §K (STOP / PROCEED), E5 and E8, as amended.
- Check in particular whether Amendment 6's top-scan rule, its "never alarms if the top candidate exceeds n*" branch, and its 10 % coverage stop rule could themselves force an outcome. Example: a detector whose maximum score is tied over many readings.
- Check whether Amendment 5's minimum-history gate (no score before j = 1,000) interacts with B4's accumulator, which keeps running before j = 1,000, so as to favour or penalise one detector.

**Pass 3 — Is any rule a judgment described as execution?** List every place where two analysts following the amended text could compute different numbers. Examples to check:
- the top-scan stopping rule when c(v) is evaluated only at candidates;
- B3 and B4 behaviour at gaps and after resets;
- D_div percentile ties;
- the rewind-series construction;
- the 64-finite-value floor;
- the half-open R̄ on the A1 grid.

**Pass 4 — Does any amendment change more than it declares?** For each, find any change to a frozen number, ratio, grid point, rule partition, event definition or report form, explicit or implied, beyond what it states. Say whether it is defensible, or should be declared or removed.

**Pass 5 — Internal consistency.** Check the amendments against each other, against Amendment 1, and against the frozen text. Examples:
- Amendment 5's j ≥ 1,000 against Amendment 1's eligibility rule;
- Amendment 6 against P-HOLD and B4's per-candidate path recomputation;
- the coverage stop rule against the FA grid and n*;
- Amendment 4.1's half-open lags against Amendment 1's E1 window text;
- Amendment 2's gaps against Amendment 3's chain rule and the rewind series;
- each amendment's suite additions against the operators they must validate.

## Output format

Number findings H1, H2, …. For each finding give:
- **Pass:** 1–5.
- **Severity:** BLOCKER, MAJOR or MINOR.
- **Location:** amendment section, or frozen section.
- **Evidence:** a short quote.
- **Why it matters.**
- **Proposed fix:** amendment wording that could be pasted in.

End with a table of all findings. If a pass finds nothing, say "Pass N: no findings" and give the strongest reason.

---
