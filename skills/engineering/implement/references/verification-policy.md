# Project-specific checks and TDD

The shared kit supplies the procedure. The project owns its commands, runtime setup and required evidence. Skill registration does not discover, install or replace a project's test/lint tooling.

## Configure once, update with the project

During setup, read project instructions, package/task scripts, CI configuration, runtime versions and existing verification wrappers. Resolve conflicting declarations with the project owner or update a stale configuration when the source of truth is clear. Preserve required checks; never remove a check just because it fails.

Record optional named commands in checks and the ordered final sequence in verification inside the project's .agent-workflow.json. Existing schema-version-1 files without checks still work. Project setup creates an empty catalog; an agent fills it from real project scripts. Initialization refuses to overwrite existing configuration, so refresh the relevant fields with targeted edits instead of rerunning init destructively.

Illustrative fragment for a project that actually defines these scripts:

```json
{
  "checks": {
    "types": ["npm", "run", "types"],
    "lint": ["npm", "run", "lint"],
    "deadcode": ["npm", "run", "deadcode"],
    "test": ["npm", "test", "--", "--runInBand"]
  },
  "verification": [["npm", "run", "verify"]]
}
```

Names are project-defined labels, not mandatory categories. Each value is a command argument array. A project may use types, typecheck, test-unit or test-integration; use its existing names/conventions. Do not copy example scripts or add a dead-code tool unless that work is requested and fits the project. Omit unavailable optional checks and record gaps where they matter.

Commands run from the project root. Use the project's wrapper for runtime selection, environment setup, workspace filters or commands needing another working directory. Keep shell logic in that maintained script, not an invented string for a shell to interpret. Secrets belong in the existing environment mechanism, not this JSON. Format-fixing commands may change files; preserve their intended order before final verification.

The optional helper validates the catalog's shape and includes it in implementation context. The coding agent executes applicable checks; the helper does not run them, select test files automatically or prove a listed command exists. Project instructions still govern additional conditional checks, such as builds, migrations or runtime QA.

## Focused TDD versus final verification

1. Read the selected issue and the relevant public behavior/test boundaries.
2. Start from the project's test command and use that runner's supported target/filter syntax to run a meaningful test for this behavior. Put the exact focused command and any required setup in the issue's Verification section; do not assume all runners accept the same flags.
3. Confirm RED fails because the behavior is missing or wrong. A missing dependency, invalid flag or broken fixture is not the intended regression.
4. Implement the behavior, run the same focused test to GREEN, then refactor with that feedback loop intact. Add the next behavior one at a time where test-first work is appropriate.
5. Broaden to affected tests and run the project's required final verification sequence before reporting success. Do not rerun every expensive check after each small red/green edit unless the task or project requires it.

A focused pass does not replace required final checks. Final checks do not replace a reproducer or human/runtime checks. Keep commands, observed outcomes, revision and anything not run in the task/result evidence. Do not weaken acceptance when an environment prevents a check; explain the remaining gap.

## Change and maintenance

When a script is renamed or a runner changes, update its project script, configuration references and command documentation/CI where applicable. Future prompts read the latest project configuration; no shared-skill edit or reinstallation is needed. If a command changes during an active agent session, explicitly reload the configuration before the next check or handoff.

Tasks may add scoped checks but must not silently override project-required verification. Avoid copying every root command into each issue: reference the project catalog and record the exact extra test/target needed for that issue. For monorepos, root wrappers or package-manager filters can expose commands for each relevant package without creating a separate shared skill per package.
