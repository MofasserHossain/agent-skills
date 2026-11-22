---
name: handoff
description: "Write a continuation record so another session, agent, workspace or person can resume the work. Use when switching harness, directory or person, or forking a side task mid-phase."
---

Write a **continuation record**: everything the next executor needs to resume without the previous session's memory. It is for work that travels: to a new harness, directory, workspace or person, or a side task forked mid-phase. A later phase in the same place usually just continues. If the user named what the next session will focus on, tailor the record to that.

## Process

### 1. Establish the current state

Read the authoritative work record, the applicable instructions and the latest evidence. Identify the target project or workspace, the current revision and the actual working-tree changes. Keep verified results apart from agent claims, planned actions and checks not yet run. An earlier summary never overrides newer code or task evidence.

**Done when:** you can say what is done (with its evidence), what is only claimed and what is untouched.

### 2. Write the record

Use the [handoff shape](templates/handoff.md) and drop sections that add nothing. State the objective, the settled decisions with their reasons, the unfinished acceptance criteria, the blockers and the next concrete action. Add a **Suggested skills** line naming the skills the next session should use. Point to the canonical specs, tasks and evidence instead of copying documents or transcripts.

- Every path must resolve in the receiving environment; when a transfer is needed, explain it rather than assuming a host path is mounted there.
- Account for uncommitted or untracked work, local-only branches, required fixtures and active processes.
- Redact secrets and personal data, and never dump the environment.

Save the record where the next executor can read it: in the project's work folder when it belongs with the work, or in the OS temporary directory for a one-off session switch.

**Done when:** the record exists and every pointer in it resolves from the receiving side.

### 3. Walk the first step

Walk the receiving agent's first action through the record. Can it find the source, identify the revision and the remaining edits, load the relevant rules, and see what is still undecided? Report missing access or artifacts explicitly.

**Done when:** resuming depends on neither proprietary session memory nor a guessed human answer.

Writing a handoff changes no task identity, status or acceptance. It launches no agent, copies no credentials and sends no messages.
