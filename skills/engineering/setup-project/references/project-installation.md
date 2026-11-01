# Project installation

The standard Skills CLI installs selected canonical folders from this repo's skills directory. Run npx skills@1.7.4 add /path/to/agent-skills/skills --agent claude-code codex from the target project. Choose only needed skills, project scope, and the usual symlink method. The canonical skill files are copied into the project; host links point within it. --copy creates separate host copies. Do not use a source-link mode when the project must work independently.

Each selected skill includes its own required references/templates. Other skill names are optional installed collaborators, not mandatory dependencies or paths to the authoring checkout. Kit research, tests, validation tools and the optional execution runner stay in the source kit. Installed skills can be used without Python.

Run setup-project if installed, or follow existing project conventions to configure actual commands, tracker and documentation. Preserve AGENTS/CLAUDE symlinks. Installation does not initialize commands, configure accounts, run an LLM or authorize publication.

For a local source, rerun skills add with the intended --skill names after reviewing source changes. Review project-local customizations before reinstalling: the standard installer can replace files and does not provide the legacy installer's local-edit protection. skills-lock.json records the local source path for maintenance; skill execution does not require that path. No global registration is required.

Earlier .agent-workflow snapshots remain supported by the source kit's legacy installer. Do not mix native entries with the same skill name. Migrate deliberately after reviewing the selected set and preserving project configuration/work records.

For another host, replace the --agent values with its Skills CLI target name; the installer owns native discovery paths and supported-name validation. Without a CLI integration, a file-capable agent can read the installed SKILL.md directly with its bundled resources. This does not add execution-helper adapters or guarantee host-specific invocation commands.

GitHub installation can use MofasserHossain/agent-skills directly once this source layout is merged. No generated copy or Python build is required. Each resource belongs to one skill; other procedures are named collaborators rather than relative filesystem links. Install missing collaborators deliberately when their guidance is needed.
