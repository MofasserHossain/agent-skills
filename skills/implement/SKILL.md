---
name: implement
description: "Implement one agreed task with focused context, meaningful tests and portable verification evidence."
---

Read the selected task, applicable project instructions, relevant spec/decisions and dependency evidence. Confirm that required prior changes are available. Work only within its scope. Pull additional library documentation and architecture detail when the task needs them; keep always-required project rules explicit rather than treating them as optional lookup material.

For behavior changes, use a narrow feedback loop: one meaningful failing test, implementation, verification, then the next behavior. Tests observe public behavior and independently known expected outcomes. For bugs, reproduce the reported symptom before fixing it. Follow the project's existing test boundaries; no implementation-mirroring tests. Read the project's named checks and issue Verification section for the actual runner command and focused target syntax. An environment/command failure is not the intended RED. See [project checks and TDD](../../references/verification-policy.md).

Use proportionate checks for copy/configuration changes and prototypes. Refactor only where it helps the task and remains covered; keep unrelated cleanup separate.

Run targeted checks while iterating and the project's required final checks before reporting success. For UI or hardware-dependent behavior, distinguish runtime checks performed from manual checks remaining.

Read [execution policy](../../references/execution-policy.md). Stop dependent work on a missing product decision; record a precise blocker. Do not infer merge/publish permission from AFK mode.

Return [the portable result](../../references/result-contract.md) with acceptance evidence. A commit, process exit or model claim is not acceptance. Follow project rules for commits and external actions.
