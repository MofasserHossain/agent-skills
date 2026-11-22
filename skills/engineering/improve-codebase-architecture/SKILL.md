---
name: improve-codebase-architecture
description: "Find modules worth deepening, with evidence from real changes, and take one into the main flow. Use when an area keeps hurting to change or test, or an architecture review is requested."
---

Survey part of the codebase for **deepening opportunities**: places where a **shallow** module, whose interface is nearly as complex as its implementation, could become a **deep** one, with a lot of behavior behind a small interface. The aim is changes that stay local and behavior that can be tested through its interface. The default output is an assessment, not a rewrite.

Use these words exactly:

- **Module**: anything with an interface and an implementation.
- **Interface**: everything a caller must know, including invariants, error modes and ordering.
- **Seam**: where an interface lives, so behavior can change without editing callers.
- **Depth**: behavior per unit of interface.
- **Leverage**: what callers gain from depth.
- **Locality**: what maintainers gain, because change and bugs concentrate in one place.

Prefer these terms over "component", "service", "API" or "boundary".

## Process

### 1. Scope before you scan

Take the direction the user named. Otherwise, walk back through recent history (`git log --oneline`, the files changed most often) and start with the **hot spots**: deepening pays off where code keeps changing. Read the project's glossary and the recorded decisions for that area.

**Done when:** the area to survey is named, with the reason for choosing it.

### 2. Collect demonstrated friction

Explore, in a subagent with a fresh context window when one is available, and note where:

- understanding one concept means bouncing between many small modules;
- a module is shallow;
- pure functions were extracted for testability while the real bugs hide in how they're called;
- coupling leaks across a seam;
- behavior can't be tested through the current interface.

Apply the **deletion test** to each suspect. Imagine deleting the module: if its complexity reappears across many callers, it earns its keep; if the complexity merely moves, the module was a pass-through. File size or helper count alone is never a reason to refactor.

**Done when:** each candidate rests on a representative change or failure path, showing what must be understood or edited today.

### 3. Present the candidates

Give each candidate a card:

```
### <Name the deepening, e.g. "Collapse the order intake pipeline">
Strength: Strong | Worth exploring | Speculative
Files: <the modules involved>
Problem: <one sentence: what hurts, with the evidence>
Solution: <one sentence: what would change>
Wins: <locality, leverage and test gains, a few words each>
Before → after: <a small diagram, when it makes the decision easier>
Risks and migration: <compatibility obligations; how each intermediate state is verified>
```

Compare each candidate with leaving the structure alone or making a smaller local fix; an attractive abstraction is not evidence for itself. Flag a candidate that contradicts a recorded decision only when the friction justifies reopening that decision. Recommend the strongest candidate, or say that none has enough support. Don't propose interfaces yet: ask which candidate to explore, unless the user already authorized a particular refactor, in which case continue within that scope.

**Done when:** a reviewer can locate the evidence, weigh the trade-off and choose a bounded next step.

### 4. Take the chosen one into the flow

Invoke the `grill-me` skill to settle the deepened module's shape: what sits behind the seam, its dependencies, and which tests survive. Then use `to-spec`, `to-tasks` and `implement` in proportion to the size of the change; a small, clear change can go straight to `implement`. Keep observable behavior unless a requirement changes it. When the user rejects a candidate for a reason a future survey would need, offer to record that reason as a decision so the candidate isn't suggested again. Fix documentation drift as a narrow task in the authoritative document, not in a second architecture manual. After delivery, `retro` records environment improvements grounded in what happened. If a named skill isn't installed, continue within this procedure where it suffices, or report the missing capability.

**Done when:** the chosen candidate has a next skill and an input, or the user has stopped.
