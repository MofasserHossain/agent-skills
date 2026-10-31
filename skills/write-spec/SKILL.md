---
name: write-spec
description: "Synthesize settled requirements and decisions into a buildable specification with acceptance and verification criteria."
---

Read the brief, decisions and relevant research/prototype verdicts. Synthesize rather than repeating the interview. Flag missing implementation-changing decisions instead of inventing them.

Use [spec template](../../templates/spec.md). Explain user behavior with concrete examples and explicit scope. Include constraints, consequential decisions and measurable acceptance criteria.

Identify existing public boundaries for meaningful tests. Record what automated checks can establish and what requires runtime/human review. Agree materially new testing boundaries during planning so routine implementation does not repeatedly interrupt the user.

Keep requirements and decisions durable; implementation navigation pointers can be separate and refreshed later. Avoid long lists of repetitive user stories that add no distinct behavior.

Publish to the chosen location/tracker only within authorization. The spec is ready when another executor can understand the outcome and how it will be judged.
