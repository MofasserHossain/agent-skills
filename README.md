# Agent Skills

Reusable skills for taking software work from an idea to a verified change. Install the skills your project needs, use them in your coding agent, and keep decisions and results in project files so another session or agent can continue.

Use a single skill for a clear fix, or connect discovery, planning, implementation and review for a larger feature. Each skill includes its own instructions, references and templates.

## Quick start

You need Git access to this private repository, Node.js for the Skills CLI, and a compatible coding agent. The pinned CLI used by this repo requires Node.js 22.20+.

From the project where you want to use the skills:

```sh
npx skills@latest add MofasserHossain/agent-skills
```

Choose the skills, agent targets and project scope in the installer. To select skills explicitly for Claude Code and Codex with the pinned CLI:

```sh
DISABLE_TELEMETRY=1 npx --yes skills@1.7.4 add MofasserHossain/agent-skills \
  --skill setup-project implement review \
  --agent claude-code codex
```

Open your agent in that project and send a request through its skill interface:

| Agent | Example message |
|---|---|
| Claude Code | `/setup-project Inspect this project's instructions and verification commands.` |
| Codex | `$setup-project Inspect this project's instructions and verification commands.` |

Then give `implement` a concrete task, for example:

```text
$implement Fix the reported preference loss after restart. Reproduce the bug,
follow the project's conventions, and verify the expected behavior.
```

Use `/implement` in Claude Code. These examples are messages inside the agent; installation does not start an agent or configure provider authentication.

Skills support any agent target recognized by the standard Skills CLI. A file-capable agent can also read a skill's `SKILL.md` directly. The optional Python execution helper supports Claude Code and Codex only.

## Choose a skill

Install only what you need. The optional `agent-workflow` router helps choose a route; it does not install its collaborators.

| Skill | Use it to |
|---|---|
| [`setup-project`](skills/engineering/setup-project/SKILL.md) | Discover project commands and organize project guidance. |
| [`agent-workflow`](skills/productivity/agent-workflow/SKILL.md) | Choose the next step or resume existing work. |
| [`intake`](skills/productivity/intake/SKILL.md) | Turn notes, documents or messages into a source-linked brief. |
| [`grill`](skills/productivity/grill/SKILL.md) | Resolve product and design decisions before implementation. |
| [`research`](skills/productivity/research/SKILL.md) | Answer a decision-changing question with source evidence. |
| [`prototype`](skills/engineering/prototype/SKILL.md) | Test an uncertain approach with a bounded experiment. |
| [`ui-design`](skills/engineering/ui-design/SKILL.md) | Design interface flows, states and appearance. |
| [`write-spec`](skills/engineering/write-spec/SKILL.md) | Turn settled decisions into a specification. |
| [`plan-tasks`](skills/engineering/plan-tasks/SKILL.md) | Split a specification into verifiable tasks with dependencies. |
| [`implement`](skills/engineering/implement/SKILL.md) | Deliver a clear fix or ready task with verification evidence. |
| [`review`](skills/engineering/review/SKILL.md) | Inspect changes against requirements and project standards. |
| [`qa`](skills/engineering/qa/SKILL.md) | Check delivered behavior and record reproducible defects. |
| [`pr`](skills/engineering/pr/SKILL.md) | Prepare a PR, check delivery status or sync after merging. |
| [`improve-codebase-architecture`](skills/engineering/improve-codebase-architecture/SKILL.md) | Assess code boundaries and propose a bounded improvement. |
| [`retro`](skills/engineering/retro/SKILL.md) | Use work evidence to identify a workflow improvement. |
| [`handoff`](skills/productivity/handoff/SKILL.md) | Preserve the current state, decisions and next action. |
| [`writing-for-agents`](skills/productivity/writing-for-agents/SKILL.md) | Write concise agent instructions with conditional references. |

### Common routes

- **Clear fix:** `implement` → verification → `review`.
- **Unclear request:** `intake` or `grill` → `implement` once scope is settled.
- **Larger feature:** `write-spec` → `plan-tasks` → `implement` → `review` and `qa`.
- **Uncertain approach:** use `research`, `prototype` or `ui-design` to resolve the specific question.
- **Session change:** use `handoff` to preserve the evidence and next step.

Follow the project's own commands and delivery rules. Add a missing collaborator deliberately when its guidance is needed. See the [skill guide](docs/skill-guide.md) for example requests and completion signals, or the [worked example](docs/walkthrough.md) for connected brief, spec and task records.

## Install from a local checkout

From this repository, list available skills or install a selection into another project:

```sh
bash scripts/install-skills.sh /path/to/project --list
bash scripts/install-skills.sh /path/to/project --skill setup-project implement review
```

Run without `--skill` in a normal terminal for interactive selection. Unattended calls require explicit skill names. The wrapper uses `skills@1.7.4`, disables telemetry and defaults to project-local Claude Code and Codex targets; override them with `--agent`.

The standard symlink method keeps selected skills under the project's `.agents/skills`, with host links sharing those files. Each skill owns its resources and can be relocated independently. Python helpers stay in this source repository.

See [installation and invocation](docs/installation.md) for direct CLI commands, other agent targets, copy mode, isolated environments, updates and legacy migration.

## How this repository is organized

```text
skills/
  engineering/       Setup, design, planning, implementation and delivery
  productivity/      Routing, discovery, research and session continuity
docs/                Guides, specifications, research and work records
scripts/             Project-local installation wrapper
tools/               Optional Python helpers and source validation
tests/               Packaging, relocation and helper tests
```

Edit canonical `skills/<category>/<name>/SKILL.md` files directly. Each skill owns its supporting resources and Codex display metadata in `agents/openai.yaml`. Categories organize the source; installed names stay flat. No generated skill copies or package build step are needed.

For work on this kit, follow [AGENTS.md](AGENTS.md) and read the relevant skill directly without self-installing. After reviewing local customizations, reinstall selected skills to update a target project. See the [folder map](docs/folder-map.md) and [workflow specification](docs/workflow-spec.md) for the source layout and contracts.

## Optional tooling and roadmap

The source repository includes standard-library Python helpers for:

- Preparing task context and previewing or explicitly dispatching one task through Claude Code or Codex.
- Validating a local dependency graph and reporting eligible work with `workflow.py next`.
- Managing independent local clones and verified archives with the [workspace helper](docs/workspaces.md).

```sh
python3 tools/workflow.py prompt TASK.md --project /path/to/project
python3 tools/workflow.py run TASK.md --project /path/to/project --agent codex
```

The run command previews until `--execute` is supplied. Process success alone does not establish task acceptance. The dependency selector does not launch, claim or accept tasks.

Automated scheduling and loops, GitHub API integration, Docker provisioning, Sandcastle orchestration and provider-specific model-effort translation remain planned. Legacy snapshot and pointer installers remain supported for existing installations. See the [execution plan](docs/execution-plan.md) and [runner assessment](docs/work/runner-adaptation/assessment.md) for implemented behavior and proposed work.

## Validate changes

From this checkout:

```sh
python3 -m unittest discover -s tests -v
python3 tools/workflow.py check
bash -n scripts/install-skills.sh
```

Tests use fake executors and cover packaging, relocation and helper behavior. They do not establish model output quality; live-agent evaluation requires a separate authorized pilot.
