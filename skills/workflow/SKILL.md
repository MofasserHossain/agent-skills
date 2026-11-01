---
name: workflow
description: "Route supplied work through appropriate planning, implementation and verification stages, or resume an existing workflow."
---

Read applicable project instructions and .agent-workflow.json when present. Preserve the user's current objective, settled decisions and action authorization.

Choose the shortest useful route:
- PR/status/delivery request: use pull-request directly and load only applicable delivery context.
- Small, clear change: implement, verify and review proportionately.
- Incoming notes/messages/tickets: intake first, then clarify only consequential gaps.
- Uncertain feature: grill; research factual uncertainties or prototype a specific behavior/UI question.
- UI/frontend uncertainty: use ui-design to connect research, flows and optional prototypes to buildable decisions. Skip it for backend-only work.
- Multi-session build: write a spec, then vertical tasks with blockers.
- Existing work: read its authoritative record and latest evidence; resume the unfinished stage.
- Architecture friction: assess a focused area, then take the selected improvement through the same planning/delivery route.

Use the relevant procedure by reading its file, or through the host's skill tool when available. These are portable instructions, not a dependency on a proprietary Skill tool.

| Stage | Procedure |
|---|---|
| Project setup | [setup-project](../setup-project/SKILL.md) |
| Incoming material | [intake](../intake/SKILL.md) |
| Architecture assessment | [improve-codebase-architecture](../improve-codebase-architecture/SKILL.md) |
| Resolve decisions | [grill](../grill/SKILL.md) |
| Investigate facts | [research](../research/SKILL.md) |
| Test a design question | [prototype](../prototype/SKILL.md) |
| Plan interface behavior and appearance | [ui-design](../ui-design/SKILL.md) |
| Write the PRD | [write-spec](../write-spec/SKILL.md) |
| PRD to issues | [plan-tasks](../plan-tasks/SKILL.md) |
| Build one task | [implement](../implement/SKILL.md) |
| Review the change | [review](../review/SKILL.md) |
| Check actual behavior | [qa](../qa/SKILL.md) |
| PR delivery, status, or post-merge sync | [pull-request](../pull-request/SKILL.md) |
| Improve the environment | [retro](../retro/SKILL.md) |

Read [task contract](../../references/task-contract.md) when creating/executing tasks, [trackers](../../references/trackers.md) when selecting storage, and [context policy](../../references/context-policy.md) when transitioning sessions/tools. Read only the selected procedure and applicable references, not the whole table's targets.

HITL decisions require the human's answer. AFK work can proceed only within settled scope. An executor can change between stages; task/spec/evidence remain the portable record.

End each stage with its artifact or result, unresolved questions and the next useful action. Do not manufacture an approval checkpoint when existing authorization already covers the next action.

When resuming, compare the latest evidence with the current revision and authoritative status. A completed planning stage does not prove implementation is ready, and an old passing check does not cover later edits. Select the earliest unfinished prerequisite that affects the requested outcome; leave unrelated completed stages alone.

If the request changes scope during a stage, identify which requirements, decisions and downstream tasks are affected. Preserve unaffected work and update the authoritative record before dependent execution. Report the selected route and its reason briefly; routing is complete when a concrete next procedure and input are identified, not when every stage has been invoked.
