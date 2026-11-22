---
name: code-review
description: "Review a diff on two separate axes: Spec (does it do what was asked?) and Standards (does it follow project rules?). Use when a change, branch or PR needs review."
---

Review the change between a **fixed point** and the current revision on two axes, and report them separately:

- **Spec:** does the change faithfully implement the originating task or spec?
- **Standards:** does it follow the project's documented standards and conventions?

**Why two axes:** code can follow every standard and still build the wrong thing, or do exactly what was asked while breaking every convention. In a single list, one axis hides the other.

## Process

### 1. Pin the fixed point

Use the commit, branch, tag or merge-base the user named; ask when there is none. Confirm that it resolves (`git rev-parse <ref>`) and that `git diff <ref>...HEAD` is not empty, and note the commits (`git log <ref>..HEAD --oneline`). Include uncommitted work only when the user intends it.

**Done when:** the diff command and the reviewed revision are recorded.

### 2. Find the spec

Look in this order: issue or task references in the commits or branch name; a path the user passed; a spec or task in the project's work folder that matches the branch or feature. If you find none, ask. When there genuinely is none, the Spec axis reports "no spec available".

**Done when:** the spec source is named, or its absence is recorded.

### 3. Find the standards

List every file that documents how code should be written: coding standards, CONTRIBUTING, project instructions. Read the [smell baseline](references/smell-baseline.md), which applies even when a project documents nothing. A documented project standard always overrides the baseline, and a baseline smell is always a judgement call. Skip anything that tooling already enforces.

**Done when:** the standards sources are listed.

### 4. Review each axis

Inspect the changed code and the surrounding behavior it affects. Run a targeted check to substantiate any consequential concern.

- **Spec:** requirements that are missing or partial; behavior nobody asked for (scope creep); requirements that look implemented but wrong; acceptance claims without evidence. Quote the spec line for each finding.
- **Standards:** each breach, with the standard it breaks (file and rule); each baseline smell, named, with the hunk quoted.

For a small change, one focused pass per axis is enough. For a large change, and when authorized, give each axis its own subagent with a fresh context window. Pass it the diff command, the commit list and only its own sources: the spec for one, the standards and the full smell baseline for the other. Cap each report at about 400 words.

**Done when:** every finding has a location, a consequence and evidence, and is labelled as a definite defect or a judgement call.

### 5. Report

```
## Spec
<findings, most severe first, or "No findings" or "No spec available">

## Standards
<findings, most severe first, or "No findings">

Summary: <n> spec and <n> standards findings. Worst per axis: <one line each>. Reviewed: <revision>.
```

Don't merge or rerank findings across the axes, and don't pick one overall winner. Separate blocking findings from optional suggestions, and state what wasn't inspected, such as a missing spec or runtime evidence. Code review doesn't replace runtime QA; point to `qa` for behavior that must be seen running. A clean verdict means no actionable defect within this scope; it never turns unperformed checks into passes. Apply fixes or post external comments only within the task's authorization.

**Done when:** the report names the reviewed revision and accounts for both axes.
