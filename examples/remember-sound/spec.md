# Feature PRD: remember sound effects

## Problem and outcome

Parents currently repeat their effects choice after restarting. Save the choice locally and restore it without changing narration.

## Requirements

- **R1:** A parent's effects toggle changes effect playback and survives a normal app restart.
- **R2:** While saved settings are loading, startup must not overwrite the saved choice with a default.
- **R3:** Missing or invalid saved settings use effects-on as the default without failing the settings screen.

## Behavior examples

An effects-off preference remains off after restart. A delayed effects-off read is never replaced by an effects-on write before that read completes. An invalid value behaves like a fresh install.

## Scope and exclusions

Local persistence and effects behavior only. Narration controls, accounts, sync, new sounds and a visual redesign are outside this feature.

## Verification strategy

Observe the public settings interface and effect behavior. Use a restart/reload persistence test and a controlled delayed-storage test; do not assert private helper calls as the behavior. Check the real settings toggle and playback on a device before acceptance.

## Sources

[Brief and resolved questions](brief.md).
