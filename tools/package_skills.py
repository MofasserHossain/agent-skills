#!/usr/bin/env python3
"""Build self-contained skill folders for the standard Skills CLI; authoring use only."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import sys

from install_project import InstallError, LEGAL_FILES, LINK, apply, inspect

KIT = Path(__file__).resolve().parents[1]
EXPORT_NAMES = {"workflow": "agent-workflow"}


def packages(kit):
    kit = Path(kit).resolve()
    skills = {path.parent.name: path for path in (kit / "skills").glob("*/SKILL.md")}
    if "workflow" not in skills:
        raise InstallError("Source kit has no workflow skill.")
    output = {}

    def read(relative):
        path = kit / relative
        if not path.resolve().is_relative_to(kit):
            raise InstallError(f"Resource leaves source kit: {relative}")
        if any(parent.is_symlink() for parent in (path, *path.parents)
               if parent != kit and parent.is_relative_to(kit)):
            raise InstallError(f"Refusing symlinked source resource: {relative}")
        if not path.is_file():
            raise InstallError(f"Missing skill resource: {relative}")
        return path.read_bytes()

    def resource_path(relative):
        parts = Path(relative).parts
        if parts[0] in {"references", "templates"}:
            return relative
        if parts[0] in {"docs", "checks"} and len(parts) == 2:
            return f"references/{parts[1]}"
        if relative in LEGAL_FILES:
            return relative
        raise InstallError(f"Resource is not distributable skill content: {relative}")

    for source_name, source_path in sorted(skills.items()):
        name = EXPORT_NAMES.get(source_name, source_name)
        files = {}
        source_relative = source_path.relative_to(kit).as_posix()
        pending = [(source_relative, "SKILL.md")]
        pending.extend((legal, legal) for legal in LEGAL_FILES if (kit / legal).exists())
        origins = {}
        while pending:
            relative, destination = pending.pop()
            if destination in origins:
                if origins[destination] != relative:
                    raise InstallError(f"Conflicting package resources: {relative}, {origins[destination]}")
                continue
            origins[destination] = relative
            data = read(relative)
            if Path(relative).suffix == ".md":
                text = data.decode()

                def rewrite(match):
                    label, target = match.groups()
                    if "://" in target or target.startswith("#"):
                        return match[0]
                    if target.startswith("/"):
                        raise InstallError(f"Absolute resource link in {relative}: {target}")
                    target_path, separator, anchor = target.partition("#")
                    dependency = Path(os.path.normpath(Path(relative).parent / target_path)).as_posix()
                    parts = Path(dependency).parts
                    if len(parts) == 3 and parts[0] == "skills" and parts[2] == "SKILL.md":
                        if parts[1] not in skills:
                            raise InstallError(f"Unknown related skill: {dependency}")
                        related = EXPORT_NAMES.get(parts[1], parts[1])
                        return f"`{related}`"
                    dependency_destination = resource_path(dependency)
                    pending.append((dependency, dependency_destination))
                    rewritten = Path(os.path.relpath(dependency_destination, Path(destination).parent)).as_posix()
                    return f"[{label}]({rewritten}{separator}{anchor})"

                text = LINK.sub(rewrite, text)
                if destination == "SKILL.md":
                    text = text.replace(f"name: {source_name}\n", f"name: {name}\n", 1)
                    if source_name == "workflow":
                        text = text.replace("Read only the selected procedure and applicable references, not the whole table's targets.",
                                            "The table describes available package choices, not this project's installed set. Read only installed procedures and relevant references.")
                    text += ("\nRelated skill names refer only to skills available in this project or host. "
                             "If one is absent, continue within this procedure where sufficient or report the missing guidance; "
                             "do not claim it ran or follow a path to the authoring checkout.\n")
                data = text.encode()
            files[destination] = data
        output.update({f"{name}/{relative}": data for relative, data in files.items()})
    return output


def build(kit, destination, check=False):
    destination = Path(destination).expanduser()
    if destination.is_symlink():
        raise InstallError(f"Refusing symlinked package output: {destination}")
    destination = destination.resolve()
    kit = Path(kit).resolve()
    if destination == kit or kit.is_relative_to(destination) or destination.is_relative_to(kit / "skills"):
        raise InstallError("Build output must be separate from authored skills.")
    files = packages(kit)
    action, previous = inspect(destination, files, "workflow-standard-skills", True)
    if check:
        if action != "unchanged":
            raise InstallError("Skill packages are missing or stale; rebuild from the source kit.")
    else:
        apply([{"path": destination, "files": files, "kind": "workflow-standard-skills",
                "action": action, "previous": previous, "project": destination.parent}])
    return {"action": action, "skills": len({Path(name).parts[0] for name in files}),
            "files": len(files), "bytes": sum(map(len, files.values())), "output": str(destination)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=KIT / "dist/skills")
    parser.add_argument("--check", action="store_true", help="Validate existing packages without writing.")
    args = parser.parse_args(argv)
    try:
        print(json.dumps(build(KIT, args.output, args.check), indent=2))
        return 0
    except (InstallError, OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
