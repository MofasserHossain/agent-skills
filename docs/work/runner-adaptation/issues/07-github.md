---
{
  "schema_version": 1,
  "id": "07-github",
  "status": "draft",
  "execution": "afk",
  "review": "human",
  "blocked_by": [
    "03-once"
  ]
}
---
# Adapt ready-task selection and delivery to GitHub records

## Context
[Adaptation specification](../spec.md) and [source assessment](../assessment.md).

## Requirements covered
R8 in the parent specification.

## Expected behavior
A chosen GitHub task can use the same runner contracts with native blockers and idempotent authorized updates.

## Acceptance criteria
- [ ] Pagination and parent-spec versus executable-task distinctions prevent missing or oversized work.
- [ ] Claims, output publication and remote revision checks withstand repeated delivery requests.
- [ ] One orchestrator owns tracker mutations; credential enforcement is documented honestly.
- [ ] No automatic merge or issue closure before project-defined acceptance/delivery conditions.

## Verification
Use a fake tracker for pagination, races, duplicate operations and failures. Do not create real labels, workflows, secrets or issues to validate.

Run `python3 -m unittest discover -s tests -v` and `python3 tools/workflow.py check` after implementation; validate packages if resources change.

## Scope
Only this outcome and the parent contract. Later integrations and external actions require their own authorization.

## Evidence
Not implemented.
