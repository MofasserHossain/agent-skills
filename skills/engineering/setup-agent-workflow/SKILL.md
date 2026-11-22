---
name: setup-agent-workflow
description: "Set up a project for these skills: record its real commands, tracker and docs in .agent-workflow.json. Use in a new project, or when its commands, tracker or agent guidance change."
---

Build the per-project configuration the other skills read from what the project **already has**. This is a guided procedure, not a script: explore, present what you found, confirm, then write. An existing usable setup can be confirmed without rewriting it.

## Process

### 1. Explore

Read the project as it is; assume nothing:

- Root instructions (`AGENTS.md`, `CLAUDE.md` and any symlink between them) and documentation maps.
- Package or task scripts, CI workflows, runtime versions and verification wrappers.
- Tracker and planning conventions: a GitHub remote, a local work folder such as `docs/work/`.
- An existing `.agent-workflow.json`, and which of these skills are installed.

Before running any command, inspect its working directory, prerequisites and side effects; deployment and live-service commands are never setup checks.

**Done when:** you can list what exists, what is missing, and where each command came from (script, CI or instructions).

### 2. Present findings, one section at a time

Lead each section with the recommended answer so the user can accept it in a word. Ask only what the environment can't settle, and skip any section that exploration already settled.

- **A. Checks.** The focused commands `implement` uses while iterating (`checks`) and the ordered final `verification` list. Where several wrappers exist, use the one the project's instructions or CI require. An empty list means unconfigured, never verified.
- **B. Tracker.** One authoritative tracker per feature: local files in the work folder, or GitHub. Keep source links when importing work. For a new backlog, use the task conventions of the `to-tasks` skill; if it isn't installed, propose the tracker without inventing a schema.
- **C. Executor default.** `claude`, `codex`, or `manual` to leave CLI selection unset. Other agent profiles are deferred.
- **D. Project guidance.** Only when creating, reorganizing or refreshing root instructions: read [adaptive project context](references/project-context.md). Reorganizing existing guidance needs a reviewed move map and a conflict report first.

**Done when:** every section has an answer or is marked as an explicit gap.

### 3. Show the drafts

Show the `.agent-workflow.json` changes and any guidance edits before writing, and let the user edit them.

**Done when:** the user accepts the drafts, or existing authorization already covers them.

### 4. Write

Create or update `.agent-workflow.json` with targeted, project-local edits that preserve existing values: `schema_version` 1, `work_dir`, `tracker`, `default_agent`, optional named `checks` and the ordered final `verification` commands. Commands are argument arrays, not shell strings; credentials never go in this file. In root instructions, add at most a useful pointer outside an approved reorganization, and preserve surrounding content, AGENTS/CLAUDE symlinks and existing rules. Setup never copies the whole catalog or installs anything globally; for installation questions read [project installation](references/project-installation.md).

**Done when:** every new local pointer resolves and every command names a real script or executable.

### 5. Report

Report what changed, where each command choice came from, which commands actually ran versus were only discovered, the installed skills, the authoritative work location, and any unresolved gaps or untested prerequisites.

**Done when:** the user can see which skills will read these settings, and knows they can edit them directly later.
