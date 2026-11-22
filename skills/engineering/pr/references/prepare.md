# Prepare, create or update

1. **Inspect.** Check the branch, worktree, staged and unstaged changes, target base and existing PRs. Creating a PR requires a user request; stop if you are on the target base branch (main, when the project names no other). Reuse an existing PR for this work and respect the project's concurrency limits. Preserve unrelated and staged changes and branch names; never switch or reset a dirty checkout blindly.
   Done when: you know the base, the branch, the changes in scope and whether a PR already exists.

2. **Verify.** Read the task or spec. Discover verification commands from the project's instructions, `.agent-workflow.json`, scripts and CI; there is no universal check command. Run the required final and conditional checks in the project's order. Stop delivery at the first failed required check and show its command and output. Fix only within scope, rerun the affected checks, and report the human checks that remain. Stale evidence never counts as current.
   Done when: every required check passed on this revision, or delivery stopped on a named failure.

3. **Prepare.** Review the full diff against the refreshed remote base, including intended uncommitted work. Prepare the commits, and a concrete title and body following the [PR title and body](pr-body.md), subject to project policy. Keep secrets and private logs out of both the code and the description.
   Done when: the commits, title and body exist locally.

4. **Gate.** Before opening a new PR, show the commits, the diff statistics and the proposed title and body, then wait for the user's go-ahead. Earlier approval of this exact result satisfies the gate. Permission to prepare a PR does not replace review of the diff, and a material scope change needs a fresh review. Finish all reversible work before this checkpoint.
   Done when: the user has approved this exact result.

5. **Publish.** Push the intended branch with an upstream and create the PR against the verified base, using connected repository tools or the project's authenticated CLI. Pass multi-line descriptions as structured text or a body file. Rewrite history only when project policy authorizes it, and protect an authorized force-push with a lease. Report the PR URL and the verification outcome, and follow the project's post-opening wait rule.
   Done when: the PR URL is confirmed from the remote.
