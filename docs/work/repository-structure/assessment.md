# Repository structure assessment

Historical assessment: the package-builder coupling described below was resolved by the direct-install skill migration. Canonical skill folders now contain their resources; no package builder or generated installation tree remains. The original findings and verification below describe the earlier revision.


Date: 2026-11-01

Scope: skill packaging, legacy installation boundaries, documentation, and using this repository's own skills to maintain it. This is an assessment, not authorization for the proposed refactors. No implementation backlog or tracker migration is introduced here.

## Intent and settled decisions

The user clarified that the pilot should improve this agent-workflow repository itself. Success means accepted changes with less clarification and rework. Preserve the provider-neutral core, Claude Code/Codex support, selected self-contained skill packages, standard project-local installation, and deliberately supported legacy installations.

## Current structure

Keep the top-level layout. `skills/` contains procedures, `references/` shared policies, `templates/` artifact shapes, `adapters/` host data, `scripts/` the installation wrapper, `tools/` Python helpers, and `tests/` their behavioral checks. `docs/`, `examples/`, and `checks/` have distinct explanatory, illustrative, and evaluation roles. The inspected code does not establish a need for a new package hierarchy, framework, dependency, or wholesale folder move.

## Recommended first change: clarify how maintainers work here

Evidence:

- README.md and docs/installation.md identify standard Skills CLI packages as the primary installation route.
- docs/folder-map.md's “Native use versus automation” section instead opens with one thin router entry and describes the legacy `--skills`/`--with-runner` snapshot layout before qualifying it at the end. Its `tools/` row also omits the now-primary maintainer packaging responsibility.
- docs/prompt-map.md starts with standard installation guidance but later says “Prefer tools/install_project.py for independent project snapshots” without explicitly limiting that recommendation to legacy use. Its statement that stages are not automatically individual slash commands also needs clearer source/legacy scope beside the standard independently discoverable packages.
- docs/prompt-map.md and docs/folder-map.md explain stage selection, but the README does not give a concrete starting example for invoking canonical source skills to maintain this repository.
- references/trackers.md already defines `docs/work/<feature>/` for local work. A second system for this repository is unnecessary. Historical conversation summaries and fictional examples serve different purposes from active work records.

Proposed direction: update the existing authoritative guides, making standard installation primary and labeling legacy/source-linked modes clearly. Add a short README example that references a canonical SKILL.md and keeps actual kit-improvement records under `docs/work/`. Link existing detail rather than creating another architecture manual. This assessment is the first such record for this effort.

Expected benefit: a maintainer can distinguish editing the skill sources, using them in this repo, and exporting them to another project without reconstructing the historical conversation.

Acceptance:

- The README gives an actionable source-skill invocation example for this repository.
- The folder map consistently distinguishes canonical source, generated packages, standard installed files, and supported legacy modes.
- Actual work records are distinguished from templates, examples, and historical summaries.
- No install command, CLI behavior, exported resource boundary, or existing project installation changes.

Verification: inspect the revised reading path and local links; run the required unit tests and kit check. If exported source resources change, rebuild packages and run the package check. No real Skills CLI installation, provider call, or external project mutation is needed.

Risk: adding more overlapping documentation. Keep the README entry short and edit existing explanations in place.

## Optional later change: give shared file operations a neutral home

Evidence: tools/package_skills.py imports `InstallError`, `LEGAL_FILES`, `LINK`, `apply`, and `inspect` from tools/install_project.py. The latter also imports register_skills and contains legacy selection, router generation, and host-entry logic. Thus the standard package builder has a transitive Python import dependency on legacy host registration, although it does not invoke that registration during a build.

The shared operations are meaningful: inventory/hashes, ownership markers, edit detection, staging, rechecks, and rollback on replacement failure. Reusing them avoids duplicating protections. No observed failure establishes that this dependency currently breaks packaging.

Proposed direction, if selected: extract cohesive managed-directory operations into a small module under tools/, consumed by both existing callers. Decide separately whether resource constants belong there; a generic utilities grab bag would obscure the boundary. Preserve script entry points, exception compatibility, ownership-marker format, local-edit protection, and generated file bytes.

Expected benefit: maintain packaging without importing legacy selection/discovery code. Benefit is maintainability, not a demonstrated performance or correctness fix.

Verification: existing packaging and legacy installer behavioral tests must still pass, including relocation, symlink rejection, local-edit refusal, and idempotence. Compare generated payload paths/bytes before and after; rebuild and check packages. Add tests only for a concrete uncovered behavior.

Risk: moving mutation code can weaken protections or break imports and legacy users. Do not combine this extraction with marker changes, legacy removal, a new Python distribution, or runner redesign.

## How to use the existing skills

Use canonical source files directly in a request; no self-installation is required for an agent that can read this checkout. Start with `skills/improve-codebase-architecture/SKILL.md` for assessment. Use `grill` only for consequential unresolved choices; a small documentation correction can go directly through `implement` and `review`. Use `write-spec` and `plan-tasks` when the selected scope needs a durable multi-task handoff. Use `retro` after delivery to record observed friction, not hypothetical improvements.

## Decision and next action

Recommendation: deliver the documentation alignment as the first bounded pilot. Defer the shared-code extraction until selected; keep all other folders and execution infrastructure unchanged. No material product decision blocks the documentation correction. Review the pilot by whether a fresh session can identify the source skill, current work record, installation route, and required checks without revisiting the conversation summary. Report any remaining ambiguity or rework; no reduction has been measured yet.

## Documentation pilot result — 2026-11-01

Status claim: implemented after the user authorized the documentation change. The recommendation above records the original assessment; this section records its delivery.

- README.md now provides a canonical source-skill invocation example and a short implement/check/review route for kit maintenance.
- docs/folder-map.md identifies generated packages, maintainer tooling, actual work records and historical summaries. Standard installation is primary; snapshot and source-linked registration are explicitly scoped as legacy/development modes.
- docs/prompt-map.md distinguishes source-file use from installed skill discovery and removes the unqualified preference for the legacy installer.
- The bounded review covered these three documentation edits against this assessment and AGENTS.md. No further findings remained. Existing installation instructions and code behavior were preserved; no exported sources changed, so no rebuild was needed.

Verification passed: `python3 -m unittest discover -s tests -v` (70 tests), `python3 tools/workflow.py check` (14 skills and local Markdown links), `python3 tools/package_skills.py --check` (14 packages, 34 files, unchanged), `bash -n scripts/install-skills.sh`, and `git diff --check`.

No blockers. Human feedback on whether the revised starting instructions are clear remains unmeasured; automated checks do not establish reduced clarification or rework. No live provider run or installation was needed. Usage and total elapsed time were not measured. The optional shared-code extraction remains deferred.
