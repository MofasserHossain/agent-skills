# Agent Workflow: Full Conversation Summary

Date: 2026-11-01 (Asia/Dhaka)

This is a historical summary of the discussion, decisions, implementation and remaining plans at the time of export. It is an authoring/reference document, not an instruction file to load into every agent session or install into projects.

We were building **your own reusable AI engineering workflow**, inspired by Matt Pocock, that you can maintain in one private local repository and selectively install into any project.

The intended experience became:

> Keep the workflow in your root repo → choose the skills a project needs → install those skills locally → use Claude or Codex to take work from incoming requirements through planning, implementation, review and QA.

Over the conversation, we researched Matt’s approach, created and connected an initial workflow kit, identified that its installation was too broad, and then changed the default approach to **standard, individually installable skill packages**.

## 1. The workflow we wanted

You wanted a structured way to handle work arriving from different places:

- An idea or feature request.
- Meeting notes.
- A client brief or document.
- A Linear or GitHub task.
- A message describing a change.
- An existing codebase problem or refactor.
- A UI design or research question.

The main flow we agreed on was:

```text
Incoming material
       ↓
Understand the request / create a brief
       ↓
Grilling: resolve consequential decisions
       ↓
Research or prototype, when needed
       ↓
PRD / specification
       ↓
Vertical implementation tasks with dependencies
       ↓
Implementation
       ↓
Code review and QA
       ↓
Findings return to the task backlog
```

This is a flexible route. A clear, small fix should go directly to implementation and proportionate verification. It should not require a PRD, research document and task breakdown simply because those skills exist.

The workflow’s purpose is to help the agent and you reach a shared understanding, preserve decisions, and produce verifiable changes.

## 2. Research into Matt’s repositories, screenshots and transcripts

You originally shared:

