# Working on Agent Workflow

Keep the core provider-neutral. Tool-specific commands belong in adapters; project commands belong in project configuration. Task records and results must survive a change of agent or model.

Use Python standard library for the helper. Add a dependency only for a concrete capability the existing implementation cannot reasonably provide.

Skill instructions should change behavior, stay concise and reference conditional detail. One source of truth per concept. Do not make every technique mandatory.

Run `python3 -m unittest discover -s tests -v` and `python3 tools/workflow.py check` after changes. Use fake executors for tests; live LLM calls, account changes, publishing and provider configuration changes require task authorization.

Do not install globally, push, merge, create remote repositories, or call external agents merely to validate the kit. Keep credentials and project run output out of Git.

When adding a capability, update README's implemented/roadmap distinction and docs/spec.md.
