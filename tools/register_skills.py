#!/usr/bin/env python3
"""Preview or register one local skill pointing at the shared workflow checkout."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import tempfile
import sys

KIT = Path(__file__).resolve().parents[1]
NAME = "agent-workflow"
MARKER = ".agent-workflow-registration.json"


class RegistrationError(Exception):
    pass


def entrypoint(kit):
    source = (kit / "skills/agent-workflow/SKILL.md").resolve()
    if not source.is_file():
        raise RegistrationError(f"Missing shared entry point: {source}")
    # A local registration uses an absolute file pointer so references are read
    # from the canonical checkout, regardless of the active project or tool.
    return (
        "---\nname: agent-workflow\n"
        'description: "Use a brief, document or ticket to plan and deliver work, '
        'or resume a feature through the shared agent workflow."\n---\n\n'
        f"Read the shared procedure at [{source.name}](<{source}>). "
        "Keep the current project as your working directory. "
        "Its instructions govern project-specific behavior.\n\n"
        "Read only the stage procedures and references needed for the request. "
        "Use supplied paths or ticket references as inputs. If no project was "
        "selected and the target is ambiguous, ask which project to use.\n"
    )


def destinations(agent=None, skills_dir=None, home=None, project=None):
    if project is not None and skills_dir is not None:
        raise RegistrationError("--project requires --agent, not --skills-dir.")
    if skills_dir is not None:
        return [Path(skills_dir).expanduser().resolve() / NAME]
    if project is not None:
        root = Path(project).expanduser().resolve()
        if not root.is_dir():
            raise RegistrationError(f"Project directory does not exist: {root}")
    else:
        root = Path.home() if home is None else Path(home)
    mapping = json.loads((KIT / "adapters/discovery.json").read_text())
    if agent not in {*mapping, "all"}:
        raise RegistrationError(f"Unknown discovery adapter: {agent}")
    names = list(mapping) if agent == "all" else [agent]
    result = []
    for name in names:
        relative = Path(mapping[name]["directory"])
        if relative.is_absolute() or ".." in relative.parts:
            raise RegistrationError(f"Invalid discovery directory for {name}")
        destination = root / relative / NAME
        if project is not None:
            # Existing agent directories may alias each other within the project.
            # Reject aliases outside it and avoid registering the same entry twice.
            parent = destination.parent.resolve()
            if not parent.is_relative_to(root):
                raise RegistrationError(f"Discovery directory leaves project: {destination}")
            destination = parent / NAME
        if destination not in result:
            result.append(destination)
    return result


def plan_registration(paths, kit):
    kit = kit.resolve()
    body = entrypoint(kit)
    marker = {"schema_version": 1, "source_root": str(kit)}
    plan = []
    for destination in paths:
        destination = Path(destination)
        if destination.is_symlink():
            raise RegistrationError(f"Refusing existing symlink: {destination}")
        if destination.exists():
            if not destination.is_dir():
                raise RegistrationError(f"Refusing existing path: {destination}")
            expected = {"SKILL.md", MARKER}
            if {p.name for p in destination.iterdir()} != expected:
                raise RegistrationError(f"Refusing unmanaged skill: {destination}")
            if any((destination / name).is_symlink() for name in expected):
                raise RegistrationError(f"Refusing symlinked registration files: {destination}")
            try:
                previous = json.loads((destination / MARKER).read_text())
                content = (destination / "SKILL.md").read_text()
            except (OSError, ValueError) as error:
                raise RegistrationError(f"Cannot inspect {destination}: {error}") from error
            if previous != marker or content != body:
                raise RegistrationError(
                    f"Registration differs at {destination}; review it before replacing."
                )
            action = "unchanged"
        else:
            action = "create"
        plan.append({"path": str(destination), "action": action})
    return plan, body, marker


def apply_registration(plan, body, marker):
    for item in plan:
        if item["action"] == "unchanged":
            continue
        destination = Path(item["path"])
        destination.parent.mkdir(parents=True, exist_ok=True)
        # Stage both files before exposing a discoverable skill directory.
        with tempfile.TemporaryDirectory(prefix=".workflow-register-", dir=destination.parent) as temp:
            staged = Path(temp) / NAME
            staged.mkdir()
            (staged / "SKILL.md").write_text(body, encoding="utf-8")
            (staged / MARKER).write_text(json.dumps(marker, indent=2) + "\n", encoding="utf-8")
            # Re-check at the mutation boundary; never overwrite another skill.
            if destination.exists() or destination.is_symlink():
                raise RegistrationError(f"Destination appeared during registration: {destination}")
            staged.rename(destination)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    target = parser.add_mutually_exclusive_group(required=True)
    target.add_argument("--agent", choices=["claude", "codex", "all"])
    target.add_argument("--skills-dir", type=Path,
                        help="Override the local skills directory for Claude Code or Codex.")
    parser.add_argument("--project", type=Path,
                        help="Register in this project's agent directories instead of your personal directories.")
    parser.add_argument("--apply", action="store_true",
                        help="Create the registration; default is read-only preview.")
    args = parser.parse_args(argv)
    try:
        paths = destinations(args.agent, args.skills_dir, project=args.project)
        plan, body, marker = plan_registration(paths, KIT)
        if args.apply:
            apply_registration(plan, body, marker)
        print(json.dumps({"applied": args.apply, "registrations": plan}, indent=2))
        return 0
    except (RegistrationError, OSError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