- [mattpocock/skills](https://github.com/mattpocock/skills)
- [mattpocock/course-video-manager](https://github.com/mattpocock/course-video-manager)

Your screenshots also identified his [AI Engineer workshop project](https://github.com/mattpocock/ai-engineer-workshop-2026-project).

We inspected the relevant skill instructions, prompts, runner scripts and setup conventions. We also investigated [Sandcastle](https://github.com/mattpocock/sandcastle).

The main findings were:

| Area | What Matt’s sources showed |
|---|---|
| Reusable procedures | Markdown `SKILL.md` files |
| Skill installation | Standard Skills CLI or agent plugins |
| Project setup | A setup skill records tracker and documentation conventions |
| Grilling | Explore the project, then resolve design decisions |
| PRD/specification | Summarize the agreed destination and testing decisions |
| Ticket creation | Divide work into bounded slices with blockers |
| TDD | Build one behavior through a red–green–refactor loop |
| Sequential execution | Bash-based Ralph scripts |
| Parallel execution | TypeScript orchestration through Sandcastle |
| Execution prompts | Separate planning, implementation, review and merge prompt files |
| QA | Verify behavior and create follow-up backlog items |

We established that Matt uses **several installation and execution patterns**. His public repositories do not prove that he always works from one central private agent workspace, or that he copies his whole workflow repository into every application.

Your shared video transcript added useful context about his intended planner → parallel implementers → reviewers → merger flow. We treated that transcript as an explanation of the demonstration, alongside the inspected source code.

## 3. Separating skills, installation and execution

This distinction became central:

| Concept | Its job |
|---|---|
| Skill | Instructions for how the agent should approach work |
| Template | The shape of an output, such as a brief or task |
| Project configuration | Commands, tracker choice and project-specific settings |
| Installer | Places selected skills where Claude/Codex discover them |
| Runner | Starts an agent process with prepared inputs |
| Scheduler | Chooses, claims and sequences eligible tasks |
| Sandbox | Provides an execution environment |
| Reviewer/integrator | Checks work and combines branches |

Installing skills does not automatically create a scheduler, Docker environment or unattended engineering system.

Likewise, a Markdown skill is already a reusable prompt. We do not need another duplicate prompt file for every skill. Additional runner prompts are useful when automation needs concrete inputs, outputs and role-specific context.

## 4. The shared source repository

Its location is:

```text
/Users/mofasserhossain/Developer/Core/Own/agent-workflow
```

This is the place where you maintain the workflow itself.

Its responsibilities include:

- Canonical skill instructions.
- Shared policies and templates.
- Installation and packaging tools.
- Optional execution tooling.
- Tests.
- Research about Matt and other approaches.
- Architecture and future execution plans.
- Examples for evaluating the workflow.

Those authoring and maintenance files belong in the root kit. They do not all belong in an application project.

We kept the core independent of a particular provider. **Claude Code and Codex are the only supported agents for now.**

The `manual` setting means “prepare context without choosing a CLI.” It is not a third agent.

## 5. Fourteen workflow procedures

| Procedure | Purpose |
|---|---|
| `workflow` | Route work to the appropriate stages |
| `setup-project` | Discover project commands, tracker and documentation conventions |
| `intake` | Turn notes, documents or messages into an understood request |
| `grill` | Resolve consequential requirement and design decisions |
| `research` | Investigate factual or technical uncertainties |
| `prototype` | Test a specific design or implementation assumption |
| `ui-design` | Plan interface flows, states and visual decisions |
| `write-spec` | Produce the PRD/specification from settled understanding |
| `plan-tasks` | Break the specification into bounded implementation tasks |
| `implement` | Build one agreed task and return verification evidence |
| `improve-codebase-architecture` | Assess a focused area for useful architectural improvements |
| `review` | Check the change against requirements and project standards |
| `qa` | Check actual behavior and record remaining acceptance work |
| `retro` | Improve the workflow after observed friction |

In the standard installable distribution, the source `workflow` procedure is named **`agent-workflow`**.

That router is optional. You can install individual procedures without installing the entire catalog.

## 6. Connecting requirements, specifications and tasks

The PRD/specification describes the destination:

- What problem we are solving.
- Who the change is for.
- Expected behavior.
- Scope and exclusions.
- Important decisions and constraints.
- Acceptance criteria.
- Verification strategy.

Implementation tasks describe bounded pieces of work toward that destination.

For work with multiple requirements, we introduced stable labels such as `R1`, `R2` and `R3`. Tasks identify which requirements they cover.

This helps answer:

> Does the backlog cover the specification, and does the delivered work satisfy the original request?

A task should contain enough information for another agent or a fresh session to continue without reconstructing the whole conversation.

## 7. Vertical slices and early integration

You asked about horizontal planning, vertical planning and tracer bullets.

We adopted the principle of creating a thin, observable outcome through the necessary layers.

For example:

```text
One user action
    → relevant interface
    → application behavior
    → persistence or service interaction
    → observable result
    → meaningful verification
```

For backend-only work, a vertical slice can be one complete endpoint or service behavior. It does not need a screen.

Some enabling work may still be necessary, but the plan should expose integration problems early rather than postponing all integration until the end.

A multi-phase plan can still be useful. Each phase should preserve a clear outcome, relevant context and a verification boundary.

## 8. HITL, AFK and review requirements

These are separate decisions:

| Setting | Meaning |
|---|---|
| HITL execution | The work needs human interaction or a consequential decision |
| AFK execution | The agent can implement within settled, bounded scope |
| Human review | A person must still evaluate the result |
| Automated review | Defined automated review may satisfy that review requirement |

An AFK task can still require human review.

AFK does not automatically authorize publishing, pushing, deployment or merging.

The task lifecycle includes:

```text
draft → ready → in-progress → review → done
                    ↘ blocked
```

A successful CLI exit, a commit, or an agent’s completion statement is not sufficient evidence that a task is accepted.

We also identified a future orchestration issue: verified integration and final human acceptance may need separate records. Otherwise, a scheduler might incorrectly mark human review complete just to release downstream work.

## 9. One authoritative tracker

You asked whether we should use local issue files, GitHub Issues, or both.

The decision was to avoid competing copies of task status.

Possible arrangements include:

- Local Markdown issues own status.
- GitHub Issues own status.
- Another tracker owns status through its available integration.

Local documents can still support externally tracked work—for example research, prototypes or a specification.

If moving from local tasks to GitHub, preserve the local-ID/issue-URL mapping and explicitly switch the authoritative tracker.

Incoming Linear or other tracker content can be used as a source. A dedicated automated integration for every service has not been implemented.

## 10. TDD and proportionate verification

Matt has a dedicated TDD skill.

Our current implementation includes test-first guidance in `implement` and the verification policy:

```text
Identify one behavior
        ↓
Write a meaningful failing test
        ↓
Confirm it fails for the intended reason
        ↓
Implement the behavior
        ↓
Pass the test
        ↓
Refactor while preserving behavior
```

We emphasized:

- Tests should observe public behavior and independently known expected outcomes.
- A missing dependency or invalid command is not a useful RED result.
- Bug fixes should reproduce the reported symptom.
- Tests should not simply mirror the implementation.
- Small copy/configuration changes and prototypes need proportionate verification.
- Focused checks during development do not replace required final checks.

We did not create a separate dedicated TDD skill in your fourteen-procedure kit.

## 11. Reusable UI design support

You clarified that UI research/design should not be specific to Shikhi Kheli.

We therefore made `ui-design` a general procedure for web and native projects.

It connects:

```text
Audience and task
      ↓
Existing behavior and evidence
      ↓
Flows and interaction states
      ↓
Visual/design choices
      ↓
Optional prototype
      ↓
Recorded decisions
      ↓
Implementation and runtime QA
```

The shared skill covers concerns such as:

- Existing components, tokens and design conventions.
- Relevant loading, empty, error and success states.
- Real versus mocked data behavior.
- Accessibility and platform-specific checks.
- Evidence gaps and assumptions.
- Clear handoff into the specification and tasks.

Product-specific rules stay in the project.

Backend projects use the same delivery workflow and skip UI design when it does not apply.

## 12. Architecture improvement as an optional route

The architecture procedure looks for evidence such as:

- Changes repeatedly spreading across unrelated files.
- Difficult testing boundaries.
- Unclear interfaces.
- Modules exposing too much internal complexity.
- Documentation contradicting actual behavior.

It produces focused candidates and recommendations.

A selected improvement then enters the normal planning and delivery flow.

It does not require a repository-wide refactor before every feature. Documentation corrections can also be handled as narrow tasks.

We used Matt’s discussion of deep modules as inspiration: useful functionality behind understandable interfaces helps both humans and agents work effectively.

## 13. Wayfinder investigation

Wayfinder is meant for a large, uncertain destination that cannot be planned sensibly in one session.

Its “tickets” can represent decisions, research questions or prototypes needed to discover the path.

That is different from an implementation backlog whose scope is already understood.

For now:

- Your `grill` procedure can maintain a lightweight decision map.
- A dedicated Wayfinder system is deferred.
- Ordinary features do not need another planning framework.

## 14. Context size, reasoning effort and token efficiency

Your goal was better accepted output with less wasted usage.

The principles we adopted were:

- Load the selected procedure and relevant project material.
- Avoid feeding every skill, issue, document and historical message into each run.
- Preserve decisions in durable work records.
- Use fresh sessions for independent tasks with complete handoffs.
- Keep a session when its reasoning remains useful.
- Slice large work rather than relying only on higher reasoning effort.
- Measure retries, rework and accepted outcomes.

Your screenshot showed a particular Claude session reporting about **660 tokens for nine skills**.

We clarified that this was a skill-discovery listing for that session. It was not proof that all nine skill bodies together cost only 660 tokens.

We did not measure an equivalent live Claude/Codex context count for your setup.

We also observed that the app’s existing `AGENTS.md` is much larger than the demonstration’s small memory contribution. We preserved its project rules rather than deleting obligations to make the initial context smaller.

The advisory effort policy was:

| Work | Starting point |
|---|---|
| Routine extraction or transformation | Low or medium |
| Ordinary implementation and synthesis | Medium |
| Difficult planning, debugging or review | High |
| Exceptionally difficult unresolved reasoning | Selectively evaluate additional effort |

Those labels are not assumed equivalent across providers. No automatic effort translation or universal savings claim has been implemented.

## 15. Project-specific verification commands

You pointed out that different projects use different commands for types, lint, tests, dead code and TDD.

We agreed that those commands belong in each project’s configuration and scripts.

For Shikhi Kheli, `.agent-workflow.json` records its actual commands:

```json
{
  "schema_version": 1,
  "work_dir": "docs/work",
  "tracker": "local",
  "default_agent": "manual",
  "checks": {
    "types": ["npm", "run", "typecheck"],
    "lint": ["npm", "run", "lint", "--", "--quiet"],
    "test": ["npm", "test", "--", "--runInBand"]
  },
  "verification": [
    ["npm", "run", "format"],
    ["bash", "./.conductor/verify.sh"]
  ]
}
```

There is no configured dead-code checker in this app. We did not add one merely to fill a generic example.

When scripts change, update the project configuration and relevant documentation. Reinstalling shared skills should not be necessary just because a project renamed a test command.

The optional execution helper passes this configuration as context. It does not automatically execute or prove the correctness of the configured checks.

## 16. Connecting the initial kit to Shikhi Kheli

The app workspace is:

```text
/Users/mofasserhossain/Developer/Core/Own/shishu-shikkha
```

We added the initial workflow connection through:

- `.agent-workflow.json`
- `docs/agents/workflow.md`
- Claude/Codex discovery entries.
- A project-local `.agent-workflow` installation.
- Short pointers in the project’s existing instructions and README.
- Relevant ignore/formatter configuration.

We preserved:

- The app’s existing product and architecture instructions.
- `CLAUDE.md` as a symlink to `AGENTS.md`.
- The existing pull-request skill.
- The user-owned review/merge process.
- Existing project commands.

No app feature was implemented as part of this workflow setup.

The example brief/spec/issues in the root kit are fictional workflow examples, not an active Shikhi Kheli feature backlog.

## 17. Correcting the overly broad first installation

This was an important evolution in the conversation.

You wanted installed projects to work without depending on the root workflow checkout.

I initially implemented that by copying the whole kit into each project. That preserved all links, but also copied unnecessary material:

- Research about Matt.
- Kit tests.
- Fictional examples.
- Development documentation.
- Installation and authoring tools.

You correctly questioned this.

We clarified that project independence requires the selected procedures and their actual supporting resources—not the entire source repository.

The progression was:

| Version | Approach |
|---|---|
| Initial connection | A broad, independent project snapshot |
| First correction | Runtime-only snapshot with skill selection |
| Second correction | A chooser with no automatic install-all default |
| Latest direction | Standard Skills CLI with independent skill packages |

The runtime cleanup reduced the app’s managed resources from **54 to 33**, while retaining its existing fourteen procedures.

That app installation remains in place today because you said you want to choose its replacement selection yourself.

## 18. Bash, Python, Node and TypeScript

You asked why this could not simply be Bash.

The answer was that these languages serve different jobs:

| Material | Role |
|---|---|
| Markdown | Instructions the agent reads |
| Bash | Convenient installation commands and simple execution loops |
| Node-based Skills CLI | Standard skill selection and installation |
| Python | Our root-kit build tools and optional custom execution helper |
| TypeScript | Matt’s Sandcastle parallel orchestration |

The installed agent skills do not need to be converted into Bash.

We ultimately chose to provide a **Bash command that uses the standard Skills installer**, matching the installation pattern you preferred.

Python remains a maintainer/build tool in the root repo and an optional legacy runner. It is not required to use the new installed Markdown skills.

## 19. Latest implementation: standard local skill installation

Your root kit now prepares self-contained packages under:

```text
agent-workflow/
  skills/                  Canonical procedure sources
  references/              Shared authoring policies
  templates/               Canonical templates
  tools/package_skills.py  Maintainer build tool
  scripts/install-skills.sh
  dist/skills/             Prepared independent packages
  docs/                    Development documentation and research
  tests/
```

The build creates independent skill folders:

```text
dist/skills/
  agent-workflow/
    SKILL.md
    references/
  grill/
    SKILL.md
  write-spec/
    SKILL.md
    templates/
  ui-design/
    SKILL.md
    references/
    templates/
  ...
```

The important packaging decisions are:

- Each skill includes its own required references/templates.
- Supporting links stay inside that skill’s folder.
- References to other procedures become optional installed skill names.
- Selecting one skill does not automatically install every related stage.
- The router is optional.
- Research, tests and execution tooling do not get installed with standard skills.
- Canonical shared material remains maintained in one source location; distribution copies are generated.

The current build produces **14 skill packages containing 34 files**.

## 20. Normal installation and maintenance commands

From the root `agent-workflow` repo:

```bash
# Inspect available skills
bash scripts/install-skills.sh /path/to/project --list

# Choose skills interactively in a normal terminal
bash scripts/install-skills.sh /path/to/project
```

You can also provide an explicit selection:

```bash
bash scripts/install-skills.sh /path/to/project \
  --skill grill research write-spec plan-tasks
```

The wrapper:

- Uses the tested `skills@1.7.4`.
- Targets project-local Claude Code and Codex.
- Disables CLI telemetry.
- Does not install globally.
- Requires explicit skill names for unattended calls.
- Guards against a silent install-all inside detected agent environments.

That last safeguard came from a real finding: the standard CLI automatically skips prompts when it detects an AI-agent environment.

These standard CLI commands use the CLI’s own installation/confirmation flow. They do not use the old custom installer’s preview/`--apply` protocol.

For maintainers editing the root kit:

```bash
python3 tools/package_skills.py
python3 tools/package_skills.py --check
```

The prepared distribution is ignored in Git and rebuilt from canonical sources.

## 21. Standard installed project layout

For the usual project-local symlink method:

```text
your-project/
  .agents/skills/<selected-skill>/
    SKILL.md
    references/       When required
    templates/        When required

  .claude/skills/<selected-skill>
    → project-local canonical skill folder

  skills-lock.json
```

The selected skill files are copied into the project. Claude’s links point within that project.

The lock file can record the local source path for future maintenance. Running already-installed skills does not require that source path to remain available.

Each project continues to own:

- Product and architectural rules.
- Verification commands.
- Tracker conventions.
- Actual research.
- Briefs and decisions.
- Specifications and implementation issues.
- QA and acceptance evidence.

## 22. Docker, Ralph and Sandcastle: future execution layer

We researched and planned them, but did not activate automated execution infrastructure.

The intended future progression is:

```text
One supervised task
       ↓
One isolated worker
       ↓
Reliable bounded sequential execution
       ↓
Independent parallel workers
       ↓
Serialized integration and combined verification
       ↓
Feature QA and human-owned delivery
```

Before parallel/unattended work, the implementation needs:

- Authoritative task state and atomic claims.
- Dependency validation.
- Separate working trees and branches.
- Concurrency and retry limits.
- Time limits.
- Environment provisioning.
- Appropriate filesystem/network/credential access.
- Portable execution results.
- Integration locking.
- Recovery from interrupted work.

We distinguished ordinary Docker containers from Docker Sandboxes’ microVM-based environment.

We also established that branch names alone do not isolate files. Parallel workers need separate working trees.

For Shikhi Kheli, Metro, Android installs, device driving and UI/audio QA need particular care because workers do not automatically get independent devices.

## 23. Validation and limits

The latest root-kit validation has:

- **70 passing tests.**
- Fourteen canonical skills passing the kit checks.
- Fresh generated packages passing the package check.
- Bash syntax validation.
- Selected exported skills passing skill validation.

We also tested the real Skills CLI in temporary projects:

1. Three selected skills installed with project-local links.
2. A separate project with only UI design installed using copies.
3. Supporting links remained valid while the source distribution was hidden.
4. The first installed project also survived relocation.
5. No Python files or full `.agent-workflow` bundle were installed in those standard test projects.

Earlier, the app integration passed its full verification:

- **58 Jest suites.**
- **508 tests.**
- Required version, type, lint and formatting checks.

No app feature, emulator behavior or model output quality was claimed to be validated by those packaging tests.

We did not publish a package, create a remote repository, push changes, open a PR, perform a final merge or launch a paid agent run for validation. The latest workflow changes remain uncommitted.

## 24. Current position and remaining work

| Area | Current status |
|---|---|
| Private local source kit | Available |
| Fourteen workflow procedures | Implemented |
| Generic UI/frontend/backend support | Implemented |
| Project-specific command configuration | Implemented |
| Standard local skill packages | Prepared and tested |
| Bash installation command | Implemented |
| Per-project skill selection | Supported |
| Independent installed resources | Tested |
| Shikhi Kheli’s migration to standard skills | Not performed; awaiting your chosen set |
| Dedicated Wayfinder | Deferred |
| Automated Ralph scheduler | Planned |
| Docker provisioning | Planned |
| Sandcastle parallel execution | Planned |
| Automated GitHub tracker adapter | Planned |
| Automatic model/effort routing | Planned |
| Public package/plugin distribution | Deferred until you want it |

The most useful next steps are to choose the skills you want for Shikhi Kheli, deliberately migrate its existing installation, and pilot the workflow on one real task. That pilot should tell us which further automation is useful before adding more infrastructure.

The lasting design is **one maintained root kit, independent project selections, project-owned context, optional execution automation, and verification evidence at every delivery stage**.
