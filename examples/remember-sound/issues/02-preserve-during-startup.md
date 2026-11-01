---
{
  "schema_version": 1,
  "id": "02-preserve-during-startup",
  "status": "ready",
  "execution": "afk",
  "review": "human",
  "blocked_by": ["01-remember-preference"]
}
---
# Preserve the saved preference during slow startup

Illustrative issue for a fictional app; not an active implementation request.

## Context

[Feature PRD](../spec.md). Requires the first issue's integrated settings behavior.

## Requirements covered

R2 in the parent PRD.

## Expected behavior

A delayed read of an effects-off preference finishes without startup replacing it with the default. Once loaded, later parent changes persist normally.

## Acceptance criteria

- [ ] A controlled slow read restores the saved choice.
- [ ] Restarting after that slow load still restores the saved choice.
- [ ] A later deliberate parent change is saved and restored normally.

## Verification

Hold the storage read pending through the public provider's startup, complete it with effects-off, then reload again and observe the preference. Use observed saved behavior as the assertion rather than mirroring the implementation's internal flags.

## Scope

Loading/persistence ordering for this setting. No generic storage framework or unrelated startup refactor.

## Evidence

No implementation or verification has been performed in this example.
