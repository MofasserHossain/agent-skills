# What belongs where

This repository is the shared toolbox. Actual feature records belong to the project being changed.

| Path | Responsibility | Read when |
|---|---|---|
| skills/ | Portable stage instructions | The corresponding stage runs |
| references/ | Task/result contracts and shared policies | A stage points to them |
| templates/ | Starting shapes for feature artifacts | Creating an artifact |
| adapters/ | Executor commands and native discovery paths | Selecting or registering a host |
| tools/ | Optional deterministic helpers | Setup, validation or explicit dispatch |
| tests/ | Helper behavior tests using fake executors/directories | Maintaining the kit |
| checks/ | Realistic behavioral pilot inputs | Evaluating the workflow |
| examples/ | Illustrative brief, PRD and issues | Learning how artifacts connect |
| docs/ | Kit design, installation, walkthrough and research | Learning or maintaining the kit |

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

The native entry point is one short pointer to the workflow procedure: relative to the project snapshot in installed mode, or absolute to the source checkout in linked mode. The Python tools are optional; reading Markdown does not require running a launcher.

Registering a local skill does not install an agent, authenticate an account, provision Docker, schedule tasks, publish issues or mark work accepted.

Project installations contain selected skills and their linked runtime dependencies, not this entire authoring layout. Use --skills to choose procedures and --with-runner for optional execution tooling; the selection manifest records the result. Research, kit tests, examples and authoring instructions stay here.

For new projects, scripts/install-skills.sh uses the standard Skills CLI against generated dist/skills. tools/package_skills.py prepares self-contained packages from canonical sources. Standard project installs contain only selected skill folders/resources and the CLI lock; the legacy .agent-workflow layout above is no longer the default.
