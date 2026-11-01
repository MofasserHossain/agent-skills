# Agent Workflow

Reusable engineering skills for turning ideas, documents, messages and tickets into verified changes. Maintain one source kit, then install only the skills each project needs. Portable skills can be installed for any agent supported by the Skills CLI, or read directly by an agent with file access. The optional execution helper supports Claude Code and Codex.

## Install from GitHub

The editable `skills/` folders are also the installable skills. No package tree, build or Python runtime is needed for installation. From the target codebase:

```sh
npx skills@latest add MofasserHossain/agent-workflow
```

Choose the skills and agents you want. For a pinned CLI and explicit project-local selection:

```sh
DISABLE_TELEMETRY=1 npx --yes skills@1.7.4 add MofasserHossain/agent-workflow --skill grill implement research --agent claude-code codex
```

The repository is private, so Git access is required. Skills CLI 1.7.4 is the pinned wrapper version; using `@latest` selects whatever version is current when you install. Do not also install old generated package paths into the same project.

## Install from a local checkout

You need Node 22.20+ for the pinned CLI and a Skills-compatible agent in the target project. From this kit checkout:

```sh
bash scripts/install-skills.sh /path/to/project --list
bash scripts/install-skills.sh /path/to/project
bash scripts/install-skills.sh /path/to/project --skill grill research write-spec
```

In a normal terminal the selector lets you choose skills; unattended/agent calls must provide explicit `--skill` names. The wrapper defaults to project-local Claude Code and Codex. Use `--agent claude-code`, `--agent codex`, or other Skills CLI targets. It disables telemetry and uses `skills@1.7.4`.

Or run the standard CLI directly from the target project:

```sh
DISABLE_TELEMETRY=1 npx skills@1.7.4 add /path/to/agent-workflow/skills --agent claude-code codex
```

The standard symlink installation creates one project-local copy of each selected skill under `.agents/skills`, with Claude Code links pointing there. Both agents read the same files. Each skill keeps its own supporting files; collaborator skills are named and are not automatically installed. A missing collaborator is reported where its guidance is needed.

See [installation, invocation and migration](docs/installation.md) for copy mode, isolated environments and existing installations. Standard installation does not include Python helpers, authenticate providers or run an agent.

## Start work in a project

Open Claude Code or Codex in the target project and invoke a selected installed skill through its supported skill interface. Start with `setup-project` if selected to record the project's commands and conventions. Use the [skill guide](docs/skill-guide.md) for entry points, example requests and signs of a useful result. Then choose the shortest route:

- Clear fix: `implement` → verification → `review`.
- Unclear request: `intake` or `grill`, then implementation when scope is settled.
- Larger change: `write-spec` → `plan-tasks` → `implement` → `review` and `qa`.
- Interface uncertainty: add `ui-design`; mobile projects keep build/device checks in their own configuration and work records.

