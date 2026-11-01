# Local workspace foundation

`tools/workspaces.py` manages independent local clones and cold Git archives. It is source-repo tooling, not an installed skill or Docker runtime. Commands preview by default; `--execute` performs the selected operation. No agent, project hook, Docker process, push or PR is started.

## Create and inspect

From this kit checkout:

```sh
python3 tools/workspaces.py create feature-login --project /path/to/project
python3 tools/workspaces.py create feature-login --project /path/to/project --execute
python3 tools/workspaces.py list
```

The default root is `~/mofasser-workspace`. To choose another root, place `--root /path/to/root` before the operation. No files are created by preview/list on an absent root. Creation requires the source repository root, a committed HEAD and no submodules. It refuses uncommitted tracked/untracked source changes unless `--committed-only` explicitly selects HEAD; ignored source files are never copied. Commit required task records and project-local skills before creation if they must be included. Snapshotting uncommitted source work is not implemented.

Each project gets a key derived from its local Git repository identity; two same-named repositories have distinct keys. Moving a source repository can change that identity. Each workspace gets its own standalone clone, branch and ownership record. Clones do not use shared/hard-linked Git objects and have no push remote; configuring an authorized remote is a separate operation. The original checkout and branch remain unchanged.

```text
mofasser-workspace/<project-key>/
  workspaces/feature-login/          Independent checkout
  records/feature-login/             Ownership and operation state
  archives/feature-login/            Verified bundle generations
```

List returns project keys, checkout paths, state, source/base revision and logical file sizes for checkout/archive. Logical bytes are not guaranteed physical disk savings. It does not measure Docker volumes or shared caches. This directory separation alone is not OS isolation; Docker provisioning is a later adapter. Never run concurrent agents in one checkout.

## Archive and reclaim storage

First stop any external agents, previews or services using the checkout. This helper does not launch, discover or stop those processes. It refuses its own concurrent operations and recorded worker claims, but cannot establish that a manually launched process is idle.

Using the project key from create/list:

```sh
python3 tools/workspaces.py archive PROJECT_KEY feature-login
python3 tools/workspaces.py archive PROJECT_KEY feature-login --execute
python3 tools/workspaces.py purge PROJECT_KEY feature-login
python3 tools/workspaces.py purge PROJECT_KEY feature-login --execute
```

This first archive format requires a clean committed checkout. It refuses changed, untracked **and ignored** files, detached HEAD, submodules and unreferenced commits. Commit work locally before archival; no push is required. Preserve unique ignored files separately and remove regenerable dependencies deliberately before retrying. It does not silently delete or omit unknown data to make an archive pass.

Archive creates a Git bundle containing all refs and verifies restoration into a disposable checkout, including the original HEAD, branches and tags. Checksums and metadata live outside the checkout. Archive does not remove the checkout. Purge rechecks ownership, archive integrity and current files/refs, then removes only the managed checkout and retains the archive/record. Symlink substitutions, modified work and original-source overlap are refused.

Every archive produces an immutable bundle generation; the latest archive manifest selects the generation used by purge/restore. Older generations remain preserved. Automatic expiry, archive deletion, pins and cache/volume cleanup are not implemented. Do not mistake a stopped runtime or a retained bundle for reclaimed space.

## Restore and failures

```sh
python3 tools/workspaces.py restore PROJECT_KEY feature-login
python3 tools/workspaces.py restore PROJECT_KEY feature-login --execute
```

Restore requires a purged workspace and absent checkout. It validates the latest bundle and reconstructs the original branches, tags, HEAD and files without a network request or push remote. Restored work can be edited, committed and archived into a new generation.

Failed create/archive/restore attempts retain their checkout/artifacts and record a failure. Interrupted operations can retain a lock or transitional state. Inspect those records before recovery; automatic stale-lock release and crash recovery are not implemented. Purge never bypasses those states. Operation locks coordinate this tool; they are not a security boundary against another process running as the same user.

The broader [workspace design](work/runner-adaptation/workspaces.md) and [runner tasks](work/runner-adaptation/issues/09-workspace-lifecycle.md) still cover future Docker execution, project hooks, supervised workers, dirty-work exports and retention policies. Tests use disposable local Git repositories; no live agent or Docker account is required.
