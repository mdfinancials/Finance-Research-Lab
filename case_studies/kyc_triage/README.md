# Project 03 — Synthetic KYC Risk-Based Review Queue

**Problem:** financial institutions must prioritise periodic reviews and investigate data-quality or risk indicators, while controlling false positives and preserving human oversight.

## Design
1. Generate six entirely fictional customer records, with identifiers prefixed `SYN-`.
2. Apply transparent rules: unusually frequent transactions, cash intensity, elevated jurisdiction indicator, PEP flag and stale KYC.
3. Produce explainable reason codes, total risk score and a priority review queue.
4. Compare priority predictions against **synthetic human-review-needed labels** using precision, recall and a confusion matrix.

## Why it matters
An explainable, auditable workflow shows how a first-line analyst could distinguish alerts needing attention from automatic conclusions. **An alert is not a finding of suspicious activity.** PEP status is not evidence of misconduct. Model thresholds are uncalibrated example values, not any bank's policies, law or risk appetite.

## Run
From root: `python -m case_studies.kyc_triage.study`

## Risks and controls
- Never use employer/customer records or other nonpublic banking data.
- Human review is mandatory; no automated account blocking or adverse outcome.
- Validate inputs and record rationales; calibrate thresholds against permitted labelled data.
- Test potential unfair outcomes, false positives and missing data.
- Real AML/CTF obligations require local regulatory and institutional controls not modelled here.

## Analyst conclusion
This educational prototype demonstrates a traceable review queue and evaluation mechanics, not production compliance readiness. Expansion would require governed data, approved policy mappings, role-based access, QA sampling and audit trails.
