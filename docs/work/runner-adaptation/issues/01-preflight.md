---
{
  "schema_version": 1,
  "id": "01-preflight",
  "status": "review",
  "execution": "afk",
  "review": "human",
  "blocked_by": []
}
---
# Inspect the whole local graph and select eligible work

## Context
[Adaptation specification](../spec.md) and [source assessment](../assessment.md).

## Requirements covered
R1 in the parent specification.

## Expected behavior
A user can inspect an explicit issues scope without launching an agent or changing task state.

## Acceptance criteria
- [ ] Only ready AFK tasks with done blockers are eligible; selection follows filename order.
- [ ] Unknown edges, duplicate ids, cycles and paths outside the work directory fail.
- [ ] Waiting, empty and recorded-complete scopes are distinct, with reasons and no mutations.

## Verification
Implemented through workflow.py next and shared inventory validation. Review the selection tests and verify the full kit checks before acceptance.

Run `python3 -m unittest discover -s tests -v` and `python3 tools/workflow.py check` after implementation; verify relocated skills if resources change.

## Scope
Only this outcome and the parent contract. Later integrations and external actions require their own authorization.

## Evidence
Implemented in tools/workflow.py with five additional selection/graph test cases in tests/test_workflow.py. All 76 kit tests passed, as did workflow check, rebuilt package check and diff check. The nine adaptation tasks were parsed through the inventory; they correctly return waiting with no selection. Human review is pending; no live executor was launched.
