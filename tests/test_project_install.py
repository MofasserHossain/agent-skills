import contextlib
import io
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

TOOLS = Path(__file__).resolve().parents[1] / "tools"
sys.path.insert(0, str(TOOLS))
import install_project as install


class ProjectInstallTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "project with spaces"
        self.project.mkdir()
        self.source = self.root / "private source"
        shutil.copytree(install.KIT, self.source, ignore=shutil.ignore_patterns(".git", "__pycache__"))

    def test_preview_makes_no_changes(self):
        items = install.plan(self.project, "all", self.source)
        self.assertEqual([item["action"] for item in items], ["create"] * 3)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_snapshot_works_without_source_and_after_moving_project(self):
        rules = self.project / "AGENTS.md"
        rules.write_text("Keep these project rules")
        config = self.project / ".agent-workflow.json"
        config.write_text(json.dumps({"schema_version": 1, "work_dir": "work", "tracker": "local"}))
        install.apply(install.plan(self.project, "all", self.source, with_runner=True))
        self.source.rename(self.root / "source unavailable")
        relocated = self.root / "relocated project"
        self.project.rename(relocated)
        relocated = relocated.resolve()
        bundle = relocated / install.BUNDLE
        for host in (".agents", ".claude"):
            entry = relocated / host / "skills/agent-workflow/SKILL.md"
            body = entry.read_text()
            self.assertNotIn(str(self.source), body)
            self.assertNotIn(str(self.project), body)
            target = re.search(r'\]\(([^)]+)\)', body).group(1)
            resolved = (entry.parent / target).resolve()
            self.assertTrue(resolved.is_relative_to(relocated))
            self.assertTrue(resolved.is_file())
            self.assertEqual([p.name for p in entry.parent.glob("SKILL.md")], ["SKILL.md"])
        result = subprocess.run([sys.executable, "-B", str(bundle / "tools/workflow.py"), "check"],
                                cwd=relocated, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        task = relocated / "work/task.md"
        task.parent.mkdir()
        task.write_bytes((bundle / "skills/engineering/plan-tasks/templates/task.md").read_bytes())
        result = subprocess.run([sys.executable, "-B", str(bundle / "tools/workflow.py"), "prompt",
                                 str(task), "--project", str(relocated)],
                                cwd=relocated, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn(str(bundle / "skills/engineering/implement/references/execution-policy.md"), result.stdout)
        self.assertNotIn(str(self.source), result.stdout)
        self.assertEqual((relocated / "AGENTS.md").read_text(), "Keep these project rules")
        self.assertFalse((relocated / ".workflow-runs").exists())

    def test_install_is_idempotent_and_update_requires_explicit_review(self):
        install.apply(install.plan(self.project, "all", self.source))
        second = install.plan(self.project, "all", self.source)
        self.assertTrue(all(item["action"] == "unchanged" for item in second))
        path = self.project / install.BUNDLE / "skills/productivity/agent-workflow/references/context-policy.md"
        before = path.stat().st_mtime_ns
        install.apply(second)
        self.assertEqual(path.stat().st_mtime_ns, before)
        changed = self.source / "skills/productivity/agent-workflow/references/context-policy.md"
        changed.write_text(changed.read_text() + "\nA reviewed update.\n")
        with self.assertRaises(install.InstallError):
            install.plan(self.project, "all", self.source)
        install.apply(install.plan(self.project, "all", self.source, update=True))
        self.assertEqual(path.read_bytes(), changed.read_bytes())

    def test_local_edits_are_preserved_even_with_update(self):
        install.apply(install.plan(self.project, "all", self.source))
        path = self.project / install.BUNDLE / "skills/engineering/implement/SKILL.md"
        path.write_text("Project-specific customization")
        with self.assertRaises(install.InstallError):
            install.plan(self.project, "all", self.source, update=True)
        self.assertEqual(path.read_text(), "Project-specific customization")

    def test_conflicting_discovery_entry_prevents_all_writes(self):
        conflict = self.project / ".claude/skills/agent-workflow"
        conflict.mkdir(parents=True)
        (conflict / "SKILL.md").write_text("Existing skill")
        with self.assertRaises(install.InstallError):
            install.plan(self.project, "all", self.source)
        self.assertFalse((self.project / install.BUNDLE).exists())
        self.assertFalse((self.project / ".agents").exists())

    def test_outside_symlinks_and_source_links_are_refused(self):
        outside = self.root / "outside"
        outside.mkdir()
        (self.project / ".agents").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(install.RegistrationError):
            install.plan(self.project, "all", self.source)
        self.assertEqual(list(outside.iterdir()), [])
        (self.source / "skills/engineering/write-spec/templates/spec.md").unlink()
        (self.source / "skills/engineering/write-spec/templates/spec.md").symlink_to(outside / "missing")
        with self.assertRaises(install.InstallError):
            install.payload(self.source)

    def test_payload_excludes_private_and_generated_state(self):
        for name in (".env", ".git/config", ".workflow-runs/session.json", "tools/__pycache__/cache.pyc"):
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("private")
        files = install.payload(self.source)
        self.assertFalse(any("__pycache__" in name or name.startswith((".env", ".git/", ".workflow-runs"))
                             for name in files))

    def test_selected_skill_installs_only_its_runtime_dependencies(self):
        files = install.payload(self.source, skills=["write-spec"])
        self.assertIn("skills/engineering/write-spec/SKILL.md", files)
        self.assertIn("skills/engineering/write-spec/templates/spec.md", files)
        self.assertIn("skills/productivity/agent-workflow/SKILL.md", files)
        self.assertNotIn("skills/engineering/implement/SKILL.md", files)
        self.assertFalse(any(name.startswith(("tools/", "adapters/", "docs/", "tests/", "examples/")) for name in files))
        router = files["skills/productivity/agent-workflow/SKILL.md"].decode()
        self.assertNotIn("](../implement/SKILL.md)", router)
        self.assertNotIn("AGENTS.md", files)
        self.assertNotIn("tools/install_project.py", files)

    def test_selected_resources_and_all_links_survive_without_source(self):
        items = install.plan(self.project, "codex", self.source, skills=["ui-design"])
        install.apply(items)
        self.source.rename(self.root / "hidden source")
        bundle = (self.project / install.BUNDLE).resolve()
        selection = json.loads((bundle / install.SELECTION).read_text())
        self.assertEqual(set(selection["included_skills"]), {"agent-workflow", "ui-design"})
        self.assertFalse(selection["with_runner"])
        for path in bundle.rglob("*.md"):
            for _, target in install.LINK.findall(path.read_text()):
                if "://" in target or target.startswith("#"):
                    continue
                resolved = (path.parent / target.split("#")[0]).resolve()
                self.assertTrue(resolved.is_relative_to(bundle))
                self.assertTrue(resolved.is_file(), f"Broken link: {path}: {target}")
        self.assertFalse((bundle / "docs/research").exists())

    def test_deliberate_update_migrates_old_router_selection_and_paths(self):
        items = install.plan(self.project, "all", self.source, skills=["agent-workflow"])
        old_files = {}
        for name, body in items[0]["files"].items():
            name = name.replace("skills/productivity/agent-workflow/", "skills/workflow/")
            if name == "skills/workflow/SKILL.md":
                body = body.replace(b"name: agent-workflow\n", b"name: workflow\n", 1)
            old_files[name] = body
        old_files[install.SELECTION] = json.dumps({
            "schema_version": 1, "requested_skills": ["workflow"],
            "included_skills": ["workflow"], "with_runner": False,
        }).encode()
        items[0]["files"] = old_files
        for item in items[1:]:
            item["files"]["SKILL.md"] = item["files"]["SKILL.md"].replace(
                b"skills/productivity/agent-workflow/SKILL.md", b"skills/workflow/SKILL.md")
        install.apply(items)
        with self.assertRaises(install.InstallError):
            install.plan(self.project, "all", self.source)
        install.apply(install.plan(self.project, "all", self.source, update=True))
        bundle = self.project / install.BUNDLE
        self.assertFalse((bundle / "skills/workflow").exists())
        self.assertTrue((bundle / "skills/productivity/agent-workflow/references/context-policy.md").is_file())
        selection = json.loads((bundle / install.SELECTION).read_text())
        self.assertEqual(selection["requested_skills"], ["agent-workflow"])
        for item in items[1:]:
            self.assertIn("skills/productivity/agent-workflow/SKILL.md", (item["path"] / "SKILL.md").read_text())

    def test_full_runtime_excludes_authoring_material_and_preserves_legal_files(self):
        (self.source / "LICENSE").write_text("Required license")
        files = install.payload(self.source)
        self.assertEqual(files["LICENSE"], b"Required license")
        self.assertFalse(any(name.startswith(("docs/research/", "tests/", "examples/")) for name in files))
        self.assertNotIn("AGENTS.md", files)
        self.assertNotIn("tools/install_project.py", files)
        self.assertNotIn("docs/execution-plan.md", files)

    def test_update_preserves_choices_and_explicit_selection_replaces_them(self):
        install.apply(install.plan(self.project, "all", self.source, skills=["write-spec"], with_runner=True))
        second = install.plan(self.project, "all", self.source)
        self.assertTrue(all(item["action"] == "unchanged" for item in second))
        install.apply(install.plan(self.project, "all", self.source, update=True, skills=["grill"], with_runner=False))
        bundle = self.project / install.BUNDLE
        self.assertTrue((bundle / "skills/productivity/grill/SKILL.md").is_file())
        self.assertFalse((bundle / "skills/engineering/write-spec").exists())
        self.assertFalse((bundle / "tools").exists())
        selection = json.loads((bundle / install.SELECTION).read_text())
        self.assertEqual(selection["requested_skills"], ["grill"])
        self.assertFalse(selection["with_runner"])

    def test_legacy_full_copy_migrates_and_only_owned_files_are_removed(self):
        items = install.plan(self.project, "all", self.source, with_runner=True)
        files = items[0]["files"]
        files.pop(install.SELECTION)
        files["docs/research/old-audit.md"] = b"Source-only material"
        install.apply(items)
        install.apply(install.plan(self.project, "all", self.source, update=True))
        bundle = self.project / install.BUNDLE
        self.assertFalse((bundle / "docs/research").exists())
        self.assertTrue((bundle / "tools/workflow.py").is_file())
        (bundle / "keep.md").write_text("Unmanaged project addition")
        with self.assertRaises(install.InstallError):
            install.plan(self.project, "all", self.source, update=True, skills=["grill"])
        self.assertEqual((bundle / "keep.md").read_text(), "Unmanaged project addition")

    def test_unknown_skill_missing_dependency_and_escaping_dependency_fail_before_writes(self):
        with self.assertRaises(install.InstallError):
            install.plan(self.project, "all", self.source, skills=["missing"])
        spec = self.source / "skills/engineering/write-spec/templates/spec.md"
        spec.unlink()
        with self.assertRaises(install.InstallError):
            install.plan(self.project, "all", self.source, skills=["write-spec"])
        spec.write_text("[outside](../../../../../outside.md)")
        with self.assertRaises(install.InstallError):
            install.plan(self.project, "all", self.source, skills=["write-spec"])
        self.assertEqual(list(self.project.iterdir()), [])

    def test_cli_selection_preview_is_nonmutating_and_reports_dependencies(self):
        result = subprocess.run([sys.executable, "-B", str(install.KIT / "tools/install_project.py"),
                                 str(self.project), "--agent", "codex", "--skills", "write-spec"],
                                capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        output = json.loads(result.stdout)
        self.assertFalse(output["applied"])
        self.assertEqual(output["selection"]["requested_skills"], ["write-spec"])
        self.assertEqual(output["selection"]["included_skills"], ["agent-workflow", "write-spec"])
        self.assertFalse(output["selection"]["with_runner"])
        self.assertEqual(list(self.project.iterdir()), [])

    def test_each_individual_selection_has_resolvable_local_links(self):
        for skill in sorted((self.source / "skills").rglob("SKILL.md")):
            with self.subTest(skill=skill.parent.name):
                files = install.payload(self.source, [skill.parent.name])
                for relative, content in files.items():
                    if Path(relative).suffix != ".md":
                        continue
                    for _, target in install.LINK.findall(content.decode()):
                        if "://" in target or target.startswith("#"):
                            continue
                        dependency = Path(os.path.normpath(Path(relative).parent / target.split("#")[0])).as_posix()
                        self.assertIn(dependency, files, f"Broken link: {relative}: {target}")

    def test_first_cli_install_requires_a_selection_before_writing(self):
        with patch.object(sys.stdin, "isatty", return_value=False), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(install.main([str(self.project), "--apply"]), 2)
        self.assertEqual(list(self.project.iterdir()), [])

    def test_chooser_uses_only_selected_numbers(self):
        paths = sorted(path for path in (install.KIT / "skills").rglob("SKILL.md") if path.parent.name != "agent-workflow")
        with patch.object(sys.stdin, "isatty", return_value=True), patch("builtins.input", return_value="1, 3, 1"), contextlib.redirect_stdout(io.StringIO()):
            selected = install.choose_skills(install.KIT)
        self.assertEqual(selected, sorted([paths[0].parent.name, paths[2].parent.name]))

    def test_cancelled_or_invalid_chooser_never_writes(self):
        for answer in ("", "0", "999", "all", "1,"):
            with self.subTest(answer=answer), patch.object(sys.stdin, "isatty", return_value=True), patch("builtins.input", return_value=answer), contextlib.redirect_stdout(io.StringIO()), contextlib.redirect_stderr(io.StringIO()):
                self.assertEqual(install.main([str(self.project), "--select", "--apply"]), 2)
                self.assertEqual(list(self.project.iterdir()), [])

    def test_cli_updates_preserve_choices_without_opening_chooser(self):
        install.apply(install.plan(self.project, "all", install.KIT, skills=["grill"]))
        output = io.StringIO()
        with patch("builtins.input", side_effect=AssertionError("No chooser needed")), contextlib.redirect_stdout(output):
            self.assertEqual(install.main([str(self.project), "--update"]), 0)
        result = json.loads(output.getvalue())
        self.assertEqual(result["selection"]["requested_skills"], ["grill"])
        self.assertTrue(all(item["action"] == "unchanged" for item in result["entries"]))

    def test_cli_can_explicitly_select_all_without_a_terminal(self):
        output = io.StringIO()
        with patch("builtins.input", side_effect=AssertionError("No chooser needed")), contextlib.redirect_stdout(output):
            self.assertEqual(install.main([str(self.project), "--all-skills"]), 0)
        result = json.loads(output.getvalue())
        expected = sorted(path.parent.name for path in (install.KIT / "skills").rglob("SKILL.md") if path.parent.name != "agent-workflow")
        self.assertEqual(result["selection"]["requested_skills"], expected)
        self.assertFalse(result["applied"])
        self.assertEqual(list(self.project.iterdir()), [])

    def test_race_does_not_replace_new_files(self):
        items = install.plan(self.project, "all", self.source)
        conflict = self.project / install.BUNDLE
        conflict.mkdir()
        (conflict / "keep.md").write_text("Arrived after preview")
        with self.assertRaises(install.InstallError):
            install.apply(items)
        self.assertEqual((conflict / "keep.md").read_text(), "Arrived after preview")
        self.assertFalse((self.project / ".agents").exists())

    def test_directory_escape_after_preview_is_refused_before_any_write(self):
        items = install.plan(self.project, "all", self.source)
        outside = self.root / "outside"
        outside.mkdir()
        (self.project / ".agents").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(install.InstallError):
            install.apply(items)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((self.project / install.BUNDLE).exists())


if __name__ == "__main__":
    unittest.main()
