---
name: pull-request
description: "Prepare or update a pull request, check PR or merge status, or sync after a confirmed merge using the project's delivery rules."
---

Read the project's root instructions and its routed delivery rules first. Keep the target project as the working directory. Project policy owns branch/base names, commit shape, title/body conventions, verification commands, merge authority, and concurrency limits; do not import defaults from another project. If a consequential policy is unknown, resolve it before the affected action.

Choose only the requested operation below. Read relevant delivery sections, not product, architecture, implementation skills or all workflow stages for a status-only task. If the task expands into edits or testing, follow those project reading routes before acting.

## Status or merge check

Identify the intended repository and PR from the request, current branch, or existing evidence. Query its actual state using an available connected repository tool or authenticated CLI. Distinguish open, closed without merge, and merged; report the URL and relevant check/review state. Do not treat closure or a successful CI run as proof of merge. Do not mutate branches, rerun app verification, or start new work for a status-only request.

## Prepare, create, or update

1. Inspect branch, worktree, staged/unstaged changes, target base and existing PRs. For creation, require a user request and stop on the target base branch (main by default when the project specifies no other base). Reuse an existing PR for this work instead of creating another; respect the project's concurrency limits. Preserve unrelated/staged changes and branch names; do not switch/reset a dirty checkout blindly.
2. Read the task/spec and discover verification commands from this repository's applicable instructions, .agent-workflow.json, scripts and CI. Run required final and conditional checks in the project's order; there is no universal check/build command. Stop delivery on the first failed required check and show its command/output. Fix only within scope, rerun affected checks and report remaining human checks; never count stale evidence as current verification.
3. Review the full diff against the refreshed remote base, including any intended uncommitted work. Prepare the commit(s) and a concrete title/body using the format below, subject to project policy. Keep secrets/private logs out of both code and description.
4. Before a new PR, show the commits, diff statistics and proposed title/body, then wait for the user's go-ahead. Existing approval of that exact result satisfies this gate; initial permission to prepare a PR does not replace diff review. Material scope changes require an updated review. Prepare all reversible work before this checkpoint.
5. After approval, push the intended branch with an upstream and create the PR against the verified base using available connected repository tools or the project's authenticated CLI. Use structured text or a body file for multiline descriptions. Rewrite history only if authorized by project policy; protect authorized force-pushes with a lease. Report the PR URL and verification outcome, following the project's post-opening wait rule. A PR request does not authorize merge or deployment.

## Title and description

Use the user's supplied title when present; otherwise follow project conventions. When the project has no title convention, use a Conventional Commit title, `<type>(<scope>): <summary>`, under 70 characters, suitable as the squash-merge entry.

Keep the body to about 25 lines unless a project template requires more. Describe the final change rather than repeating commit messages:

- `## Summary`: one or two sentences explaining the concrete change and why.
- `## Changes`: short bullets grouped by area, with user-visible fixes first.
- `## Verification`: one line per check actually performed; identify checks not run and why.
- `## Notes`: only when needed for a material risk, follow-up or manual step, in one or two lines.

Use no tables or long explanations in the default body. Preserve required repository templates instead of overriding them with this format.

## Sync after merge

Verify the PR really merged and read the project's post-merge rules. Fetch and update the intended local base safely, preserving dirty work and existing workspace branch names. Do not delete branches, reset unrelated changes, start another task or open a new PR unless authorized. If the request was only to check status, report it without syncing.

## Result

Return the operation performed, PR URL/state when available, checks actually run, local changes made, and remaining blockers or human checks. If remote access is unavailable, report that limit; do not infer remote state from local Git alone. This procedure runs through the current agent, not a separate automatic PR bot or worker.

Before repeating a create/update operation after a failure, query the remote state to see whether it already succeeded. Reuse the intended existing PR rather than creating a duplicate. If its branch head changed since inspection, refresh the diff and verification assessment before an authorized write; do not overwrite concurrent edits using a stale description or revision assumption.

Tie delivery evidence to the revision it covers. Distinguish local preparation, successful push and confirmed PR creation/update in the result so a partially completed operation can resume without repeating side effects. A failed remote request leaves its outcome unknown until checked.
