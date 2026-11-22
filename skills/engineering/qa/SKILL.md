---
name: qa
description: "Check a revision's running behavior against its acceptance criteria and record evidence. Use when built work needs runtime or manual verification, or a fix needs rechecking."
---

Exercise the real behavior of a pinned revision against each acceptance criterion, and record what passed, what failed and what was not performed. QA is a feedback loop: it can run on an integrated, verifiable increment while other work continues. A clean automated suite is not acceptance.

## Process

### 1. Pin what you test

Read the task or spec, then fix the revision and environment under test. Never test a working tree another worker is changing, and respect shared device and browser ownership.

**Done when:** the revision, the environment and the criteria in scope are recorded.

### 2. Plan each check

For every criterion, set the preconditions (representative data, user role, configuration) and the expected outcome. Derive the expectation from the agreed requirement, never from what the implementation happens to do. Include the relevant failure, empty and platform-specific states.

**Done when:** each criterion maps to a check with an expected outcome.

### 3. Exercise and record

Run the real user flows wherever the environment allows; use disposable data when a check changes state. Record each result in the [QA template](templates/qa.md):

| Criterion | Check | Expected | Actual | Status |
|---|---|---|---|---|
| R1: <criterion> | <steps or command> | <expected outcome> | <observed, with an evidence link> | passed / failed / not performed |

A screenshot can't stand in for behavior that needs interaction or sound. When an environment failure stops a check, mark it "not performed" with its cause; that is not a product defect.

**Done when:** every in-scope criterion has a row.

### 4. File defects

Search the authoritative backlog first, and update a matching issue instead of duplicating it. Otherwise create one bounded task with reproduction steps, expected and actual behavior, impact, evidence, the failing criterion and its blockers. Use the project's task convention, or the contract of the `to-tasks` skill; if neither is available, return a defect report instead of inventing tracker metadata. Local task creation follows current authorization; remote publication needs explicit authorization. A new product request isn't a defect: send it back to `grill-me` or the spec before it becomes AFK work.

**Done when:** every failed row links to its defect.

### 5. Verdict and recheck

Report **accepted**, **changes needed** or **pending evidence**. A failing criterion keeps acceptance open even when a follow-up task exists, and a human-only judgement stays pending until a human completes it. After a fix is integrated, recheck the affected criterion and the neighboring behavior it could regress, keeping the original failure on record.

**Done when:** every in-scope criterion is accounted for and the verdict follows from the table.
