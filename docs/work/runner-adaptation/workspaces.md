# Workspace organization and archival

The full lifecycle below is the target design. Its standalone local-checkout foundation is implemented in tools/workspaces.py; see [commands and current limits](../../workspaces.md). Docker, worker/process supervision, hooks and retention are not implemented. The workspace root requested for this user is `~/mofasser-workspace`; make it configurable. One manager supports many registered projects and many workspaces per project, while ordinary execution in an existing checkout remains available.

## Layout and ownership

```text
mofasser-workspace/
  <project-key>/
    workspaces/<workspace-id>/     Disposable checkout when stored on the host
    records/<workspace-id>/        Manifest, run references and lifecycle journal
    archives/<workspace-id>/       Verified recovery artifacts after archival
```

Use a stable project key incorporating repository identity, not just its display name: two repositories can both be named app. A runtime-private checkout lives inside the sandbox instead; its manifest records that location rather than pretending the host workspace folder contains it. Records and recovery artifacts must live outside the checkout/volume being removed. Keep credentials and generated runtime output out of Git.

The manager owns creation, claims, runtime identity, export and deletion. Project configuration owns setup, preview, verification and cleanup commands. Reuse existing commands; optional setup.sh, run.sh and archive.sh are project hooks, not a new mandatory script convention. Each runtime/checkout has one active writer. Allocate ports, databases and temporary resources per workspace; lock genuinely shared devices/services.

## Lifecycle

Create -> ready -> running -> review -> stopped -> archived -> purged.

These describe workspace resources, not a second task status board. Stopped means execution has ended but disk is still occupied. Archived means work and recovery evidence are preserved and owned services stopped. Purged means disposable checkout/runtime resources have been removed; it does not mean the compact archive was deleted. A failed hook or export leaves a recoverable state and prevents claiming reclamation succeeded.

Normal execution in a pre-existing user checkout is unmanaged unless explicitly adopted; cleanup never deletes that original repository. Creating a workspace creates a local branch, not automatic remote publication. Dirty source inclusion must be selected explicitly and recorded.

## Archive before reclaiming space

1. Acquire workspace ownership and refuse active workers, checks, previews or other consumers. Stop owned services gracefully and confirm they actually stopped.
2. Inventory tracked/untracked changes, local-only commits and required ignored artifacts. A merged PR or a clean Git status alone is insufficient: ignored configuration/data and unpushed history can still be unique. Explicitly regenerable dependencies/caches can be omitted; unknown ignored material prevents automatic purge until classified.
3. Preserve required work using a verified Git export plus a manifest and necessary file artifacts, or verify the exact required history is durably available remotely. Export the task evidence and pending decisions too. Validate local exports by restoring them in a disposable checkout. A patch alone does not preserve untracked files, binary content, local history or required data.
4. Run the project's cleanup hook for resources it created, recording the outcome. The manager still verifies preservation and deletion eligibility; a hook exit of zero is not proof that all work was saved.
5. Mark archived only after durable preservation succeeds. Reclaim the managed checkout, sandbox and explicitly workspace-owned volumes when requested or allowed by an explicit retention policy. Record actual removal results. Resume purged work by restoring a new checkout/runtime from the archive, not by assuming deleted processes can restart.

Validate resolved paths, ownership markers, runtime ids and resource references immediately before deletion. Refuse paths outside the configured root, symlink substitutions, the original source checkout and resources used by another workspace. Use runtime-specific removal operations; never issue a machine-wide Docker prune to archive one workspace. A stopped sandbox/volume can still occupy disk; image caches may be shared and require a separate policy.

## Retention and visibility

Provide workspace listing with project, lifecycle state, last activity, runtime and measured disk usage where available. Separate checkout, runtime/volume, archive and shared-cache sizes; label unavailable values and do not promise estimates equal reclaimed bytes.

Cleanup previews list exact owned resources, estimated savings and reasons an item cannot be removed. Automatic cleanup is disabled until the user chooses a retention policy. A configured policy may reclaim safely archived disposable resources after a chosen interval or when a configured budget is exceeded. Age or budget pressure never overrides missing evidence, active use or ownership checks. Protect/pin important workspaces.

Keep compact archive records under their own retention budget. Deleting the recovery archive is a separate explicit action or previously authorized policy, with its own inventory; otherwise archives themselves can grow without bound. No fixed age or disk threshold is assumed by this design.

## Acceptance cases

Use disposable directories and fake runtimes. Cover active workers; local-only commits; untracked and binary changes; unknown ignored files; failed export/restore; cleanup-hook failure; shared-volume protection; external-path/symlink swaps; interrupted removal and retry; archive restoration; pinned workspaces; and a dry run that changes nothing. Verify original project repositories remain untouched. No live Docker deletion is needed for these tests.
