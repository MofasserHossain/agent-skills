#!/usr/bin/env python3
"""Preview or install a self-contained project workflow snapshot for Claude/Codex."""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
from pathlib import Path
import sys
import tempfile

from register_skills import destinations, RegistrationError
from skill_catalog import ALIASES, discover

KIT = Path(__file__).resolve().parents[1]
BUNDLE = ".agent-workflow"
MARKER = ".workflow-install.json"
SELECTION = ".selection.json"
LEGAL_FILES = ("LICENSE", "LICENSE.md", "LICENSE.txt", "NOTICE", "NOTICE.md", "THIRD_PARTY_NOTICES.md")
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


class InstallError(Exception):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def inventory(root):
    files = {}
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if "__pycache__" in relative.parts or path.suffix in {".pyc", ".pyo"}:
            continue
        if path.is_symlink():
            raise InstallError(f"Refusing symlink in snapshot: {path}")
        if path.is_file() and relative.as_posix() != MARKER:
            files[relative.as_posix()] = path.read_bytes()
    return files


def payload(kit, skills=None, with_runner=False):
    """Collect selected procedures and their local linked dependencies, not the source repo."""
    kit = Path(kit).resolve()
    try:
        catalog = discover(kit)
    except ValueError as error:
        raise InstallError(str(error)) from error
    available = set(catalog)
    requested = sorted({ALIASES.get(name, name)
                        for name in (skills if skills is not None else available - {"agent-workflow"})})
    if not requested or any(name not in available for name in requested):
        raise InstallError("Select existing skill names from the source kit.")
    selected = set(requested) | {"agent-workflow"}
    if with_runner:
        selected.update({"implement", "plan-tasks"})
    files = {}

    def read(relative):
        path = kit / relative
        if not path.resolve().is_relative_to(kit):
            raise InstallError(f"Dependency leaves source kit: {relative}")
        if any(parent.is_symlink() for parent in (path, *path.parents) if parent != kit and parent.is_relative_to(kit)):
            raise InstallError(f"Refusing symlink in dependency: {relative}")
        if not path.is_file():
            raise InstallError(f"Missing workflow dependency: {relative}")
        return path.read_bytes()

    def dependencies(content, relative):
        result = []
        for _, target in LINK.findall(content):
            if "://" in target or target.startswith("#"):
                continue
            if target.startswith("/"):
                raise InstallError(f"Absolute dependency in {relative}: {target}")
            result.append(Path(os.path.normpath(Path(relative).parent / target.split("#")[0])).as_posix())
        return result

    router_path = catalog["agent-workflow"].relative_to(kit).as_posix()
    pending = []
    for name in sorted(selected):
        for resource in sorted(catalog[name].parent.rglob("*")):
            if resource.is_symlink():
                raise InstallError(f"Refusing symlink in skill resources: {resource}")
            if resource.is_file():
                pending.append(resource.relative_to(kit).as_posix())
    router = read(router_path).decode()
    if with_runner:
        pending.extend(("tools/workflow.py", "tools/skill_catalog.py", "adapters/agents.json"))
    pending.extend(name for name in LEGAL_FILES if (kit / name).exists())
    while pending:
        relative = pending.pop()
        if relative in files or relative == router_path:
            continue
        content = read(relative)
        files[relative] = content
        if Path(relative).suffix == ".md":
            pending.extend(dependencies(content.decode(), relative))
    lines = []
    for line in router.splitlines():
        stage = re.search(r"^\|[^|]+\| `([^`]+)` \|$", line)
        if stage and stage[1] not in selected:
            continue
        lines.append(line)
    router = "\n".join(lines) + "\n\nOnly the stages listed above are installed. If a needed procedure is absent, report it; do not read the authoring checkout or claim the procedure ran. Add capabilities through the source installer.\n"
    files[router_path] = router.encode()
    files[SELECTION] = (json.dumps({"schema_version": 1, "requested_skills": requested,
                                  "included_skills": sorted(selected), "with_runner": with_runner}, indent=2) + "\n").encode()
    files["README.md"] = (
        "# Installed agent workflow\n\n"
        "Use the agent-workflow entry in Claude Code or Codex, or read skills/productivity/agent-workflow/SKILL.md. "
        "Project rules, .agent-workflow.json and work records belong to the project. "
        "Load only the selected stage and relevant references.\n\n"
        "Installed procedures: " + ", ".join(sorted(selected)) + ".\n\n"
        + ("Optional helper: python3 .agent-workflow/tools/workflow.py check from the project root. "
           "Run previews do not execute an agent; execution requires --execute.\n\n" if with_runner else "")
        + "This installation is independent of the authoring checkout. Update from that checkout with "
        "tools/install_project.py PROJECT --update; preview first, then add --apply. "
        "Omitting selection flags preserves the installed selection. An explicit --skills list replaces "
        "the selection; linked dependencies are included automatically. Local edits are protected. "
        "The source kit keeps its development docs, research, tests and installer.\n"
    ).encode()
    return files


