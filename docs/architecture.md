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
| Executor | Read a portable prompt in project context; return output and exit status | Claude Code CLI and Codex CLI; manual prints context only |
| Model/effort | Native configuration within an executor | Advisory policy; no automatic flag translation |
| Tracker | Stable tasks, dependencies, evidence and one authoritative status | Local helper; GitHub through available agent tools |
| Runtime | Workspace and tools with explicit resource boundaries | Host dispatch; Docker adapter planned |
| Intake source | Read supplied material with provenance | Text/file inputs; connected tools when available |

Only Claude Code and Codex are supported now. Registry overrides customize their CLI argument arrays; other executor names are rejected. The core interface remains portable so additional adapters can be introduced later when requested. Model and effort remain in native configuration.

Do not assume equivalent effort labels or capabilities across providers. Capability and permission limitations must be surfaced before dependent work.

## Control ownership

For v0.1, task status is edited deliberately by the human or supervising agent. The dispatch helper records process outcome but never closes an issue or marks a task complete.

Before scheduling is added, orchestration must own claims, status transitions, pushes and tracker mutations. Executor results are claims to validate. Project policy remains authoritative for commits, PRs, merge and deployment.

## Installation versus execution

The kit is authored separately, but its skills/ folders are directly installable with the standard Skills CLI. A resource has one owning skill and all filesystem links remain inside that folder. Shared procedures are named collaborators and are not automatically installed. No generated package tree, link rewriting or build/runner code is installed. Legacy snapshots/source-linked development mode remain supported deliberately. Project rules and work records stay local. Sandbox workspaces must contain readable skill folders; host-only symlinks do not provision resources.

Standard installation registers each selected skill with its own concise discovery metadata. Its body/resources load as needed; no whole-kit router is mandatory. Legacy snapshot registration uses one thin router entry instead. Discovery directories are host-specific adapter data; the procedures and work records remain neutral. Registration is an explicit operation separate from project setup and executor dispatch.

Keep the runtime independent of agent choice: moving from Claude to Codex should not require changing task records or rewriting Docker policy.

The standalone tools/workspaces.py helper owns independent local checkout records and verified Git archive generations outside disposable checkout directories. It is not a runtime/agent supervisor and is not bundled with skills. See [workspace commands and limits](workspaces.md).
