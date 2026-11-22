---
name: research
description: "Answer a factual question that blocks a decision, from primary sources, with cited findings. Use when a decision waits on documentation, API, version or platform facts."
---

Resolve one factual uncertainty that a decision is waiting on, using **primary sources**: the project itself, official documentation, source code, specifications and first-party APIs, rather than a secondary write-up of them. Research informs the decision; it never makes a product decision silently.

## Process

### 1. Bound the question

State the question, the decision it informs, and what evidence would support the option, rule it out or leave it open. Reuse existing research when it still answers the question.

**Done when:** you would know when to stop.

### 2. Delegate when it pays

When the reading is long and independent, and delegation is authorized, run it in a background subagent with a fresh context window. Give it a narrow brief (the question, the decision and where to save the findings) and keep working meanwhile. Otherwise research it yourself.

**Done when:** the research is running in a subagent, or you are doing it directly.

### 3. Read primary sources

Start with the project's own sources, then official documentation, source code or other first-party evidence. Follow each claim back to the source that owns it, and check time-sensitive claims at that source. Check version, platform and operating conditions before applying a source to this project. When credible sources conflict, explain the mismatch and which claim stays uncertain; never average them.

**Done when:** the evidence settles the decision, or the exact missing source or experiment is named.

### 4. Record the findings

Write the answer with its supporting evidence, a source link for each claim, the date, the limits of applicability and the implication for the decision. Keep observed facts apart from inference, and any recommendation apart from measured results. When future sessions will benefit, save one focused Markdown note where the project keeps such notes; if it has no convention, choose a sensible place and say where. Leave out unrelated search results and copies of whole manuals.

**Done when:** the answer, its evidence and its limits are recorded or returned.
