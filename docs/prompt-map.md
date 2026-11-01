# Stage instructions, runner prompts and project context

For entry-point selection and example requests, see the [skill guide](skill-guide.md). Canonical behavior stays in the procedures below; human examples do not form another prompt library.

## Standard local installation

Use the Skills CLI against canonical skills/ folders for new projects. Each stage is directly discoverable and keeps filesystem resources inside its own folder. Collaborators are named skills, not relative paths to uninstalled siblings. The agent-workflow router is optional. Read the installed copy; no package build or Python helper is needed for ordinary use. The helper/direct-path examples below remain optional source/legacy workflows. See [installation](installation.md).

## Separate instructions already available

A SKILL.md is a reusable prompt/procedure file with discovery metadata. Its filename does not make it less of a prompt. Keep the stage behavior in one canonical file instead of copying the same instructions into an additional prompt library.

| Work | Canonical procedure | Supporting artifact shape | Current invocation |
|---|---|---|---|
| Resolve requirements | [grill](../skills/productivity/grill/SKILL.md) | Brief and decisions | Current interactive agent |
| Research and plan a UI | [ui-design](../skills/engineering/ui-design/SKILL.md) | [optional design record](../skills/engineering/ui-design/templates/design.md) | Current agent; relevant frontend/full-stack tasks only |
| Create the feature PRD | [write-spec](../skills/engineering/write-spec/SKILL.md) | [spec template](../skills/engineering/write-spec/templates/spec.md) | Current agent reads the settled brief/decisions |
| PRD to implementation issues | [plan-tasks](../skills/engineering/plan-tasks/SKILL.md) | [task template](../skills/engineering/plan-tasks/templates/task.md) and [contract](../skills/engineering/plan-tasks/references/task-contract.md) | Current agent reads the agreed PRD and existing work |
| Implement one issue | [implement](../skills/engineering/implement/SKILL.md) | [result contract](../skills/engineering/implement/references/result-contract.md) | Current agent, or the optional one-task helper |
| PR preparation, updates, status and post-merge sync | [pr](../skills/engineering/pr/SKILL.md) | Project-owned delivery rules and verification evidence | Current agent, using available repository tools/CLI |
| Review and QA | [review](../skills/engineering/review/SKILL.md), [qa](../skills/engineering/qa/SKILL.md) | [QA template](../skills/engineering/qa/templates/qa.md) | Current agent; required human judgments remain pending |

Templates specify the shape of an output. Procedures specify how to produce or evaluate it. Project briefs/specs/issues are the actual inputs and outputs, not copies of the procedures.

## How the implementation helper composes context

[tools/workflow.py](../tools/workflow.py) currently assembles this request in make_prompt:

1. Project and selected issue paths, instruction precedence and action boundaries.
2. Project configuration, including required verification commands.
3. The active implementation procedure, with supporting links resolved against the shared kit.
4. The selected task body, including its source/PRD references.
5. The portable result contract and the instruction to leave status for supervised evaluation.

The small transport wrapper is Python text; the engineering instructions remain in the separate implementation skill. Referenced project instructions and PRD material are read by the executor as needed, not all embedded by the helper. In linked mode, the source checkout must remain readable. With a project snapshot, the same helper runs from .agent-workflow/tools and resolves supporting resources within that installed snapshot. The runtime dependencies and agent still need provisioning.

The helper's prompt/run commands are implementation-only. There is no stage flag for automatic PRD generation, ticket generation, batch planning, review or merging. Those procedures work through the current file-capable agent; their automatic context assembly/dispatch is future runner work. See the [execution plan](execution-plan.md). External prompt wrappers may be useful when that runner has concrete input/output contracts; they should reference canonical stage behavior instead of duplicating it.

## Work from a project, reuse the kit

Open the agent in the target project's checkout or worktree. Keep that project as the working directory so Git, dependency tools, tests and instruction discovery use the intended codebase. The shared kit is a toolbox, not the working directory for application edits.

Without native registration, use a request such as:

> Work in /absolute/path/to/project. Read /absolute/path/to/agent-workflow/skills/engineering/write-spec/SKILL.md and the project's instructions. Turn docs/work/feature/brief.md and its settled decisions into docs/work/feature/spec.md. Report any missing decisions.

For the next stage:

> In the same project, read /absolute/path/to/agent-workflow/skills/engineering/plan-tasks/SKILL.md and docs/work/feature/spec.md. Prepare vertical issues with requirement coverage, blockers and verification under docs/work/feature/issues/.

These are usage examples, not another set of stage instructions. Replace the paths; creating issues follows the existing authorization and agreed decisions. In this kit's own checkout, use relative canonical paths such as `skills/engineering/implement/SKILL.md` and keep actual work records under `docs/work/<feature>/`. Templates provide artifact shapes, examples are fictional, and conversation summaries provide historical background.

Standard installed skills are individually discoverable through the host's supported invocation mechanism. Merely having the source files in `skills/` does not register them with a host. Legacy/source-linked registration exposes one thin router entry; invoke that entry with the stage and source reference, or read the procedure directly.

The helper can be invoked by absolute path from elsewhere because --project selects the target:

```sh
python3 /absolute/path/to/agent-workflow/tools/workflow.py prompt /absolute/path/to/project/docs/work/feature/issues/01-task.md --project /absolute/path/to/project
python3 /absolute/path/to/agent-workflow/tools/workflow.py run /absolute/path/to/project/docs/work/feature/issues/01-task.md --project /absolute/path/to/project --agent codex
```

The run command previews unless --execute is added. Actual dispatch sets the subprocess working directory to the project; supplying a project path does not itself grant filesystem permission or provision a remote workspace. A native interactive agent needs its own workspace/access configuration.

For new independent project installations, use the standard Skills CLI route described above. `tools/install_project.py` maintains legacy `.agent-workflow` snapshots; it is not the default for new projects. Optional source-linked pointers remain available for deliberate development use. Choose one discovery mode/scope per agent/project to avoid duplicate entries. Each project keeps its own rules, configuration and work records. [Installation](installation.md) explains installation and legacy migration; adding .agent-workflow.json alone does not register skills. Containers and remote machines need the selected resources provisioned at a path they can read.

## What Matt's sources establish

The inspected sources show multiple mechanisms, not one universal central workspace:

- The [workshop snapshot](https://github.com/mattpocock/ai-engineer-workshop-2026-project/tree/8f1ea9b0a210caddd5f8d1749be636f7b22a9e62/.claude/skills) tracks ordinary project-local skill files, including write-a-prd and prd-to-issues. Its .agents entry is a symlink to .claude; that aliases the local directory rather than duplicating it.
- [Course Video Manager's runner](https://github.com/mattpocock/course-video-manager/blob/b47b1ec54cc7742326ca2682e49f09803cdac303/.sandcastle/main.ts) loads separate plan/implement/review/merge prompt files with per-run arguments. Those wrappers are project-local. Its [review prompt](https://github.com/mattpocock/course-video-manager/blob/b47b1ec54cc7742326ca2682e49f09803cdac303/.sandcastle/review/prompt.md) also refers to a globally installed code-review skill, showing that shared and local instructions can coexist.
- His [skills README](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/README.md) documents plugin installation and editable-file installation as alternatives, followed by setup once per target repo. The setup skill records project-specific tracker and domain conventions.

These files do not establish his private IDE/session arrangement or prove that he always copies everything, or always controls every repository by path from a single workspace. This kit deliberately shares procedures while leaving project state and execution context local.
