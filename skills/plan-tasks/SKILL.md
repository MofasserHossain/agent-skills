---
name: plan-tasks
description: "Divide an agreed specification into small end-to-end tasks with explicit dependencies and verification."
---

Read the agreed spec and existing implementation. Search for already-satisfied requirements before creating work.

Create narrow vertical slices: each delivers a demonstrable or independently verifiable outcome through the necessary layers. Prefer an early tracer bullet across integration boundaries. For broad mechanical migrations, use compatible expand/migrate/contract steps when vertical feature slices cannot stay green.

Use [task contract](../../references/task-contract.md) and [task template](../../templates/task.md). Each task names behavior, acceptance criteria, scope, verification, execution/review mode and true blockers. Dependency means required work is complete/integrated, not just that it appears earlier in a list.

Check that the tasks cover the spec without adding features. Mark unresolved decision work HITL or blocked. Review consequential granularity choices with the user; do not re-approve a breakdown already authorized.

Use [tracker conventions](../../references/trackers.md). Store status once. Do not create an implementation ticket for every internal function or repeat the complete PRD in every task.
