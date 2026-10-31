# Matt Pocock workflow source audit

Audit date: 2026-11-01 (Asia/Dhaka).

## Result

Docker isolation is explicitly present in course-video-manager. The setup is broader than the seven-stage diagram: reusable engineering skills, repository-specific instructions, multiple execution engines, dependency management, review automation, runtime validation, and feedback into the agent environment.

The earlier research missed plans/backlog and understated .sandcastle and the GitHub-native AFK platform. This audit corrects that omission.

## Scope and reproducibility

The complete file trees of both repositories were inventoried without API truncation:

- mattpocock/skills: commit 4ae2317ddb22b046e26455e4f9c9b3aaaf62212d, 184 file entries.
- mattpocock/course-video-manager: commit b47b1ec54cc7742326ca2682e49f09803cdac303, 2,602 file entries.

157 selected source files were retrieved: 72 from skills and 85 from course-video-manager. These include every SKILL.md in skills, relevant supporting templates, all agent workflow YAML files, local orchestration sources and prompts, backlog scripts, and the platform spec. Key sources were read directly and cross-checked through targeted searches.

This is a workflow source audit, not an audit of all application code. The executable workflows, Docker environments, live GitHub settings, credentials, and task outcomes were not tested. File presence establishes what the snapshot contains, not what Matt currently runs most frequently. No full video transcript was reviewed in this pass.

The original source manifest and retrieved files were cached at /tmp/matt-workflow-audit-2026-11-01 during the audit. That temporary cache is not bundled here; the pinned repository revisions and source links below provide the durable references.

## 1. Docker: the exact source locations

### A. Docker Sandbox backlog runner

