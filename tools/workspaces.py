#!/usr/bin/env python3
"""Manage independent local checkouts and verified cold archives; no agent dispatch."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import uuid

DEFAULT_ROOT = Path.home() / "mofasser-workspace"
NAME = re.compile(r"[a-z0-9][a-z0-9-]{0,63}\Z")
STATES = {"creating", "ready", "archiving", "archived", "purging", "purged", "restoring", "failed"}


class WorkspaceError(Exception):
    pass


def git(directory, *arguments):
    # Do not execute repository hooks when checking out or restoring a workspace.
    result = subprocess.run(["git", "-c", "core.hooksPath=" + os.devnull, *arguments],
                            cwd=directory, capture_output=True, text=True, timeout=120)
    if result.returncode:
        raise WorkspaceError(f"Git {arguments[0]} failed: {result.stderr.strip()}")
    return result.stdout.strip()


def now():
    return datetime.now(timezone.utc).isoformat()


def valid_name(value):
    if not NAME.fullmatch(value):
        raise WorkspaceError("Names must contain lowercase letters, digits and hyphens (64 characters max).")
    return value


def inside(root, *parts):
    """Reject symlinks and escapes in all manager-owned path components."""
    root = Path(root).expanduser().absolute()
    if root.is_symlink():
        raise WorkspaceError(f"Workspace root cannot be a symlink: {root}")
    root = root.resolve()
    candidate = root.joinpath(*parts)
    if not candidate.resolve().is_relative_to(root):
        raise WorkspaceError(f"Path leaves workspace root: {candidate}")
    current = root
    for part in candidate.relative_to(root).parts:
        current /= part
        if current.is_symlink():
            raise WorkspaceError(f"Refusing manager-path symlink: {current}")
    return candidate


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    descriptor, temporary = tempfile.mkstemp(prefix=".record-", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w") as handle:
            json.dump(value, handle, indent=2)
            handle.write("\n")
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        Path(temporary).unlink(missing_ok=True)


def paths(root, project, workspace):
    valid_name(project)
    valid_name(workspace)
    return (inside(root, project, "workspaces", workspace),
            inside(root, project, "records", workspace),
            inside(root, project, "archives", workspace))


def load(root, project, workspace):
    checkout, record, archive = paths(root, project, workspace)
    try:
        value = json.loads((record / "workspace.json").read_text())
    except (OSError, ValueError) as error:
        raise WorkspaceError(f"Cannot read workspace record: {error}") from error
    if (not isinstance(value, dict) or value.get("schema_version") != 1
            or value.get("project") != project or value.get("id") != workspace
            or value.get("checkout") != str(checkout)
            or not isinstance(value.get("state"), str) or value["state"] not in STATES
            or value.get("runtime") != "local-checkout"
            or not isinstance(value.get("source"), str) or not Path(value["source"]).is_absolute()):
        raise WorkspaceError("Invalid workspace ownership record.")
    source = Path(value.get("source", "")).resolve()
    if source == checkout or source.is_relative_to(checkout) or checkout.is_relative_to(source):
        raise WorkspaceError("Workspace overlaps its source repository.")
    return value, checkout, record, archive


@contextmanager
def lock(record):
    if (record / "worker.lock").exists():
        raise WorkspaceError("Workspace has a worker claim; stop or recover it before changing lifecycle state.")
    marker = record / "operation.lock"
    try:
        descriptor = os.open(marker, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as error:
        raise WorkspaceError("Workspace operation is locked; inspect interrupted work before recovery.") from error
    try:
        with os.fdopen(descriptor, "w") as handle:
            json.dump({"pid": os.getpid(), "started_at": now()}, handle)
        yield
    finally:
        marker.unlink(missing_ok=True)


def transition(record, value, state, **updates):
    value.update(updates, state=state, updated_at=now())
    write_json(record / "workspace.json", value)


def clean_snapshot(checkout):
    if (not checkout.is_dir() or not (checkout / ".git").is_dir()
            or (checkout / ".git").is_symlink()):
        raise WorkspaceError("Workspace must be a standalone Git checkout.")
    if Path(git(checkout, "rev-parse", "--show-toplevel")).resolve() != checkout.resolve():
        raise WorkspaceError("Git workspace root does not match its ownership record.")
    if git(checkout, "status", "--porcelain", "--untracked-files=all", "--ignored"):
        raise WorkspaceError("Workspace has changed, untracked or ignored files. Preserve them before archival/purge.")
    if any(line and (line[0].islower() or line[0] == "S")
           for line in git(checkout, "ls-files", "-v").splitlines()):
        raise WorkspaceError("Sparse/assume-unchanged files require inspection before archival.")
    if any(line.startswith("160000 ") for line in git(checkout, "ls-files", "--stage").splitlines()):
        raise WorkspaceError("Submodule workspaces are not supported by this archive version.")
    unreachable = git(checkout, "fsck", "--unreachable", "--no-reflogs", "--no-progress")
    if any("unreachable commit " in line for line in unreachable.splitlines()):
        raise WorkspaceError("Unreferenced commits exist; retain them with a branch or tag before archival.")
    head = git(checkout, "rev-parse", "HEAD")
    refs = git(checkout, "show-ref")
    branch = git(checkout, "symbolic-ref", "--short", "HEAD")
    return {"head": head, "refs": refs, "branch": branch, "worktree_sha256": tree_digest(checkout)}


def digest(path):
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(checkout):
    """Compare actual files with a restored export, including modes and symlink targets."""
    entries = []
    for base, directories, files in os.walk(checkout, followlinks=False):
        base = Path(base)
        if base == checkout:
            directories[:] = [name for name in directories if name != ".git"]
        links = [name for name in directories if (base / name).is_symlink()]
        directories[:] = [name for name in directories if name not in links]
        for name in files + links:
            path = base / name
            mode = path.lstat().st_mode
            content = os.readlink(path) if path.is_symlink() else digest(path)
            entries.append((path.relative_to(checkout).as_posix(), mode, content))
    return hashlib.sha256(json.dumps(sorted(entries)).encode()).hexdigest()


def restore_checkout(bundle, checkout, snapshot):
    # Only called for a fresh, absent checkout; never reset an existing directory.
    if checkout.exists():
        raise WorkspaceError("Restore destination already exists.")
    git(checkout.parent, "init", "--", str(checkout))
    git(checkout, "fetch", "--update-head-ok", "--no-tags", str(bundle), "+refs/*:refs/*")
    git(checkout, "symbolic-ref", "HEAD", "refs/heads/" + snapshot["branch"])
    git(checkout, "reset", "--hard", snapshot["head"])
    if clean_snapshot(checkout) != snapshot:
        raise WorkspaceError("Restored checkout differs from the archive.")


def bytes_used(path):
    total = 0
    if path.is_dir():
        for base, directories, files in os.walk(path, followlinks=False):
            directories[:] = [name for name in directories if not (Path(base) / name).is_symlink()]
            for name in files:
                item = Path(base) / name
                if not item.is_symlink():
                    total += item.stat().st_size
    return total


def create(root, source, workspace, execute=False, committed_only=False):
    valid_name(workspace)
    source = Path(source).expanduser().resolve()
    if Path(git(source, "rev-parse", "--show-toplevel")).resolve() != source:
        raise WorkspaceError("--project must name the repository root.")
    common = git(source, "rev-parse", "--git-common-dir")
    identity = (source / common).resolve()
    slug = re.sub(r"[^a-z0-9-]+", "-", source.name.lower()).strip("-")[:40] or "project"
    project = slug + "-" + hashlib.sha256(str(identity).encode()).hexdigest()[:12]
    checkout, record, _ = paths(root, project, workspace)
    managed_root = Path(root).expanduser().resolve()
    if source.is_relative_to(managed_root) or managed_root.is_relative_to(source):
        raise WorkspaceError("Workspace root and source repository must not overlap.")
    if checkout.exists() or record.exists():
        raise WorkspaceError("Workspace id already exists; choose another id or restore its archive.")
    dirty = bool(git(source, "status", "--porcelain", "--untracked-files=all"))
    if dirty and not committed_only:
        raise WorkspaceError("Source has uncommitted work. Commit it or explicitly choose --committed-only.")
    if any(line.startswith("160000 ") for line in git(source, "ls-files", "--stage").splitlines()):
        raise WorkspaceError("Submodule checkouts are not supported yet.")
    head = git(source, "rev-parse", "HEAD")
    value = {"schema_version": 1, "project": project, "id": workspace,
             "source": str(source), "checkout": str(checkout), "base_revision": head,
             "branch": "workspace/" + workspace, "runtime": "local-checkout",
             "state": "creating", "created_at": now(), "updated_at": now(),
             "committed_only": committed_only, "source_had_changes": dirty}
    if not execute:
        return {**value, "executed": False}
    for directory in (inside(root), inside(root, project), record.parent,
                      checkout.parent, inside(root, project, "archives")):
        directory.mkdir(parents=True, exist_ok=True, mode=0o700)
    record.mkdir(exist_ok=False, mode=0o700)
    with lock(record):
        write_json(record / "workspace.json", value)
        try:
            checkout.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            git(source, "clone", "--no-local", "--no-checkout", "--", str(source), str(checkout))
            git(checkout, "remote", "remove", "origin")
            git(checkout, "checkout", "-b", value["branch"], head)
            transition(record, value, "ready")
        except Exception:
            transition(record, value, "failed")
            raise
    return {**value, "executed": True}


def archive_workspace(root, project, workspace, execute=False):
    value, checkout, record, archive = load(root, project, workspace)
    if value["state"] not in {"ready", "archived"}:
        raise WorkspaceError("Workspace is not ready for archival; inspect its recorded state.")
    snapshot = clean_snapshot(checkout)
    if not execute:
        return {"id": workspace, "operation": "archive", "checkout_bytes": bytes_used(checkout),
                "executed": False, "note": "Clean committed checkout only; no processes are stopped automatically."}
    with lock(record):
        if clean_snapshot(checkout) != snapshot:
            raise WorkspaceError("Workspace changed before archival.")
        archive.mkdir(parents=True, exist_ok=True, mode=0o700)
        transition(record, value, "archiving")
        try:
            generation = "snapshot-" + uuid.uuid4().hex
            bundle = archive / (generation + ".bundle")
            git(checkout, "bundle", "create", str(bundle), "--all")
            git(checkout, "bundle", "verify", str(bundle))
            # Verify reconstruction, rather than relying on the bundle command's exit alone.
            with tempfile.TemporaryDirectory(prefix="verify-", dir=record) as temporary:
                restore_checkout(bundle, Path(temporary) / "checkout", snapshot)
            if clean_snapshot(checkout) != snapshot:
                raise WorkspaceError("Workspace changed during archival; checkout retained.")
            manifest = {"schema_version": 1, "project": project, "id": workspace,
                        "snapshot": snapshot, "bundle": bundle.name,
                        "bundle_sha256": digest(bundle), "created_at": now()}
            write_json(archive / (generation + ".json"), manifest)
            write_json(archive / "archive.json", manifest)
            transition(record, value, "archived")
        except Exception:
            transition(record, value, "failed")
            raise
    return {**value, "executed": True, "archive": str(archive), "purged": False}


def verified_archive(archive, project, workspace):
    try:
        metadata = json.loads((archive / "archive.json").read_text())
        if not isinstance(metadata, dict) or not isinstance(metadata.get("bundle"), str) or not re.fullmatch(
                r"snapshot-[a-f0-9]{32}\.bundle", metadata["bundle"]):
            raise WorkspaceError("Invalid archive bundle name.")
        bundle = archive / metadata["bundle"]
        if (metadata.get("schema_version") != 1 or metadata.get("project") != project
                or metadata.get("id") != workspace or bundle.is_symlink()
                or (archive / "archive.json").is_symlink()
                or digest(bundle) != metadata.get("bundle_sha256")):
            raise WorkspaceError("Archive ownership or checksum validation failed.")
    except (OSError, ValueError, AttributeError) as error:
        raise WorkspaceError(f"Cannot validate archive: {error}") from error
    return metadata, bundle


def purge(root, project, workspace, execute=False):
    value, checkout, record, archive = load(root, project, workspace)
    if value["state"] != "archived":
        raise WorkspaceError("Only an archived workspace can be purged.")
    metadata, _ = verified_archive(archive, project, workspace)
    if clean_snapshot(checkout) != metadata["snapshot"]:
        raise WorkspaceError("Workspace differs from its archive; deletion refused.")
    result = {"id": workspace, "operation": "purge", "path": str(checkout),
              "checkout_bytes": bytes_used(checkout), "archive_retained": str(archive), "executed": False}
    if not execute:
        return result
    with lock(record):
        # Revalidate paths, archive and current contents immediately before deletion.
        _, checkout, _, archive = load(root, project, workspace)
        metadata, _ = verified_archive(archive, project, workspace)
        if clean_snapshot(checkout) != metadata["snapshot"]:
            raise WorkspaceError("Workspace changed before deletion.")
        transition(record, value, "purging")
        shutil.rmtree(checkout)
        transition(record, value, "purged")
    return {**result, "executed": True, "state": "purged"}


def restore(root, project, workspace, execute=False):
    value, checkout, record, archive = load(root, project, workspace)
    if value["state"] != "purged" or checkout.exists():
        raise WorkspaceError("Restore requires a purged workspace and an absent checkout.")
    metadata, bundle = verified_archive(archive, project, workspace)
    if not execute:
        return {"id": workspace, "operation": "restore", "checkout": str(checkout), "executed": False}
    with lock(record):
        transition(record, value, "restoring")
        try:
            restore_checkout(bundle, checkout, metadata["snapshot"])
            transition(record, value, "ready")
        except Exception:
            transition(record, value, "failed")
            raise
    return {**value, "executed": True}


def list_workspaces(root):
    root = inside(root)
    results = []
    if root.exists():
        for marker in sorted(root.glob("*/records/*/workspace.json")):
            project, workspace = marker.parents[2].name, marker.parent.name
            value, checkout, _, archive = load(root, project, workspace)
            results.append({**value, "checkout_bytes": bytes_used(checkout),
                            "archive_bytes": bytes_used(archive)})
    return {"root": str(root), "workspaces": results,
            "note": "Logical file bytes; no shared cache/runtime usage or reclaim estimate. No process management."}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=DEFAULT_ROOT)
    commands = parser.add_subparsers(dest="action", required=True)
    commands.add_parser("list")
    create_cmd = commands.add_parser("create")
    create_cmd.add_argument("name")
    create_cmd.add_argument("--project", type=Path, required=True)
    create_cmd.add_argument("--committed-only", action="store_true")
    create_cmd.add_argument("--execute", action="store_true")
    for name in ("archive", "purge", "restore"):
        cmd = commands.add_parser(name)
        cmd.add_argument("project_key")
        cmd.add_argument("name")
        cmd.add_argument("--execute", action="store_true")
    args = parser.parse_args(argv)
    try:
        if args.action == "list":
            result = list_workspaces(args.root)
        elif args.action == "create":
            result = create(args.root, args.project, args.name, args.execute, args.committed_only)
        else:
            operation = {"archive": archive_workspace, "purge": purge, "restore": restore}[args.action]
            result = operation(args.root, args.project_key, args.name, args.execute)
        print(json.dumps(result, indent=2))
        return 0
    except (WorkspaceError, OSError, subprocess.TimeoutExpired) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
