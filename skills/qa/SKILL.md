---
name: qa
description: "Check delivered behavior against acceptance criteria and record runtime and manual verification evidence."
---

Read the task/spec and revision under review. Map acceptance criteria to meaningful checks using [QA template](templates/qa.md).

Exercise actual user flows where the environment permits. Include relevant failure/empty states and platform-specific constraints. Respect shared device/browser courtesy rules and use disposable data when mutation is part of the check.

Record expected versus actual behavior, environment, commands/screenshots/log references and failures. Do not substitute screenshots for behavior that requires interaction or sound. Distinguish passed checks, failed checks and checks not performed.

QA is a feedback loop and may run on an integrated, verifiable increment while other implementation continues. Pin the tested revision/environment; do not test a working tree another worker is changing. Respect shared device ownership.

Search the authoritative backlog before filing a defect. Update an existing matching issue or create one bounded task with reproduction steps, expected/actual behavior, impact, evidence, source requirement and relevant blockers. Use the project's existing task convention, or consult installed `plan-tasks` for the local contract. If neither is available, return a defect report instead of inventing tracker metadata. Local task creation follows the current authorization; remote publication requires authorization. Separate defects from new product requests; scope changes return to grilling/spec decisions before becoming AFK-ready work.

Return ready fixes to planning/implementation and recheck the affected behavior after integration. A failing agreed criterion keeps acceptance open even when a follow-up task exists. Keep human-only judgments pending until a human actually completes them. Acceptance requires the agreed checks and review, not merely a clean automated suite.

Establish preconditions and expected outcomes before exercising each criterion: representative starting data, user role, environment and relevant configuration. Derive expectations from the agreed requirement rather than the observed implementation. When an environment failure prevents a check, record it as not performed with its cause, separate from a product defect.

Finish with every in-scope criterion accounted for and a verdict of accepted, changes needed or pending evidence. Link defects to the failing criterion and retain the original failure when recording a successful recheck. Recheck affected neighboring behavior where the fix can plausibly regress it; avoid repeating unrelated checks without a reason.
