# Portable result

Every executor returns a concise report containing:

- Task id and status claim: implemented, blocked, already-satisfied, or incomplete.
- What changed, with revision/diff references.
- Each acceptance criterion and its evidence or explicit remaining gap.
- Verification commands and outcomes, including anything not run.
- Manual review/QA still needed.
- Blockers or unresolved decisions.
- Usage and elapsed time when the executor exposes them; otherwise mark unavailable.

Provider transcript/session ids are optional supplementary pointers. They do not replace this portable report.

Do not equate elapsed time, commit count or successful exit with completion. Already-satisfied tasks require evidence too.
