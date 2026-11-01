# From a source to an implementation issue

Open the agent in the project being changed. Read the shared workflow through its native entry point or its canonical file. Keep project rules and feature records in that project.

The [example](../examples/remember-sound/brief.md) concerns a fictional app; it is not a new Shikhi Kheli feature or an active task for this kit.

## 1. Supply material

> Use the shared workflow with the meeting notes below. Prepare a brief and explore relevant existing behavior. Resolve product decisions before implementation.

The agent preserves source references, checks the code, separates assumptions and records the [brief](../examples/remember-sound/brief.md). Grilling asks what the source and code cannot settle. Research and prototypes are detours only when they answer a named uncertainty.

## 2. Capture the agreed PRD

> Use write-spec to capture the decisions we settled. Include behavior examples, distinct requirements and verification.

The result is [spec.md](../examples/remember-sound/spec.md). The PRD records the destination; requirement labels let later tasks refer to it. These decisions come from the conversation/evidence, not a second round of invention.

## 3. Review and write issues

> Use plan-tasks on this PRD. Show narrow slices, requirements covered, HITL/AFK, review requirements and blockers. Create the issues after the breakdown is agreed.

The example has two issues:

| Issue | Coverage | Blockers |
|---|---|---|
| [Remember the preference](../examples/remember-sound/issues/01-remember-preference.md) | R1, R3 | None |
| [Preserve it during startup](../examples/remember-sound/issues/02-preserve-during-startup.md) | R2 | First issue |

Each slice has observable acceptance criteria and a meaningful verification plan. This is not a storage layer task followed by an unrelated UI layer task.

## 4. Implement one eligible issue

> Use implement on the selected issue. Read its parent PRD and relevant project rules. Return acceptance evidence and remaining checks.

The executor may be the current agent, another CLI or a future sandboxed worker. It receives the issue, PRD pointers and useful prior evidence. It does not need all historical messages or unrelated issue bodies.

Use TDD where it provides a meaningful feedback loop: a failing behavioral test, implementation, then the next behavior. Follow required final checks. Return a portable result; successful process completion does not mark the issue done.

## 5. Review, QA and resume

Review compares the change with both standards and the PRD. QA checks actual behavior and records what still needs a human. Resolve required review/QA before updating status to done.

A fresh agent resumes from the work records and revision. Native shortcuts vary, while these artifact contracts stay the same. The current kit offers procedures and one-task dispatch; task claiming, automatic status transitions, loops, GitHub publication and Docker remain separate milestones.
