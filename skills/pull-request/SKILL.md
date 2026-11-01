---
name: pull-request
description: "Prepare or update a pull request, check PR or merge status, or sync after a confirmed merge using the project's delivery rules."
---

Read the project's root instructions and its routed delivery rules first. Keep the target project as the working directory. Project policy owns branch/base names, commit shape, title/body conventions, verification commands, merge authority, and concurrency limits; do not import defaults from another project. If a consequential policy is unknown, resolve it before the affected action.

Choose only the requested operation below. Read relevant delivery sections, not product, architecture, implementation skills or all workflow stages for a status-only task. If the task expands into edits or testing, follow those project reading routes before acting.

## Status or merge check

Identify the intended repository and PR from the request, current branch, or existing evidence. Query its actual state using an available connected repository tool or authenticated CLI. Distinguish open, closed without merge, and merged; report the URL and relevant check/review state. Do not treat closure or a successful CI run as proof of merge. Do not mutate branches, rerun app verification, or start new work for a status-only request.

## Prepare, create, or update

1. Inspect branch, worktree, staged/unstaged changes, target base, existing PRs, and the relevant diff. Preserve unrelated changes and existing staged content; do not blanket-stage or discard work. Respect project limits on simultaneous PRs and branch naming. Do not switch/reset a dirty checkout blindly.
2. Read the task/spec and existing verification evidence needed to describe the actual change. Run project-required final checks and conditional checks before committing/delivery; do not invent check exemptions or count stale evidence as current verification. Resolve failures within scope and report remaining human checks.
3. Prepare the required commit(s), title and body according to project policy. Lead with the concrete problem and resulting behavior; include useful validation and limitations. Prefer a structured tool argument or a temporary body file for multiline text. Keep secrets and private run logs out of commits/descriptions.
4. Perform only actions already authorized by the user or approved plan. Preparation does not itself authorize pushing, publishing, force-pushing, or merging. When authorization is required, finish the concrete reviewable preparation before asking; do not ask again for an already-authorized action. Rewrite commit history only as permitted by project policy, protecting unrelated work; use lease protection if a force-push is authorized.
5. Use available connected repository tools or the project's authenticated CLI to create/update the intended PR against the verified base. Refresh its title/body when scope changes. Report the PR link, verification outcome and remaining human checks; follow the project's post-opening wait rule. Do not merge unless separately authorized and project rules permit it.

## Sync after merge

Verify the PR really merged and read the project's post-merge rules. Fetch and update the intended local base safely, preserving dirty work and existing workspace branch names. Do not delete branches, reset unrelated changes, start another task or open a new PR unless authorized. If the request was only to check status, report it without syncing.

## Result

Return the operation performed, PR URL/state when available, checks actually run, local changes made, and remaining blockers or human checks. If remote access is unavailable, report that limit; do not infer remote state from local Git alone. This procedure runs through the current agent, not a separate automatic PR bot or worker.

Before repeating a create/update operation after a failure, query the remote state to see whether it already succeeded. Reuse the intended existing PR rather than creating a duplicate. If its branch head changed since inspection, refresh the diff and verification assessment before an authorized write; do not overwrite concurrent edits using a stale description or revision assumption.

Tie delivery evidence to the revision it covers. Distinguish local preparation, successful push and confirmed PR creation/update in the result so a partially completed operation can resume without repeating side effects. A failed remote request leaves its outcome unknown until checked.
