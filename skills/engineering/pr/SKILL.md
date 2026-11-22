---
name: pr
description: "Prepare, create or update a pull request, check PR or merge status, or sync after a merge, under the project's delivery rules. Use for any pull request operation."
---

Deliver a change through a pull request under the **project's** delivery rules. Project policy owns branch and base names, commit shape, title and body conventions, verification commands, merge authority and concurrency limits; never import defaults from another project. Resolve an unknown consequential policy before the action it affects, and keep the target project as the working directory.

## Process

### 1. Pick the operation

Read the project's root instructions and its delivery rules, then read only the branch you need:

- **Status or merge check** → [status](references/status.md). Read-only: never change branches, rerun app checks or start new work.
- **Prepare, create or update** → [prepare](references/prepare.md), plus the [PR title and body](references/pr-body.md).
- **Sync after a confirmed merge** → [sync](references/sync.md).

If the task grows into edits or testing, follow the project's reading routes for that work before acting.

**Done when:** one operation is chosen and its reference is read.

### 2. Run it

Follow that branch's steps. Before repeating a create or update after a failure, query the remote state, because the first attempt may have succeeded; reuse the intended PR instead of creating a duplicate. If the branch head changed since you inspected it, refresh the diff and the verification assessment before any authorized write, so you never overwrite concurrent work with stale assumptions.

**Done when:** the branch's own completion check holds.

### 3. Report

Return the operation performed, the PR URL and state when available, the checks that actually ran (tied to the revision they cover), local changes made, and remaining blockers or human checks. Keep local preparation, a successful push and a confirmed PR creation or update apart, so a partial run can resume without repeating side effects. A failed remote request leaves its outcome unknown until you check it. Without remote access, say so; never infer remote state from local Git alone.

**Done when:** someone could resume or verify the delivery from your report without re-running anything.

A PR request never authorizes merge or deployment. This procedure runs through the current agent, not a separate PR bot.
