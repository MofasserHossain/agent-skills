# Architecture

```text
Sources -> intake -> resolved decisions -> spec -> tasks -> verified result
                                  |                     |
                            project rules          selected executor
                                                        |
                                                 selected environment
```

## Stable core

Skills describe outcomes and procedures in Markdown. Project configuration declares local commands and constraints. Tasks carry identity, source references, acceptance criteria, execution mode and dependencies. These remain unchanged when an executor changes.

The agent's proprietary session history is optional context, never the only record of a decision or result.

## Replaceable edges

| Edge | Contract | Initial support |
|---|---|---|
| Executor | Read a portable prompt in project context; return output and exit status | Manual, Claude Code CLI, Codex CLI, custom command arrays |
| Model/effort | Native configuration within an executor | Advisory policy; no automatic flag translation |
| Tracker | Stable tasks, dependencies, evidence and one authoritative status | Local helper; GitHub through available agent tools |
| Runtime | Workspace and tools with explicit resource boundaries | Host dispatch; Docker adapter planned |
| Intake source | Read supplied material with provenance | Text/file inputs; connected tools when available |

A custom executor needs no change to the core: add a registry entry with a command array that accepts the full prompt on stdin. SDK or HTTP agents can implement a small wrapper exposing that interface. Model and effort can be selected in that wrapper or native configuration.

Do not assume equivalent effort labels or capabilities across providers. Capability and permission limitations must be surfaced before dependent work.

## Control ownership

For v0.1, task status is edited deliberately by the human or supervising agent. The dispatch helper records process outcome but never closes an issue or marks a task complete.

Before scheduling is added, orchestration must own claims, status transitions, pushes and tracker mutations. Executor results are claims to validate. Project policy remains authoritative for commits, PRs, merge and deployment.

## Installation versus execution

The kit checkout is shared. Each project owns its configuration and work records. A sandbox must receive a readable kit installation or the selected instructions and references explicitly; host symlinks outside the mounted workspace are not assumed to work.

Keep the runtime independent of agent choice: moving from Claude to Codex should not require changing task records or rewriting Docker policy.
