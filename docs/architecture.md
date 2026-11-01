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

The kit is authored separately. New projects install selected self-contained skill packages through the standard Skills CLI from tracked packages/skills; dist/skills is an optional ignored preview. A maintainer build rewrites local resource links and converts optional cross-skill references to names. No build/runner code is copied into standard installed skills. Legacy .agent-workflow snapshots and source-linked development mode remain supported for existing users. Each project owns its configuration and work records. A sandbox must receive a readable kit installation or the selected instructions and references explicitly; host symlinks outside the mounted workspace are not assumed to work.

Standard installation registers each selected skill with its own concise discovery metadata. Its body/resources load as needed; no whole-kit router is mandatory. Legacy snapshot registration uses one thin router entry instead. Discovery directories are host-specific adapter data; the procedures and work records remain neutral. Registration is an explicit operation separate from project setup and executor dispatch.

Keep the runtime independent of agent choice: moving from Claude to Codex should not require changing task records or rewriting Docker policy.

The standalone tools/workspaces.py helper owns independent local checkout records and verified Git archive generations outside disposable checkout directories. It is not a runtime/agent supervisor and is not bundled with skills. See [workspace commands and limits](workspaces.md).
