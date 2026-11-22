---
name: implement
description: "Build one task or clear fix test-first and return evidence for every acceptance criterion. Use when behavior is settled: a ready task, a reproducible bug or a small clear change."
---

Build one scoped piece of work whose intended behavior is settled, one **red → green** slice at a time, and return evidence for each acceptance criterion. A commit, a process exit or a model's claim is not acceptance.

## Process

### 1. Load the task

Read the selected task, the project's instructions, the relevant spec and decisions, and evidence that the task's blockers are done and integrated. Pull library documentation and architecture detail when the task needs them; rules the project always requires are never optional reading. Then check whether the requested behavior is already satisfied. If it is, return that evidence instead of manufacturing a change.

**Done when:** you can state the acceptance criteria and the scope boundary, and you have confirmed the prerequisites are available.

### 2. Reproduce a bug first

For a bug, get a feedback loop that goes **red** on the reported symptom before you read code to build a theory. When the cause isn't obvious after a first look, read [diagnosing bugs](references/diagnosing-bugs.md).

**Done when:** you have run one command that shows the user's symptom, or you have reported why no such loop can be built.

### 3. Build in vertical slices

For each behavior, at a **seam** agreed in the spec or task:

1. **Red:** write one test that fails because the behavior is missing or wrong. A missing dependency, an invalid flag or a broken fixture is not the intended red.
2. **Green:** write only enough code to make it pass.
3. Move to the next behavior. One test, one implementation, repeat; never write all the tests first.

Tests observe public behavior. Expected values come from an independent source (a known literal, a worked example, the spec), never recomputed the way the code computes them. Read the project's named checks and the task's Verification section for the runner and its focused-target syntax; see [project checks and TDD](references/verification-policy.md). Copy, configuration and prototypes get proportionate checks. Refactor only where it helps the task and stays covered; keep unrelated cleanup out.

**Done when:** every acceptance criterion has a passing test or a named runtime or manual check.

### 4. Verify

Run focused checks while iterating, and the project's required final checks before reporting success. For UI or hardware-dependent behavior, keep the runtime checks you performed apart from the manual checks that remain.

**Done when:** the final checks ran on the current revision, or each check that couldn't run is named with its reason.

### 5. Report

Read the [execution policy](references/execution-policy.md) and return the [portable result](references/result-contract.md). Account for each acceptance criterion as demonstrated, failed or unverified, and name blockers and manual checks. A missing product decision stops dependent work; record it as a precise blocker. Follow the project's rules for commits and external actions; AFK mode never implies permission to merge or publish. Name what comes next: `code-review` for the diff, `qa` for behavior that must be seen running.

**Done when:** the report accounts for every acceptance criterion.
