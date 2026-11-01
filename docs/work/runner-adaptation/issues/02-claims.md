---
{
  "schema_version": 1,
  "id": "02-claims",
  "status": "draft",
  "execution": "afk",
  "review": "human",
  "blocked_by": [
    "01-preflight"
  ]
}
---
# Claim a task and recover interrupted ownership

## Context
[Adaptation specification](../spec.md) and [source assessment](../assessment.md).

## Requirements covered
R2 in the parent specification.

## Expected behavior
Two dispatches cannot unintentionally edit one workspace; interrupted ownership is inspectable and safely recoverable.

## Acceptance criteria
- [ ] Managed and existing run dispatch share an exclusive workspace boundary.
- [ ] A claim binds task digest, run id and workspace; changed eligibility prevents launch.
- [ ] Crash fixtures cover every claim/state ordering point; stale age alone never authorizes release.

## Verification
Use fake processes for contention and changed-task races, and interruption fixtures for recovery. Do not start a live agent.

Run `python3 -m unittest discover -s tests -v` and `python3 tools/workflow.py check` after implementation; verify relocated skills if resources change.

## Scope
Only this outcome and the parent contract. Later integrations and external actions require their own authorization.

## Evidence
Not implemented.
