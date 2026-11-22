---
name: writing-for-agents
description: "Write and fix documents agents read: skills, AGENTS.md or CLAUDE.md, pointed-to docs. Use when creating, renaming or editing a skill, or when instructions misfire, duplicate or get ignored."
---

Every document an agent reads is made of **steps** (what to do, in order) and **reference** (rules and facts consulted on demand), reached through a **context pointer**: a skill description, or an AGENTS.md line naming a doc. The pointer's wording decides when the agent reaches the material. Good writing makes the agent take the same *process* on every run. When the document is a skill, also read [skill mechanics](references/skill-mechanics.md).

## Process

### 1. Name the behavior change

Read the current document, everything that points to it, and the observed failure: a transcript, a wrong artifact, a skipped step. Preserve the user's scope, the project's rules and existing invocation settings. To reorganize a project's root guidance, use the `setup-agent-workflow` skill's context refresh; if it isn't installed, return a concrete proposal and keep the current layout.

**Done when:** you can say in one sentence what the agent should do differently, and which observed run showed it.

### 2. Place each piece on the hierarchy

1. **In-file step**: what every run does, in order.
2. **In-file reference**: rules consulted during the steps. A flat list of rules is fine.
3. **Disclosed reference**: a file in the same folder, behind a pointer that states its condition ("For a UI question, read `references/ui.md`").

Inline what every branch needs; disclose what only some branches reach (**progressive disclosure**). Keep a concept's definition, rules and caveats under one heading (**co-location**). Keep project commands, product vocabulary and authorization in the project's own sources.

**Done when:** each piece has a rung, every disclosed file has a pointer naming when to read it, and every local link stays inside the document's own folder.

### 3. Write the steps

Number steps in execution order and end each on a **completion criterion**: a checkable condition ("every acceptance criterion has evidence or a named gap"), never a feeling ("understanding reached"). Put each rule inside the step it governs; a rule appended after its step is **sediment**, read only after the moment it mattered. Show the exact output shape when format matters: a template, an example round, a table.

**Done when:** every step ends in "Done when", and no rule sits after the step it constrains.

### 4. Write the pointer

Start with the **leading word**, the concept the agent should think with (*grill*, *tracer bullet*, *seam*), then the distinct situations that should trigger the document, one phrase per branch. Collapse synonyms that rename one branch, and cut anything the body already says.

**Done when:** a reader can tell from the pointer alone when to reach for the document, and when not to.

### 5. Prune

- Delete each sentence that doesn't change behavior compared with the agent's default (a **no-op**). When a word is too weak to beat the default, use a stronger word (*relentless*, not *be thorough*), not more words.
- Keep each meaning in one place (**single source of truth**). Point to the environment (package scripts, config, `--help`) instead of copying it, unless the lookup is expensive or the knowledge is unwritten: a reason, a convention, a gotcha.
- State the target behavior. A prohibition drags the forbidden behavior into attention; keep one only as a hard guardrail, paired with what to do instead.

**Done when:** every remaining sentence earns its place and no meaning appears twice.

### 6. Verify

Trace a realistic request through the document and inspect the resulting artifact where you can. Check links, collaborator names and absence handling, and conflicts with other instructions. Valid metadata or headings are not evidence that behavior improved; prefer a narrow correction tied to an observed failure, and keep human-facing examples in documentation rather than in always-loaded text.

**Done when:** the traced request takes the intended path, and anything left unverified is reported.

## Reference

### The two loads

Always-loaded text (a description, an AGENTS.md line) costs **context load** on every turn, whether or not it fires. A document the human must remember to invoke costs **cognitive load** instead. Move detail behind pointers to cut context load; add a router when there are more entries than a person can remember.

### Leading words

A leading word is a compact concept the model already knows: *fog of war*, *tracer bullet*, *red* and *green*, *one-way door*. Define it once in bold, then repeat the word, never the definition. When the same word lives in prompts, docs and code, the agent links them and reaches the material more reliably. Prefer an existing word; an invented one recruits no prior knowledge and must be defined. Hunt for passages a leading word could replace: "fast, deterministic, low-overhead" is a *tight* loop.

### When to split

Split a sequence when later steps tempt the agent to rush the current one; hiding them only works across a real context boundary, such as a subagent or a handoff. Split by invocation when a distinct trigger should reach a piece on its own, or several documents need it. Every split costs either an always-loaded pointer or one more name to remember.

Use [pointer examples](references/pointers.md) when deciding whether to inline or link guidance.
