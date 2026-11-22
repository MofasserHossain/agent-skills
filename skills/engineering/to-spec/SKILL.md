---
name: to-spec
description: "Turn settled decisions into a written spec for multi-session work, without re-interviewing. Use after grilling when work spans several tasks or sessions, or when asked for a spec or PRD."
---

Synthesize what is already settled into a **spec** (you may know it as a PRD): a buildable description of the feature that another executor can understand and judge. **Don't interview again.** Flag any missing decision that would change the implementation; never invent one. A small standalone task needs no spec.

## Process

### 1. Gather the decisions

Read the brief, the settled decisions, and any research or prototype verdicts. Explore the code wherever the spec must describe existing behavior, using the project's glossary terms and respecting its recorded decisions.

**Done when:** every decision the spec relies on has a source, and missing decisions are listed as open.

### 2. Agree the test seams

Sketch the **seams** where behavior will be tested: prefer existing public boundaries, and the highest one that can observe the behavior. Fewer seams are better. Note what automated checks can establish and what needs runtime or human review. Confirm materially new seams with the user now, so implementation doesn't stop to ask later.

**Done when:** the user accepts the seams, or the spec reuses existing boundaries unchanged.

### 3. Write the spec

Use the [spec template](templates/spec.md).

- Describe behavior from the user's side, with concrete examples and explicit exclusions.
- Give each distinct requirement a stable label (R1, R2) that tasks and QA will cite, and keep the labels stable through revisions.
- Prefer one example per distinct behavior over long lists of near-identical user stories. A refactor can specify interfaces and invariants instead.
- Leave out file paths and code snippets, which go stale. The exception is a prototype snippet that states a decision more precisely than prose (a state machine, a type shape); inline only that part and say it came from the prototype.

**Done when:** every section is filled from settled material or deliberately omitted.

### 4. Check readiness

Trace each acceptance criterion to a requirement and a feasible check. Remove invented requirements, and mark criteria whose evidence can't be obtained yet. Any unresolved question that would change the implementation keeps the spec from being AFK-ready.

**Done when:** another executor could build and judge the work from the spec alone. Publish it to the chosen location or tracker only within existing authorization.
