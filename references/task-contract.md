# Task contract

A local task is Markdown with JSON frontmatter:

```text
---
{
  "schema_version": 1,
  "id": "01-example",
  "status": "ready",
  "execution": "afk",
  "review": "human",
  "blocked_by": []
}
---
# A narrow observable outcome

## Context
Source and spec references.

## Expected behavior
What becomes possible.

## Acceptance criteria
- [ ] A specific observable result.

## Verification
How to check the result; include manual checks if needed.

## Scope
Boundaries and relevant constraints.

## Evidence
Record commands, outcomes, changed revision and remaining checks.
```

JSON is used inside the frontmatter to keep parsing dependency-free. Metadata is authoritative; do not repeat editable status in a board.

Statuses: draft, ready, in-progress, blocked, review, done. Done means the required acceptance/review conditions are satisfied. A review status keeps human checks visible.

Execution: hitl or afk. Review: human or automated. AFK execution does not imply permission to merge, publish, spend money or message others.

blocked_by contains sibling task ids within the same issues directory. Dependency completion is done, not merely code written on another unintegrated branch.

Task identity does not change with the executor. Keep unresolved product decisions out of AFK-ready work. Use stable descriptions of behavior and interfaces; implementation navigation pointers may be refreshed as code moves.
