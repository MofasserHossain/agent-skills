# Tracker conventions

Choose one authoritative tracker per feature.

## Local

One task file per issue under docs/work/<feature>/issues/. Metadata carries identity, status, execution/review and blockers; the body carries behavior, acceptance criteria and evidence. Work records may be committed with project source unless that project chooses a private location.

## GitHub

A spec may be a parent issue; implementation tasks are flat sub-issues. Use native blocking relationships where available. Parent membership does not itself create a dependency.

The issue owns status and acceptance evidence. Local research/prototypes/spec documents can remain linked references. Execute tracker operations with available authorized tools; the v0.1 helper does not implement a GitHub API client.

## Publish a local draft

Review the breakdown, publish the tasks when requested, record id/URL mappings, and explicitly switch authoritative status to GitHub. Preserve local drafts as references instead of continuing to edit both status copies.

Linear and other trackers can implement the same contract later. An incoming Linear ticket can be an intake source even when implementation work is tracked elsewhere; preserve the original link and clarify update ownership.