def metadata(files, kind):
    return {"schema_version": 1, "kind": kind,
            "files": {name: digest(content) for name, content in sorted(files.items())}}


def entry_files(destination, bundle):
    target = os.path.relpath(bundle / "skills/productivity/agent-workflow/SKILL.md", destination)
    body = (
        "---\nname: agent-workflow\n"
        'description: "Plan, implement, review and verify work using this project’s workflow."\n'
        "---\n\n"
        f"Read [the workflow]({Path(target).as_posix()}). "
        "Keep this project as the working directory and follow its instructions. "
        "Read only the selected stage and relevant references.\n"
    )
    return {"SKILL.md": body.encode()}


def inspect(destination, files, kind, update):
    if destination.is_symlink():
        raise InstallError(f"Refusing existing symlink: {destination}")
    wanted = metadata(files, kind)
    if not destination.exists():
        return "create", None
    if not destination.is_dir():
        raise InstallError(f"Refusing existing path: {destination}")
    marker = destination / MARKER
    if marker.is_symlink():
        raise InstallError(f"Refusing symlinked ownership marker: {marker}")
    try:
        previous = json.loads(marker.read_text())
    except (OSError, ValueError) as error:
        raise InstallError(f"Unmanaged installation at {destination}; nothing overwritten.") from error
    if not isinstance(previous, dict) or previous.get("schema_version") != 1 or previous.get("kind") != kind:
        raise InstallError(f"Unmanaged installation at {destination}; nothing overwritten.")
    current = metadata(inventory(destination), kind)
    if current != previous:
        raise InstallError(f"Local edits at {destination}; preserve or reconcile them before updating.")
    if current == wanted:
        return "unchanged", previous
    if not update:
        raise InstallError(f"Snapshot differs at {destination}; review and use --update to replace an unedited installation.")
    return "update", previous


def plan(project, agent, kit, update=False, skills=None, with_runner=None):
    project = Path(project).expanduser().resolve()
    if not project.is_dir():
        raise InstallError(f"Project directory does not exist: {project}")
    kit = Path(kit).resolve()
    bundle = project / BUNDLE
    if kit == bundle or kit.is_relative_to(bundle):
        raise InstallError("Run installation from a separate source checkout, not from the destination snapshot.")
    # Validate all discovery locations before any mutation, including aliases.
    paths = destinations(agent=agent, project=project)
    if (bundle / SELECTION).is_file() and not (bundle / SELECTION).is_symlink():
        previous_selection = json.loads((bundle / SELECTION).read_text())
        if skills is None:
            skills = previous_selection["requested_skills"]
        if with_runner is None:
            with_runner = previous_selection["with_runner"]
    elif with_runner is None:
        # Preserve the helper during migration from the earlier full-copy installation.
        with_runner = (bundle / "tools/workflow.py").is_file()
    entries = [(bundle, payload(kit, skills, with_runner), "workflow-project-snapshot")]
    entries.extend((path, entry_files(path, bundle), "workflow-project-entry") for path in paths)
    result = []
    for path, files, kind in entries:
        if not path.parent.resolve().is_relative_to(project):
            raise InstallError(f"Destination leaves project: {path}")
        action, previous = inspect(path, files, kind, update)
        result.append({"path": path, "files": files, "kind": kind,
                       "action": action, "previous": previous, "project": project})
    return result


