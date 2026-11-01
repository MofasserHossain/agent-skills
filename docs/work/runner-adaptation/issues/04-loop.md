---
{
  "schema_version": 1,
  "id": "04-loop",
  "status": "draft",
  "execution": "afk",
  "review": "human",
  "blocked_by": [
    "03-once"
  ]
}
---
# Execute a bounded sequence using the shared once operation

## Context
[Adaptation specification](../spec.md) and [source assessment](../assessment.md).

## Requirements covered
R5 in the parent specification.

## Expected behavior
A user can run eligible tasks sequentially within explicit count and time limits and inspect why execution stopped.

## Acceptance criteria
- [ ] Count, per-run and total time bounds are validated and enforced.
- [ ] Each iteration re-reads current eligibility; cycles and blocked dependencies never fall back to a candidate.
- [ ] Failure and invalid evidence stop with typed reasons; independent ready tasks can proceed while HITL/review dependents wait.
- [ ] No automatic replay or marking human review done to unblock another task.

## Verification
Use fake workers and an injectable clock or short disposable processes to verify bounds, graph changes and all stop reasons.

Run `python3 -m unittest discover -s tests -v` and `python3 tools/workflow.py check` after implementation; validate packages if resources change.

## Scope
Only this outcome and the parent contract. Later integrations and external actions require their own authorization.

## Evidence
Not implemented.
