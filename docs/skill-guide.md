# Choosing and using skills

Use the smallest procedure that resolves the current problem. These examples are requests to an installed skill, or to the corresponding canonical file when working in this checkout. They are not additional agent instructions. Project rules and existing authorization still apply.

## Choose an entry point

| Situation | Start with | Example request |
|---|---|---|
| New project or scattered project guidance | `setup-project` | “Inspect existing instructions and commands. Prepare the project context for these selected skills.” |
| Unsure which route fits | `agent-workflow` | “Resume this feature from its latest work record and evidence.” |
| Notes, messages or conflicting requests | `intake` | “Turn these notes into a source-linked brief; surface contradictions with the existing ticket.” |
| Product or design choices remain open | `grill` | “Resolve the offline behavior for this feature using the brief and existing decisions.” |
| A factual answer would change a decision | `research` | “Verify whether the platform supports this background operation; cite primary evidence and limitations.” |
| A runnable experiment would settle a choice | `prototype` | “Test whether this state transition can lose pending edits; preserve the experiment and verdict.” |
| Interface flows or appearance need design | `ui-design` | “Design the empty, loading, error and success states for this flow using our platform conventions.” |
| Decisions are settled and work spans sessions | `write-spec` | “Synthesize these decisions into a spec; flag any implementation-changing gaps.” |
| Agreed work needs several tasks | `plan-tasks` | “Break this spec into verifiable outcomes with coverage, blockers and checks.” |
| A clear fix or one ready task | `implement` | “Fix the reported preference loss. Reproduce it and return evidence against the ticket.” |
| A bounded change needs inspection | `review` | “Review this diff against the task and project standards; report defects with evidence.” |
| Delivered behavior needs runtime checks | `qa` | “Check this revision against the acceptance criteria; record failures and unperformed checks.” |
| PR preparation, status or delivery | `pull-request` | “Check this PR's review and merge status using the project's delivery policy.” |
| Module boundaries repeatedly slow changes | `improve-codebase-architecture` | “Assess this subsystem and recommend one bounded improvement with code evidence.” |
| Observed workflow friction needs correction | `retro` | “Use these run records to identify the smallest correction and a way to evaluate it.” |

If an installed collaborator is absent, use the current procedure where sufficient or add the needed skill deliberately. Installation does not require the full catalog.

## What a useful result looks like

The procedure and its linked contracts define completion. For a quick review, look for these signals:

- Discovery separates agreed decisions from open questions. It does not ask you to rediscover facts the agent can inspect.
- A spec records decisions you recognize, concrete behavior and checks; it does not fill template sections with invented scope.
- A task delivers an observable outcome and names real prerequisites. The first task can start, or its blocking decision is explicit.
- Implementation connects acceptance criteria to actual evidence. “Already satisfied” is a valid result when verified.
- Review names the revision, actionable defects and limits of its inspection. QA records what actually ran and what remains pending.
- A handoff lets another agent find the current work, reasons and next action without relying on the previous provider's session.

For example, “implement storage, then implement UI, then add tests” usually hides outcomes until late. A preference feature could instead start with “remember the chosen setting across restart,” followed by “recover safely when saved data is invalid.” Each slice crosses the layers it needs and has its own check. The second depends on the first only if it actually needs that implementation.

Additional stage-specific signals matter too: setup separates discovered commands from exercised ones; research explains source applicability; prototypes give a verdict tied to observations; UI design identifies unresolved contracts and recovery behavior. Architecture work shows a real change burden, PR recovery checks what happened remotely, and a retrospective proposes a correction with a way to evaluate it. Each procedure owns its detailed rules.

## Avoid unnecessary stages

A typo can go straight to implementation and proportionate verification. A bug with a known expected behavior needs reproduction and a fix, not a fresh product interview. A larger ambiguous feature may need discovery, a spec and tasks. Research and prototypes answer named questions; they are not default ceremonies.

Keep a useful discovery conversation through spec and task synthesis. Start a fresh session when the next task has enough durable context to stand alone. See the [context policy](../skills/agent-workflow/references/context-policy.md) for transitions and handoffs, the [prompt map](prompt-map.md) for canonical procedures, and the [walkthrough](walkthrough.md) for connected artifacts.

## Evaluate improvements

Structural validation establishes that skills are packaged and linked correctly. It does not establish that their prompts outperform another kit. Use the [pilot scenarios](../skills/retro/references/pilot-scenarios.md) on comparable tasks and record corrections, acceptance, review effort, elapsed time and available usage. Compare accepted outcomes rather than prompt length. Live agent runs require task authorization.
