---
name: qa
description: "Check delivered behavior against acceptance criteria and record runtime and manual verification evidence."
---

Read the task/spec and revision under review. Map acceptance criteria to meaningful checks using [QA template](../../templates/qa.md).

Exercise actual user flows where the environment permits. Include relevant failure/empty states and platform-specific constraints. Respect shared device/browser courtesy rules and use disposable data when mutation is part of the check.

Record expected versus actual behavior, environment, commands/screenshots/log references and failures. Do not substitute screenshots for behavior that requires interaction or sound. Distinguish passed checks, failed checks and checks not performed.

Return defects to appropriately scoped tasks. Keep human-only judgments pending until a human actually completes them. Acceptance requires the agreed checks and review, not merely a clean automated suite.