Start `claude` or `codex` from the target project. Inside Claude Code, invoke `/setup-project` or `/implement <task reference>`; inside Codex, use `$setup-project` or `$implement <task reference>`. These are agent messages, not shell commands. For Docker or another isolated workspace, provision the project-local skill folders inside that environment and start the agent there; see the [isolated execution guide](docs/installation.md#run-inside-docker-sandbox-or-another-isolated-environment). See the [installation and invocation walkthrough](docs/installation.md#start-claude-code-or-codex-and-use-an-installed-skill) for setup, shared symlinks and runner distinctions.

Use only skills you selected; add another when needed. The optional `agent-workflow` router helps select a route. Decisions and results stay in the target project's work records so another session or agent can continue.

## Maintain the skills

Edit the skill you want to improve directly:

```text
skills/
  agent-workflow/SKILL.md
  implement/
    SKILL.md
    references/
  write-spec/
    SKILL.md
    templates/spec.md
```

Each resource has one owning skill. Local links stay inside that skill's folder; other procedures are referred to by installed skill name, with a fallback when absent. The optional router is named `agent-workflow` in both source and installation. There is no generated installation copy or resource-link rewriting step.

For changes to this kit, read the relevant `skills/<name>/SKILL.md` directly; no self-installation is needed. Keep actual kit work under `docs/work/<feature>/`, project rules/commands in the target project, and historical research in the source repo. See the [folder map](docs/folder-map.md).

After editing, run the checks below and inspect the relocated-skill tests. Reinstall selected skills to update a target project after reviewing its local customizations. Python is needed only for source validation and optional helpers, not installed skill use.

## Available capabilities

- Fifteen procedures: optional routing/setup, intake, grilling, research, prototypes, UI design, PRD/spec writing, vertical tasks, implementation, architecture assessment, review, QA, pull-request delivery/status/sync and retrospective.
- Local-file/GitHub conventions with one authoritative tracker and portable requirement/task/result records.
- Adaptive project context setup: reviewed move maps for existing instructions, essential root constraints, conditional phase/task reading routes, and preservation audits. Project-owned docs stay separate from skill installation and updates.
- Project-specific verification commands and focused TDD guidance. Frontend, full-stack and backend projects use the same core flow with conditional checks.
- The `pull-request` procedure uses project-specific checks and delivery rules, a concise title/body format, and a commits/diff review checkpoint before opening a new PR. It also handles status and post-merge sync; it does not automate merging.
- QA sends reproducible defects back to the backlog; review checks requirements and project standards.
- All fifteen procedures define scoped decisions and useful completion signals: routing/resumption, setup evidence, source-linked intake, bounded research, prototype verdicts, design readiness, architecture tradeoffs, planning coverage, implementation evidence, review, QA, PR recovery and evidence-based retrospective. Human usage examples live in the skill guide; behavioral superiority remains a pilot question.

Use only the stages the work needs. The [prompt map](docs/prompt-map.md) explains the procedures, [project routes](skills/ui-design/references/project-routes.md) covers UI/frontend/backend work, and the [worked example](docs/walkthrough.md) shows brief → spec → issues. Authoring research and the [kit specification](docs/workflow-spec.md) stay in this repo.

## Optional execution tooling

The root kit retains a Python helper for explicit one-task dispatch through Claude Code or Codex. It is separate from standard skill installation. It previews until `--execute` is supplied, uses native authentication/settings, and does not accept a task merely because a process exits successfully.

```sh
python3 tools/workflow.py prompt TASK.md --project /path/to/project
python3 tools/workflow.py run TASK.md --project /path/to/project --agent codex
```

The read-only selector validates a complete local dependency graph and reports eligible work or why it must wait:

```sh
python3 tools/workflow.py next /path/to/project/docs/work/feature/issues --project /path/to/project
```

It does not launch, claim or accept tasks. Filename order is the default; `complete` means all existing records say done, not that this command reverified them. Invalid graphs fail before dispatch. The [Matt runner assessment and adaptation specification](docs/work/runner-adaptation/assessment.md) separates inspected source behavior, implemented preflight and proposed once/loop/runtime work.

The separate [workspace helper](docs/workspaces.md) creates independent local clones, lists logical disk usage, verifies clean committed archives and supports explicit purge/restore under ~/mofasser-workspace (configurable). It does not launch Docker or agents. Worker supervision, project hooks and automatic retention remain planned.

Automated scheduling/loops, GitHub API integration, Docker provisioning, Sandcastle orchestration and provider-specific model-effort translation remain planned. The [execution plan](docs/execution-plan.md) describes those future capabilities. Legacy snapshot/pointer installers remain available for existing installations, but are not the default installation route.

## Verify this repository

```sh
python3 -m unittest discover -s tests -v
python3 tools/workflow.py check
bash -n scripts/install-skills.sh
```

Tests use local fake executors. Real provider authentication, model output quality and Docker behavior require a separate pilot. No publishing, global installation or paid model call is needed for these checks.
