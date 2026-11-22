---
name: to-tasks
description: "Split a spec into tracer-bullet tasks with acceptance criteria, requirement coverage and real blockers. Use when an agreed spec needs a build plan, or work must be broken into tasks or issues."
---

Break agreed work into **tasks**: thin vertical slices, each declaring the tasks that **block** it. A plan with one entry per layer or per function hides the outcome until the end; tracer bullets prove the whole path early.

## Process

### 1. Read the spec and the code

Read the agreed spec and the current implementation. Before creating work for a requirement, check whether it is already satisfied. Look for a small refactor that would make the rest easy: make the change easy, then make the easy change.

**Done when:** you know which requirements need work and which are already met, with evidence for each.

### 2. Draft the slices

- Each task cuts a narrow but complete path through every layer it needs: data, service, interface, tests. A backend slice can be a complete observable API or job with no screen.
- A finished task is demonstrable or verifiable on its own.
- Each task fits one fresh agent session.
- The first task is a **tracer bullet** across the integration boundaries; an enabling refactor comes before it.
- A **blocker** means the other task is done and integrated, not merely earlier in the list.

**Wide refactors** are the exception. One mechanical change that breaks many call sites at once (renaming a column, retyping a shared symbol) can't land as a green vertical slice, so sequence it **expand → migrate → contract**:
1. Add the new form beside the old.
2. Migrate call sites in batches, each batch its own task blocked by the expand.
3. Delete the old form in a final task blocked by every batch.

**Done when:** every in-scope requirement maps to a task, or to evidence that it is already met, and every task lists its blockers.

### 3. Quiz the user

Show the breakdown as a numbered list:

```
1. <Title>: <the end-to-end behavior it delivers>
   Blocked by: <task numbers, or "none">  ·  Mode: AFK | HITL  ·  Covers: R1, R3
```

Then ask: is the granularity right, or too coarse or too fine? Does each task depend only on tasks that truly gate it? Should any tasks merge or split? Mark work that waits on an unresolved decision as HITL or blocked. Iterate until the user approves; a breakdown that is already authorized needs no second approval.

**Done when:** the user approves the breakdown.

### 4. Write the tasks

Use the [task template](templates/task.md) and the [task contract](references/task-contract.md): behavior, acceptance criteria, scope, verification, execution and review mode, and blockers. In **Requirements covered**, link the spec's labels instead of copying the requirement text. Store status once, in the tracker the project chose; read the [tracker conventions](references/trackers.md). Create blocking tasks first, so later tasks can reference real identifiers. Leave the parent issue or spec unchanged.

**Done when:** every blocker chain ends in ready work or an explicit open decision with no cycles, and any gaps or overlaps against the whole spec are deliberate.

Work then starts at the **frontier**: every task whose blockers are done.
