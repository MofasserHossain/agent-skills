---
name: ui-design
description: "Settle interface flows, states and visual direction before building, or investigate a UI problem. Use when interaction, layout or usability is uncertain; skip for backend-only work."
---

Turn an uncertain interface into decisions that are ready to build: the flow, its states, the data it depends on and the visual direction, all within the project's own design system. Product-specific rules stay in the project; never assume an audience, industry, stack or style.

## Process

### 1. Establish the baseline

Read the project's instructions, its design tokens and components, the relevant interface and the supplied evidence. Name the actual audience, platform, task and observable success, and the decision or friction at stake. Keep observed behavior apart from hypotheses. For a consequential evidence gap, invoke the `research` skill. Prefer first-party guidance, original research and real project or user observations, and record each source's date, audience, platform and limits. Inspiration is neither usability evidence nor permission to reuse assets.

**Done when:** the decision to make, and the evidence behind it, are written down.

### 2. Sketch the flow before the pixels

Map entry → action → feedback → recovery → exit. Include only the relevant states: empty, loading, error, success, validation, permissions, interruption, offline. For data-driven screens, name the real API or data contract and mark mocks and assumptions. Walk the flow with representative content and with the edge conditions that could change the design: long text, missing data, small screens, interrupted input. Account for how entered work survives navigation, errors and retries.

**Done when:** every relevant state has defined behavior or a named open question.

### 3. Choose the direction

Reuse the project's visual system, and check existing components before proposing new variants. Compare a few materially different options only where a real choice remains. For a named uncertainty, invoke the `prototype` skill and match its fidelity and platform to the question; static images can't establish keyboard, touch, responsive layout, audio or real-data behavior. Settle the open visual and product choices with the human, and keep choices that are already authorized. Never invent user-study results or claim usability from AI personas. If a collaborator skill isn't installed, continue within this procedure where it suffices, or report the missing capability.

**Done when:** a direction is chosen, with its rationale and evidence.

### 4. Record and hand off

Record the direction, rationale, evidence and gaps in the [design record](templates/design.md) or the project's own convention, but only when that helps later work. Carry the agreed behavior and checks into the spec or task by reference; requirement labels and acceptance criteria stay authoritative there. Full-stack work joins UI states to service and data outcomes in the same slices, never frontend layers first and backend later. Plan checks in proportion to the change: real flow and state behavior, responsive layouts, keyboard and focus (or native accessibility), text and contrast, locales and motion, measured against the project's accessibility target. Automated scans supplement runtime and human evaluation; they don't establish conformance. Read [project routes](references/project-routes.md) when one feature spans UI, frontend and backend. Send defects found in real use through `qa`.

**Done when:** the consequential interaction choices are settled, every relevant state has defined behavior, data assumptions are explicit and remaining checks have owners. A missing human choice or API contract is named against the behavior it affects; never call the design approved while one remains.
