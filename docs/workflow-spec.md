# Workflow specification — v0.1

## Outcome

Use one version-controlled kit across projects and agent tools. A user supplies an idea, document, ticket, message or meeting record. The workflow identifies the right amount of planning, resolves necessary decisions, produces bounded tasks, and connects changes to verification evidence.

## Requirements

1. Work in any folder with an agent capable of reading the kit and project files.
2. Preserve source references and distinguish requirements, suggestions, assumptions and decisions.
3. Route small work directly; do not require a PRD for every change.
4. Support research/prototypes when they resolve named uncertainties.
5. For multi-session work, produce a spec and vertical implementation tasks with dependencies.
6. Classify execution as HITL or AFK independently of human review.
7. Preserve task identity, decisions and acceptance criteria when changing agents.
8. Keep agent selection, model/effort, tracker and runtime as separate choices.
9. Use one authoritative task status per feature.
10. Evaluate completion through observable evidence, with human-only checks explicitly pending.
11. Load relevant instructions instead of assembling the whole kit into every prompt.
12. Preserve existing project constraints and action authorization.

## Initial implementation

The repository is named `agent-skills` (`MofasserHossain/agent-skills`). The optional router remains `agent-workflow`; existing `.agent-workflow.json` configuration and legacy `.agent-workflow` installations retain their names.

The optional execution helper supports Claude Code and Codex only; portable skill installation accepts any supported Skills CLI target. Discovery adapters and CLI selection cover those two; manual is a context-only mode with no process launch. Additional agents are deferred. Registry overrides may customize supported CLI profiles but cannot introduce another executor name.

Portable Markdown skills, shared references, templates, executor registry and an optional Python helper. The helper supports local initialization, task parsing/validation, narrow context generation, dependency checks, launch previews and explicit one-task CLI dispatch. Dispatch does not schedule work or mutate task status.

An optional registration tool previews or installs one thin native entry point for supported local agents. Choose personal scope across projects, or --project for one existing project. It points at this checkout rather than duplicating stage instructions; existing registrations and project rules are preserved. Project scope validates discovery paths within the target and deduplicates local directory aliases. A worked brief/PRD/issues example documents how artifacts connect. Multi-issue PRDs use stable requirement labels and task coverage references.

A focused architecture-assessment route identifies evidence-backed improvements before they become scoped tasks. The execution plan separates worker integration, final human acceptance and issue closure; Docker/Sandcastle scheduling remains a future backend, not an active dependency.

QA procedures feed reproducible defects back into the authoritative backlog and recheck integrated fixes; a follow-up issue does not erase a failed acceptance criterion. Review handoffs explicitly include applicable standards, while implementers pull supporting context as needed. The proposed runner separates judgment-based batch planning from deterministic eligibility enforcement; automatic replanning and role-specific prompt assembly remain planned.

An optional ui-design procedure connects audience/task research, interaction flows, states, prototypes and selected design decisions to the existing spec/task/QA contracts. It applies across web and native projects; product-specific constraints stay in the project. Frontend, full-stack and backend work use the same core workflow with conditional checks. Backend-only work skips UI design; a backend vertical slice does not require a screen. UI support is a Markdown procedure, not new runner automation.

Project configuration supports an optional named checks catalog alongside its ordered final verification list. Setup discovers existing project scripts and instructions; implementation uses runner-specific focused commands for TDD. The helper validates command arrays and passes current configuration as context, without running checks automatically. Existing schema-version-1 configurations without checks remain valid.

The legacy project installer copies selected skills and their linked runtime dependencies under .agent-workflow and creates relative Claude/Codex discovery entries. A first installation requires a selection; --select opens a terminal chooser with nothing preselected, --skills provides explicit names, and --all-skills explicitly selects every procedure; --with-runner adds the optional helper and its required implementation resources. The installed router lists only available stages. Authoring research, tests, examples, maintenance instructions and roadmap docs remain in the source kit. Updates preserve selection unless explicitly replaced; legacy full-copy installs can migrate without deleting local edits. It supports preview, idempotent installation and explicit updates of unedited managed snapshots; unrelated files and local customizations are preserved. Installed projects work without the source checkout and after relocation. Optional linked registration remains a development mode. Context cost is evaluated through progressive disclosure and actual host measurements, not inferred from disk size.

Local task metadata has a versioned contract. Provider-specific output stays in per-run artifacts; the portable report shape is independent of it.

