# Install and use canonical skills

The same `skills/<category>/<name>/` folders are edited, reviewed and installed. Every filesystem resource is inside its owning skill; other procedures are referred to by installed name. No generated package tree or build step is required.

## GitHub installation

Run from your target codebase:

```sh
npx skills@latest add MofasserHossain/agent-skills
```

Choose the required skills, agents and project scope. The private repository requires existing Git access. For the pinned CLI and an explicit selection:

```sh
DISABLE_TELEMETRY=1 npx --yes skills@1.7.4 add MofasserHossain/agent-skills --skill grill implement research --agent claude-code codex
```

The CLI discovers canonical `skills/` folders directly. This layout takes effect on GitHub when the migration is merged; local testing can use this checkout's skills directory beforehand. Do not use the removed generated-distribution path.

## Local installation

A fresh checkout is ready to install; no Python build is needed. From this root repo:

```sh
bash scripts/install-skills.sh /path/to/project --list
bash scripts/install-skills.sh /path/to/project
```

The first lists the catalog without installing. The second opens the standard selector for project-local skills (Claude Code/Codex by default) in a normal terminal. Inside an agent environment, supply explicit --skill names: the CLI automatically skips prompts there, and the wrapper prevents a silent install-all. Select only what you need; the router and setup procedure are optional. The wrapper defaults to the tested `skills@1.7.4` and disables telemetry. That CLI requires Node 22.20+; installed Markdown skills need no Python.

For explicit selection:

```sh
bash scripts/install-skills.sh /path/to/project --skill grill research write-spec
```

Choose the intended host explicitly when a project uses only one:

```sh
bash scripts/install-skills.sh /path/to/project --agent claude-code --skill grill research
bash scripts/install-skills.sh /path/to/project --agent codex --skill grill research
```

Omitting `--agent` retains the default of both Claude Code and Codex. `--agent claude-code codex` selects both explicitly; `-a` and `--agent=codex` are also supported. Other agent names are forwarded to the Skills CLI, which validates supported targets and owns their installation paths. Missing agent values are rejected before the CLI runs. Skill selection and agent selection are independent.

The standard CLI shows its installation summary and confirmation. `--yes` skips confirmation only when an explicit --skill selection is supplied to the wrapper. `--skill '*'` explicitly selects every skill; the wrapper rejects the broader --all flag because it also selects all agents. Global installation is outside this wrapper's scope.

Alternatively, run directly from the target project:

```sh
DISABLE_TELEMETRY=1 npx skills@1.7.4 add /path/to/agent-skills/skills --agent claude-code codex
```

These are real installation commands, not the legacy helper's preview/--apply protocol. Use --list to inspect first and the normal interactive confirmation when installing.

## Start Claude Code or Codex and use an installed skill

From this source checkout, install a chosen starter set into the target codebase using the canonical skill folders:

```sh
bash scripts/install-skills.sh /path/to/project --agent claude-code codex --skill setup-project agent-workflow
```

The router is named `agent-workflow` in source and installation. Select the standard symlink method to share each installed copy between the two hosts. Add `implement`, `review` or planning skills when needed; the router does not install its collaborators. To select every skill deliberately, use `--skill '*'` instead. Do not use `--copy` when shared references are wanted.

Start the chosen agent from the target codebase, not the kit checkout:

```sh
cd /path/to/project
claude
```

Or start Codex there:

```sh
cd /path/to/project
codex
```

The following are messages typed **inside the agent**, not shell commands. Run setup once, then invoke an installed procedure with the actual task reference:

| Purpose | Claude Code | Codex |
|---|---|---|
| Record project conventions | `/setup-project` | `$setup-project` |
| Choose or resume a route | `/agent-workflow Resume docs/work/feature/` | `$agent-workflow Resume docs/work/feature/` |
| Resolve uncertain requirements | `/grill Resolve offline behavior from docs/work/feature/brief.md` | `$grill Resolve offline behavior from docs/work/feature/brief.md` |
| Implement a settled task | `/implement Work on docs/work/feature/issues/01-task.md` | `$implement Work on docs/work/feature/issues/01-task.md` |
| Review the change | `/review Review the current diff against that task` | `$review Review the current diff against that task` |

Only installed skills are available. Select the skill from the host's picker when names collide with built-ins or another installation. In particular, Codex's built-in `/review` is distinct from this kit's `$review` skill. If a new skill does not appear, refresh/restart the session and inspect the project skill files and link targets. A direct fallback is: “Read .agents/skills/implement/SKILL.md and implement docs/work/feature/issues/01-task.md.” Preserve the skill folder's bundled resources.

