---
name: ui-design
description: "Research and plan user flows, interaction states and visual decisions for web or native interfaces before implementation, or investigate an existing UI problem. Skip for backend-only work or a clear UI fix with no design uncertainty."
---

Read project instructions, existing design tokens/components, the relevant interface and supplied evidence. Identify the actual audience, platform, task and observable success. Keep product-specific requirements in that project; do not assume a particular age group, industry, stack or visual style.

Establish a baseline and name the decision or observed friction. Distinguish observed behavior from hypotheses. Use [research](../research/SKILL.md) for consequential evidence gaps: prefer relevant first-party guidance, original research and actual project/user observations. Record source, date, audience/platform and limitations. Inspiration is not usability evidence or permission to reuse assets.

Sketch entry, action, feedback, recovery and exit before visual polish. Include only relevant states, such as empty/loading/error/success, validation, permissions, interruption or unavailable connectivity. For data-driven interfaces, identify the real API/data contract; mark mocks and assumptions explicitly.

Reuse the project's visual system. Compare a small number of materially different options only where a real choice remains. Use [prototype](../prototype/SKILL.md) for a named uncertainty; match the fidelity and platform to the question. Static images cannot establish keyboard, touch, responsive layout, audio or actual data behavior.

Work through unresolved visual/product choices with the human; preserve choices already authorized. Record the selected direction, rationale, evidence and remaining gaps using the [optional design record](../../templates/design.md) or the existing project convention. Do not invent user-study results or claim usability from AI personas. Add a separate record only when it helps later work.

Carry agreed behavior and verification into the spec/task by reference. Keep requirement ids and acceptance criteria authoritative there. Full-stack work joins UI states to service/data outcomes; do not split every issue into frontend then backend layers. Backend-only tasks use the core workflow without this stage.

Plan checks proportionate to the change: actual flow/state behavior, responsive layouts, keyboard/focus/semantics or native accessibility, text/contrast, relevant locales and motion. Use applicable platform guidance and the project's accessibility target. Automated checks supplement runtime and human evaluation; they do not establish conformance or user success by themselves.

Return decisions, linked artifacts, evidence gaps and the next implementation/verification step. Feed defects found during actual use through [QA](../qa/SKILL.md). Read [project routes](../../docs/project-routes.md) when combining UI, frontend and backend work.
