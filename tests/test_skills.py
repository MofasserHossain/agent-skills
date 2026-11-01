import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

KIT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

SPEC = importlib.util.spec_from_file_location("skill_workflow", KIT / "tools/workflow.py")
workflow = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workflow)
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


class SkillInstallationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "source with spaces"
        shutil.copytree(KIT, self.source, ignore=shutil.ignore_patterns(".git", "__pycache__", "dist"))

    def test_canonical_skills_are_directly_installable_after_source_removal(self):
        self.assertEqual(workflow.check_skills(self.source), 17)
        project = self.root / "target project"
        installed = project / ".agents/skills"
        for entry in (self.source / "skills").rglob("SKILL.md"):
            skill = entry.parent
            shutil.copytree(skill, installed / skill.name)
            host = project / ".claude/skills" / skill.name
            host.parent.mkdir(parents=True, exist_ok=True)
            host.symlink_to(Path(os.path.relpath(installed / skill.name, host.parent)), target_is_directory=True)
        self.source.rename(self.root / "source unavailable")
        project.rename(self.root / "relocated project")
        project = self.root / "relocated project"
        for skill in (project / ".agents/skills").iterdir():
            with self.subTest(skill=skill.name):
                self.assertEqual((project / ".claude/skills" / skill.name).resolve(), skill.resolve())
                for resource in skill.rglob("*.md"):
                    for _, target in LINK.findall(resource.read_text()):
                        if "://" in target or target.startswith("#"):
                            continue
                        resolved = (resource.parent / target.split("#")[0]).resolve()
                        self.assertTrue(resolved.is_relative_to(skill.resolve()))
                        self.assertTrue(resolved.is_file(), f"Broken reference: {resource}: {target}")
                self.assertFalse(any(p.suffix == ".py" for p in skill.rglob("*")))
        self.assertTrue((project / ".agents/skills/write-spec/templates/spec.md").is_file())

    def test_one_selected_skill_has_only_its_own_resources(self):
        selected = self.root / "only-write-spec"
        shutil.copytree(self.source / "skills/engineering/write-spec", selected)
        self.source.rename(self.root / "source unavailable")
        self.assertTrue((selected / "templates/spec.md").is_file())
        self.assertFalse((selected / "references/execution-policy.md").exists())
        for resource in selected.rglob("*.md"):
            for _, target in LINK.findall(resource.read_text()):
                if "://" not in target and not target.startswith("#"):
                    self.assertTrue((resource.parent / target.split("#")[0]).resolve().is_relative_to(selected))
                    self.assertTrue((resource.parent / target.split("#")[0]).is_file())

    def test_validation_rejects_missing_escaping_absolute_and_symlinked_resources(self):
        template = self.source / "skills/engineering/write-spec/templates/spec.md"
        template.unlink()
        with self.assertRaises(workflow.WorkflowError):
            workflow.check_skills(self.source)
        for content in ("[outside](../../../../outside.md)", "[absolute](/tmp/outside.md)"):
            template.write_text(content)
            with self.assertRaises(workflow.WorkflowError):
                workflow.check_skills(self.source)
        template.unlink()
        outside = self.root / "outside.md"
        outside.write_text("external")
        template.symlink_to(outside)
        with self.assertRaises(workflow.WorkflowError):
            workflow.check_skills(self.source)

    def fake_npx(self):
        executable_dir = self.root / "bin"
        executable_dir.mkdir()
        executable = executable_dir / "npx"
        executable.write_text(f"#!{sys.executable}\nimport os,sys,json\nprint(json.dumps({{'cwd':os.getcwd(),'args':sys.argv[1:],'telemetry':os.environ.get('DISABLE_TELEMETRY')}}))\n")
        executable.chmod(0o755)
        return {**os.environ, "PATH": str(executable_dir) + os.pathsep + os.environ["PATH"]}

    def test_bash_wrapper_passes_only_selected_project_skills_to_two_agents(self):
        project = self.root / "project with spaces"
        project.mkdir()
        result = subprocess.run(["bash", str(self.source / "scripts/install-skills.sh"),
                                 str(project), "--skill", "write-spec", "--yes"],
                                env=self.fake_npx(), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        execution = json.loads(result.stdout)
        self.assertEqual(Path(execution["cwd"]).resolve(), project)
        self.assertEqual(execution["args"], ["--yes", "skills@1.7.4", "add", str(self.source / "skills"),
                                             "--agent", "claude-code", "codex", "--skill", "write-spec", "--yes"])
        self.assertEqual(execution["telemetry"], "1")
        self.assertEqual(list(project.iterdir()), [])

    def test_wrapper_forwards_agent_selection_and_rejects_missing_values(self):
        project = self.root / "project"
        project.mkdir()
        environment = self.fake_npx()
        wrapper = ["bash", str(self.source / "scripts/install-skills.sh"), str(project)]
        for flags, expected in ((["--agent", "codex"], ["codex"]),
                                (["--agent=claude-code"], ["claude-code"]),
                                (["--agent", "cursor", "opencode"], ["cursor", "opencode"]),
                                (["--agent=*"], ["*"]),
                                (["-a", "codex", "claude-code"], ["codex", "claude-code"]),
                                (["-a", "codex", "-a", "claude-code"], ["codex", "claude-code"])):
            with self.subTest(flags=flags):
                result = subprocess.run([*wrapper, *flags, "--skill", "grill", "--yes"],
                                        env=environment, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                arguments = json.loads(result.stdout)["args"]
                start = arguments.index("--agent") + 1
                end = arguments.index("--skill")
                self.assertEqual(arguments[start:end], expected)
                self.assertEqual(arguments[end:], ["--skill", "grill", "--yes"])
        for flags in (["--agent"], ["--agent="], ["--agent=-g"],
                      ["--agent", "--list"]):
            with self.subTest(invalid=flags):
                result = subprocess.run([*wrapper, *flags], env=environment,
                                        capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(result.stdout, "")
        self.assertEqual(list(project.iterdir()), [])

    @unittest.skipUnless(os.name == "posix", "PTY behavior")
    def test_agent_terminal_cannot_silently_select_all(self):
        project = self.root / "project"
        project.mkdir()
        master, slave = os.openpty()
        try:
            result = subprocess.run(["bash", str(self.source / "scripts/install-skills.sh"), str(project)],
                                    stdin=slave, env={**os.environ, "CODEX_CI": "1"},
                                    capture_output=True, text=True, timeout=5)
        finally:
            os.close(master)
            os.close(slave)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--skill", result.stderr)
        self.assertEqual(list(project.iterdir()), [])

    def test_bash_wrapper_requires_selection_for_unattended_calls(self):
        project = self.root / "project"
        project.mkdir()
        for flags in ([], ["--yes"], ["--global"], ["--all"], ["--agent", "other"]):
            with self.subTest(flags=flags):
                result = subprocess.run(["bash", str(self.source / "scripts/install-skills.sh"), str(project), *flags],
                                        input="", capture_output=True, text=True)
                self.assertEqual(result.returncode, 2)
                self.assertEqual(list(project.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
