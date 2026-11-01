# Agent Workflow: Historical Decisions

Date: 2026-11-01 (Asia/Dhaka)

This condensed record preserves the reasons behind the initial workflow design. It is historical background, not session instructions or an installation/status guide. Current behavior belongs in the [README](../../README.md), [workflow specification](../workflow-spec.md), and [installation guide](../installation.md). Subsequent kit-improvement decisions and evidence belong under `docs/work/<feature>/`.

## Decisions and reasons

- **One maintained kit, independent project selections.** Maintain canonical skills and shared resources in this repository. Projects need only their selected procedures and supporting resources, not the kit's research, tests, examples or authoring tools.
- **Standard installation replaced broad snapshots.** Early installation copied too much of the source kit. The design evolved through selected runtime snapshots to standard Skills CLI packages. Each package carries its own required resources; optional sibling skills do not become filesystem dependencies. The router is optional. Legacy snapshots require deliberate migration because projects may have local edits and different selections.
- **Procedures and execution are separate.** Markdown skills already supply reusable instructions. Installation makes them discoverable; it does not create a scheduler or sandbox. Additional runner prompts are justified by concrete automation contracts, rather than duplicating every skill. Python serves maintainer tooling and optional dispatch; a Bash wrapper provides the standard installation entry point.
- **Keep the core provider-neutral.** Claude Code and Codex were the selected agents. Manual mode prepares context without launching an agent. Task identity, requirements, decisions and results must survive a change of executor or model.
- **Projects own their context.** Product rules, platform constraints, verification commands, tracker choice and actual work records belong in the project being changed. Shared UI guidance applies to web and native work; backend-only tasks skip it. A renamed project test command should not require reinstalling shared skills.
- **Use only the stages the work needs.** Clear small changes can go directly to implementation and proportionate verification. Larger work benefits from settled decisions, specifications and vertical tasks with requirement coverage. Thin observable outcomes expose integration problems early; a backend slice does not require a screen.
- **Preserve decisions instead of relying on chat history.** Fresh sessions need durable handoffs, not the full conversation. One tracker owns task status. Moving trackers requires an explicit authority switch and preserved identity mapping.
- **Execution autonomy and acceptance are independent.** An AFK task can still require human review. Process success, a commit or an agent's completion claim does not establish acceptance or authorize delivery actions. Future scheduling must distinguish verified integration from final human acceptance rather than marking human review complete to release dependencies.
- **Verification follows behavior.** Meaningful test-first work checks observable outcomes; trivial edits and prototypes receive proportionate checks. QA findings return to the authoritative backlog without erasing failed acceptance criteria. Required device or human checks remain explicit.
- **Add infrastructure from evidence.** Start with supervised bounded work before scheduling and isolated parallel execution. Branch names alone do not isolate files; parallel workers need separate working trees and serialized integration. Shared devices need explicit coordination. A dedicated Wayfinder system was deferred; uncertain long efforts can use a lightweight decision map in the grill procedure.
- **Measure accepted outcomes.** Reduce clarification, rework and wasted context through relevant instructions and complete handoffs. Discovery metadata is not the cost of all skill bodies. Model-effort labels are not assumed equivalent across providers, and no universal token savings were established.

## Sources and continuing work

Matt Pocock's public skills, workshop and runner repositories informed the design. They showed several installation/execution patterns, not proof of a single private workspace arrangement. Source evidence and limitations are kept in the [research index](../research/sources.md) and [workshop comparison](../research/workshop-comparison.md).

Use the [prompt map](../prompt-map.md) for stage use, [context-cost guide](../context-cost.md) for measurement limits, and [execution plan](../execution-plan.md) for proposed orchestration. Those documents hold the detail; this record does not duplicate their commands, capability inventories, validation counts or roadmap status.
