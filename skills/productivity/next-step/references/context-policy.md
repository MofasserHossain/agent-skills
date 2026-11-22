# Context policy

Load the current skill, the project's instructions and the selected work record first. Follow source, spec and research pointers when they matter. Load only what the next step needs, never every skill, task or diff.

## Phase boundaries

A **phase** is a chunk of work inside a session: grilling, implementing, QA. Decide how to move on only at the **boundary** between two phases; mid-phase, continue, or send the remaining independent work to a subagent. Ask in order; the first yes wins:

1. **Continue?** Yes when the next phase needs this one as a **primary source** (grilling → spec → tasks want the reasoning verbatim, not a summary of it) and the context window still has room. Continuing costs nothing and loses nothing, so rule it out first.
2. **Clear?** Yes when nothing in this session matters to what comes next. Clearing a relevant session loses the *why* behind the work, and reading the diff later won't bring it back.
3. **Handoff?** Only when the work travels: to a new harness, a new directory or workspace, another person, or a side task forked mid-phase. Use the `handoff` skill.
4. **Subagent?** Yes when the task is tightly scoped and can run AFK, such as a review that reads a diff and reports. Start it with a fresh context window and a narrow brief.
5. **Otherwise compact**, with an instruction naming the next phase ("compact: next we QA the export flow").

Every move except continuing replaces the session (a primary source) with a summary (a secondary source): less noise, but lossy. Pay that cost only when staying costs more. These are judgement calls; their value is in asking them in order, at the boundary.

## What a record keeps

A handoff or summary states the objective, agreed decisions with their reasons, open questions, the current revision, the next action and pointers to artifacts. Point to artifacts instead of copying them, and never copy credentials. Research notes record sources, date, findings and limitations. An easily repeated lookup rarely needs a permanent copy.

Keep stable instruction prefixes reusable and task context narrow. Judge context changes by quality and total cost per accepted result; never shrink context by dropping essential constraints.

When choosing a model or reasoning effort, use [model policy](model-policy.md); native settings remain the executor's responsibility.
