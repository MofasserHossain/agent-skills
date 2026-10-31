---
name: prototype
description: "Build a small experiment to resolve a specific uncertainty about behavior, state or appearance."
---

Name the question, the smallest experiment that can answer it, and the decision the result will enable.

For logic/state, expose transitions and edge cases. For UI, provide a small number of materially different alternatives when choice is needed. Match the project's platform where that is necessary to answer the question.

Use a clearly marked scratch location or separate branch/worktree. Keep persistence disposable unless persistence is the question. Skip production hardening and broad test coverage that would not improve the experiment.

Let the human judge appearance/intent when needed. Record the question, observed outcome, verdict and a pointer to the artifact. Carry the validated decision into the spec. Prototype code needs deliberate production implementation and verification before it ships.
