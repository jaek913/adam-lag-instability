# Independent check of DESIGN Amendments 7–14 and suite findings S-1 to S-6 — prompt (paste as the ONLY message of a fresh session, followed by the package)

You are an adversarial reviewer of eight amendments to a public pre-registration, and of the six synthetic-suite findings that prompted most of them. The package below has five parts:

1. **Amendments 7–14**, verbatim as appended to DESIGN.md (under review).
2. **The frozen text they modify**, verbatim from the public tag `prereg-v1`: the DESIGN header, D.0–D.3 (with §K), D.5 and D.7.
3. **Suite findings S-1 to S-6** with their evidence, verbatim from the author's findings file.
4. **The suite grader's verdict**, verbatim.
5. **Amendments 1–6**, context only. They are already in force and are not under review here.

No data, code or decision log is provided. Judge only what is written. Do not browse the web.

**Background, stated once.**
- **The design.** A fast–slow moving-average divergence detector (D_div) is compared with four baseline alarms (B1–B4) on how early they warn of loss spikes, at a matched false-alarm rate. The statistic is the mean lead, with misses counted as 0, and the per-resample minimum contrast C_min against the best baseline. The comparison is made on a public training log (A1). Its result (E2) decides a kill rule (§K): REFUTE stops the project. §K is frozen.
- **What has been read on A1.**
  - Step index, null masks and run metadata.
  - Loss values, to enumerate events: 61 events at k = 4, 57 eligible, public before Amendment 7.
  - Byte hashes of the stored files.
  - **No gradient-norm value has entered any computation.** No detector score, threshold or lead exists on real data.
- **The suite (D.5).** Synthetic series must pass before E2 may touch real data. While building it, the author found six problems (S-1 to S-6). After S-1 to S-4, the criterion or construction was changed by amendment, some after a failed run. S-5 is a severity record. S-6 is unresolved.
  - The frozen D.5 text says the suite must be "committed and ALL PASS before any hashed-data run".
  - The author's working standard says suite failures may fix code only, "never rules/thresholds/report form", and flags "any saturating/tie-prone/no-dynamic-range metric" as verdict-invalid.
- **One fact about Amendment 14.3, stated by the project owner.** Its clause "the cell fails unless D_div and at least one baseline meet the ≥ 80 % detection condition at both L of every pair" was added by the project owner to prevent a vacuous pass, before any dynamic-range cell was run. In the graded run, B2 and B4 separate cleanly; D_div does not.

**This is a single-round check.** There is no follow-up message and no fix round. Your reply is final.

## Seven passes, one concern each — keep them separate

**Pass 1 — Permissibility.** The frozen header rule says: "No amendment to §K's thresholds, windows, spike definition, or FA grid is permitted after A1 is touched." For each of Amendments 7–14:
- does it change any of those four things, or only suite construction and suite criteria?
- could it have been chosen with knowledge that favours one E2 outcome?

**Pass 2 — Can every rule still return each of its outcomes?** Cover E2 (SUPPORT / INCONCLUSIVE / REFUTE) and §K (STOP / PROCEED) as amended, using the suite's measured outcome rates in Parts 3–4. State plainly whether, at A1's realised regime, E2 can plausibly return SUPPORT, and what a REFUTE would and would not establish.

**Pass 3 — Is any rule a judgment described as execution?** List every place in Amendments 7–14 where two analysts could compute different numbers, or choose a construction after seeing a result.

**Pass 4 — Does any amendment change more than it declares?** Look for changes to a frozen number, rule partition, event definition or report form, explicit or implied, beyond what each amendment states.

**Pass 5 — Internal consistency.** Check Amendments 7–14 against each other, against Amendments 1–6 and against the frozen text. Examples:
- 8.1's reference oracle against the frozen D.5 pass criteria;
- 12.2's per-experiment gates against D.5's "before any hashed-data run";
- 14.1's move of the broken fixture;
- the seed-disjointness claims.

**Pass 6 — Question (a): S-6.** Is S-6 a **pipeline failure**, meaning the E2 verdict is invalid because the lead statistic has no usable dynamic range? Or is it a **property of D_div**, meaning the pipeline resolves lead differences, as B2 and B4 show, while D_div's lead responds weakly, so it should be reported beside E2 as a limitation? Give the strongest case for each reading, then your verdict, and what evidence would change it.

**Pass 7 — Question (b): correction or rescue?** For each of S-1, S-2, S-3, S-4, S-6 (and S-5 if relevant): was the post-failure change, or the proposed treatment, a **legitimate correction** of a test that was mis-specified for what it was meant to check? Or a **rescue** that lowers a bar to let the experiment proceed? Judge by these questions:
- whether the original criterion could be met by any correct pipeline;
- whether the change was fixed before the run that graded it;
- whether it was graded on fresh seeds;
- whether it weakens what the suite certifies about E2.

## Output format

Number findings R1, R2, …. For each finding give:
- **Pass:** 1–7.
- **Severity:** BLOCKER, MAJOR or MINOR.
- **Location:** amendment section, frozen section or finding id.
- **Evidence:** a short quote.
- **Why it matters.**
- **Proposed fix:** amendment wording that could be pasted in.

For Passes 6 and 7 also give an explicit verdict line:
- `S-6: PIPELINE-INVALID` or `S-6: METHOD PROPERTY`;
- `S-n: CORRECTION` or `S-n: RESCUE` for each finding.

End with a table of all findings and verdicts. If a pass finds nothing, say "Pass N: no findings" and give the strongest reason.
