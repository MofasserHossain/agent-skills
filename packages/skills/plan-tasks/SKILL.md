---
name: plan-tasks
description: "Split agreed multi-session work into independently verifiable tasks with requirement coverage and true blockers."
---

Read the agreed spec and existing implementation. Search for already-satisfied requirements before creating work.

Create narrow vertical slices: each delivers a demonstrable or independently verifiable outcome through the necessary layers. Prefer an early tracer bullet across integration boundaries. For broad mechanical migrations, use compatible expand/migrate/contract steps when vertical feature slices cannot stay green.

Use [task contract](references/task-contract.md) and [task template](templates/task.md). Each task names behavior, acceptance criteria, scope, verification, execution/review mode and true blockers. Dependency means required work is complete/integrated, not just that it appears earlier in a list.

In **Requirements covered**, link to the parent PRD's requirement labels or sections. Check the resulting coverage against the whole spec; gaps and overlaps should be deliberate. Preserve the parent's wording by reference instead of copying every requirement into every issue.

Check that the tasks cover the spec without adding features. Mark unresolved decision work HITL or blocked. Review consequential granularity choices with the user; do not re-approve a breakdown already authorized.

Use [tracker conventions](references/trackers.md). Store status once. Do not create an implementation ticket for every internal function or repeat the complete PRD in every task.

Before declaring the breakdown ready, walk each blocker chain: it must terminate in ready work or an explicit unresolved decision, with no cycles. Check every in-scope requirement has a task or evidence it is already satisfied. An internal layer alone is not a deliverable; a backend slice can be a complete observable API or job without a UI.

Related skill names refer only to skills available in this project or host. If one is absent, continue within this procedure where sufficient or report the missing guidance; do not claim it ran or follow a path to the authoring checkout.
