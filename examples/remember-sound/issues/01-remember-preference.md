---
{
  "schema_version": 1,
  "id": "01-remember-preference",
  "status": "ready",
  "execution": "afk",
  "review": "human",
  "blocked_by": []
}
---
# Remember the parent's effects preference

Illustrative issue for a fictional app; not an active implementation request.

## Context

[Feature PRD](../spec.md).

## Requirements covered

R1 and R3 in the parent PRD.

## Expected behavior

The effects toggle changes playback, persists the choice locally, and restores it after restart. Missing or invalid data uses the agreed default. Narration remains independent.

## Acceptance criteria

- [ ] Effects-off remains off after a normal restart.
- [ ] Changing the preference controls game effects without changing narration.
- [ ] Missing or invalid stored data uses the default without breaking settings.

## Verification

Test through the public settings interface and observed effects behavior. Exercise a normal reload plus missing/invalid storage. Verify the toggle and playback on a device before acceptance.

## Scope

Implement the narrow settings-to-storage-to-playback path. The separately tracked delayed-startup scenario is handled by the next issue.

## Evidence

No implementation or verification has been performed in this example.
