# Adaptive project context

Use this method for frontend, backend, native, and full-stack repositories. The method is shared; product knowledge and policy stay in the target project. Do not require this authoring checkout at runtime.

## Inspect before proposing

Read existing root instructions, symlinks, documentation maps, product/architecture guides, task procedures, configuration, command scripts and CI. Inspect the working tree; preserve unrelated and pre-existing edits. Identify authoritative sources and mandatory rules embedded in descriptions, not just headings. Reuse suitable documents and their layout; create only guides the actual material warrants. Do not scaffold empty glossaries, ADRs or a fixed documentation tree.

Distinguish three operations: installing/updating selected skills, initial project setup, and an explicitly requested setup refresh. Installation is not permission to rewrite project-owned docs. Skill updates preserve those docs; reconcile customizations deliberately. Setup does not select, reinstall or migrate skills unless separately requested.

## Propose existing-project changes

Before rewriting root instructions, show a concrete section/rule-to-destination move map, conditional reading triggers, and genuine policy conflicts. Include rules embedded in feature descriptions and conditional verification obligations. Obtain approval for that proposal; do not repeat intake or approval when the current authorization already covers it. Materially different changes need a revised proposal. Flag contradictory rules instead of choosing new policy. For a new project without guidance, create minimal instructions from verified facts and ask about consequential unknown policies rather than inventing them.

## Write essential instructions and explicit routes

Keep project identity/scope, consequential feasibility and safety constraints, authorization boundaries, essential commands, and the reading map in the root. Retain a discoverable summary of high-impact restrictions there and require the applicable detail for affected work. Concision is an editorial aim, not a line quota that permits losing rules.

Route by both phase and task, with exact repository-relative paths and conditions. Do not rely on automatic nested AGENTS discovery. Do not move everything into one guide that must still be read on every task. Read relevant sections rather than all guides upfront:

- Intake/PRD: relevant product/work records and constraints; architecture when existing behavior or feasibility affects scope.
- UI research/design/prototypes/code: applicable UI and asset guidance in any phase; backend-only work skips it.
- Implementation planning: relevant architecture, development constraints, maintenance and verification strategy.
- Code/content/config changes: applicable development and maintenance rules, plus relevant feature sections; UI/copy guidance when affected.
- Testing/behavior changes: verification guidance and behavior requirements.
- Dependencies/runtime/native/security/privacy: applicable dedicated rules and conditional checks.
- Final review/QA: acceptance criteria, changed-area guides, verification and human checks.
- Commit/PR/release: existing task procedures, authorization rules and delivery/release checks.

Adapt these triggers to actual project obligations; they are not a mandatory list of new guides. Keep task procedures in selected skills instead of duplicating them into project guides. Keep command selection in project configuration and implementations in existing scripts/wrappers; preserve exact focused, final, bundle/native and device conditions where present. Preserve AGENTS/CLAUDE single-source arrangements, including symlinks.

Use native skill discovery instead of embedding a skill catalog, skill bodies, or reference contents in root instructions. Where AGENTS.md owns shared project rules and a separate CLAUDE.md is needed, keep CLAUDE.md to a pointer to those rules plus essential Claude-specific exceptions; do not duplicate AGENTS.md. A pointer does not reduce context if it requires reading the same large document on every task. Keep shared root rules focused too, and route conditional detail by task. Do not create an extra root file when the existing arrangement already works.

Keep skill descriptions short and specific enough for selection. Load the selected skill body when used and its supporting files only for applicable conditions; do not instruct the agent to preload every skill or reference. Preserve automatic discovery by default. Explicit-only invocation is a host-local preference when requested, not a mandatory policy added to portable skills.

## Audit and report

Keep a temporary original snapshot during editing, not a second long-term authoritative copy. Account for every substantive rule and its final destination, including embedded requirements. Consolidate only equivalent duplicates; retain the distinction between examples, descriptions and mandatory rules. Repair relative links and references such as “this file” after relocation. Check destination documents for contradictions before consolidating.

Verify coverage, reading triggers, relative links/anchors, symlinks, and command names/arguments against scripts, wrappers and configuration. Walk representative planning, UI, service/backend, verification and delivery tasks through the map. Run the target project's applicable checks. Report changes, checks, unresolved conflicts and remaining human checks. Root line/word/byte counts describe size only; do not equate them with tokens or claim measured model cost savings without host measurements.

For prompt-only changes, use scenario review rather than tests that merely restate prose. Review at least: an existing native app with shared-device/native checks; a small backend without UI docs; a new project with unknown policy; and an existing custom documentation layout. Verify the resulting procedure preserves project rules, avoids unnecessary scaffolding and remains usable after skill relocation.
