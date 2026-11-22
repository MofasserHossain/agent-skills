# Diagnosing bugs

For a bug that resists a first look: an intermittent failure, a regression between two known-good states, a performance drop. Redact every secret in the commands and output you show, writing `<REDACTED>` in its place.

## 1. Build a tight feedback loop

**This is the skill.** Once you have a fast, deterministic signal that goes **red** on this bug, bisection, hypotheses and instrumentation all become mechanical. Try these, roughly in order:

1. A failing test at whatever seam reaches the bug.
2. A curl or HTTP script against a running dev server.
3. A CLI run on a fixture input, diffed against known-good output.
4. A headless browser script that asserts on the DOM, console or network.
5. A replay of a captured request, payload or event log.
6. A throwaway harness that runs the smallest subset of the system.
7. A property or fuzz loop, for output that is only sometimes wrong.
8. A bisection harness (`git bisect run`) between a good state and a bad one.
9. A differential run: old version against new, or one configuration against another.
10. A step-by-step script that drives a human, as a last resort. It still captures structured output.

Then **tighten** the loop. Make it faster (cache setup, narrow scope), sharper (assert the exact symptom, not "didn't crash") and deterministic (pin time, seed randomness, isolate files and network). For a flaky bug, raise the reproduction rate by looping, parallelizing or adding stress until it is debuggable.

**Done when:** you have already run one command that is red-capable (it asserts the user's exact symptom), deterministic, fast and runnable without a human. If you catch yourself building a theory before that command exists, stop. If no loop is possible, list what you tried and ask for access, a captured artifact, or permission to instrument.

## 2. Reproduce and minimise

Confirm that the loop shows the failure the user described, not a nearby one. Then cut inputs, callers, configuration and steps one at a time, re-running after each cut.

**Done when:** every remaining element is load-bearing: removing any one of them turns the loop green.

## 3. Hypothesise

Write 3–5 ranked, falsifiable hypotheses before testing any of them, each with its prediction: "If X is the cause, changing Y makes the bug disappear." Show the ranking to the user when they are available; they often re-rank it instantly.

**Done when:** each hypothesis states the observation that would refute it.

## 4. Instrument

Each probe tests one prediction; change one variable at a time. Prefer a debugger or REPL, then targeted logs at the boundaries that separate the hypotheses. Tag every temporary log with one prefix (`[DEBUG-a4f2]`) so cleanup is a single search. For a performance regression, measure a baseline first, then bisect.

**Done when:** one hypothesis survives and observation has refuted the others.

## 5. Fix and lock it down

Turn the minimised reproduction into a failing test at a seam that exercises the real bug pattern. Watch it fail, apply the fix, watch it pass, then rerun the original loop. If no seam can reproduce the real pattern, say so: that is an architecture finding for `improve-codebase-architecture`.

**Done when:** the original loop is green, the regression test passes (or its missing seam is recorded), every tagged log is gone, and the confirmed cause is written in the commit or the result.

Adapted from the `diagnosing-bugs` skill in mattpocock/skills (MIT).
