---
name: setup-project
description: "Configure a project to use the shared workflow while preserving its existing instructions and tools."
---

Inspect project instructions, verification scripts, repository boundaries and existing planning/tracker conventions. Reuse them.

Configure .agent-workflow.json using the helper or equivalent edits. It records work_dir, tracker, default_agent and verification commands. Commands use argument arrays, not shell fragments. Keep credentials out of it.

Show unknown verification requirements clearly; an empty commands list means unconfigured, not verified. Ask only choices the environment cannot settle, such as a new tracker preference.

Keep the shared kit separate from project records. Add a short pointer to existing instructions only when useful and authorized; preserve AGENTS/CLAUDE symlinks and surrounding content. Setup never requires copying all skills or global installation.

Read [installation](../../docs/installation.md) for portable use and [tracker conventions](../../references/trackers.md) when selecting the authoritative tracker.
