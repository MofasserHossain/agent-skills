---
{
  "schema_version": 1,
  "id": "05-docker",
  "status": "draft",
  "execution": "afk",
  "review": "human",
  "blocked_by": [
    "03-once"
  ]
}
---
# Run the same once contract in an explicitly selected Docker Sandbox

## Context
[Adaptation specification](../spec.md) and [source assessment](../assessment.md).

## Requirements covered
R6 in the parent specification.

## Expected behavior
A configured isolated runtime can execute the same bounded task without changing its task or evidence contracts.

## Acceptance criteria
- [ ] Version/profile preflight separates current sbx commands from historical docker sandbox syntax.
- [ ] Project-contained skills, command I/O, workspace mapping and exported artifacts are verified with fake runtime commands.
- [ ] Isolation failure cannot fall back silently to host; owned resource cleanup retains failed work.
- [ ] Host credential/network access and authentication prerequisites are explicit; no account configuration is performed by tests.

## Verification
Use a fake runtime executable for lifecycle/argv/failure tests. Real sandbox compatibility needs a separately authorized pilot.

Run `python3 -m unittest discover -s tests -v` and `python3 tools/workflow.py check` after implementation; verify relocated skills if resources change.

## Scope
Only this outcome and the parent contract. Later integrations and external actions require their own authorization.

## Evidence
Not implemented.
