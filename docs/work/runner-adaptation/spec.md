# Reliable once and bounded-loop adaptation

Status: proposed execution design. R1 local preflight is implemented. A local-checkout subset of R9 is now implemented; Docker/worker lifecycle and the remaining runner requirements are still proposed. Source findings and rationale are in the [assessment](assessment.md). Existing task/status contracts remain authoritative until a versioned migration is implemented and tested.

## Outcome and scope

Run one eligible implementation task, or a bounded series, with the same portable records across Claude Code/Codex and host/isolated environments. Preserve interactive skill use and standard skill installation independently of runner tooling. Keep the Python core standard-library only. Sandcastle may become an optional backend if a concrete capability warrants it; its prompts, runtime and GitHub policies are not mandatory dependencies.

No automatic merge, unrestricted publishing, new executor names, global installation or provider/account configuration is implied. A runtime pilot and paid/live worker execution need task authorization. GitHub skill distribution is a separate capability, now implemented through directly installable canonical skills (replacing PR #2’s generated distribution); this design does not replace it.

## Requirements

- **R1 — Eligibility:** Inspect one explicit local issues directory, validate duplicate ids, unknown dependencies and cycles across the whole graph, then choose only ready AFK tasks whose blockers are done. Default order is filename order, not inferred importance. Return eligible work and exclusion reasons. Waiting, empty scope and records already complete are distinct. Invalid graphs are errors. Re-read immediately before a claim; a preview is not a reservation.
- **R2 — Claims and recovery:** A managed run acquires an exclusive project/worktree lease and a task claim before source edits. Persist run id, task digest, workspace/revision, runtime, phase and timestamps without copying the environment. A crash leaves recoverable evidence; stale claims are never cleared merely because a timeout elapsed. Recovery checks ownership and active processes before release. Direct dispatch and managed dispatch share the lock boundary so they cannot accidentally compete.
- **R3 — Once:** Preview by default. With explicit execution, validate config, tools, runtime and worktree policy, claim one eligible task, materialize its focused prompt/resources, invoke the selected adapter once, collect a portable report, run configured checks and persist the verdict. No task status change may precede a durable recovery record. Missing/malformed output stops in a diagnosable state; it never silently retries implementation.
- **R4 — Evidence and acceptance:** The supervisor validates task identity/digest, revision, criterion coverage, reported outcome, actual check results and pending judgments. Passing commands do not prove semantic correctness. Human-review tasks enter review until the human actually accepts them. Automated acceptance needs an agreed review/evidence policy; otherwise it also stops at review. Already-satisfied reports require evidence but no artificial commit. Worker output cannot directly close or complete tasks.
- **R5 — Bounded loop:** Loop calls the same once implementation with positive run-count, per-run timeout and total elapsed limits. Re-read authoritative state after every run. Stop with explicit reasons for failed execution, invalid report, unmet decision, exhausted limits, no eligible work or active claim. An unrelated HITL item need not block independent AFK work. A dependent of a review task remains waiting under the current contract. No automatic review bypass or dependency weakening.
- **R6 — Runtime boundary:** Host and Docker Sandbox use the same task, report and supervision contracts. Preflight verifies installed versions, workspace mapping, readable project-local skills, dependencies, command I/O and artifact export. Provider command flags stay in agent adapters; environment setup stays in runtime adapters. No implicit host fallback if isolation fails. Cleanup preserves failed work and requires ownership evidence before deleting resources.
- **R7 — Output repair:** Repair only a failed extraction/report step when the adapter can resume it safely. Cap attempts, preserve the original output and record every correction. Without safe session resumption, stop for inspection instead of replaying side effects. Do not pay for a second extraction call on output-only tasks unless the first output failed validation.
- **R8 — Delivery and tracker ownership:** Local task records remain the first backend. A later GitHub adapter paginates, distinguishes parent specs from executable tasks, reads native blockers and uses idempotent claims/updates. Publishing belongs to an authorized delivery operation, with remote revision checks and one completion owner. No worker credential-boundary claim without technical enforcement. Human merge remains governed by project policy.

- **R9 — Workspace lifecycle and disk reclamation:** Support the configurable central project/workspace layout, explicit runtime/checkouts, project hooks, ownership records, verified archival, resumable cleanup and scoped purging defined in [workspace lifecycle](workspaces.md). Keep original repositories safe. Show disk usage and cleanup previews; automatic reclamation requires a chosen retention policy and never overrides preservation checks.

## Proposed commands and records

Only `next` below exists today. The other commands are interface proposals, not executable instructions:

| Operation | Inputs | Result |
|---|---|---|
| `next ISSUES --project PROJECT` | Local task records/config | Read-only JSON snapshot; no launch, claim or status change |
| managed `once` | Explicit task or issues scope, executor, runtime, execution flag, time bound | One durable attempt with accepted/review/blocked/failed verdict |
| managed `loop` | Same scope/policy plus count and total duration bounds | Sequential once records and typed stop reason |
| recovery | Specific interrupted run and ownership evidence | Inspect, resume a safe phase or release a claim; no work replay by default |
| acceptance | Specific reviewed task, revision and acceptance evidence | Deliberate final transition by the authorized supervisor |

Keep provider output under ignored `.workflow-runs/`. A versioned portable report adds task id, task digest, revision, status claim, criterion evidence, check results and pending human checks to the existing result contract. The worker writes its report; the supervisor writes a separate evaluation so an agent claim is not mistaken for a verified verdict. Store task status once; run phase is history, not a competing task board.

Use atomic file replacement plus compare-and-swap against the claimed task digest for local transitions. Define ordering between task updates and journal writes, including recovery at each interruption point. The host runtime provides coordination, not isolation against a malicious worker with identical filesystem permissions.

## State and integration decision

Preserve `ready -> in-progress -> review -> done` and `blocked` for unresolved prerequisites. Execution failure belongs in the run record; recovery determines whether task work is resumable, blocked or eligible for a deliberate retry. Never automatically reset a task with partial edits to ready.

Under the current contract, only done unblocks dependents. For the first sequential release, finish review/acceptance before dependent work; loop may continue only independent ready tasks. If a project needs an entire feature implemented before human acceptance, a later version must explicitly represent verified integration separately, bind it to an available revision and invalidate it on regressions. Do not repurpose review or falsify human approval to achieve chaining.

Parallel execution is deferred until sequential claims, recovery and evidence work. It then requires distinct worktrees, conflict-aware scheduling, sequential integration and combined verification. Docker alone does not provide task acceptance or independent shared devices.

## Verification and rollout

Use fake executors and disposable fixtures for selection, contention, state changes during claim, crash points, timeouts, malformed/mismatched reports, failed verification, pending human review, no-commit success, budget exhaustion and unsafe retries. Fake runtime commands validate argv, mount/resource declarations, lifecycle and no-fallback behavior without credentials or Docker.

Authorize a real host pilot only after those pass. Authorize an isolated pilot separately after read-only version/availability checks identify the installed Docker profile. Evaluate correctness, resumed work, human correction burden and total accepted-result cost; do not claim superiority from architecture alone.

Each implementation task is in [issues](issues/01-preflight.md), with coverage and real blockers. These records are drafts for the remaining work, not authorization to launch external workers or provision accounts.
