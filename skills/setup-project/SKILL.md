---
name: setup-project
description: "Configure a project to use the shared workflow while preserving its existing instructions and tools."
---

Inspect project instructions, task/package scripts, CI checks, runtime versions, verification wrappers, repository boundaries and existing planning/tracker conventions. Reuse them; do not assume script names or install a new checker merely to fill an example.

Create or update .agent-workflow.json with schema_version 1 using project-local edits; preserve existing values. It records work_dir, tracker, default_agent, optional named checks for iteration and the ordered final verification commands. Commands use argument arrays, not shell fragments. Use claude or codex for an executor default, or manual to leave CLI selection unset. Other agent profiles are deferred. Keep credentials out of it.

Show unknown verification requirements clearly; an empty commands list means unconfigured, not verified. Ask only choices the environment cannot settle, such as a new tracker preference.

Read [adaptive project context](references/project-context.md) when creating, reorganizing, or refreshing project guidance. Keep essential constraints and explicit phase/task reading routes in root instructions; reuse project-owned documents for conditional detail. Existing-project reorganization needs a concrete reviewed move map and conflict report before rewriting; existing approval covers that proposal without another grilling session.

Identify this project's installed skills and configuration; standard skill installation does not require an execution helper. Keep workflow procedures separate from project records. Preserve AGENTS/CLAUDE symlinks and existing rules; outside an approved context reorganization, add only a useful authorized pointer and preserve surrounding content. Setup never requires copying all skills or global installation.

Discover focused check commands and required final checks from project scripts, CI and existing wrappers. Preserve unrelated configuration and required checks; registration and command discovery are separate. For additional TDD guidance, consult `implement` if installed; setup itself does not require running implementation.

Read [installation](references/project-installation.md) for portable use. Choose one authoritative tracker per feature and retain source links when importing work; consult `plan-tasks` for task-record conventions if creating a backlog, or return the proposed tracker choice without inventing a schema.

Distinguish discovered commands from commands actually exercised. Inspect their working directories, prerequisites and side effects before running them; deployment or live-service commands are not setup checks. Where several wrappers exist, use the path required by project instructions or CI rather than assembling a competing command sequence.

Finish with the configuration/guidance changed, sources of command choices, available skills, authoritative work location and unresolved setup gaps. Check that new local reading pointers resolve and commands name real scripts or executables; report untested prerequisites explicitly. An existing usable setup can be confirmed without rewriting it.
