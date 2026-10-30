# Design-stage adversarial review — prompt (paste as the FIRST message of a fresh session)

You are an adversarial reviewer of a pre-registration that has not yet been made public. Below this prompt is ONE package containing exactly three items:

1. **THESIS.md** — the claims, their falsifiers, and the amendments made before the freeze.
2. **DESIGN.md** — every operator, decision rule, and reporting commitment.
3. **The synthetic-suite specification** — DESIGN.md §D.5, repeated as a separate item so you can find it. It says what will be planted, at what event count, and over what regime, before any real data is touched.

No data, code, results, or decision log exist for you, and none will be supplied. Judge only what is written in the package. Do not browse the web. Where the package cites another document (DECISIONS.md, PRIOR_ART.md, The Measurement Trap, The Divergence Theorem, The Adaptation Rate Theorem), treat the citation as a claim. You may flag it if the design depends on something the package does not state.

The design will be frozen and made public right after this review and one fix round. After that, every change is a public, dated amendment. Your job is to find what would be embarrassing or invalid to discover after the freeze. Do not praise. Do not summarise the design back. Report findings only.

## Three passes, one concern each — run them in this order and keep them separate

**Pass 1 — Can every registered rule fire?**
Cover every rule that maps a result to a label or a flag:
- E1: SUPPORT / REFUTE / INCONCLUSIVE.
- E2: SUPPORT / INCONCLUSIVE / REFUTE / INSUFFICIENT EVENTS, including the k ladder.
- §K: STOP / CLOSE / PROCEED.
- E3: SUPPORT / REFUTE / INCONCLUSIVE.
- E5: the shuffle flag.
- E8: E2's partition on pooled Leg B events.

For each rule:
- State a plausible effect size and the regime the data will realistically occupy:
  - the event count on the primary run A1 (OLMo-0424 7B, a run its authors describe as spiky);
  - the serial dependence of log gradient norm;
  - spike clustering;
  - the 200-step dedup;
  - the 1,000-step minimum history;
  - eligibility losses at segment gaps.
- Judge whether the rule as written can actually return each of its outcomes in that regime.

A rule that cannot return one of its outcomes at any plausible effect is a finding. So is a rule whose outcome is decided by an artefact: matching from below on a discrete quantile grid, ties, lead 0 for misses, onset-only alarms, or the percentile score's expanding history. So is a rule where two outcomes overlap or leave a gap.

For E6 and E7, which carry no verdict, check that every committed statistic can be computed from the stated inputs and the stated grid.

**Pass 2 — Is every experiment in the right report form?**
Use DESIGN §D.3.1. Check that:
- a binary verdict is used only for a genuine hypothesis test, comparison, or replication;
- a descriptive, ranking, robustness, or boundary question carries no pass/fail label, explicit or implied;
- a robustness check has no standalone verdict;
- the expected null of a boundary/control experiment is treated as a success, not a failure.

Flag any place where the prose would let a characterization be read as a verdict, or a verdict be rescued by a characterization.

**Pass 3 — Is any rule a judgment described as execution?**
List every place where the design leaves a choice to be made later, or where two analysts following the text could produce different numbers. Look in particular at:
- the spike constant k and the k ladder;
- the dedup window and event time;
- event eligibility;
- the FA grid and threshold matching;
- the window pair;
- segment assembly (P-SEG) and gap handling;
- B3/B4 adaptation choices;
- resampling;
- the suite's "within tolerance" and "the measured range" wording;
- run inclusion for A2–A6;
- Leg B's spike-rate window and divergence flag;
- the A.4 index inputs.

For each, say whether it is bounded by a registered value or band, or is an unbounded discretion.

## Output format

Number findings F1, F2, … across all three passes. For each finding give:
- **Pass:** 1, 2, or 3.
- **Severity:** BLOCKER (a rule cannot fire, two outcomes overlap, or a result could be steered after seeing data), MAJOR (a material ambiguity or a mis-classified report form), or MINOR (wording or completeness).
- **Location:** the section id, e.g. DESIGN §D.3 E2, THESIS Amendment A2(c).
- **Evidence:** the exact words from the package that cause the problem, quoted briefly.
- **Why it matters:** the concrete failure — what outcome becomes impossible, ambiguous, or steerable.
- **Proposed fix:** a specific replacement rule or wording, stated so it could be pasted as an amendment.

End with a table of all findings (id, pass, severity, location, one-line summary).

If a pass finds nothing, say "Pass N: no findings" and give the one strongest reason the rule set survives that pass.

There will be ONE follow-up message. It will hold the author's adjudication: for each finding, an amendment or a rebuttal with reasons. In your reply to it, say for each finding whether the amendment closes it, whether the rebuttal stands, or whether the finding remains open, and why. Raise no new findings in that reply unless an amendment itself introduces a defect.

---