def apply(items):
    # Recheck ownership/content at the mutation boundary before changing any entry.
    for item in items:
        if not item["path"].parent.resolve().is_relative_to(item["project"]):
            raise InstallError(f"Destination leaves project: {item['path']}")
        action, previous = inspect(item["path"], item["files"], item["kind"], True)
        if (action, previous) != (item["action"], item["previous"]):
            raise InstallError(f"Installation changed during preparation: {item['path']}")
    for item in items:
        if item["action"] == "unchanged":
            continue
        path = item["path"]
        if not path.parent.resolve().is_relative_to(item["project"]):
            raise InstallError(f"Destination leaves project: {path}")
        path.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.TemporaryDirectory(prefix=".workflow-install-", dir=path.parent) as temp:
            staged = Path(temp) / "new"
            staged.mkdir()
            for relative, content in item["files"].items():
                target = staged / relative
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(content)
            (staged / MARKER).write_text(json.dumps(metadata(item["files"], item["kind"]), indent=2) + "\n")
            action, previous = inspect(path, item["files"], item["kind"], True)
            if (action, previous) != (item["action"], item["previous"]):
                raise InstallError(f"Installation changed during preparation: {path}")
            backup = Path(temp) / "previous"
            if item["action"] == "update":
                path.rename(backup)
            try:
                staged.rename(path)
            except BaseException:
                if backup.exists() and not path.exists():
                    backup.rename(path)
                raise


def choose_skills(kit):
    if not sys.stdin.isatty():
        raise InstallError("The chooser requires an interactive terminal; use --skills NAME ... or --all-skills.")
    paths = sorted(path for name, path in discover(kit).items() if name != "agent-workflow")
    print("Choose this project's skills. Nothing is preselected; required dependencies are added automatically.")
    for number, path in enumerate(paths, 1):
        description = re.search(r'^description: (.+)$', path.read_text(), re.M)
        detail = description[1].strip('"') if description else ""
        print(f"  {number}. {path.parent.name}: {detail}")
    try:
        answer = input("Enter numbers separated by commas (blank cancels): ").strip()
    except (EOFError, KeyboardInterrupt) as error:
        raise InstallError("Selection cancelled; nothing changed.") from error
    if not answer:
        raise InstallError("Selection cancelled; nothing changed.")
    try:
        numbers = [int(value.strip()) for value in answer.split(",")]
        if any(number < 1 or number > len(paths) for number in numbers):
            raise ValueError
    except ValueError as error:
        raise InstallError("Choose only numbers from the displayed list; nothing changed.") from error
    return sorted({paths[number - 1].parent.name for number in numbers})


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", type=Path)
    parser.add_argument("--agent", choices=["claude", "codex", "all"], default="all")
    selection = parser.add_mutually_exclusive_group()
    selection.add_argument("--skills", nargs="+", choices=sorted(set(discover(KIT)) | set(ALIASES)),
                        help="Select procedures; required dependencies are included. Omit on updates to preserve selection.")
    selection.add_argument("--select", action="store_true", help="Choose skills interactively, with nothing preselected.")
    selection.add_argument("--all-skills", action="store_true", help="Explicitly select every maintained procedure.")
    runner = parser.add_mutually_exclusive_group()
    runner.add_argument("--with-runner", action="store_true", dest="with_runner", default=None,
                        help="Include the optional one-task helper and its implementation dependencies.")
    runner.add_argument("--without-runner", action="store_false", dest="with_runner",
                        help="Install Markdown procedures without the execution helper.")
    parser.add_argument("--apply", action="store_true", help="Write the snapshot and discovery entries; default previews.")
    parser.add_argument("--update", action="store_true", help="Allow replacing an unedited managed snapshot after review.")
    args = parser.parse_args(argv)
    try:
        project = args.project.expanduser().resolve()
        if not project.is_dir():
            raise InstallError(f"Project directory does not exist: {project}")
        skills = args.skills
        if args.all_skills:
            skills = sorted(set(discover(KIT)) - {"agent-workflow"})
        elif args.select or (skills is None and not (project / BUNDLE).exists()):
            skills = choose_skills(KIT)
        items = plan(project, args.agent, KIT, args.update, skills, args.with_runner)
        if args.apply:
            apply(items)
        print(json.dumps({"applied": args.apply,
                          "selection": json.loads(items[0]["files"][SELECTION]),
                          "entries": [{"path": str(item["path"]), "action": item["action"],
                                       "file_count": len(item["files"]),
                                       "removed_files": sorted(set((item["previous"] or {}).get("files", {})) - set(item["files"])),
                                       "bytes": sum(map(len, item["files"].values()))}
                                      for item in items]}, indent=2))
        return 0
    except (InstallError, RegistrationError, OSError, ValueError, KeyError, TypeError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
