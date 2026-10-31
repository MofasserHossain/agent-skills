# Installation and project setup

Keep this repository in a stable location, for example next to your project repositories. It has its own Git history and remote. No application repository contains a copy of the entire kit.

## Portable use first

Tell any file-capable agent to read `skills/workflow/SKILL.md` by absolute path, then work in your project. The helper can also assemble a self-contained active skill with a task and project configuration.

```sh
python3 /path/to/agent-workflow/tools/workflow.py init /path/to/project
python3 /path/to/agent-workflow/tools/workflow.py agents
```

Fill in the generated project's verification commands and conventions. Do not rename, replace or duplicate existing instruction files.

Before dispatching CLI runs, add `.workflow-runs/` to the project's `.gitignore`. These private local artifacts can contain provider output and should not enter project history. Project initialization leaves that file unchanged so existing ignore conventions can be respected.

A short optional project pointer is enough:

> Shared workflow: read /path/to/agent-workflow/skills/workflow/SKILL.md when asked to take work through planning and delivery. Project rules here remain authoritative.

Absolute paths are machine-local configuration. Document the kit location for each machine; avoid committing another person's home path as a universal convention.

## Native discovery

Agent-specific skill discovery is an optional adapter. Register the shared checkout using the chosen agent's supported mechanism after checking its current documentation. This version does not install global skills or plugins.

## Swap agents

Use `--agent claude`, `--agent codex`, or another registry entry. The default is manual. Project configuration may choose a default executor, but the selection is not embedded in tasks.

A custom registry has `schema_version: 1` and an `agents` object. Each entry has a label, notes and either a command array or null for manual use. Commands accept the whole prompt on stdin. They run in the selected project directory without a shell.

Do not place secrets in registries. Use the executor's normal authentication mechanism.

## Publish

Create a remote repository under the user's chosen account and visibility when requested. Push this kit independently of application repositories. No remote is created by project setup.