Invocation references: [Claude Code skills](https://code.claude.com/docs/en/skills), [Codex skill examples](https://developers.openai.com/blog/eval-skills), [Codex CLI](https://developers.openai.com/codex/cli/). Commands were documented on 2026-11-01; no live model session was launched to validate them.

### Run inside Docker Sandbox or another isolated environment

For isolated execution, keep the actual project checkout, selected skill folders, project rules and work records together inside the environment the agent can read. Personal host skill directories and symlinks back to this authoring checkout are not assumed to be available.

With skills already installed in the project-local layout above and a configured Docker Sandboxes installation, the currently documented local entry points are:

```sh
sbx run claude /path/to/project
# Or, in a separate session:
sbx run codex /path/to/project
```

Use the same `/setup-project`, `/implement` or `$setup-project`, `$implement` messages inside the chosen agent. These are alternative sessions; two agents must not edit the same working tree concurrently. Keep `.agents/skills` and `.claude/skills` together so their project-internal symlinks resolve inside the sandbox.

A mounted project workspace can expose source edits to the host; it is not the same as keeping changes in a separate clone. For stronger separation, prepare a checkout inside the isolated environment or use the installed sandbox's documented clone mode, then install/copy the selected self-contained skill folders into that checkout. Ensure uncommitted/untracked installed skills actually arrive there before starting work. A symlink to a host-only path does not provision its target. For any other container, VM or remote workspace, apply the same resource rule and start the agent from its internal project path.

Docker Sandbox provisioning, authentication and installed CLI compatibility are prerequisites, not performed by this kit's installer. Current Docker documentation uses `sbx`; verify your installed version instead of assuming older `docker sandbox` examples match. See [Docker usage](https://docs.docker.com/ai/sandboxes/usage/), [Claude sandbox configuration](https://docs.docker.com/ai/sandboxes/agents/claude-code/) and [Codex sandbox configuration](https://docs.docker.com/ai/sandboxes/agents/codex/). No Docker command or credential setup was executed to validate this guide.

The existing helper starts a process in the environment where the helper itself runs. Running it on the Mac starts a host worker; to run that helper within an already-provisioned isolated environment, provision its source/runtime resources there and invoke it there. It does not cross into Docker automatically. A managed Docker runtime adapter and bounded once/loop remain [planned](work/runner-adaptation/spec.md).

### Optional worker dispatch is separate

The normal installed-skill route above runs in your existing interactive agent. It does not install the Python runner. If you deliberately use the helper from this authoring checkout, configure the target's .agent-workflow.json and local task records first, then preview:

```sh
python3 /path/to/agent-skills/tools/workflow.py run /path/to/project/docs/work/feature/issues/01-task.md --project /path/to/project --agent codex
```

`--agent claude` selects the helper's Claude adapter (the Skills CLI target name is `claude-code`). Add `--execute` only when launching that worker is authorized; preview does not run it. Docker and managed once/loop are not activated by installing skills or invoking a slash/dollar command. See the [execution plan](execution-plan.md).

## Files in the project

With Claude Code and Codex both selected in symlink mode, the CLI creates one canonical folder per skill under `.agents/skills`, which Codex reads, and relative `.claude/skills` links for Claude. A single-agent unattended installation can use a direct copy instead: `.claude/skills` for Claude or `.agents/skills` for Codex. Selecting only Codex does not request a Claude installation:

```text
.agents/skills/<selected-skill>/SKILL.md
.agents/skills/<selected-skill>/references/   Only when needed
.agents/skills/<selected-skill>/templates/    Only when needed
.claude/skills/<selected-skill>              Link within this project
skills-lock.json                            Installer maintenance metadata
```

Use --copy for separate host copies when preferred. Do not choose source-link development mode when the project must remain independent. Verify the installer version's resulting paths; symlink fallback can produce copies.

Each skill keeps its own resources: local supporting links stay inside its folder. Cross-skill references name optional skills, with no paths to uninstalled siblings or the author's checkout. The agent-workflow router describes the catalog and checks availability; installing it does not install the entire workflow.

Research about Matt, tests, examples, source-only tools and the optional execution runner stay in the root repo. Each project keeps its actual requirements/research/specs/issues, product rules and commands. The source kit's visibility does not protect copied content if that content is committed publicly.

## Project configuration and updates

Invoke a selected skill through the host's supported discovery/invocation mechanism. A session may need a refresh. Run setup-project if installed to inspect real project scripts, tracker and documentation conventions; preserve existing instructions and AGENTS/CLAUDE symlinks. It can write project configuration directly without the Python helper. See [project checks](../skills/engineering/implement/references/verification-policy.md).

After source edits, run the source checks and rerun skills add for the intended --skill names. Local source paths in skills-lock.json support maintenance; they are not needed to execute already-copied skills. Review project-local skill edits before reinstalling: standard installation can overwrite them and does not provide our legacy local-edit guard. Do not assume local sources have the same update behavior as Git-hosted sources; rerunning add is the verified local refresh route.

There is one editable/installable tree under skills. Supporting files stay with their owner; collaborator names do not create filesystem dependencies on absent siblings. Installation copies only the selected folders and does not publish source changes or install the optional runner.

## Earlier generated-package installations

If skills-lock.json points to the old generated-distribution path, the installed files continue to work. To update, preserve local edits and deliberately rerun skills add from this repo or its skills directory for the same chosen names and agents. Check the installation summary and refreshed lock; do not assume the old source entry will update itself. There is no second package tree to rebuild. The source router now lives at skills/productivity/agent-workflow with the same installed name as before.

Local validation of the direct layout used the cached Skills CLI 1.7.4: all 15 canonical skills were listed and installed into a disposable project for Claude Code/Codex. After hiding the source and moving the project, all 15 relative Claude links and 17 supporting-resource links resolved. No agent invocation or account setup was performed.

## Existing legacy installations

Earlier projects may contain .agent-workflow plus a thin agent-workflow entry. Those remain supported by tools/install_project.py and tools/register_skills.py; their ownership markers protect local edits. Their --select/--skills, --update and --apply behavior is separate from the standard CLI.

Migrate after choosing the intended skill set. Preserve the project's AGENTS/CLAUDE instructions, .agent-workflow.json and work records. Review/back up local changes to the managed bundle and its native entries. Remove only the owned legacy installation and update project pointers before installing the chosen standard skills; the agent-workflow name can otherwise conflict with the old entry. Do not remove unrelated skills. An existing project is not migrated merely by changing the source layout.

Existing project selections remain unchanged until deliberately migrated. Use the source wrapper with --list to inspect available skills without changing an installation.

Historical generated-layout validation used Skills CLI 1.7.4: a three-skill selection using project-internal symlinks, and a separate one-skill UI selection using --copy. Both retained working local references after the source distribution was hidden; the first also survived moving the project. The current suite separately validates canonical skill copies and project-internal links after source removal and project relocation; it does not establish live model behavior.

Checked 2026-11-01 against the [Skills CLI reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-add) and [installer source](https://github.com/vercel-labs/skills/blob/main/src/installer.ts). Matt's [editable-file installation](https://github.com/mattpocock/skills#installation-30-second-setup) uses the same CLI pattern.

## Other agents

Pass a target supported by the pinned Skills CLI, for example `--agent cursor` or `--agent opencode`, together with the desired `--skill` names. These use the same canonical skill folders, not new executor adapters. Unknown names are rejected by the CLI; this wrapper does not claim universal native-agent compatibility. To list the skill catalog without installing, use `--list`.

For a host without Skills CLI integration, supply the canonical skill folder and ask it to read `SKILL.md`, following its local resource links. Keep the whole folder together. This provides the procedure without promising automatic discovery, slash commands or process dispatch. Existing project rules and task authorization still apply.

Source-linked development registrations that still point to the old skills/workflow path must be reviewed and refreshed to skills/productivity/agent-workflow. Preserve edited entries; the registration tool refuses replacements rather than silently overwriting them. Existing copied standard skill installations do not depend on the moved source path.

## Categorized source and PR rename

Source folders are grouped under `skills/engineering/` and `skills/productivity/`. Skills CLI discovers the nested catalog and installs selected names directly under the agent's skill directory. Each folder carries its own resources and `agents/openai.yaml` display metadata. The YAML provides Codex labels and a suggested prompt; it does not launch a command or change invocation permissions.

The installed `pull-request` skill is now named `pr`: use `/pr` in Claude Code or `$pr` in Codex after selecting it during installation. Existing `pull-request` copies remain until deliberately removed; preserve customizations and avoid keeping conflicting copies. The legacy snapshot helper accepts `pull-request` as an alias for `pr`.
