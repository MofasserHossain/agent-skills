---
name: retro
description: "Look back on real work and fix the environment behind its friction: checks, standards, navigation, instructions, tools. Use after a session went sideways, a mistake repeats, or a retrospective is requested."
---

Improve the agent's **environment**, not the code: the checks, standards, navigation, instructions and tools that the next run starts from. Every proposal traces to an observed failure; producing more instructions is not a success.

## Process

### 1. Read the primary sources

Read the session or run the user names (the current one by default): its artifacts, transcript or logs, and the actual outcome. A summary of the session is a weaker source than the session itself.

**Done when:** you can point to the moments that caused rework.

### 2. Find candidates

Search each category. The *use when* names the session signal that points there:

- **Navigation.** *Use when* finding the right file or fact took long. Add a **navigation pointer**, or expose a hidden dependency between files.
- **Automated checks.** *Use when* the agent made a mistake a check could catch, or the project has no guardrail at all (no pre-commit hook and no CI running lint, types and tests). Read the project's existing check commands first: an existing check that sits unwired or broken is the finding, not a new check.
- **Coding standards.** *Use when* review missed a mistake. A **mechanical** rule (a banned API, an import shape, a file location) becomes a deterministic check; written standards are for **judgement calls**. Standards bind the review stage, which carries the least context pressure, not the implementer.
- **Steering files.** *Use when* AGENTS.md or CLAUDE.md has grown large. Move rules into standards or checks, and keep the root file for essential rules and pointers.
- **No-ops.** *Use when* instructions are long. Delete lines that don't change behavior.
- **Tool economy.** *Use when* a tool call was expensive or a custom tool wastes tokens.
- **Information access.** *Use when* the agent lacked a crucial fact. Expose dev server logs, or grant read-only access to a service.
- **Work shape.** *Use when* rework came from missing context, unclear decisions, badly sized tasks or weak verification.

**Done when:** each candidate names the observed failure behind it, or is labelled as a hypothesis.

### 3. Locate the owner

Put each correction where the behavior is owned: project configuration, a shared skill, a checker or a work record. A project-specific convention stays in that project; a shared skill changes only when the lesson applies across its intended uses. Read the existing guidance before adding a rule, and revise or remove whatever the correction supersedes.

**Done when:** each candidate has exactly one owning place.

### 4. Present, most severe first

For each candidate, give the observed problem, its supported cause (or an explicit hypothesis), the smallest correction, and an evaluation case that would show the correction failed. Where data exists, compare cost per accepted result, latency and review effort, keeping measured savings apart from hypotheses. Use the [pilot scenarios](references/pilot-scenarios.md) to evaluate behavioral changes.

**Done when:** the list is ordered by severity. Apply only authorized corrections, and keep the example that demonstrated each issue. If the records don't support a change, report the missing evidence and leave the procedure alone.
