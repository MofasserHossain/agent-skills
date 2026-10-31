---
name: review
description: "Review a bounded change against its originating requirements and project standards, with actionable evidence."
---

Pin a revision/diff boundary and identify the originating spec/task. Read applicable project standards.

Evaluate two separate questions:
- Spec: missing/incorrect behavior, scope drift and unsupported acceptance claims.
- Standards: correctness, maintainability and project conventions.

Inspect changed code and relevant surrounding behavior. Use targeted checks to substantiate consequential concerns. Leave mechanical formatting to existing tools. Distinguish definite defects from judgment calls.

For small changes, one focused pass is enough. Independent review agents are optional when authorized and valuable; do not multiply reviewers by default.

Report findings with location, consequence and evidence. Report no-spec/no-runtime-evidence limitations explicitly. Code review is not a substitute for runtime QA. Apply fixes or post external reviews only within the task's authorization.