Setup also supports adaptive project documentation: inspect and reuse existing sources, propose a concrete move map and flag conflicts before an existing-project rewrite, retain essential constraints plus phase/task reading routes, and audit every rule, link, symlink and command after relocation. New projects get minimal verified guidance with consequential unknown policies raised explicitly. Installation/skill updates do not overwrite project-owned context; setup refresh is deliberate. Root size is descriptive, not a token/cost measurement. The procedure adapts to native, frontend, backend and full-stack projects without mandatory guide scaffolding. This is implemented Markdown guidance, not automatic documentation migration tooling.

A portable pull-request procedure supports status/merge checks, preparation, creation/updates and post-merge sync through the current agent. Project-owned delivery guidance controls branch/commit conventions, checks and authority. Read-only status requests avoid implementation context and mutations; delivery actions require existing authorization. This is implemented skill guidance for Claude Code and Codex, not automated GitHub tracking, scheduling or merging.

The human skill guide provides entry-point selection, realistic invocation examples and outcome signals without duplicating canonical procedures. Discovery, specification, decomposition, implementation and review include explicit readiness checks: material decisions accounted for, acceptance traceable to requirements, complete coverage and acyclic blockers, already-satisfied behavior verified, and review verdicts bounded by actual evidence. These are implemented Markdown procedures; comparative behavioral effectiveness remains unmeasured until authorized pilots.

## Later milestones

- Add other agent adapters only when requested; preserve the current Claude/Codex scope meanwhile.

- Pilot on one real feature and a small bug. Measure correctness, rework, review burden, latency and usage where available.
- Add authoritative state transitions, task claims and interrupted-run recovery before automated scheduling.
- Add bounded loop execution and validated output extraction. Exit-code success alone cannot complete a task.
- Add a GitHub tracker adapter and deliberate local-to-GitHub publication.
- Add Docker Sandbox runtime provisioning with explicit workspace/credential/network boundaries.
- Evaluate parallel execution only after sequential runs work reliably.

## Acceptance for v0.1

- Existing project instructions are preserved by initialization.
- A task can produce the same core context for different executors.
- HITL, blocked and unmet-dependency tasks cannot be dispatched as AFK implementation.
- A failed, missing or timed-out executor returns failure rather than acceptance.
- Run artifacts avoid copying the entire environment.
- No provider SDK or paid model call is necessary to test the helper.
- Skills and references validate with no dangling internal links.
- Native registration previews without writes, supports personal/project scope, refuses conflicting skills and project-directory escapes, and is idempotent for an identical registration.
- Installed project snapshots preserve internal references, survive source unavailability/project relocation, and refuse updates over local edits.
- Implemented capabilities and planned capabilities are distinguished in documentation.

## Decisions still requiring a pilot

Which default effort is cost-effective for each task class; provider CLI compatibility on the user's machine; how much context each phase needs; GitHub publication and closure semantics; isolation/runtime configuration. No universal token threshold is assumed.

## Direct skill installation

The canonical skills/ folders are also the installation input for GitHub shorthand and local Skills CLI use. The router has the uniform name agent-workflow. Each skill owns its supporting references/templates; local links never leave that folder. Cross-skill collaboration uses installed names and explicit missing-guidance fallbacks, without automatically installing the full catalog. Task/result conventions keep one owner instead of copied package resources.

No generated package tree, distribution build or link rewriting is required. workflow.py check validates per-skill boundaries, metadata and source links; relocation tests exercise copied folders with the source unavailable. The project-local wrapper delegates agent paths to the pinned Skills CLI. Installed skills do not include Python runners. Legacy snapshot/registration tools remain deliberately supported; old workflow router selections map to agent-workflow during a supervised update. Existing project installations are not migrated automatically.

## Procedure quality across the catalog

All seventeen skills include stage-specific safeguards and completion signals. Routing checks current evidence before resumption and propagates scope changes. Setup separates inspected commands from exercised checks. Intake preserves recoverable source pointers and searches for duplicates. Research bounds investigation by a decision and checks source applicability. Prototypes define observations and return supported, rejected or inconclusive verdicts. UI design checks relevant content/state boundaries and outstanding contract assumptions. Architecture recommendations compare demonstrated change burden against smaller alternatives. QA derives expectations from requirements, separates environment failures and retains recheck history. PR delivery checks remote state before retrying mutations and ties evidence to revisions. Retrospectives put corrections in the owning source and define a falsifiable evaluation case. These complement the discovery, specification, task, implementation and review readiness checks above.

These are portable procedural improvements, not new helper automation or evidence that live agents obey them. The catalog evaluation cases remain authoring inputs; execution quality needs authorized pilots.

