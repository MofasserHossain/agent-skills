# PR title and body

## Title

Use the user's title when they give one; otherwise follow the project's conventions. With no project convention, use a Conventional Commit title under 70 characters: `<type>(<scope>): <summary>`, or `<type>: <summary>` when a scope adds nothing. Describe the concrete outcome. Apply the same default to new branch commit subjects when the project has no commit convention.

When the project squash-merges, the PR title becomes the single commit subject on the base branch: `fix(auth): avoid repeated sign-in requests` turns into a history entry such as `fix(auth): avoid repeated sign-in requests (#190)`. Keep the PR number out of the title itself. Squashing belongs to the separately authorized merge; merge settings and existing history stay unchanged unless that work is requested. A signature badge is separate from title formatting and from passing checks; never claim a commit is signed without verifying it.

## Body

A project template always wins. Otherwise, keep the body to about 25 lines and describe the final change rather than repeating commit messages:

```markdown
## Summary
<one or two sentences: what changed and why>
<the smallest visual that makes it clear, when one helps>

## Changes
- <user-visible fixes first, then grouped by area>

## Evidence
- Before: <failing run, screenshot or output>. After: <passing run, screenshot or output>.
- <one line per check actually run on this revision; missing evidence and unrun checks named, with reasons>

## Merge danger
Door: <one-way | two-way>. Blast radius: <who or what could break: users, consumers, data>.
```

- **Summary visual.** Pick the smallest view that makes the point and place it beside the sentence it supports: pseudocode for logic, a call tree for control flow, a shallow file tree for responsibilities, a component tree for UI structure, a Mermaid diagram for interactions, or a `diff` sketch when the point is what changed. Most changes need one visual or none.
- **Evidence.** For a visual change, a screenshot is the strongest evidence when the environment can capture one. Execution evidence comes next: the test that failed and now passes, or command output. Never invent a baseline or imply that a check ran.
- **Merge danger.** A **two-way door** is cheap to walk back: revert and redeploy. A **one-way door** isn't: a destructive migration, a published API, deleted data. For a one-way door, name the irreversible effect and the recovery step. Keep the **blast radius** to one honest line, with no speculative risk lists.
- No tables or long explanations in the default body.

Adapted from the `pr` skill in mattpocock/skills (MIT), which credits Dex Horthy's show-me skill.
