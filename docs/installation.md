# GitHub distribution

Use the self-contained `packages/skills` tree for GitHub installation:

```sh
DISABLE_TELEMETRY=1 npx --yes skills@1.7.4 add https://github.com/MofasserHossain/agent-workflow/tree/main/packages/skills --list
DISABLE_TELEMETRY=1 npx --yes skills@1.7.4 add https://github.com/MofasserHossain/agent-workflow/tree/main/packages/skills --skill grill implement research --agent claude-code codex --yes
```

Select only the desired skills. The full path avoids authored `skills/` folders,
which depend on shared source resources. Tracked packages bundle those resources
and rewrite their links; the router is exported as `agent-workflow`.

Maintainers rebuild with `python3 tools/package_skills.py --output packages/skills`
and validate with the same command plus `--check`. Include generated changes in
the source change's PR. Keep the build manifest; never edit package output by hand.
The default ignored `dist/skills` remains available for optional maintainer previews.
GitHub availability follows the reviewed commit/merge; preparing packages does
not publish them. No automation or optional Python runner is installed.

# Install selected skills from the local kit

Use the standard Skills CLI against the tracked `packages/skills` directory. This is the primary route for new projects; any agent supported by the pinned Skills CLI can be targeted. The optional execution helper remains Claude Code/Codex only.

## Local installation

A fresh checkout already contains reviewed packages. Maintainers rebuild after editing canonical sources:

```sh
python3 tools/package_skills.py --output packages/skills
```

Then, from this root repo:

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
DISABLE_TELEMETRY=1 npx skills@1.7.4 add /path/to/agent-workflow/packages/skills --agent claude-code codex
```

These are real installation commands, not the legacy helper's preview/--apply protocol. Use --list to inspect first and the normal interactive confirmation when installing.

## Start Claude Code or Codex and use an installed skill

From this source checkout, install a chosen starter set into the target codebase using its tracked packages:

```sh
bash scripts/install-skills.sh /path/to/project --agent claude-code codex --skill setup-project agent-workflow
```

The source router `workflow` exports as `agent-workflow`; invoke and install it by that exported name. Select the standard symlink method to share each installed copy between the two hosts. Add `implement`, `review` or planning skills when needed; the router does not install its collaborators. To select every skill deliberately, use `--skill '*'` instead. Do not use `--copy` when shared references are wanted.

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
python3 /path/to/agent-workflow/tools/workflow.py run /path/to/project/docs/work/feature/issues/01-task.md --project /path/to/project --agent codex
```

`--agent claude` selects the helper's Claude adapter (the Skills CLI target name is `claude-code`). Add `--execute` only when launching that worker is authorized; preview does not run it. Docker and managed once/loop are not activated by installing skills or invoking a slash/dollar command. See the [execution plan](execution-plan.md).

## Files in the project

The standard symlink method creates a project-local canonical folder per selected skill. Codex discovers that canonical `.agents/skills` location; when Claude Code is selected, its `.claude/skills` entry links there. Selecting only Codex does not request a Claude installation:

```text
.agents/skills/<selected-skill>/SKILL.md
.agents/skills/<selected-skill>/references/   Only when needed
.agents/skills/<selected-skill>/templates/    Only when needed
.claude/skills/<selected-skill>              Link within this project
skills-lock.json                            Installer maintenance metadata
```

Use --copy for separate host copies when preferred. Do not choose source-link development mode when the project must remain independent. Verify the installer version's resulting paths; symlink fallback can produce copies.

Each package is self-contained: local supporting links stay inside its folder. Cross-skill references name optional skills, with no paths to uninstalled siblings or the author's checkout. The agent-workflow router describes the catalog and checks availability; installing it does not install the entire workflow.

Research about Matt, tests, examples, build scripts and the optional execution runner stay in the root repo. Each project keeps its actual requirements/research/specs/issues, product rules and commands. The source kit's visibility does not protect copied content if that content is committed publicly.

## Project configuration and updates

Invoke a selected skill through the host's supported discovery/invocation mechanism. A session may need a refresh. Run setup-project if installed to inspect real project scripts, tracker and documentation conventions; preserve existing instructions and AGENTS/CLAUDE symlinks. It can write project configuration directly without the Python helper. See [project checks](../references/verification-policy.md).

After source edits, rebuild and validate packages/skills; regenerate dist/skills only when using an optional local preview. Then rerun skills add for the intended --skill names. Local source paths in skills-lock.json support maintenance; they are not needed to execute already-copied skills. Review project-local skill edits before reinstalling: standard installation can overwrite them and does not provide our legacy local-edit guard. Do not assume local sources have the same update behavior as Git-hosted sources; rerunning add is the verified local refresh route.

The local preview distribution under dist/skills is ignored in Git; packages/skills is the tracked GitHub distribution. Maintainers rebuild both from canonical sources; hand edits to generated output are rejected by the builder. The build preserves applicable license/notice files. It does not publish, install globally, or run an agent. The tracked GitHub path reuses these independent skill folders. Plugin/npm publication remains outside this installation.

## Existing legacy installations

Earlier projects may contain .agent-workflow plus a thin agent-workflow entry. Those remain supported by tools/install_project.py and tools/register_skills.py; their ownership markers protect local edits. Their --select/--skills, --update and --apply behavior is separate from the standard CLI.

Migrate after choosing the intended skill set. Preserve the project's AGENTS/CLAUDE instructions, .agent-workflow.json and work records. Review/back up local changes to the managed bundle and its native entries. Remove only the owned legacy installation and update project pointers before installing the chosen standard skills; the agent-workflow name can otherwise conflict with the old entry. Do not remove unrelated skills. An existing project is not migrated merely by preparing this distribution.

Existing project selections remain unchanged until deliberately migrated. Use the source wrapper with --list to inspect available skills without changing an installation.

Validated locally with Skills CLI 1.7.4: a three-skill selection using project-internal symlinks, and a separate one-skill UI selection using --copy. Both retained working local references after the source distribution was hidden; the first also survived moving the project. These are filesystem/installation checks, not claims about model output quality.

Checked 2026-11-01 against the [Skills CLI reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-add) and [installer source](https://github.com/vercel-labs/skills/blob/main/src/installer.ts). Matt's [editable-file installation](https://github.com/mattpocock/skills#installation-30-second-setup) uses the same CLI pattern.

## Other agents

Pass a target supported by the pinned Skills CLI, for example `--agent cursor` or `--agent opencode`, together with the desired `--skill` names. These use the same self-contained packages, not new executor adapters. Unknown names are rejected by the CLI; this wrapper does not claim universal native-agent compatibility. To list the package catalog without installing, use `--list`.

For a host without Skills CLI integration, supply the prepared skill folder and ask it to read `SKILL.md`, following its local resource links. Keep the whole folder together. This provides the procedure without promising automatic discovery, slash commands or process dispatch. Existing project rules and task authorization still apply.
