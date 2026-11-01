---
{
  "schema_version": 1,
  "id": "08-pilot",
  "status": "draft",
  "execution": "hitl",
  "review": "human",
  "blocked_by": [
    "04-loop",
    "05-docker",
    "06-output-repair",
    "09-workspace-lifecycle"
  ]
}
---
# Evaluate the sequential runner and runtime on an authorized task

## Context
[Adaptation specification](../spec.md) and [source assessment](../assessment.md).

## Requirements covered
R2, R3, R4, R5, R6, R7, R9 in the parent specification.

## Expected behavior
A human can judge whether real execution meets the contracts and improves accepted-result effort.

## Acceptance criteria
- [ ] Record executor/runtime versions, authorized scope, command profile and actual outcomes.
- [ ] Exercise interruption/recovery and required review without duplicate side effects.
- [ ] Measure acceptance, correction burden, latency and available usage; report unavailable evidence.
- [ ] Compare with interactive execution before expanding concurrency or enabling unattended project delivery.

## Verification
Requires explicit live-run and runtime/account authorization where applicable. Do not infer it from this draft task. GitHub live validation is separate if task 07 is adopted.

Run `python3 -m unittest discover -s tests -v` and `python3 tools/workflow.py check` after implementation; validate packages if resources change.

## Scope
Only this outcome and the parent contract. Later integrations and external actions require their own authorization.

## Evidence
Not implemented.
