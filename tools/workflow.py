#!/usr/bin/env python3
"""Portable project setup, focused task context and explicit executor dispatch."""
from __future__ import annotations

import argparse
from collections import deque
import json
import math
import os
from pathlib import Path
import re
import shutil
import signal
import subprocess
import sys
import time
from datetime import datetime, timezone

KIT = Path(__file__).resolve().parents[1]
CONFIG = ".agent-workflow.json"
SUPPORTED_AGENTS = {"claude", "codex"}
STATUSES = {"draft", "ready", "in-progress", "blocked", "review", "done"}
ID_PATTERN = re.compile(r"[a-z0-9][a-z0-9-]{0,79}\Z")


class WorkflowError(Exception):
    pass


def read_json(path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise WorkflowError(f"Cannot read JSON from {path}: {error}") from error


def beneath(path, root):
    resolved = path.resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise WorkflowError(f"Path leaves the configured directory: {path}")
    return resolved


def load_config(project):
    config = read_json(project / CONFIG)
    if not isinstance(config, dict) or config.get("schema_version") != 1:
        raise WorkflowError("Project configuration requires schema_version 1.")
    if config.get("tracker") not in {"local", "github"}:
        raise WorkflowError("tracker must be local or github.")
    work_dir = config.get("work_dir")
    if not isinstance(work_dir, str) or not work_dir or Path(work_dir).is_absolute():
        raise WorkflowError("work_dir must be a relative project directory.")
    work = beneath(project / work_dir, project)
    if work == project or work_dir.split("/")[0] == ".git":
        raise WorkflowError("work_dir must be a dedicated planning directory.")
    commands = config.get("verification", [])
    if not isinstance(commands, list) or any(
        not isinstance(cmd, list) or not cmd
        or any(not isinstance(arg, str) for arg in cmd) or not cmd[0]
        for cmd in commands
    ):
        raise WorkflowError("verification must contain command argument arrays.")
    checks = config.get("checks", {})
    if not isinstance(checks, dict) or any(
        not isinstance(name, str) or not re.fullmatch(r"[a-z][a-z0-9-]{0,63}", name)
        or not isinstance(cmd, list) or not cmd
        or any(not isinstance(arg, str) for arg in cmd) or not cmd[0]
        for name, cmd in checks.items()
    ):
        raise WorkflowError("checks must map lowercase check names to command argument arrays.")
    default_agent = config.get("default_agent", "manual")
    if not isinstance(default_agent, str) or default_agent not in {*SUPPORTED_AGENTS, "manual"}:
        raise WorkflowError("default_agent must be claude, codex or manual (no CLI selected).")
    return config, work


def load_registry(path=None):
    registry = read_json(Path(path).resolve() if path else KIT / "adapters/agents.json")
    if not isinstance(registry, dict) or registry.get("schema_version") != 1:
        raise WorkflowError("Executor registry requires schema_version 1.")
    agents = registry.get("agents")
    if not isinstance(agents, dict) or not agents:
        raise WorkflowError("Executor registry must contain agents.")
    for name, entry in agents.items():
        if not isinstance(name, str) or not isinstance(entry, dict):
            raise WorkflowError("Invalid executor entry.")
        if "command" not in entry:
            raise WorkflowError(f"Executor {name} is missing command.")
        if name not in {*SUPPORTED_AGENTS, "manual"}:
            raise WorkflowError(f"Unsupported executor: {name}; supported agents are claude and codex.")
        command = entry["command"]
        if name == "manual" and command is not None:
            raise WorkflowError("manual is context-only and cannot run a command.")
        if name in SUPPORTED_AGENTS and command is None:
            raise WorkflowError(f"Executor {name} needs a command argument array.")
        if command is not None and (
            not isinstance(command, list) or not command
            or any(not isinstance(arg, str) for arg in command) or not command[0]
        ):
            raise WorkflowError(f"Executor {name} needs an argument array or null.")
    return agents


def read_task(path):
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as error:
        raise WorkflowError(f"Cannot read task {path}: {error}") from error
    if len(text.encode("utf-8")) > 131072:
        raise WorkflowError("Task exceeds 128 KiB; use references for supporting material.")
    match = re.match(r"\A---\r?\n(.*?)\r?\n---\r?\n", text, re.S)
    if not match:
        raise WorkflowError(f"Task requires JSON frontmatter: {path}")
    try:
        metadata = json.loads(match[1])
    except ValueError as error:
        raise WorkflowError(f"Invalid task frontmatter: {path}: {error}") from error
    if not isinstance(metadata, dict) or metadata.get("schema_version") != 1:
        raise WorkflowError("Task requires schema_version 1.")
    task_id = metadata.get("id")
    if not isinstance(task_id, str) or not ID_PATTERN.fullmatch(task_id):
        raise WorkflowError("Task id must use lowercase letters, digits and hyphens.")
    if not isinstance(metadata.get("status"), str) or metadata["status"] not in STATUSES:
        raise WorkflowError(f"Invalid status for {task_id}.")
    if not isinstance(metadata.get("execution"), str) or metadata["execution"] not in {"afk", "hitl"}:
        raise WorkflowError(f"Invalid execution mode for {task_id}.")
    if not isinstance(metadata.get("review"), str) or metadata["review"] not in {"human", "automated"}:
        raise WorkflowError(f"Invalid review requirement for {task_id}.")
    blockers = metadata.get("blocked_by")
    if not isinstance(blockers, list) or any(
        not isinstance(item, str) or not ID_PATTERN.fullmatch(item)
        for item in blockers
    ):
        raise WorkflowError(f"Invalid blockers for {task_id}.")
    if task_id in blockers or len(blockers) != len(set(blockers)):
        raise WorkflowError(f"Self-dependency or duplicate blocker for {task_id}.")
    body = text[match.end():].strip()
    for heading in ("## Expected behavior", "## Acceptance criteria", "## Verification"):
        if heading not in body:
            raise WorkflowError(f"{task_id} is missing {heading}.")
    return metadata, text


def task_inventory(directory, work):
    directory = beneath(Path(directory), work)
    if not directory.is_dir():
        raise WorkflowError(f"Issues directory does not exist: {directory}")
    peers = {}
    records = {}
    for peer in sorted(directory.glob("*.md")):
        # All issue files are tasks. A symlink cannot introduce external context.
        peer = beneath(peer, work)
        item, text = read_task(peer)
        if item["id"] in peers:
            raise WorkflowError(f"Duplicate task id: {item['id']}")
        peers[item["id"]] = item
        records[item["id"]] = (peer, item, text)
    dependents = {task_id: [] for task_id in peers}
    remaining = {}
    for task_id, item in peers.items():
        remaining[task_id] = len(item["blocked_by"])
        for blocker in item["blocked_by"]:
            if blocker not in peers:
                raise WorkflowError(f"Unknown blocker: {blocker} (required by {task_id})")
            dependents[blocker].append(task_id)
    frontier = deque(task_id for task_id, count in remaining.items() if count == 0)
    while frontier:
        for dependent in dependents[frontier.popleft()]:
            remaining[dependent] -= 1
            if remaining[dependent] == 0:
                frontier.append(dependent)
    unresolved = [task_id for task_id, count in remaining.items() if count]
    if unresolved:
        raise WorkflowError("Dependency cycle or dependent on a cycle: " + ", ".join(unresolved))
    return records, peers


def selected_task(task, project, work):
    path = beneath(Path(task), work)
    metadata, text = read_task(path)
    _, peers = task_inventory(path.parent, work)
    return path, metadata, text, peers


def next_task(directory, work):
    records, peers = task_inventory(directory, work)
    eligible, waiting = [], []
    for task_id, (path, metadata, _) in records.items():
        if metadata["status"] == "done":
            continue
        reasons = []
        if metadata["execution"] != "afk":
            reasons.append("requires-human-input")
        if metadata["status"] != "ready":
            reasons.append("status:" + metadata["status"])
        reasons.extend("unfinished-blocker:" + blocker for blocker in metadata["blocked_by"]
                       if peers[blocker]["status"] != "done")
        item = {"id": task_id, "path": str(path)}
        if reasons:
            waiting.append({**item, "reasons": reasons})
        else:
            eligible.append(item)
    state = "empty" if not records else "ready" if eligible else "waiting" if waiting else "complete"
    return {"schema_version": 1, "state": state, "selected": eligible[0] if eligible else None,
            "eligible": eligible, "waiting": waiting, "task_count": len(records),
            "executed": False, "claimed": False,
            "note": "Read-only snapshot in filename order; revalidate before dispatch. No claims or acceptance inferred."}


def require_eligible(metadata, peers):
    if metadata["execution"] != "afk":
        raise WorkflowError("HITL work must be handled interactively.")
    if metadata["status"] != "ready":
        raise WorkflowError(f"Task is {metadata['status']}, not ready.")
    pending = [
        task_id for task_id in metadata["blocked_by"]
        if peers[task_id]["status"] != "done"
    ]
    if pending:
        raise WorkflowError("Unfinished blockers: " + ", ".join(pending))


def absolute_links(text, source):
    def replace(match):
        label, target = match.groups()
        if "://" in target or target.startswith("#") or target.startswith("/"):
            return match[0]
        return f"[{label}]({(source.parent / target).resolve()})"
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", replace, text)


def make_prompt(project, config, task_path, task_text):
    instruction_path = KIT / "skills/implement/SKILL.md"
    instructions = instruction_path.read_text(encoding="utf-8")
    instructions = re.sub(r"\A---\n.*?\n---\n", "", instructions, count=1, flags=re.S)
    instructions = absolute_links(instructions, instruction_path)
    result = (KIT / "skills/implement/references/result-contract.md").read_text(encoding="utf-8")
    return (
        "# Portable implementation request\n\n"
        f"Project: {project}\nTask source: {task_path}\n"
        "Read all applicable project instructions before acting. Follow source/spec "
        "references as needed. Project rules and the user's authorization govern actions. "
        "This request does not authorize external publication or credential changes.\n\n"
        "## Project configuration\n"
        + json.dumps(config, indent=2)
        + "\n\n## Active procedure\n" + instructions.strip()
        + "\n\n## Selected task\n" + task_text.strip()
        + "\n\n## Required report\n" + result.strip()
        + "\n\nLeave task status unchanged; return evidence for the supervising "
        "human/agent to evaluate. Report missing decisions instead of guessing.\n"
    )


def init_project(project):
    project = project.resolve()
    if not project.is_dir():
        raise WorkflowError(f"Project directory does not exist: {project}")
    config = {
        "schema_version": 1,
        "work_dir": "docs/work",
        "tracker": "local",
        "default_agent": "manual",
        "checks": {},
        "verification": [],
    }
    try:
        with (project / CONFIG).open("x", encoding="utf-8") as handle:
            handle.write(json.dumps(config, indent=2) + "\n")
    except FileExistsError as error:
        raise WorkflowError(f"{CONFIG} already exists; no files changed.") from error
    print(f"Created {project / CONFIG}")
    print("Configure verification commands. Existing instruction files were left unchanged.")


def dispatch(command, prompt, project, output, timeout):
    output.mkdir(mode=0o700, parents=True, exist_ok=False)
    os.chmod(output, 0o700)
    start = time.monotonic()
    process = None
    status, returncode = "failed", None
    try:
        with (output / "stdout.txt").open("w") as stdout, (output / "stderr.txt").open("w") as stderr:
            process = subprocess.Popen(
                command, cwd=project, stdin=subprocess.PIPE,
                stdout=stdout, stderr=stderr, text=True,
                start_new_session=(os.name == "posix"),
            )
            try:
                process.communicate(input=prompt, timeout=timeout)
                returncode = process.returncode
                status = "process-completed" if returncode == 0 else "failed"
            except (subprocess.TimeoutExpired, KeyboardInterrupt) as error:
                status = "timed-out" if isinstance(error, subprocess.TimeoutExpired) else "interrupted"
                if os.name == "posix":
                    try:
                        os.killpg(process.pid, signal.SIGKILL)
                    except ProcessLookupError:
                        pass
                else:
                    process.kill()
                process.communicate()
                returncode = 124 if status == "timed-out" else 130
    except OSError as error:
        (output / "stderr.txt").write_text(str(error) + "\n", encoding="utf-8")
        returncode = 127
    finally:
        summary = {
            "schema_version": 1, "status": status,
            "returncode": returncode, "elapsed_seconds": round(time.monotonic() - start, 3),
            "accepted": False,
            "note": "Process outcome only. Review acceptance evidence and required checks.",
        }
        (output / "result.json").write_text(json.dumps(summary, indent=2) + "\n")
    return returncode


def check_skills(kit):
    """Validate directly installable folders without generating or rewriting files."""
    skills = sorted((Path(kit) / "skills").glob("*/SKILL.md"))
    errors = []
    if not skills:
        errors.append("No canonical skills found.")
    for skill in skills:
        if skill.parent.is_symlink():
            errors.append(f"Symlinked skill folder: {skill.parent}")
            continue
        content = skill.read_text(encoding="utf-8")
        if f"name: {skill.parent.name}\n" not in content or "description:" not in content:
            errors.append(f"Invalid skill metadata: {skill}")
        for resource in skill.parent.rglob("*"):
            if resource.is_symlink():
                errors.append(f"Symlinked skill resource: {resource}")
                continue
            if resource.is_file() and resource.suffix == ".md":
                for target in re.findall(r"\]\(([^)]+)\)", resource.read_text(encoding="utf-8")):
                    if "://" in target or target.startswith("#"):
                        continue
                    local = (resource.parent / target.split("#")[0]).resolve()
                    if target.startswith("/") or not local.is_relative_to(skill.parent.resolve()):
                        errors.append(f"Skill link leaves its installed folder: {resource}: {target}")
                    elif not local.is_file():
                        errors.append(f"Missing skill resource: {resource}: {target}")
    if errors:
        raise WorkflowError("\n".join(errors))
    return len(skills)


def check_kit():
    count = check_skills(KIT)
    errors = []
    for path in KIT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        for target in re.findall(r"\]\(([^)]+)\)", path.read_text(encoding="utf-8")):
            if "://" in target or target.startswith("#") or target.startswith("/"):
                continue
            local = (path.parent / target.split("#")[0]).resolve()
            if not local.exists():
                errors.append(f"Broken link in {path.relative_to(KIT)}: {target}")
    load_registry()
    read_task(KIT / "skills/plan-tasks/templates/task.md")
    if errors:
        raise WorkflowError("\n".join(errors))
    print(f"Validated {count} directly installable skills, local Markdown links, registry and task template.")


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="action", required=True)
    sub.add_parser("check")
    init = sub.add_parser("init")
    init.add_argument("project", type=Path)
    agents = sub.add_parser("agents")
    agents.add_argument("--registry", type=Path)
    next_cmd = sub.add_parser("next", help="Inspect one local issues directory; do not launch or claim work.")
    next_cmd.add_argument("issues", type=Path)
    next_cmd.add_argument("--project", type=Path, required=True)
    for action in ("prompt", "run"):
        cmd = sub.add_parser(action)
        cmd.add_argument("task", type=Path)
        cmd.add_argument("--project", type=Path, required=True)
        if action == "run":
            cmd.add_argument("--agent", choices=sorted(SUPPORTED_AGENTS))
            cmd.add_argument("--registry", type=Path)
            cmd.add_argument("--execute", action="store_true")
            cmd.add_argument("--timeout", type=float, default=1800)
    args = parser.parse_args(argv)
    try:
        if args.action == "check":
            check_kit()
            return 0
        if args.action == "init":
            init_project(args.project)
            return 0
        if args.action == "agents":
            for name, entry in load_registry(args.registry).items():
                if name == "manual":
                    continue
                command = entry["command"]
                available = command is None or shutil.which(command[0]) is not None
                print(f"{name}: {entry.get('label', name)}; "
                      f"{'available' if available else 'CLI not installed'}")
            return 0
        project = args.project.resolve()
        config, work = load_config(project)
        if config["tracker"] != "local":
            raise WorkflowError("The local helper cannot dispatch GitHub-owned tasks.")
        if args.action == "next":
            print(json.dumps(next_task(args.issues, work), indent=2))
            return 0
        task_path, metadata, text, peers = selected_task(args.task, project, work)
        prompt = make_prompt(project, config, task_path, text)
        if args.action == "prompt":
            print(prompt, end="")
            return 0
        require_eligible(metadata, peers)
        if not math.isfinite(args.timeout) or args.timeout <= 0:
            raise WorkflowError("--timeout must be positive and finite.")
        agent = args.agent or config.get("default_agent", "manual")
        registry = load_registry(args.registry)
        if agent not in registry:
            raise WorkflowError(f"Unknown executor: {agent}")
        command = registry[agent]["command"]
        if not args.execute:
            print(json.dumps({
                "task": metadata["id"], "agent": agent, "runtime": "host",
                "command": command, "timeout_seconds": args.timeout,
                "prompt_bytes": len(prompt.encode("utf-8")), "executed": False,
            }, indent=2))
            return 0
        if command is None:
            print(prompt, end="")
            return 0
        if shutil.which(command[0]) is None:
            raise WorkflowError(f"Executor is not installed: {command[0]}")
        stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
        output = beneath(project / ".workflow-runs", project) / f"{metadata['id']}-{stamp}"
        code = dispatch(command, prompt, project, output, args.timeout)
        print(f"Run evidence: {output}")
        print("Task status unchanged. Process completion is not acceptance.")
        return code
    except WorkflowError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