[plans/backlog](https://github.com/mattpocock/course-video-manager/tree/b47b1ec54cc7742326ca2682e49f09803cdac303/plans/backlog) includes:

- Dockerfile: extends Docker's Claude Code sandbox template, upgrades the CLI, loads GitHub authentication for subprocesses, and wraps Claude to inject an OAuth token.
- common.sh: derives repository/sandbox names and checks prerequisites.
- setup.sh: builds/pushes the template and initializes the sandbox.
- once.sh: collects issues and recent RALPH commits, then starts one session.
- afk.sh: repeats bounded sessions, streams output, and recognizes a completion marker.
- cleanup.sh: removes the sandbox and local template image.
- prompt.md: task priority, exploration, implementation, commits, and issue outcomes.
- docker-sandbox-learnings.md: detailed failed approaches, authentication behavior, WSL2 issues, template setup and lessons.

The troubleshooting document is the clearest answer to the user's Docker question. Its CLI/version claims describe the environment in which the notes were written; they must be checked against current Docker documentation before implementation. In particular, its docker sandbox command syntax and token-injection workaround should not automatically become our new setup.

The snapshot's once/AFK scripts retrieve all returned open issue bodies/comments and recent commit messages. That is simple but can duplicate substantial context. The prompt does not explicitly filter HITL tasks, and gh issue list is not explicitly paginated. These are limitations to address if adapting it.

### B. Sandcastle Docker/worktree orchestration

[.sandcastle/main.ts](https://github.com/mattpocock/course-video-manager/blob/b47b1ec54cc7742326ca2682e49f09803cdac303/.sandcastle/main.ts) imports the Docker adapter from @ai-hero/sandcastle.

It runs:

1. A planner to select work using issue relationships.
2. Up to four implementation/review workers concurrently.
3. A merger for branches that produced commits.
4. Up to ten outer iterations.

[.sandcastle/Dockerfile](https://github.com/mattpocock/course-video-manager/blob/b47b1ec54cc7742326ca2682e49f09803cdac303/.sandcastle/Dockerfile) builds a Node-based environment with Git, GitHub CLI, pnpm and Claude Code. Its comments describe a worktree bind-mounted into the container. This is separate from plans/backlog's Docker Sandbox microVM setup.

The local runner is configured to reach a host test Postgres service through host.docker.internal. It is not a self-contained environment with no host connections.

The four accompanying role prompts are plan-prompt.md, implement-prompt.md, review-prompt.md, and merge-prompt.md. The package.json sandcastle script invokes this main.ts entry point.

### C. GitHub Actions execution

The agent-* workflow YAML files invoke .sandcastle subcommands. The implement, implement-prd, review, implement-pr, update-branch and related TypeScript runners use noSandbox() in this snapshot.

They execute on GitHub-hosted Ubuntu runners; they do not add the local Sandcastle Docker boundary. The directory name .sandcastle is not evidence that every run is containerized.

Adaptation: keep execution environment selectable. Distinguish host execution, a disposable CI machine, a regular container, and Docker Sandbox microVM isolation.

## 2. The reusable planning and implementation skills

[ask-matt](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/ask-matt/SKILL.md) is the main workflow map.

### Normal feature route

grill-with-docs -> optional prototype/research -> to-spec -> to-tickets -> implement or implement-spec -> code-review -> PR -> retro.

Important qualifications:

- Small work can go from grilling to implementation in the same session; specs and tickets are for multi-session work.
- grill-with-docs composes grilling with domain-modeling. It is not a standalone large interview prompt.
- The glossary defines domain language. ADRs record consequential tradeoffs sparingly.
- to-spec synthesizes resolved conversation rather than restarting the interview.
- to-tickets produces independently verifiable vertical slices with blockers. Wide mechanical refactors have an expand-contract exception.
- implement works one ticket; implement-spec orchestrates fresh implementers in separate worktrees against an integration branch.
- tdd works one behavior/test/implementation at a time at agreed public boundaries.
- code-review evaluates two separate axes: project standards and fidelity to the originating spec.
- prototype distinguishes UI questions from logic/state questions and retains the experiment as a source outside main.
- research produces cited primary-source findings.

### Other entry routes

- triage: incoming bugs/requests, verification, previous rejection checks, and durable agent briefs. Already-generated tickets do not need another triage pass.
- diagnosing-bugs: first build a narrow reproduction/check, then investigate hypotheses and validate the fix.
- to-questionnaire: prepare questions when required knowledge belongs to another person.
- wayfinder: multi-session planning for an effort too uncertain to resolve in one grilling conversation.

[wayfinder](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/wayfinder/SKILL.md) is especially relevant to the user's multi-phase planning question. It maintains a map of decision tickets, blocking edges, resolved decisions, unspecified areas, and scope. Research can be AFK; grilling and prototype judgment require HITL. Planning decisions are distinct from implementation deliverables. Once the map is resolved, it normally feeds to-spec and to-tickets.

### Maintenance and usability

- improve-codebase-architecture and codebase-design help make modules easier to understand and test.
- handoff creates a portable pointer-based continuation document.
- wizard supports procedures requiring genuine human access or action.
- retro improves navigation, tools, checks, standards and instruction quality based on observed failures.
- writing-for-agents describes information hierarchy, context pointers, progressive disclosure and pruning.
- pr helps package results for review.

These are separate capabilities, not mandatory steps for every request.

## 3. The GitHub-native AFK platform

[docs/agents/afk-agent-platform-spec.md](https://github.com/mattpocock/course-video-manager/blob/b47b1ec54cc7742326ca2682e49f09803cdac303/docs/agents/afk-agent-platform-spec.md) is the most comprehensive operational reference.

It describes eight workflows:

| Workflow | Purpose |
|---|---|
| To Issues | Convert a PRD into flat native sub-issues |
| Implement | Build one standalone issue and open a PR |
| Implement PRD | Build one sub-issue per run on a persistent PRD branch |
| Review | Review and improve a PR; return comments/results |
| Implement PR | Address reviewer feedback |
| Update Branch | Integrate the base branch and resolve conflicts when necessary |
| Promote Queued | Make work eligible after native blockers complete |
| Architecture Review | Scheduled identification of architecture improvements |

Operational pieces include:

- Trigger and state labels: agent:to-issues, agent:implement, agent:queued, agent:in-progress, agent:review, agent:blocked; update-branch also has a workflow trigger.
- Per-item concurrency controls and a shared group for workflows that mutate the same PR.
- Refusals for nested PRDs, duplicate decomposition, and already-targeted standalone issues.
- One sub-issue per PRD run, with accumulated commits, draft PR creation, and resume after failure.
- Native GitHub blocker relationships for queue promotion; parent/sub-issue relationships do not themselves mean blocking.
- Structured runner input/output contracts.
- Failure artifacts and comments explaining how to retry.
- Branch-head checks to avoid overwriting concurrent PR changes.
- Human review/merge at the platform boundary rather than automatic approval.

The spec's control separation is worth adopting: the agent prepares code and result files; orchestration owns pushes and tracker changes. It is an architectural intention, not proof that credentials are technically inaccessible in the reference implementation.

## 4. Retry and structured-output design

[run-with-retry.ts](https://github.com/mattpocock/course-video-manager/blob/b47b1ec54cc7742326ca2682e49f09803cdac303/.sandcastle/run-with-retry.ts) resumes the same session to repair invalid structured output, with three total attempts by default.

[run-with-extraction.ts](https://github.com/mattpocock/course-video-manager/blob/b47b1ec54cc7742326ca2682e49f09803cdac303/.sandcastle/run-with-extraction.ts) separates doing work from extracting its result when repeating the work would repeat side effects. Output-only tasks use a single-pass path.

Useful principle for our token goal: repair the failed output instead of rerunning successful implementation. Do not pay for a second extraction pass when the output itself is the entire task.

## 5. Context and token efficiency

[writing-for-agents](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/productivity/writing-for-agents/SKILL.md) emphasizes:

- Keep shared meanings in one authoritative location.
- Put branch-specific reference behind precise pointers.
- Avoid restating easily discoverable configuration.
- Remove instructions that do not change behavior.
- Evaluate splits against both agent context and human effort.

[PHASE-BOUNDARIES.md](https://github.com/mattpocock/skills/blob/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/engineering/ask-matt/PHASE-BOUNDARIES.md) is more nuanced than always starting fresh:

1. Continue when the existing conversation is valuable and there is room.
2. Clear when the context is irrelevant to the next task.
3. Handoff when work must travel to another tool, directory or person.
4. Use an isolated agent for suitable bounded independent work.
5. Otherwise compact at an appropriate boundary.

Its token-count heuristics are the author's guidance, not universal model limits. Grilling/spec/ticket generation retain relevant reasoning together where practical; implementation tickets can start fresh.

The review prompt begins with diff statistics and reads patches selectively. Targeted tests are recommended during iteration, with exhaustive CI coverage. The app also has a rough 5,500-token file-size guard based on bytes/4, with exclusions. That is a maintainability heuristic, not an accurate tokenizer or per-run token budget.

No general high/xhigh reasoning router or per-task token budget policy was found in the inspected execution sources. Those remain our customization. The source snapshot uses explicit Claude model strings; it does not establish a universal cheapest/best model allocation.

## 6. Installation and reuse across folders

setup-matt-pocock-skills configures each repository's tracker, triage vocabulary and domain documentation. It discovers existing guidance and updates it rather than blindly duplicating files.

The plugin manifest includes 27 engineering/productivity skills. The stable set is separate from misc and in-progress.

scripts/link-skills.sh demonstrates Matt's maintainer-local symlink approach for sharing one skill checkout across agent directories. It explicitly says it is a development-only helper, not a supported installer. We should not present it as his recommended public installation command.

Our proposed reuse model remains sound: install a shared skill package once, retain project-specific rules and records inside each repository, and explicitly make the shared package available in sandbox environments.

## 7. New and beta material

[skills/in-progress](https://github.com/mattpocock/skills/tree/4ae2317ddb22b046e26455e4f9c9b3aaaf62212d/skills/in-progress) is explicitly beta and excluded from the plugin.

software-factory defines service boundaries: tracker, ticket sources, git host, orchestrator, runner, observability; plus tasks, triggers and runs. It asks what each task reads/writes, what follows it, where humans return, and how duplicate work is prevented.

loop-me designs recurring workflows through grilling. chief-of-staff concerns a broader personal knowledge/work system. claude-handoff, setup-ts-deep-modules, writing-beats, writing-fragments and writing-shape are additional experiments.

These can inform our design without becoming required dependencies.

## 8. QA is more than a final checklist

The repository-specific verify-cvm skill requires checking visible UI behavior in the actual app and capturing evidence. It uses per-run data clones, scratch storage, a write ledger, and controls around external services and the author's recording activity.

The generic code-review skill's standards/spec checks are a different activity from runtime QA. Our version should preserve that distinction.

For Shikhi Kheli, the equivalent should reuse existing emulator courtesy rules, light/dark/tablet checks, offline behavior, audio review and Bangla review. CVM's web/database-specific harness is not directly reusable.

## 9. Conflicts and incomplete guarantees to resolve before reuse

These are source findings, not claims that the whole system is broken:

1. The local implement-prompt.md initially says to close the issue, then later says not to close it. Our task contract must have one completion owner.
2. The local planner can select a candidate even when every issue is blocked. Our AFK scheduler should stop or escalate when no genuinely eligible task exists.
3. The local backlog script has no explicit HITL exclusion in its prompt. Our scheduler should check readiness and human-decision dependencies explicitly.
4. ADR 0008 says the single-issue runner has no commit check; the executable implement.ts checks that the branch is ahead of main. The PRD runner intentionally permits zero-commit runs. Our completion check should verify acceptance criteria, including already-satisfied tasks.
5. docs/agents/testing.md recommends targeted local tests, while several execution prompts demand full tests before committing. Our project adapter should specify one consistent testing policy.
6. The platform spec says the agent never holds a GitHub token; the workflow job has GH_TOKEN in its environment and the noSandbox runner shares that environment. The ownership contract is clearer than the enforced credential boundary.
7. Local merger instructions and docs/agents/merging.md allow agent merge activity, while the AFK platform spec leaves approval and merge to humans. These are different execution policies. Shikhi Kheli's user-owned merge rule must prevail.
8. References to older Docker CLI behavior and authentication workarounds require current verification.
9. File names, skills documentation and operational scripts evolve independently. Pin a source revision and follow executable entry points when resolving drift.

## 10. Coverage map for our own setup

| Capability | Matt reference | Our treatment |
|---|---|---|
| Select workflow depth | ask-matt | Adopt a small router |
| Meeting/message/document intake | triage, questionnaire, agent briefs | Add source-preserving intake across channels |
| Grilling and shared language | grilling, domain-modeling | Adapt to our question style and project rules |
| Multi-session discovery | wayfinder | Optional route for genuinely uncertain work |
| Research and prototypes | research, prototype | Use only for named uncertainties |
| PRD and vertical tickets | to-spec, to-tickets | Adopt contracts; support chosen tracker |
| HITL/AFK distinction | wayfinder, triage roles | Make explicit on eligible tasks and decisions |
| Single-task execution | implement, backlog/once | Build and validate first |
| Sequential AFK | backlog/afk, PRD chain | Add bounded runs and failure recovery |
| Parallel work | implement-spec, main.ts | Defer until sequential execution earns trust |
| Isolation | backlog Docker Sandbox, Sandcastle Docker | Optional runtime adapter; verify current APIs |
| Code review and feedback | code-review, review/implement-PR workflows | Retain standards/spec separation |
| Runtime QA evidence | verify-cvm | Adapt to platform |
| Output validation/retry | retry/extraction wrappers | Add where automation actually needs it |
| Context transitions | phase-boundaries, handoff | Preserve useful context; avoid automatic resets |
| Reuse across folders | setup skill, plugin package | Shared installation plus project configuration |
| Model/effort/cost policy | No general policy found | Our measured customization |
| Retrospective improvements | retro | Fix observed environment failures |
| Release/merge authority | Different policies in source | Explicit per-project rule; user merges here |

## Recommended next deliverable

Write our workflow specification using this coverage map. Separate:

- Reusable reasoning/procedure skills.
- Project contracts and tracker adapter.
- Agent runner adapter.
- Execution environment/isolation.
- Deterministic orchestration and verification.

Start with intake, appropriate planning, one ready task, checks and human review. Preserve optional routes for larger decisions and AFK operation. Add automation based on pilot evidence, not because every source contains another script.

The remaining research is full video/transcript review and a current runtime compatibility check for whichever sandbox and agent we choose. Neither is a reason to treat every historical script as current or install all experimental skills.
