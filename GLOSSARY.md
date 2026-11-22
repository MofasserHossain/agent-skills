# Agent Skills

The working language of this kit: the words its skills, templates, docs and helper use for the work moving from a request to a verified change. Use these terms exactly. A skill that needs a new term adds it here first.

## Language

**Source**:
Original material a request comes from: a meeting note, message, document or an item in another tracker.
_Avoid_: input, raw ticket

**Brief**:
A source-linked summary of one requested outcome: the problem, explicit requirements, decisions, constraints and open questions. `to-brief` produces it.
_Avoid_: intake document, summary

**Decision**:
A settled choice together with its reason. Choices about intent, preference and trade-off belong to the human.
_Avoid_: assumption (an assumption is a decision nobody has confirmed)

**ADR**:
A short record of a decision that is hard to reverse, surprising without context and the result of a real trade-off.
_Avoid_: design doc

**Spec**:
The buildable description of a multi-session feature: behavior, labelled requirements, decisions and how acceptance will be judged. `to-spec` produces it. You may know this document as a PRD.
_Avoid_: PRD, plan, specification document

**Requirement**:
One distinct behavior a spec commits to, with a stable label (R1, R2) that tasks and QA cite.
_Avoid_: user story (when you mean the commitment itself)

**Task**:
One buildable vertical slice: an observable outcome with acceptance criteria, verification and blockers, sized for one fresh session. `to-tasks` produces tasks; `implement` builds one.
_Avoid_: ticket, story, implementation issue

**Issue**:
The tracker record that holds a task or a spec: a GitHub issue, or one file in a feature's local `issues/` folder. Say task for the work and issue only for the record.
_Avoid_: ticket (except when quoting a system that uses the word)

**Tracer bullet**:
An early task that cuts a thin path through every layer it needs, so the whole path is proven before it is widened.
_Avoid_: spike, skeleton

**Blocker**:
A task or decision that must be done (integrated, not merely written) before another task can start.
_Avoid_: dependency (when you mean list order only)

**Frontier**:
Every open item whose blockers are all resolved: the questions that can be asked now, or the tasks that can start now.

**HITL**:
Work that needs a human in the loop for judgement, access or a decision. The agent never supplies the human's side.

**AFK**:
Work an agent can finish with the human away from the keyboard, within settled scope. AFK never grants permission to merge, publish, spend money or message others.

**Seam**:
A public boundary where behavior is observed and tested without reaching inside.
_Avoid_: boundary (alone), layer

**Acceptance criterion**:
An observable condition that decides whether a task or requirement is met.

**Evidence**:
The observed result of a check that actually ran (command output, screenshot, reproduction), tied to the revision it covers.
_Avoid_: claim, "should work"

**Verdict**:
The outcome a stage reports from its evidence, such as accepted / changes needed / pending evidence for QA, or supported / rejected / inconclusive for a prototype.

## Relationships

- A **source** yields one **brief** per outcome; unrelated outcomes get separate briefs.
- A **spec** holds many **requirements**; each **task** cites the requirements it covers.
- An **issue** holds one **task**, or one **spec** as a parent issue.
- A **task** has zero or more **blockers**; the task **frontier** is every task whose blockers are done.
- A task is done when every **acceptance criterion** has **evidence**, or an explicit pending human check.

## Flagged ambiguities

- "PRD" and "spec" named the same document. Resolved: **spec**.
- "Task", "issue" and "ticket" all named the unit of work. Resolved: **task** is the work, **issue** is the tracker record, and "ticket" is not used.
- "Intake" named both a stage and a skill. Resolved: the skill is `to-brief` and its output is a **brief**.
- "Review" names the `code-review` skill and also a task status (`review`: required human checks remain). The status keeps its name in task metadata.
