---
name: prototype
description: "Answer one design question with a throwaway experiment: a state model to click through, or UI variants to compare. Use when something runnable or visible would settle a choice."
---

A prototype is **throwaway code that answers one question**. The question decides its shape, and the answer, not the code, is what moves into the real work.

## Process

### 1. State the question

Name the question, the decision it unblocks, and the observation that would support or reject the proposed approach. Choose fidelity around that observation: a clickable mock can answer a navigation question, but restart recovery needs real state transitions.

**Done when:** the question and the deciding observation are written at the top of the prototype.

### 2. Pick the branch

- **"Does this logic or state model feel right?"** → read [logic prototype](references/logic.md): one shareable HTML file driving a pure module.
- **"What should this look like?"** → read [UI prototype](references/ui.md): several radically different variants on one route, switched with `?variant=`.

If the question is ambiguous and the user isn't reachable, follow the surrounding code (a backend module → logic; a page or component → UI) and state that assumption at the top.

**Done when:** one branch is chosen.

### 3. Build it, throwaway from day one

- Place it beside what it prototypes, named so nobody mistakes it for production, in a marked scratch location or on a `prototype/<name>` branch or worktree.
- Make it run with one command or one double-click.
- Keep state in memory unless persistence is the question; then use a scratch store whose name says it can be wiped.
- Skip tests, hardening and abstractions that wouldn't improve the answer.
- Show the full relevant state after every action or variant switch.
- Make every substitute for a real service or data source visible, so it can't pass as evidence about integration.

**Done when:** the user can run it and watch the state change.

### 4. Capture the verdict

Let the human judge appearance and intent. Record the question, the observations and environment, and the verdict: **supported**, **rejected** or **inconclusive**, with the assumptions the prototype did not test. Carry the validated decision into the spec or task. Keep the prototype itself as a **primary source**: commit it to a throwaway branch, out of main, and link that branch from the work record. An inconclusive result needs a smaller follow-up or a named blocker, never silent promotion into implementation. Prototype code is rewritten and verified before it ships.

**Done when:** the verdict and a link to the kept prototype are in the work record.
