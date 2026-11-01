# Install selected skills from the local kit

Use the standard Skills CLI against the prepared `dist/skills` directory. This is the primary route for new projects; only Claude Code and Codex are currently supported.

## Local installation

A fresh source checkout first needs its distributions prepared by the maintainer:

```sh
python3 tools/package_skills.py
```

Then, from this root repo:

```sh
bash scripts/install-skills.sh /path/to/project --list
bash scripts/install-skills.sh /path/to/project
```

The first lists the catalog without installing. The second opens the standard selector for project-local Claude Code/Codex skills in a normal terminal. Inside an agent environment, supply explicit --skill names: the CLI automatically skips prompts there, and the wrapper prevents a silent install-all. Select only what you need; the router and setup procedure are optional. The wrapper defaults to the tested `skills@1.7.4` and disables telemetry. That CLI requires Node 22.20+; installed Markdown skills need no Python.

For explicit selection:

```sh
bash scripts/install-skills.sh /path/to/project --skill grill research write-spec
```

The standard CLI shows its installation summary and confirmation. `--yes` skips confirmation only when an explicit --skill selection is supplied to the wrapper. `--skill '*'` explicitly selects every skill; the wrapper rejects the broader --all flag because it also selects all agents. Global installation and other agents are outside this wrapper's scope.

Alternatively, run directly from the target project:

```sh
DISABLE_TELEMETRY=1 npx skills@1.7.4 add /path/to/agent-workflow/dist/skills --agent claude-code codex
```

These are real installation commands, not the legacy helper's preview/--apply protocol. Use --list to inspect first and the normal interactive confirmation when installing.

## Files in the project

The standard symlink method creates a project-local canonical folder per selected skill, plus host links:

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

After source edits, rebuild dist/skills. Then rerun skills add for the intended --skill names. Local source paths in skills-lock.json support maintenance; they are not needed to execute already-copied skills. Review project-local skill edits before reinstalling: standard installation can overwrite them and does not provide our legacy local-edit guard. Do not assume local sources have the same update behavior as Git-hosted sources; rerunning add is the verified local refresh route.

The generated distribution is ignored in Git. Maintainers rebuild it from canonical sources; hand edits to generated output are rejected by the builder. The build preserves applicable license/notice files. It does not publish, install globally, or run an agent. Future Git/plugin/npm packaging can reuse these independent skill folders, but no publishing integration is activated now.

## Existing legacy installations

Earlier projects may contain .agent-workflow plus a thin agent-workflow entry. Those remain supported by tools/install_project.py and tools/register_skills.py; their ownership markers protect local edits. Their --select/--skills, --update and --apply behavior is separate from the standard CLI.

Migrate after choosing the intended skill set. Preserve the project's AGENTS/CLAUDE instructions, .agent-workflow.json and work records. Review/back up local changes to the managed bundle and its native entries. Remove only the owned legacy installation and update project pointers before installing the chosen standard skills; the agent-workflow name can otherwise conflict with the old entry. Do not remove unrelated skills. An existing project is not migrated merely by preparing this distribution.

Existing project selections remain unchanged until deliberately migrated. Use the source wrapper with --list to inspect available skills without changing an installation.

Validated locally with Skills CLI 1.7.4: a three-skill selection using project-internal symlinks, and a separate one-skill UI selection using --copy. Both retained working local references after the source distribution was hidden; the first also survived moving the project. These are filesystem/installation checks, not claims about model output quality.

Checked 2026-11-01 against the [Skills CLI reference](https://github.com/vercel-labs/skills/blob/main/docs/commands.md#skills-add) and [installer source](https://github.com/vercel-labs/skills/blob/main/src/installer.ts). Matt's [editable-file installation](https://github.com/mattpocock/skills#installation-30-second-setup) uses the same CLI pattern.
