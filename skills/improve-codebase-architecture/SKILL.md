---
name: improve-codebase-architecture
description: Find evidence-backed architecture improvements in a difficult or frequently changed area and turn a selected candidate into scoped work.
---

Use this route when the user requests an architecture assessment, repeated changes are hard to isolate, or missing test boundaries obstruct a real feature. Ordinary feature work does not require a whole-codebase review.

Scope the assessment to the named area. Otherwise inspect recent change hotspots before widening the search. Read existing project architecture guidance and consequential decisions.

Look for demonstrated friction: one concept scattered across many files, duplicated behavior, leaky boundaries, interfaces nearly as complex as their implementation, or bugs that cannot be tested through public behavior. File size or the number of helpers alone is not a reason to refactor.

For each useful candidate, report the current structure, specific evidence, a proposed direction, expected benefit, migration/verification approach and material risks. Prefer a simple public interface hiding meaningful behavior. Preserve observable behavior unless a requirement explicitly changes it. Use a small before/after diagram when it makes the decision easier.

Recommend the strongest candidate; distinguish evidence from speculation. The default output is an assessment, not a repository-wide rewrite. If the user already authorized a particular refactor, continue within that scope rather than asking again.

Take a selected candidate through [grill](../grill/SKILL.md) when decisions remain, then [write-spec](../write-spec/SKILL.md), [plan-tasks](../plan-tasks/SKILL.md) and [implement](../implement/SKILL.md) in proportion to its size. A small, clear change can proceed directly. Preserve behavior with meaningful tests and record consequential tradeoffs where future readers need them.

Documentation drift can be fixed as a narrow documentation task. Update the authoritative document instead of making a second competing architecture manual. After delivery, use [retro](../retro/SKILL.md) for environment improvements grounded in what happened.
