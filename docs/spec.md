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

Portable Markdown skills, shared references, templates, executor registry and an optional Python helper. The helper supports local initialization, task parsing/validation, narrow context generation, dependency checks, launch previews and explicit one-task CLI dispatch. Dispatch does not schedule work or mutate task status.

Local task metadata has a versioned contract. Provider-specific output stays in per-run artifacts; the portable report shape is independent of it.

## Later milestones

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
- Implemented capabilities and planned capabilities are distinguished in documentation.

## Decisions still requiring a pilot

Which default effort is cost-effective for each task class; provider CLI compatibility on the user's machine; how much context each phase needs; GitHub publication and closure semantics; isolation/runtime configuration. No universal token threshold is assumed.
