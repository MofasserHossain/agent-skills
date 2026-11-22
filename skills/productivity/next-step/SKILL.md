---
name: next-step
description: "Find the next step: pick the shortest route through these skills, or resume unfinished work from its records. Use when unsure which skill fits or what to do next."
---

Choose the **shortest route** that reaches a verified result, or resume the earliest unfinished stage. Read the project's instructions and `.agent-workflow.json` when present, and keep the user's objective, settled decisions and authorization.

Use a named skill by invoking it, or by reading its `SKILL.md` when the host has no skill tool. The catalog lists the whole kit, not what this project installed: route only to installed skills. When one is missing, say which guidance is missing and continue only where the current procedure suffices. Never claim a skill ran.

## Process

### 1. Find the starting point

- **New request:** match it to a route below.
- **Existing work:** read its authoritative record (spec, task, issue) and the latest evidence, and compare that evidence with the current revision. A finished planning stage doesn't prove the build is ready, and an old passing check doesn't cover later edits.

**Done when:** you know whether this is new work or a resume, and which record is authoritative.

### 2. Pick the route

**Main flow: from idea to merged change**

1. `grill-me` settles the open decisions. Start with `to-brief` when the work arrives as notes, messages or documents.
2. **Shaping** detours answer one question each: `research` for facts, `prototype` when only something runnable or visible can decide, `ui-design` for interface flows and states.
3. A multi-session build goes `to-spec` → `to-tasks` → `implement` once per task, each task in a fresh context. A one-session build goes straight to `implement`.
4. `code-review` checks the diff on two axes, Spec and Standards. `qa` checks running behavior against the acceptance criteria.
5. `pr` delivers the change. `retro` turns friction from the run into environment fixes.

**Shortcuts**

- Clear fix or small settled change → `implement`, then `code-review` in proportion.
- PR status, merge check or post-merge sync → `pr` alone, with delivery context only.
- Architecture friction → `improve-codebase-architecture`; the chosen candidate re-enters the main flow at `grill-me`.
- Work moving to another session, agent, workspace or person → `handoff`.
- Skill or instruction quality → `writing-for-agents`.
- Unknown commands or tracker in a new project → `setup-agent-workflow` first.

**Done when:** one route is chosen, with its reason in one line.

### 3. Hand over

Name the next skill and its exact input: the brief, spec path, task file or diff. When resuming, pick the earliest unfinished prerequisite that affects the outcome and leave finished, unrelated stages alone. When scope changed mid-stage, name the affected requirements, decisions and tasks, keep unaffected work, and update the authoritative record before dependent work starts. Task records and tracker conventions belong to `to-tasks`.

**Done when:** the next skill and its input are named. Routing is done here, not when every stage has run.

## Human and agent work

HITL decisions wait for the human's answer; AFK work proceeds only inside settled scope. The executor may change between stages; the brief, spec, tasks and evidence are the portable record. Skip approval checkpoints that existing authorization already covers. End each stage with its artifact, its open questions and the next useful action.

At the boundary between phases or sessions (continue, clear, hand off, subagent or compact), read [context policy](references/context-policy.md).

## Catalog

| Stage | Skill |
|---|---|
| Set up a project | `setup-agent-workflow` |
| Turn raw material into a brief | `to-brief` |
| Settle decisions | `grill-me` |
| Investigate facts | `research` |
| Test a design question | `prototype` |
| Design interface flows and states | `ui-design` |
| Write the spec | `to-spec` |
| Split the spec into tasks | `to-tasks` |
| Build one task | `implement` |
| Review the diff | `code-review` |
| Check running behavior | `qa` |
| Deliver a pull request | `pr` |
| Improve the environment | `retro` |
| Assess architecture | `improve-codebase-architecture` |
| Continue elsewhere | `handoff` |
| Improve agent instructions | `writing-for-agents` |
