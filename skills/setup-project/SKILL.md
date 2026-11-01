---
name: setup-project
description: "Configure a project to use the shared workflow while preserving its existing instructions and tools."
---

Inspect project instructions, task/package scripts, CI checks, runtime versions, verification wrappers, repository boundaries and existing planning/tracker conventions. Reuse them; do not assume script names or install a new checker merely to fill an example.

Create or update .agent-workflow.json with schema_version 1 using project-local edits; preserve existing values. It records work_dir, tracker, default_agent, optional named checks for iteration and the ordered final verification commands. Commands use argument arrays, not shell fragments. Use claude or codex for an executor default, or manual to leave CLI selection unset. Other agent profiles are deferred. Keep credentials out of it.

Show unknown verification requirements clearly; an empty commands list means unconfigured, not verified. Ask only choices the environment cannot settle, such as a new tracker preference.

Identify this project's installed skills and configuration; standard skill installation does not require an execution helper. Keep workflow procedures separate from project records. Add a short pointer to existing instructions only when useful and authorized; preserve AGENTS/CLAUDE symlinks and surrounding content. Setup never requires copying all skills or global installation.

Read [project checks and TDD](../../references/verification-policy.md) when discovering or refreshing commands. Preserve unrelated configuration and required checks; registration and command discovery are separate.

Read [installation](../../references/project-installation.md) for portable use and [tracker conventions](../../references/trackers.md) when selecting the authoritative tracker.
