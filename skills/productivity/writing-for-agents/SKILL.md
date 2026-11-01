---
name: writing-for-agents
description: "Create or improve skills and agent instructions when unclear triggers, duplicated rules or poor navigation cause inconsistent work."
---

## Identify the decision the writing changes

Read the current instructions, their callers and the observed problem. Preserve the user's scope, project rules and existing invocation policy. State what the agent should do differently; avoid adding generic reminders merely to make the document look comprehensive.

## Organize around use

Give each concept one authoritative owner. Skill descriptions should distinguish actual triggering situations; the body supplies the procedure and observable completion conditions. Keep essential steps visible. Put substantial conditional detail in local supporting files with precise reading triggers. A short skill needs no extra directories or fixed number of sections.

Keep filesystem resources inside the skill that owns them. Name other installed skills as collaborators and explain what happens when they are absent. Templates describe output shape, not a second copy of the process. Codex agents/openai.yaml supplies UI metadata; it does not replace SKILL.md or guarantee equivalent behavior in another host.

Keep project commands, product vocabulary and authorization in that project's authoritative sources. For reorganizing existing root guidance, use installed setup-project's context-refresh procedure; if unavailable, preserve the layout and return a concrete proposal instead of silently relocating rules. Use [pointer examples](references/pointers.md) when deciding whether to inline or link guidance.

## Verify the revision

Check links, resource portability, conflicting rules, repeated meanings and conditions for loading each reference. Trace a realistic request through the instructions and inspect the resulting artifact where available. Validation of metadata or headings is not evidence that the agent makes better decisions. Prefer a narrow correction supported by observed failures, and keep human examples in documentation instead of expanding every always-loaded instruction.
