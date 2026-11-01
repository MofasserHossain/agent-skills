# Execution policy

Separate execution mode (HITL/AFK), review requirement, executor, model/effort, tracker and runtime.

An AFK implementation task is eligible only when it is ready, dependencies are done, required tools are available, and unresolved decisions cannot change its scope. A ready task still obeys project action permissions.

The v0.1 helper dispatches one explicitly selected local task on the host. It previews by default; --execute starts a process. It cannot sandbox a process, enforce the semantic correctness of a model response, or schedule/claim tasks. Avoid concurrent dispatch to the same working tree; scheduling/locks are a later milestone.

Automated sequential/parallel scheduling and Docker/Sandcastle integration remain planned in the authoring kit. Integrating a worker branch is separate from final acceptance and PR merge; follow project policy. Do not mark required human review complete merely to release dependent work.

A process exit of zero means transport completion, not acceptance. The executor must produce the report in result-contract.md. A supervising human/agent checks evidence and updates task status.

If clarification is required, record the question and its consequence. Continue independent authorized work if useful; never substitute a guessed human answer.

Bound retries and duration. An interrupted CLI may leave partial source edits; inspect its diff and run artifacts before resuming. Before adding external side effects, specify ownership and idempotency. A retry of output extraction must not repeat completed commits or tracker writes.
