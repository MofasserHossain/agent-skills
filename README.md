# Agent Workflow

A reusable workflow for turning ideas, documents, messages and tickets into verified changes. The workflow is independent of the coding agent, model, tracker and execution environment.

## Start here

Requires Python 3.10+ for the optional local helper. The Markdown skills also work without Python.

```sh
python3 tools/workflow.py agents
python3 tools/workflow.py init /path/to/project
python3 tools/workflow.py prompt /path/to/project/docs/work/feature/issues/01-task.md --project /path/to/project
```

In any agent with file access, start with:

> Read /absolute/path/to/agent-workflow/skills/workflow/SKILL.md. Use this workflow for the work I provide in this project.

This requires no copying of skills into each project and no global configuration changes. Keep this checkout somewhere stable. Update it deliberately through Git.

## What is included

- Twelve portable skills with focused instructions, shared contracts and templates.
- Local-file and GitHub task conventions; one authoritative tracker per feature.
- A dependency-free helper for project initialization, executor discovery, context preparation and explicit one-task dispatch.
- Manual, Claude Code, Codex and custom command profiles. Models and permissions remain configurable in their native tools.
- Behavioral tests for the helper and realistic scenarios for piloting the skills.
- A design specification and pinned research provenance.

## What is not implemented yet

Automated task scheduling/loops, a GitHub API adapter, Docker provisioning, global skill installation and native model-effort translation are later milestones. The helper dispatches explicitly selected local tasks on the host. It never treats a successful process exit as feature acceptance.

Read [the specification](docs/spec.md), [architecture](docs/architecture.md) and [installation](docs/installation.md).

## Choose an executor

```sh
python3 tools/workflow.py run TASK.md --project /path/to/project --agent claude
python3 tools/workflow.py run TASK.md --project /path/to/project --agent codex
```

These print a launch preview. Add `--execute` to actually start the selected CLI. That uses the CLI's existing authentication and permissions and may consume its usage allowance. The helper never logs into a provider, installs a CLI, or adds permission-bypass flags.

Use `--registry /path/to/agents.json` for another agent or customized CLI arguments. The registry is an explicit list, not a dependency on a provider SDK.

## Project data

Project setup creates only `.agent-workflow.json`. It leaves existing AGENTS.md, CLAUDE.md and project code alone. Planning records stay with the project; shared procedures stay here.

Local tasks use Markdown with a small JSON frontmatter block, which is a YAML-compatible subset that Python can read without a YAML dependency. See [the task contract](references/task-contract.md).

For GitHub work, use [tracker conventions](references/trackers.md) through the agent's available GitHub tools. Do not maintain two competing copies of status.

## Verify this repository

```sh
python3 -m unittest discover -s tests -v
python3 tools/workflow.py check
```

CLI transport is tested with a local fake executor. Real provider authentication, model output quality and Docker behavior require a separate pilot.
