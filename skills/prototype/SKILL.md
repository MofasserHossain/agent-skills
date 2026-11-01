---
name: prototype
description: "Build a small experiment to resolve a specific uncertainty about behavior, state or appearance."
---

Name the question, the smallest experiment that can answer it, and the decision the result will enable.

For logic/state, expose transitions and edge cases. For UI, provide a small number of materially different alternatives when choice is needed. Match the project's platform where that is necessary to answer the question.

Use a clearly marked scratch location or separate branch/worktree. Keep persistence disposable unless persistence is the question. Skip production hardening and broad test coverage that would not improve the experiment.

Let the human judge appearance/intent when needed. Record the question, observed outcome, verdict and a pointer to the artifact. Carry the validated decision into the spec. Prototype code needs deliberate production implementation and verification before it ships.

Before building, state the observation that would support or reject the proposed approach. Choose fidelity around that observation: a clickable mock can answer navigation questions, while restart recovery requires real state transitions. Make substitutes for real services or data visible so they do not accidentally become evidence about integration.

Conclude with supported, rejected or inconclusive, tied to the observations and environment. Preserve a reproducible way to inspect or rerun the experiment and identify which assumptions it did not test. An inconclusive experiment needs a smaller follow-up or a named blocker, not silent promotion into implementation.
