---
name: agent-workflow
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
| Project setup | `setup-project` |
| Incoming material | `intake` |
| Architecture assessment | `improve-codebase-architecture` |
| Resolve decisions | `grill` |
| Investigate facts | `research` |
| Test a design question | `prototype` |
| Plan interface behavior and appearance | `ui-design` |
| Write the PRD | `write-spec` |
| PRD to issues | `plan-tasks` |
| Build one task | `implement` |
| Review the change | `review` |
| Check actual behavior | `qa` |
| PR delivery, status, or post-merge sync | `pull-request` |
| Improve the environment | `retro` |

The table is the catalog, not this project's installed set. Use only available procedures. Task-record and tracker conventions belong to `plan-tasks`; consult them when creating records or choosing storage. Read [context policy](references/context-policy.md) when transitioning sessions/tools. Load only the selected procedure and relevant references. If a collaborator is absent, continue where the current procedure is sufficient or identify the missing guidance; never claim it ran.

HITL decisions require the human's answer. AFK work can proceed only within settled scope. An executor can change between stages; task/spec/evidence remain the portable record.

End each stage with its artifact or result, unresolved questions and the next useful action. Do not manufacture an approval checkpoint when existing authorization already covers the next action.

When resuming, compare the latest evidence with the current revision and authoritative status. A completed planning stage does not prove implementation is ready, and an old passing check does not cover later edits. Select the earliest unfinished prerequisite that affects the requested outcome; leave unrelated completed stages alone.

If the request changes scope during a stage, identify which requirements, decisions and downstream tasks are affected. Preserve unaffected work and update the authoritative record before dependent execution. Report the selected route and its reason briefly; routing is complete when a concrete next procedure and input are identified, not when every stage has been invoked.
