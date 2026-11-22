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
  --skill setup-agent-workflow implement code-review \
  --agent claude-code codex
```

Open your agent in that project and send a request through its skill interface:

| Agent | Example message |
|---|---|
| Claude Code | `/setup-agent-workflow Inspect this project's instructions and verification commands.` |
| Codex | `$setup-agent-workflow Inspect this project's instructions and verification commands.` |

Then give `implement` a concrete task, for example:

```text
$implement Fix the reported preference loss after restart. Reproduce the bug,
follow the project's conventions, and verify the expected behavior.
```

Use `/implement` in Claude Code. These examples are messages inside the agent; installation does not start an agent or configure provider authentication.

Skills support any agent target recognized by the standard Skills CLI. A file-capable agent can also read a skill's `SKILL.md` directly. The optional Python execution helper supports Claude Code and Codex only.

## Choose a skill

Grouped by when you reach for them. Install only what you need; the optional `next-step` router names the others but does not install them. The words used here (brief, spec, task, issue) are defined in [GLOSSARY.md](GLOSSARY.md).

### 1. Getting started

Set up once, then find your way around. **Start with `setup-agent-workflow`.**

| Skill | What it does |
|---|---|
| [`setup-agent-workflow`](skills/engineering/setup-agent-workflow/SKILL.md) | Set up one project so the other skills know its commands, tracker and docs. |
| [`next-step`](skills/productivity/next-step/SKILL.md) | Find the next step for your work: pick a route, or resume where you left off. |

### 2. Main flow

From idea to merged change, in order. **Start with `grill-me`**, or with `to-brief` when the work arrives as notes or messages.

| Skill | What it does |
|---|---|
| [`to-brief`](skills/productivity/to-brief/SKILL.md) | Turn notes, messages or documents into a source-linked brief. |
| [`grill-me`](skills/productivity/grill-me/SKILL.md) | Get interviewed about a plan until every decision is settled and recorded. |
| [`to-spec`](skills/engineering/to-spec/SKILL.md) | Turn settled decisions into a written spec. |
| [`to-tasks`](skills/engineering/to-tasks/SKILL.md) | Split a spec into small tasks an agent can build, each with its blockers. |
| [`implement`](skills/engineering/implement/SKILL.md) | Build one task test-first and return evidence for each acceptance criterion. |
| [`code-review`](skills/engineering/code-review/SKILL.md) | Review a diff against the spec and against the project's standards. |
| [`qa`](skills/engineering/qa/SKILL.md) | Check the running behavior against the acceptance criteria. |
| [`pr`](skills/engineering/pr/SKILL.md) | Prepare a pull request, check its status, or sync after it merges. |
| [`retro`](skills/engineering/retro/SKILL.md) | Look back on real work and fix the environment that caused friction. |

### 3. Shaping

Answer one open question; the answer feeds the main flow. **Start with `research`.**

| Skill | What it does |
|---|---|
| [`research`](skills/productivity/research/SKILL.md) | Get a cited answer from primary sources. |
| [`prototype`](skills/engineering/prototype/SKILL.md) | Answer a design question with a small throwaway experiment. |
| [`ui-design`](skills/engineering/ui-design/SKILL.md) | Settle interface flows, states and visual direction before building. |

### 4. Upkeep

Keep the codebase healthy; generates work for the main flow. **Start with `improve-codebase-architecture`.**

| Skill | What it does |
|---|---|
| [`improve-codebase-architecture`](skills/engineering/improve-codebase-architecture/SKILL.md) | Find the modules worth deepening, with evidence, and take one into the main flow. |

### 5. Sessions and instructions

Keep work portable and agent instructions sharp.

| Skill | What it does |
|---|---|
| [`handoff`](skills/productivity/handoff/SKILL.md) | Write up the current work so another session or agent can continue it. |
| [`writing-for-agents`](skills/productivity/writing-for-agents/SKILL.md) | Write and fix skills and other documents agents read. |

### Common routes

- **Clear fix:** `implement` → `code-review`.
- **Notes or messages to act on:** `to-brief` → `grill-me` for open decisions → `implement` once scope is settled.
- **Larger feature:** `grill-me` → `to-spec` → `to-tasks` → `implement` per task → `code-review` and `qa` → `pr` → `retro`.
- **Open question:** `research`, `prototype` or `ui-design` answers it, then the main flow resumes.
- **Changing session, agent or workspace:** `handoff`.

Follow the project's own commands and delivery rules. Add a missing collaborator deliberately when its guidance is needed. See the [skill guide](docs/skill-guide.md) for example requests and completion signals, or the [worked example](docs/walkthrough.md) for connected brief, spec and task records.

## Install from a local checkout

From this repository, list available skills or install a selection into another project:

```sh
bash scripts/install-skills.sh /path/to/project --list
bash scripts/install-skills.sh /path/to/project --skill setup-agent-workflow implement code-review
```

Run without `--skill` in a normal terminal for interactive selection. Unattended calls require explicit skill names. The wrapper uses `skills@1.7.4`, disables telemetry and defaults to project-local Claude Code and Codex targets; override them with `--agent`.

The standard symlink method keeps selected skills under the project's `.agents/skills`, with host links sharing those files. Each skill owns its resources and can be relocated independently. Python helpers stay in this source repository.

For Claude only, add `--agent claude-code`; Claude discovers the shared files through `.claude/skills` links. Installation does not paste skill instructions into `CLAUDE.md`. Setup guidance keeps root rules focused, avoids duplicating skill catalogs, and routes detailed instructions to the selected skill and relevant references. See [context cost](docs/context-cost.md) for discovery versus activation and measurement limits.

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
