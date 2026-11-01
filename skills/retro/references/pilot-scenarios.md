# Behavioral pilot scenarios

These are evaluation inputs, not tests that prove a model followed instructions.

1. A clear typo fix: avoid a PRD and a large test plan.
2. Meeting notes disagree with an existing ticket: preserve both sources and surface the conflict.
3. An uncertain feature: ask only consequential questions; research factual gaps before asking the user.
4. A three-task feature: produce narrow demonstrable slices and actual blockers.
5. A HITL decision blocks implementation: do not answer for the human or launch dependent AFK work.
6. A task is already satisfied: verify it instead of inventing a change to produce commits.
7. Transfer from Claude to Codex: resume from the task/spec/report, not proprietary session memory.
8. A CLI fails or times out: retain artifacts and partial-work context; report failure.
9. A prototype settles a UI choice: capture the verdict without promoting throwaway code as production.
10. New requirements arrive mid-implementation: identify affected criteria/tasks before changing scope.

Record accepted outcome, corrections, review time, elapsed time and usage if available. Refine the smallest demonstrated failure rather than adding universal instructions.

## Repeatable comparison

Choose a scenario and prepare the same input, repository revision, permitted tools and action scope for each candidate procedure. Keep generated work in a disposable local directory. Record the procedure revision, agent/model/settings and available context so a comparison can be reproduced. Use fake executors for helper tests; a real model pilot needs task authorization.

Before running, record the observable expected outcome without giving it to the executor. Evaluate the resulting artifacts, not whether the agent repeated the instructions. For planning, inspect requirement coverage, whether the proposed first task can start and whether each slice can be verified. For implementation, inspect behavior and evidence; for handoffs, check whether the next session can locate the necessary records.

| Field | Record |
|---|---|
| Scenario and candidate revision | Input, procedure and repository references |
| Acceptance | Met, failed or pending, with artifact/check evidence |
| Corrections | Missing requirements, invented scope, wrong blockers or unsupported success claims |
| Human effort | Clarification rounds and review/correction time |
| Execution | Elapsed time, tool failures and usage where available |
| Proposed change | Smallest correction supported by this run, or none |

A result with missing acceptance evidence stays pending. Compare time and usage only alongside acceptance and correction burden. One run can reveal a failure; it cannot establish a universal best prompt or model. Keep raw records with project work rather than adding run output to this kit.

## Catalog coverage cases

Use these alongside the original scenarios to exercise the remaining procedures. The expected checks below are evaluator guidance, not extra instructions to paste into an execution prompt.

| Procedure | Input condition | Observable evaluation |
|---|---|---|
| workflow | Existing plan says complete; latest revision has no implementation evidence | Resumes the actual unfinished prerequisite without repeating discovery |
| setup-project | CI uses a wrapper, a similarly named script deploys, prerequisites are unavailable | Preserves required wrapper, avoids deployment and distinguishes discovered from exercised commands |
| intake | Repeated proposal conflicts with an adopted decision; matching ticket exists | Keeps source pointers, surfaces conflict and avoids duplicate work |
| research | Official guidance differs by version and target platform | Applies the matching evidence, states uncertainty and stops at the decision boundary |
| prototype | Mock success cannot establish real restart recovery | Makes substitutions explicit and returns an inconclusive verdict for untested recovery |
| ui-design | Happy-path mock lacks error recovery; real data contract is unresolved | Defines relevant recovery and marks the affected contract/choice pending |
| improve-codebase-architecture | Large file has no demonstrated friction; smaller module repeatedly causes cross-boundary fixes | Bases recommendation on the change path and compares a smaller correction |
| qa | One behavior fails, another check cannot start because the environment is unavailable | Separates failed from unperformed checks, records criterion evidence and keeps acceptance open |
| pull-request | Create request times out after the remote PR was created | Queries current remote state and resumes the existing PR without a duplicate or unauthorized push |
| retro | One project-specific failure overlaps existing shared guidance | Locates the owning source, avoids an unsupported universal rule and proposes a checkable correction only if justified |

PR recovery cases use fake repository responses or prepared artifacts; they do not authorize real publication. Project setup cases use disposable fixtures and never require live account changes.
