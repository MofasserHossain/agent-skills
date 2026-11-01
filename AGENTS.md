# Working on Agent Workflow

The optional execution helper supports Claude Code and Codex only. Portable skills can be installed for any agent supported by the standard Skills CLI, or read directly by a file-capable agent. Keep manual as a context-only mode, not another agent. Additional agent adapters are deferred until requested.

Keep the core provider-neutral. Tool-specific commands belong in adapters; project commands belong in project configuration. Task records and results must survive a change of agent or model.

Use Python standard library for the helper. Add a dependency only for a concrete capability the existing implementation cannot reasonably provide.

Skill instructions should change behavior, stay concise and reference conditional detail. One source of truth per concept. Do not make every technique mandatory.

Run `python3 -m unittest discover -s tests -v` and `python3 tools/workflow.py check` after changes. Use fake executors for tests; live LLM calls, account changes, publishing and provider configuration changes require task authorization.

Do not install globally, push, merge, create remote repositories, or call external agents merely to validate the kit. Keep credentials and project run output out of Git.

When adding a capability, update README's implemented/roadmap distinction and docs/workflow-spec.md.

New projects use the standard Skills CLI against prepared dist/skills folders. Keep packaging/build tools in this source repo; each exported skill must survive relocation with only its own resources. Validate with python3 tools/package_skills.py --check after rebuilding. The Bash wrapper supports project-local Skills CLI agent targets, defaulting to Claude Code/Codex; the CLI owns target validation and discovery paths. Legacy snapshots are migrated deliberately after user selection.

The reviewed GitHub distribution lives at packages/skills. After changing canonical skills or their resources, rebuild with `python3 tools/package_skills.py --output packages/skills` and validate with the same command plus `--check`; include the generated diff and ownership manifest in the same PR. Do not hand-edit it. Keep dist/skills ignored for local previews. GitHub install examples must use the explicit packages/skills path to avoid discovering authoring-only folders.
