---
name: to-brief
description: "Turn meeting notes, messages, documents or tracker issues into a source-linked brief. Use when work arrives as raw material, sources conflict, or one request mixes several outcomes."
---

Turn raw material into a **brief**: one requested outcome with its problem, requirements, decisions, constraints and open questions, each traceable to the **source** that said it. Synthesize; ask the user only what the sources and the project can't answer.

## Process

### 1. Read the sources

Read the supplied material and every accessible source it references; pasted text is enough when no integration exists. Record which sources were read and which stayed unavailable. An unread source is an evidence gap, never support for a claim that the request is complete.

**Done when:** every source is listed as read or unavailable.

### 2. Check what already exists

Before asking the user anything, check the project:

- **Already built:** search for the requested behavior by its domain concept, not only the request's wording, and say where you looked.
- **Duplicates:** search existing issues, specs and tasks for the same request.
- **Prior decisions:** read recorded decisions or rejections the request touches.
- **The claim:** for a reported bug, try to reproduce it from the given steps.

**Done when:** each check has a result (found, not found, or couldn't check) with where you looked.

### 3. Form the brief

Use the [brief template](templates/brief.md), dropping empty sections. For each requirement or decision that would change the implementation, keep a source pointer precise enough to recover the original statement: a document section, a message timestamp. Keep these apart:

- Explicit requirements, suggestions and assumptions. A proposal stays a proposal until it is adopted.
- Conflicts. Show both sides; repetition or a later timestamp alone doesn't settle a conflict.
- Unrelated outcomes. Give each its own brief.

**Done when:** every material statement has a source pointer and no conflict was resolved silently.

### 4. Name the next step

List the material open questions, with who or what can answer each, and recommend a route: `implement` for a small, clear task; `grill-me` for open decisions; `research` or `prototype` for a named uncertainty; `to-spec` for multi-session work. When an existing issue already states the same contract, point to it instead of writing a new brief.

**Done when:** every material gap has a next action.

Writing to an external tracker, sending messages or publishing needs task authorization; keeping a source's URL doesn't authorize writing to it.
