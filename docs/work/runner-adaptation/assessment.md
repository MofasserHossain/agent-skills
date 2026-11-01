# Matt runner adaptation assessment

Checked 2026-11-01 (Asia/Dhaka). This is a source review, not a live execution benchmark. No agent, Docker environment, credential setup or GitHub automation was started. The earlier [workflow audit](../../research/matt-pocock-audit.md) covers the wider skill system; this assessment focuses on execution.

## Source revision

Course Video Manager was checked at `c76ad7e626cbc0a47c12818c6fcab4897d0f2038`. The files below were read at that revision, not inferred from README claims.

| Source | What it actually does | Adaptation |
|---|---|---|
| [once.sh](https://github.com/mattpocock/course-video-manager/blob/c76ad7e626cbc0a47c12818c6fcab4897d0f2038/plans/backlog/once.sh) | Supplies open issues and recent RALPH commits to one Claude Docker Sandbox session | One worker per bounded task; select scope outside the agent |
| [afk.sh](https://github.com/mattpocock/course-video-manager/blob/c76ad7e626cbc0a47c12818c6fcab4897d0f2038/plans/backlog/afk.sh) | Repeats sessions up to an iteration count and stops on an assistant completion marker | Bounded loop over one shared once implementation; typed stop reasons |
| [backlog prompt](https://github.com/mattpocock/course-video-manager/blob/c76ad7e626cbc0a47c12818c6fcab4897d0f2038/plans/backlog/prompt.md) | Agent chooses one issue, implements, commits and closes/comments on it | Preserve focused implementation; project policy owns commits and publication, supervisor owns acceptance |
| [Sandcastle entry point](https://github.com/mattpocock/course-video-manager/blob/c76ad7e626cbc0a47c12818c6fcab4897d0f2038/.sandcastle/main.ts) | Planner, up to four Docker workers with review, then an agent merger, across ten iterations | Separate selection, execution, review and integration; defer parallelism |
| [retry wrapper](https://github.com/mattpocock/course-video-manager/blob/c76ad7e626cbc0a47c12818c6fcab4897d0f2038/.sandcastle/run-with-retry.ts) | Repairs structured output in the same session with a capped attempt count | Repair output without replaying implementation or external actions |
| [extraction wrapper](https://github.com/mattpocock/course-video-manager/blob/c76ad7e626cbc0a47c12818c6fcab4897d0f2038/.sandcastle/run-with-extraction.ts) | Separates side-effecting work from resumable result extraction | Portable report first; provider-specific session resumption stays in adapters |
| [AFK platform spec](https://github.com/mattpocock/course-video-manager/blob/c76ad7e626cbc0a47c12818c6fcab4897d0f2038/docs/agents/afk-agent-platform-spec.md) | GitHub-native triggers, queue promotion, runner output contracts, review and human merge | Adopt ownership and recovery boundaries; keep local tasks usable without GitHub |

## Changes needed rather than literal copies

1. The [local planner](https://github.com/mattpocock/course-video-manager/blob/c76ad7e626cbc0a47c12818c6fcab4897d0f2038/.sandcastle/plan-prompt.md) explicitly falls back to a candidate when every issue is blocked. Our selector must return waiting, never weaken a dependency to keep running.
2. The [implementation prompt](https://github.com/mattpocock/course-video-manager/blob/c76ad7e626cbc0a47c12818c6fcab4897d0f2038/.sandcastle/implement-prompt.md) first requests issue closure, then forbids it. Our orchestrator must have one owner for tracker changes.
3. The local scripts send all returned issue bodies/comments and recent commits on every iteration. Our worker needs one selected task and relevant pointers; selection should not require an extra model call or the whole backlog in its prompt.
4. The local Sandcastle entry point uses commit presence to select branches for review/merging. A verified already-satisfied task may need no commit; commits also do not demonstrate acceptance.
5. The [single-issue runner](https://github.com/mattpocock/course-video-manager/blob/c76ad7e626cbc0a47c12818c6fcab4897d0f2038/.sandcastle/implement/implement.ts) uses `noSandbox()`. The `.sandcastle` directory name is not proof of Docker isolation. Its [workflow](https://github.com/mattpocock/course-video-manager/blob/c76ad7e626cbc0a47c12818c6fcab4897d0f2038/.github/workflows/agent-implement.yml) has a job-level GitHub token and includes a force push. The platform spec's control ownership is useful, but it does not establish a technically enforced credential boundary in that reference runner.
6. The loop's completion string is an agent claim. Our supervisor must account for task readiness, process outcome, report validity, required checks and human review separately.

These are identified design differences and source limitations, not benchmark evidence that our future runner performs better.

## Docker compatibility

The reference backlog uses `docker sandbox run`. Current Docker documentation describes `sbx run` and a CLI migration. A runtime adapter must probe the installed CLI/version and match a tested command profile; do not paste historical setup/authentication scripts into this kit. See [usage and migration guidance](https://docs.docker.com/ai/sandboxes/usage/), [Claude configuration](https://docs.docker.com/ai/sandboxes/agents/claude-code/) and [Codex configuration](https://docs.docker.com/ai/sandboxes/agents/codex/).

The agent pages document project-local configuration availability and startup defaults that bypass the agent's own approval/sandbox checks inside the outer sandbox. Therefore runtime selection is a real permission/environment choice, not just prefixing a host command. Provision the exported skills inside the workspace, resolve project-internal links, and define host access explicitly. Do not mount personal agent directories or credentials just to make a demo work.

Docker Sandbox microVMs, ordinary Docker containers and a disposable GitHub runner are different runtimes. An existing Codex conversation does not establish which one a newly dispatched worker will use.

## Repo coverage and next action

Implemented: portable skills, one-task host dispatch with timeout/artifacts, and a read-only `next` selector validating the complete local dependency graph. It separates ready, waiting, complete and empty; complete means existing records say done, not newly verified acceptance. Invalid graphs fail rather than selecting around them.

Not implemented: atomic claims, managed state transitions, structured acceptance evaluation, resumable once, bounded loop, runtime provisioning, GitHub tracker automation or parallel integration. See the [adaptation specification](spec.md) and its dependency-ordered [tasks](issues/01-preflight.md). Do not advertise `next` as an autonomous scheduler.

The subsequent workspace/storage requirement is tracked separately in [workspace lifecycle](workspaces.md) and [task 09](issues/09-workspace-lifecycle.md). It is a proposed capability, not a claim about Matt’s implementation.
