import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
import package_skills as package
from install_project import InstallError, LINK


class PackagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name).resolve()
        self.source = self.root / "source with spaces"
        shutil.copytree(package.KIT, self.source, ignore=shutil.ignore_patterns(".git", "__pycache__", "dist"))
        self.output = self.root / "packages"

    def test_each_package_is_self_contained_after_source_removal(self):
        package.build(self.source, self.output)
        self.source.rename(self.root / "source unavailable")
        skills = [path for path in self.output.iterdir() if path.is_dir()]
        self.assertEqual(len(skills), 15)
        for skill in skills:
            with self.subTest(skill=skill.name):
                body = (skill / "SKILL.md").read_text()
                self.assertIn(f"name: {skill.name}\n", body)
                self.assertNotIn(str(self.source), body)
                for path in skill.rglob("*.md"):
                    for _, target in LINK.findall(path.read_text()):
                        if "://" in target or target.startswith("#"):
                            continue
                        resolved = (path.parent / target.split("#")[0]).resolve()
                        self.assertTrue(resolved.is_relative_to(skill))
                        self.assertTrue(resolved.is_file(), f"Broken reference: {path}: {target}")
                self.assertFalse(any(path.suffix == ".py" for path in skill.rglob("*")))
                self.assertFalse((skill / "docs/research").exists())
        self.assertTrue((self.output / "write-spec/templates/spec.md").is_file())
        self.assertFalse((self.output / "write-spec/references/execution-policy.md").exists())
        router = (self.output / "agent-workflow/SKILL.md").read_text()
        self.assertIn("not this project's installed set", router)
        self.assertNotIn("](../", router)

    def test_build_is_idempotent_detects_stale_packages_and_protects_local_edits(self):
        self.assertEqual(package.build(self.source, self.output)["action"], "create")
        self.assertEqual(package.build(self.source, self.output, check=True)["action"], "unchanged")
        changed = self.source / "templates/spec.md"
        changed.write_text(changed.read_text() + "\nUpdated requirements.\n")
        with self.assertRaises(InstallError):
            package.build(self.source, self.output, check=True)
        self.assertEqual(package.build(self.source, self.output)["action"], "update")
        (self.output / "grill/SKILL.md").write_text("Local edited distribution")
        with self.assertRaises(InstallError):
            package.build(self.source, self.output)
        self.assertEqual((self.output / "grill/SKILL.md").read_text(), "Local edited distribution")

    def test_missing_external_and_symlinked_resources_are_rejected(self):
        resource = self.source / "templates/spec.md"
        original = resource.read_bytes()
        resource.unlink()
        with self.assertRaises(InstallError):
            package.packages(self.source)
        resource.symlink_to(self.root / "outside.md")
        with self.assertRaises(InstallError):
            package.packages(self.source)
        resource.unlink()
        resource.write_text("[outside](../../outside.md)")
        with self.assertRaises(InstallError):
            package.packages(self.source)
        resource.write_bytes(original)
        self.output.symlink_to(self.root / "elsewhere", target_is_directory=True)
        with self.assertRaises(InstallError):
            package.build(self.source, self.output)

    def test_legal_notices_are_preserved_and_authoring_files_are_excluded(self):
        (self.source / "LICENSE").write_text("Required terms")
        files = package.packages(self.source)
        for name in ("grill", "write-spec", "agent-workflow"):
            self.assertEqual(files[f"{name}/LICENSE"], b"Required terms")
        self.assertFalse(any("/tests/" in path or "/research/" in path or path.endswith("/AGENTS.md") for path in files))

    def fake_npx(self):
        executable_dir = self.root / "bin"
        executable_dir.mkdir()
        executable = executable_dir / "npx"
        executable.write_text(f"#!{sys.executable}\nimport os,sys,json\nprint(json.dumps({{'cwd':os.getcwd(),'args':sys.argv[1:],'telemetry':os.environ.get('DISABLE_TELEMETRY')}}))\n")
        executable.chmod(0o755)
        return {**os.environ, "PATH": str(executable_dir) + os.pathsep + os.environ["PATH"]}

    def test_bash_wrapper_passes_only_selected_project_skills_to_two_agents(self):
        package.build(self.source, self.source / "dist/skills")
        project = self.root / "project with spaces"
        project.mkdir()
        result = subprocess.run(["bash", str(self.source / "scripts/install-skills.sh"),
                                 str(project), "--skill", "write-spec", "--yes"],
                                env=self.fake_npx(), capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        execution = json.loads(result.stdout)
        self.assertEqual(Path(execution["cwd"]).resolve(), project)
        self.assertEqual(execution["args"], ["--yes", "skills@1.7.4", "add", str(self.source / "dist/skills"),
                                             "--agent", "claude-code", "codex", "--skill", "write-spec", "--yes"])
        self.assertEqual(execution["telemetry"], "1")
        self.assertEqual(list(project.iterdir()), [])

    def test_wrapper_forwards_agent_selection_and_rejects_missing_values(self):
        package.build(self.source, self.source / "dist/skills")
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
        package.build(self.source, self.source / "dist/skills")
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
        package.build(self.source, self.source / "dist/skills")
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
