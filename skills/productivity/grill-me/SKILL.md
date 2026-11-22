---
name: grill-me
description: "Grill the user relentlessly about a plan until every decision is settled and recorded. Use when product or design choices are open, an idea needs stress-testing, or the user says 'grill me'."
---

Interview the user relentlessly until you share one understanding of the work. Map the open decisions as a **design tree**: each decision branches into the decisions that depend on it.

## Process

### 1. Load what is settled

Read the brief, the project's instructions and recorded decisions, and its glossary when it has one. Mark what is already settled; never ask it again.

**Done when:** you have the starting tree: settled decisions, open decisions, and which open ones depend on others.

### 2. Ask in rounds

The **frontier** is every open decision whose prerequisites are settled: what you can ask now without guessing at answers you haven't heard. Ask the whole frontier in one round, numbered, each with your recommendation:

```
**Q1 — <short title>**: <the question, with options when they help>
→ Recommended: <your answer, with a one-line reason>
```

Word each question so that "yes" accepts your recommendation. Use concrete examples and counterexamples. A question that depends on another question still open belongs in a later round. Then wait for the answers.

**Done when:** the round is sent and the user has answered it.

### 3. Find facts yourself

**Facts are your job; decisions are the user's.** When a question needs a fact from the code, docs or environment, look it up instead of asking, in a subagent with a fresh context window when one is available. Only the questions downstream of a running lookup wait for it. Invoke the `research` skill for a factual gap outside the project, and the `prototype` skill when only something runnable or visible can settle a choice; if either isn't installed, make the narrowest direct check yourself. Stop widening the interview when the remaining uncertainty can't change scope, acceptance or implementation.

**Done when:** no question asks the user for something you could have looked up.

### 4. Record as you go

- **Decision:** write it with its reason where the feature keeps its records (brief, spec or decision log), the moment it settles.
- **Term:** when a word is fuzzy or overloaded ("account" meaning two things), propose one precise term and update the project's glossary with the term, a one-sentence definition and an `_Avoid_:` line for the rejected synonyms.
- **ADR:** offer one only when the decision is hard to reverse, surprising without context and the result of a real trade-off; otherwise skip it.

**Done when:** every settled decision is written down with its reason.

### 5. Close the tree

Recompute the frontier after each round and continue. Before ending, check that the examples and counterexamples agree with the recorded rules, and that every remaining open decision has an owner or a next investigation. An unanswered question is not agreement, and you never supply the human's side of the exchange.

**Done when:** the frontier is empty, or every open branch has an owner, and the user confirms the shared understanding. Then continue any authorized work whose prerequisites are settled.

## Too big for one session

When the effort is too uncertain for one session, keep a low-resolution **decision map**: settled decisions with links, the open frontier, blockers, and a "not yet specified" list for questions that can't be phrased sharply yet. Resolve one ready decision per session. This is planning, not a build backlog.
