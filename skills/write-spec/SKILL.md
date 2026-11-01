---
name: write-spec
description: "Record settled decisions as a buildable specification for multi-session work; use after discovery, not to restart it."
---

Read the brief, decisions and relevant research/prototype verdicts. Synthesize rather than repeating the interview. Flag missing implementation-changing decisions instead of inventing them.

Use [spec template](../../templates/spec.md). Explain user behavior with concrete examples and explicit scope. Include constraints, consequential decisions and measurable acceptance criteria.

Give distinct requirements stable labels such as R1 and R2 when the work spans several issues. Preserve those labels through revisions so tasks and QA can point to the agreed behavior. A standalone small task does not need an invented PRD.

Identify existing public boundaries for meaningful tests. Record what automated checks can establish and what requires runtime/human review. Agree materially new testing boundaries during planning so routine implementation does not repeatedly interrupt the user.

Keep requirements and decisions durable; implementation navigation pointers can be separate and refreshed later. Avoid long lists of repetitive user stories that add no distinct behavior.

Publish to the chosen location/tracker only within authorization. The spec is ready when another executor can understand the outcome and how it will be judged.

Before declaring the spec ready, trace each acceptance criterion to an agreed requirement and a feasible check. Remove invented requirements and identify criteria whose evidence cannot yet be obtained. A refactor may specify interfaces and invariants instead of forcing user stories.
