---
{
  "schema_version": 1,
  "id": "03-once",
  "status": "draft",
  "execution": "afk",
  "review": "human",
  "blocked_by": [
    "02-claims"
  ]
}
---
# Run one task through evidence collection and supervised evaluation

## Context
[Adaptation specification](../spec.md) and [source assessment](../assessment.md).

## Requirements covered
R3, R4 in the parent specification.

## Expected behavior
A selected local task runs once and returns a durable evaluated result without equating process exit with acceptance.

## Acceptance criteria
- [ ] Preview has no effects; execution preserves an inspectable journal and report.
- [ ] Malformed reports, wrong task/revision, failed checks and pending judgments prevent acceptance.
- [ ] Human review remains pending; already-satisfied behavior can be evidenced without a commit.
- [ ] Acceptance transitions use the claimed task digest and preserve partial work on failure.

## Verification
Use fake workers and check commands for success, invalid output, timeout, changed revision and human-review cases. Keep the portable result schema versioned.

Run `python3 -m unittest discover -s tests -v` and `python3 tools/workflow.py check` after implementation; verify relocated skills if resources change.

## Scope
Only this outcome and the parent contract. Later integrations and external actions require their own authorization.

## Evidence
Not implemented.
