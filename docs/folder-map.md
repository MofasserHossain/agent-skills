# What belongs where

This repository is the shared toolbox. Actual feature records belong to the project being changed; improvements to this kit use this repository's `docs/work/<feature>/`.

| Path | Responsibility | Read when |
|---|---|---|
| skills/ | Portable stage instructions | The corresponding stage runs |
| dist/skills/ | Generated self-contained packages; ignored in Git | Building or installing selected skills |
| references/ | Task/result contracts and shared policies | A stage points to them |
| templates/ | Starting shapes for feature artifacts | Creating an artifact |
| adapters/ | Executor commands and native discovery paths | Selecting or registering a host |
| tools/ | Maintainer packaging, validation and optional execution/legacy helpers | Building packages, checking the kit or explicit dispatch/legacy maintenance |
| scripts/ | Standard project-local Skills CLI installation wrapper | Installing selected prepared packages |
| tests/ | Helper behavior tests using fake executors/directories | Maintaining the kit |
| checks/ | Realistic behavioral pilot inputs | Evaluating the workflow |
| examples/ | Illustrative brief, PRD and issues | Learning how artifacts connect |
| docs/ | Kit design, installation, walkthrough and research | Learning or maintaining the kit |
| docs/work/ | Actual kit-improvement decisions, tasks when needed, and evidence | Maintaining or resuming work on this kit |
| docs/conversation-summaries/ | Historical discussion summaries | Recovering background; current work records hold subsequent decisions |

## Files that drive ordinary work

- [skills/workflow/SKILL.md](../skills/workflow/SKILL.md): routing and stage pointers.
- The selected stage's SKILL.md and any relevant references.
- Your project's AGENTS.md and optional .agent-workflow.json.
- Your project's actual brief, PRD/spec, selected issue and evidence.

The agent does not read every folder at session start. [Project routes](project-routes.md) explain optional UI/frontend planning and backend/full-stack adaptation. See the [prompt map](prompt-map.md) for stage files, runtime composition and project/workspace examples.

## Similar names with different purposes

- [docs/workflow-spec.md](workflow-spec.md) specifies this toolbox.
- [templates/spec.md](../templates/spec.md) is the reusable feature PRD structure.
- A project's docs/work/<feature>/spec.md is the actual feature PRD.
- [AGENTS.md](../AGENTS.md) governs changes to this repository. It is not automatically a global rule for unrelated projects.
- [adapters/agents.json](../adapters/agents.json) chooses implementation CLI transport; [adapters/discovery.json](../adapters/discovery.json) tells the registration helper where a host discovers skills.

## Native use versus automation

For new projects, `scripts/install-skills.sh` uses the standard Skills CLI against generated `dist/skills/`. `tools/package_skills.py` prepares those packages from canonical sources. Selected packages are copied into project-local skill folders with their own resources; the standard symlink method adds host links within that project. See [installation](installation.md) for the resulting paths and copy option. The optional router exports as `agent-workflow`; each selected skill is independently discoverable.

While maintaining this kit, an agent can read `skills/<name>/SKILL.md` directly without installing it. Installed projects read their own selected copies. Python is used to build packages here; ordinary installed-skill use does not require a Python launcher.

Standard installations contain selected skill folders/resources and installer lock metadata. Research, kit tests, examples, authoring docs and execution tooling stay in the source repo. Installing skills does not authenticate an agent, provision Docker, schedule tasks, publish issues or mark work accepted.

Legacy installations use a `.agent-workflow` snapshot and one thin router entry. Only the legacy `tools/install_project.py` uses `--skills`, `--with-runner` and a selection manifest. Optional source-linked registration points a thin entry at this checkout and requires it to remain readable. These modes remain supported for existing installations and deliberate development use; they are not the default for new projects. Migrate only after selecting skills and preserving local edits, as described in [installation](installation.md).
