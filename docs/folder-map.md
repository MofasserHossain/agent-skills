# What belongs where

This repository is the shared toolbox. Actual feature records belong to the project being changed; improvements to this kit use this repository's `docs/work/<feature>/`.

| Path | Responsibility | Read when |
|---|---|---|
| skills/engineering/ | Engineering procedures with skill-local resources | Editing or using the corresponding skill |
| skills/productivity/ | Routing, discovery, handoff and instruction writing | Use or maintain these procedures |
| adapters/ | Executor commands and native discovery paths | Selecting or registering a host |
| tools/ | Source validation and optional execution/legacy helpers | Checking the kit or explicit dispatch/legacy maintenance |
| scripts/ | Standard project-local Skills CLI installation wrapper | Installing selected canonical skill folders |
| tests/ | Helper behavior tests using fake executors/directories | Maintaining the kit |
| examples/ | Illustrative brief, PRD and issues | Learning how artifacts connect |
| docs/ | Kit design, installation, walkthrough and research | Learning or maintaining the kit |
| docs/work/ | Actual kit-improvement decisions, tasks when needed, and evidence | Maintaining or resuming work on this kit |
| docs/conversation-summaries/ | Historical discussion summaries | Recovering background; current work records hold subsequent decisions |

## Files that drive ordinary work

Edit the owning folder under `skills/` directly. Skill-local references/templates are canonical resources, not generated copies. No packaging step or link rewriting is needed. Other skills are named collaborators; their absence must be handled by the current procedure. Source tests validate the same folders that users install. Each skill's `agents/openai.yaml` provides Codex interface metadata; `tools/skill_catalog.py` discovers unique installed names across categories.

- [skills/productivity/agent-workflow/SKILL.md](../skills/productivity/agent-workflow/SKILL.md): routing and stage pointers.
- The selected stage's SKILL.md and any relevant references.
- Your project's AGENTS.md and optional .agent-workflow.json.
- Your project's actual brief, PRD/spec, selected issue and evidence.

The agent does not read every folder at session start. [Project routes](../skills/engineering/ui-design/references/project-routes.md) explain optional UI/frontend planning and backend/full-stack adaptation. See the [prompt map](prompt-map.md) for stage files, runtime composition and project/workspace examples.

## Similar names with different purposes

- [docs/workflow-spec.md](workflow-spec.md) specifies this toolbox.
- [spec template](../skills/engineering/write-spec/templates/spec.md) is the reusable feature PRD structure.
- A project's docs/work/<feature>/spec.md is the actual feature PRD.
- [AGENTS.md](../AGENTS.md) governs changes to this repository. It is not automatically a global rule for unrelated projects.
- [adapters/agents.json](../adapters/agents.json) chooses implementation CLI transport; [adapters/discovery.json](../adapters/discovery.json) tells the registration helper where a host discovers skills.

## Native use versus automation

For new projects, `scripts/install-skills.sh` uses the standard Skills CLI against canonical `skills/`. Selected folders and their local resources are copied into project-local discovery directories; symlink mode shares them between agents. See [installation](installation.md). The router is named `agent-workflow` in source and installation and is optional.

An agent maintaining this kit can read `skills/<category>/<name>/SKILL.md` directly. Installed projects read selected local copies. Python is used for source checks and optional execution tools; ordinary skill use requires no helper or build.

Standard installations contain selected skill folders/resources and installer lock metadata. Research, kit tests, examples, authoring docs and execution tooling stay in the source repo. Installing skills does not authenticate an agent, provision Docker, schedule tasks, publish issues or mark work accepted.

Legacy installations use a `.agent-workflow` snapshot and one thin router entry. Only the legacy `tools/install_project.py` uses `--skills`, `--with-runner` and a selection manifest. Optional source-linked registration points a thin entry at this checkout and requires it to remain readable. These modes remain supported for existing installations and deliberate development use; they are not the default for new projects. Migrate only after selecting skills and preserving local edits, as described in [installation](installation.md).