The project-local Bash installer accepts explicit Claude Code, Codex or both via --agent/-a while retaining both as its default. It rejects missing host values and delegates supported-target validation to the Skills CLI, independently of selected skills. Fake CLI tests cover argument forwarding and invalid targets; this does not configure provider accounts or install another agent.

Portable skills now support other Skills CLI agent targets through --agent, with provider-specific discovery paths delegated to that CLI. Agents outside its integrations can read an exported skill folder directly. This expands skill distribution, not helper dispatch: the executor registry still supports Claude Code/Codex and manual remains context-only. Fake CLI tests cover forwarding additional and multiple targets without installing or calling external agents.

## Runner adaptation preflight

The optional helper now provides `next ISSUES --project PROJECT`: a read-only local selector in stable filename order. It validates the whole scoped graph for unknown blockers, duplicate identities, cycles and escaped paths, and reports eligible candidates plus reasons for waiting. Empty scope, waiting work and records already marked done are distinct. Direct task dispatch uses the same graph validation. No claims, launch, status updates or semantic acceptance are inferred. GitHub-owned tasks remain unsupported by this local helper.

The [runner adaptation assessment](work/runner-adaptation/assessment.md) compares a pinned Matt runner revision and current Docker documentation. Its linked specification and draft tasks define proposed claims/recovery, managed once, bounded loop, runtime and output-repair contracts. Those execution capabilities remain planned; preflight does not implement a scheduler or provision Docker.

Workspace lifecycle and storage reclamation are specified in the [runner workspace design](work/runner-adaptation/workspaces.md). A standalone local-checkout foundation now implements previewed creation, listing with logical disk sizes, verified clean-checkout archival, explicit purge and restoration. Docker execution, worker management, hooks and automated retention remain planned. A configurable central root holds independent project/workspace identities. Verified recovery artifacts live outside disposable checkouts/volumes. Archive and purge are distinct; cleanup previews, owned-resource checks, pinned workspaces and explicitly configured retention protect original repositories and unpreserved work.


The workspace helper lives in tools/workspaces.py and is not shipped with skills. It creates independent clones without a push remote, requires an explicit committed-only selection for dirty source checkouts, protects the original repository, and uses operation locks. This first archive format accepts only clean committed files, refusing untracked/ignored changes, submodules, detached HEAD and unreferenced commits rather than discarding them. A checksummed Git bundle is restored and compared before archive succeeds; purge retains that archive and rechecks current refs/files. No setup hooks or worker processes are started, and callers must stop external processes before manual archival/purge. It supplies no Docker isolation by itself.

The source-only migration removes generated skill copies and moves shared authoring resources to their owning skills. It changes installation layout, not the executor/runtime scope or task acceptance rules. The same relocation and helper tests remain required.

PR creation now discovers required commands from the target repository rather than prescribing a package manager. It stops delivery on a failed required check, presents commits/diff statistics plus the proposed title/body, and waits for approval of that result. Project title/templates take precedence; defaults are a Conventional Commit title under 70 characters and a short Summary/Changes/Verification body with Notes only when needed. Read-only PR status checks remain separate.

Conventional Commit defaults now allow a useful optional scope, apply to new branch subjects when no project convention exists, and prepare the PR title for a project-selected squash merge. PR numbers belong to the resulting history entry, not the PR title. Merge method/settings and signature verification remain separate from title formatting; this guidance does not merge PRs or configure signing.

PR descriptions use small visuals only where they clarify the change, revision-specific execution evidence and observed before/after results where available. Missing baselines and unperformed checks stay explicit. Material risk notes identify affected consumers or data, reversibility and recovery steps when relevant; routine changes need no risk section. Project templates still take precedence.

## Skill catalog organization

Canonical skills live in `skills/engineering/<name>/` and `skills/productivity/<name>/`; installed names are globally unique and independent of category. The catalog contains seventeen skills, including portable handoff and instruction writing. The PR skill is named `pr`; the legacy installer accepts `pull-request` as an alias. Source discovery rejects duplicate names and symlinked skill roots or categories. Each skill owns its relocatable resources and Codex `agents/openai.yaml` interface metadata. Metadata supplies display labels and a suggested invocation, while `SKILL.md` owns behavior. No generated distribution or mandatory invocation policy is introduced.

Workspace lifecycle and execution remain in `tools/`. Categorization does not add Docker provisioning, scheduling or an unattended task loop; those remain separate roadmap capabilities.
