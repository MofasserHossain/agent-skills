# Agent Workflow

Reusable engineering skills for turning ideas, documents, messages and tickets into verified changes. Maintain one source kit, then install only the skills each project needs. Current target agents are Claude Code and Codex.

## Install from this local repo

You need Python 3 to build the packages, Node 22.20+ for the pinned Skills CLI, and Claude Code or Codex in the target project. Installed Markdown skills do not require Python. Clone this repository with your GitHub account's access, then prepare the ignored distribution:

```sh
git clone https://github.com/MofasserHossain/agent-workflow.git
cd agent-workflow
python3 tools/package_skills.py
python3 tools/package_skills.py --check
```

The prepared `dist/skills` folders work with the standard [Skills CLI](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-add). From this checkout, list or choose skills for an existing project:

```sh
bash scripts/install-skills.sh /path/to/project --list
bash scripts/install-skills.sh /path/to/project
```

In a normal terminal outside an agent, the second command opens the standard skill selector. Inside Claude/Codex automation, pass explicit --skill names; the CLI auto-disables prompts there. Select the skills you want and use project scope. The wrapper targets Claude Code and Codex only. It disables CLI telemetry and uses the tested Skills CLI version 1.7.4, which requires Node 22.20+.

You can name a selection explicitly:

```sh
bash scripts/install-skills.sh /path/to/project --skill grill research write-spec plan-tasks
```

Or use the standard CLI directly from the target project:

```sh
DISABLE_TELEMETRY=1 npx skills@1.7.4 add /path/to/agent-workflow/dist/skills --agent claude-code codex
```

Each selected skill includes its own needed references/templates. The standard symlink method copies canonical skill folders into the target project and creates host links within that project. It does not require the authoring checkout during agent use. Other named skills are optional collaborators; they are not installed automatically.

No `.agent-workflow` bundle, Python helper, source research, kit tests, examples or development docs are needed for this installation. The optional `agent-workflow` skill routes among the skills actually installed; it is not a requirement to install the whole catalog.

Run `setup-project` if you selected it, or follow existing project conventions. Each project owns its instructions, `.agent-workflow.json` command catalog and actual briefs/specs/issues. Installing skills does not run an agent or configure provider accounts.

See [installation and migration](docs/installation.md). In particular, standard reinstallation can replace edited skill files; review local customizations before updating. Existing legacy snapshots remain untouched until a deliberate migration.

## Start work in a project

Open Claude Code or Codex in the target project and invoke a selected installed skill through its supported skill interface. Start with `setup-project` if selected to record the project's commands and conventions. Then choose the shortest route:

- Clear fix: `implement` → verification → `review`.
- Unclear request: `intake` or `grill`, then implementation when scope is settled.
- Larger change: `write-spec` → `plan-tasks` → `implement` → `review` and `qa`.
- Interface uncertainty: add `ui-design`; mobile projects keep build/device checks in their own configuration and work records.

Use only skills you selected; add another when needed. The optional `agent-workflow` router helps select a route. Decisions and results stay in the target project's work records so another session or agent can continue.

## Maintain the root kit

To work on this repository, open the agent here and reference the canonical skill directly. No self-installation is needed for an agent that can read this checkout. For example:

> Read skills/improve-codebase-architecture/SKILL.md and assess packaging boundaries. Record evidence and recommendations under docs/work/packaging-boundaries/. Recommend one bounded improvement before changing code.

For a small, agreed change, ask the agent to use `skills/implement/SKILL.md`, run the required checks below, and use `skills/review/SKILL.md` to review the result. Use planning stages only when the work needs them. Actual kit-improvement records belong under `docs/work/<feature>/`; examples are illustrative and conversation summaries are historical context. See the [folder map](docs/folder-map.md) for resource boundaries.

Canonical instructions remain under `skills/`, with shared authoring references and templates. Prepare or refresh independent distribution folders after editing them:

```sh
python3 tools/package_skills.py
python3 tools/package_skills.py --check
```

Python is a maintainer/build tool here, not an installed-skill runtime requirement. Generated packages stay under the ignored `dist/skills/`; they contain no symlinks or references back to this checkout. Build before installing from a fresh clone. The same self-contained skill format can be used in a future Git/plugin/npm distribution; nothing is published by this build.

## Available capabilities

- Fourteen procedures: optional routing/setup, intake, grilling, research, prototypes, UI design, PRD/spec writing, vertical tasks, implementation, architecture assessment, review, QA and retrospective.
- Local-file/GitHub conventions with one authoritative tracker and portable requirement/task/result records.
- Project-specific verification commands and focused TDD guidance. Frontend, full-stack and backend projects use the same core flow with conditional checks.
- QA sends reproducible defects back to the backlog; review checks requirements and project standards.

Use only the stages the work needs. The [prompt map](docs/prompt-map.md) explains the procedures, [project routes](docs/project-routes.md) covers UI/frontend/backend work, and the [worked example](docs/walkthrough.md) shows brief → spec → issues. Authoring research and the [kit specification](docs/workflow-spec.md) stay in this repo.

## Optional execution tooling

The root kit retains a Python helper for explicit one-task dispatch through Claude Code or Codex. It is separate from standard skill installation. It previews until `--execute` is supplied, uses native authentication/settings, and does not accept a task merely because a process exits successfully.

```sh
python3 tools/workflow.py prompt TASK.md --project /path/to/project
python3 tools/workflow.py run TASK.md --project /path/to/project --agent codex
```

Automated scheduling/loops, GitHub API integration, Docker provisioning, Sandcastle orchestration and provider-specific model-effort translation remain planned. The [execution plan](docs/execution-plan.md) describes those future capabilities. Legacy snapshot/pointer installers remain available for existing installations, but are not the default installation route.

## Verify this repository

```sh
python3 -m unittest discover -s tests -v
python3 tools/workflow.py check
python3 tools/package_skills.py --check
bash -n scripts/install-skills.sh
```

Tests use local fake executors. Real provider authentication, model output quality and Docker behavior require a separate pilot. No publishing, global installation or paid model call is needed for these checks.
