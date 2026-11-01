"""Discover canonical skills by installed name, independent of source categories."""
from pathlib import Path
import json
import re

ALIASES = {"workflow": "agent-workflow", "pull-request": "pr"}


def discover(kit):
    root = Path(kit).resolve() / "skills"
    if root.is_symlink():
        raise ValueError("Refusing a symlinked skills root.")
    if root.exists() and any(child.is_symlink() for child in root.iterdir()):
        raise ValueError("Refusing symlinked skill categories or folders.")
    result = {}
    for entry in sorted(root.rglob("SKILL.md")):
        relative = entry.relative_to(root)
        if len(relative.parts) not in {2, 3}:
            raise ValueError(f"Unsupported skill nesting: {relative}")
        name = entry.parent.name
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]{0,63}", name):
            raise ValueError(f"Invalid skill directory name: {name}")
        if any(parent.is_symlink() for parent in (entry, entry.parent, *entry.parents)
               if parent.is_relative_to(root)):
            raise ValueError(f"Refusing symlinked skill: {relative}")
        if name in result:
            raise ValueError(f"Duplicate installed skill name: {name}")
        result[name] = entry
    if not result:
        raise ValueError("No canonical skills found.")
    return result


def validate_interface(entry):
    """Check our quoted interface fields; this is not a general YAML parser."""
    path = entry.parent / "agents/openai.yaml"
    if path.is_symlink() or not path.is_file():
        raise ValueError(f"Missing or symlinked Codex metadata: {path}")
    fields = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        match = re.fullmatch(r"  (display_name|short_description|default_prompt): (.+)", line)
        if match:
            name, text = match.groups()
            if name in fields:
                raise ValueError(f"Duplicate interface field {name}: {path}")
            try:
                fields[name] = json.loads(text)
            except ValueError as error:
                raise ValueError(f"Use double-quoted interface strings: {path}") from error
    if (set(fields) != {"display_name", "short_description", "default_prompt"}
            or any(not isinstance(value, str) or not value.strip() for value in fields.values())
            or not 25 <= len(fields["short_description"]) <= 64
            or not re.search(r"\$" + re.escape(entry.parent.name) + r"(?![a-z0-9-])", fields["default_prompt"])):
        raise ValueError(f"Incomplete or inconsistent Codex interface metadata: {path}")
    return fields
