---
{
  "schema_version": 1,
  "id": "06-output-repair",
  "status": "draft",
  "execution": "afk",
  "review": "human",
  "blocked_by": [
    "03-once"
  ]
}
---
# Repair report extraction without rerunning implementation

## Context
[Adaptation specification](../spec.md) and [source assessment](../assessment.md).

## Requirements covered
R7 in the parent specification.

## Expected behavior
A malformed report can be corrected in a resumable adapter without repeating the task work or delivery actions.

## Acceptance criteria
- [ ] Correction attempts are capped and retain original output and feedback.
- [ ] Adapters without safe resume stop for inspection.
- [ ] A fake side-effect counter stays at one across report repair; output-only tasks avoid an unconditional extraction pass.

## Verification
Use fake adapter sessions with invalid then valid output, exhausted repair and unavailable resume. No provider calls.

Run `python3 -m unittest discover -s tests -v` and `python3 tools/workflow.py check` after implementation; verify relocated skills if resources change.

## Scope
Only this outcome and the parent contract. Later integrations and external actions require their own authorization.

## Evidence
Not implemented.
