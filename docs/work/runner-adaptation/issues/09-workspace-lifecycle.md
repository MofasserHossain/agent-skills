---
{
  "schema_version": 1,
  "id": "09-workspace-lifecycle",
  "status": "draft",
  "execution": "afk",
  "review": "human",
  "blocked_by": [
    "05-docker"
  ]
}
---
# Manage workspaces, verified archives and scoped disk cleanup

## Context
[Workspace lifecycle](../workspaces.md) and [runner specification](../spec.md).

## Requirements covered
R9; R6 runtime ownership and evidence export.

## Expected behavior
Multiple projects can retain independent workspaces under a configurable root and reclaim disposable resources without losing work or deleting original repositories.

## Acceptance criteria
- [ ] Stable project/workspace identities distinguish same-named repos; runtime-private checkouts have accurate locations.
- [ ] Project setup/preview/archive hooks run only in their declared context; active writers and shared resources are protected.
- [ ] Archive exports unique commits, required changed files and task evidence outside disposable resources and verifies restoration.
- [ ] Purge refuses active, unpreserved, externally referenced or unowned resources; interruption and retry remain inspectable.
- [ ] List/cleanup preview shows state, available size measurements, removal candidates and refusal reasons without deletion.
- [ ] Automatic retention requires explicit policy; pinned workspaces and recovery-archive retention are separate controls.
- [ ] Original repositories and other workspaces remain untouched.

## Verification
Use disposable paths and fake runtimes for every acceptance case in the lifecycle document. Run the full unit suite, workflow check and both package checks. No machine-wide prune, live deletion, account configuration or external worker call.

## Scope
Implement the lifecycle against the runtime and claims contracts. No automatic remote branch deletion, publication, merge or new UI platform.

## Evidence
Local-checkout foundation implemented in tools/workspaces.py with disposable Git tests for independent creation, verified clean Git archives, scoped purge/restore, locks and refusal cases. Docker resources, hooks, worker supervision, dirty-work exports and automatic retention remain unimplemented. This task is not complete.
