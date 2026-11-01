import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location(
    "register_skills", Path(__file__).resolve().parents[1] / "tools/register_skills.py"
)
register = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(register)


class RegistrationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.destination = self.root / "personal skills" / register.NAME

    def test_preview_never_creates_directories(self):
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            code = register.main(["--skills-dir", str(self.destination.parent)])
        self.assertEqual(code, 0)
        self.assertFalse(self.destination.parent.exists())
        self.assertFalse(json.loads(out.getvalue())["applied"])

    def test_registration_is_one_thin_entry_with_resolvable_source(self):
        plan, body, marker = register.plan_registration([self.destination], register.KIT)
        register.apply_registration(plan, body, marker)
        self.assertEqual(sorted(p.name for p in self.destination.iterdir()),
                         [register.MARKER, "SKILL.md"])
        source = Path(json.loads((self.destination / register.MARKER).read_text())["source_root"])
        self.assertTrue((source / "skills/agent-workflow/SKILL.md").is_file())
        self.assertIn(str(source / "skills/agent-workflow/SKILL.md"), body)
        self.assertNotIn("name: implement", body)

    def test_reregistration_preserves_existing_file(self):
        plan, body, marker = register.plan_registration([self.destination], register.KIT)
        register.apply_registration(plan, body, marker)
        before = (self.destination / "SKILL.md").stat().st_mtime_ns
        second, _, _ = register.plan_registration([self.destination], register.KIT)
        self.assertEqual(second[0]["action"], "unchanged")
        register.apply_registration(second, body, marker)
        self.assertEqual((self.destination / "SKILL.md").stat().st_mtime_ns, before)

    def test_unmanaged_skill_is_not_overwritten(self):
        self.destination.mkdir(parents=True)
        existing = self.destination / "SKILL.md"
        existing.write_text("Existing personal instructions")
        with self.assertRaises(register.RegistrationError):
            register.plan_registration([self.destination], register.KIT)
        self.assertEqual(existing.read_text(), "Existing personal instructions")

    def test_edited_managed_skill_is_not_overwritten(self):
        plan, body, marker = register.plan_registration([self.destination], register.KIT)
        register.apply_registration(plan, body, marker)
        (self.destination / "SKILL.md").write_text("Personal edit")
        with self.assertRaises(register.RegistrationError):
            register.plan_registration([self.destination], register.KIT)
        self.assertEqual((self.destination / "SKILL.md").read_text(), "Personal edit")

    def test_all_destinations_are_validated_before_apply(self):
        conflict = self.root / "other" / register.NAME
        conflict.mkdir(parents=True)
        (conflict / "SKILL.md").write_text("Keep")
        with self.assertRaises(register.RegistrationError):
            register.plan_registration([self.destination, conflict], register.KIT)
        self.assertFalse(self.destination.exists())

    def test_existing_symlink_is_not_followed_or_replaced(self):
        original = self.root / "original"
        original.mkdir()
        self.destination.parent.mkdir()
        self.destination.symlink_to(original, target_is_directory=True)
        with self.assertRaises(register.RegistrationError):
            register.plan_registration([self.destination], register.KIT)
        self.assertTrue(self.destination.is_symlink())

    def test_race_does_not_overwrite_new_destination(self):
        plan, body, marker = register.plan_registration([self.destination], register.KIT)
        self.destination.mkdir(parents=True)
        (self.destination / "SKILL.md").write_text("Created by somebody else")
        with self.assertRaises(register.RegistrationError):
            register.apply_registration(plan, body, marker)
        self.assertEqual((self.destination / "SKILL.md").read_text(), "Created by somebody else")

    def test_native_paths_are_under_the_selected_home(self):
        paths = register.destinations(agent="all", home=self.root)
        self.assertEqual(set(paths), {
            self.root / ".agents/skills/agent-workflow",
            self.root / ".claude/skills/agent-workflow",
        })

    def test_apply_uses_custom_directory_without_touching_home(self):
        out = io.StringIO()
        with patch.object(register.Path, "home", side_effect=AssertionError("Home not needed")):
            with contextlib.redirect_stdout(out):
                code = register.main(["--skills-dir", str(self.destination.parent), "--apply"])
        self.assertEqual(code, 0)
        self.assertTrue((self.destination / "SKILL.md").is_file())

    def test_registration_points_to_same_kit_from_different_projects(self):
        script = register.KIT / "tools/register_skills.py"
        for name in ("project-a", "project-b"):
            project = self.root / name
            project.mkdir()
            result = subprocess.run(
                [sys.executable, str(script), "--skills-dir",
                 str(self.destination.parent), "--apply"],
                cwd=project, capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            marker = json.loads((self.destination / register.MARKER).read_text())
            self.assertEqual(marker["source_root"], str(register.KIT))

    def test_project_preview_does_not_create_skill_directories(self):
        project = self.root / "project with spaces"
        project.mkdir()
        out = io.StringIO()
        with patch.object(register.Path, "home", side_effect=AssertionError("Home not needed")):
            with contextlib.redirect_stdout(out):
                code = register.main(["--agent", "all", "--project", str(project)])
        self.assertEqual(code, 0)
        self.assertEqual(list(project.iterdir()), [])
        plan = json.loads(out.getvalue())
        self.assertFalse(plan["applied"])
        self.assertEqual({Path(item["path"]) for item in plan["registrations"]}, {
            project.resolve() / ".agents/skills/agent-workflow",
            project.resolve() / ".claude/skills/agent-workflow",
        })

    def test_project_apply_from_another_directory_preserves_project_files(self):
        project = self.root / "target project"
        project.mkdir()
        rules = project / "AGENTS.md"
        rules.write_text("Existing project rules")
        ignores = project / ".gitignore"
        ignores.write_text("existing-ignore/\n")
        elsewhere = self.root / "elsewhere"
        elsewhere.mkdir()
        args = [sys.executable, str(register.KIT / "tools/register_skills.py"),
                "--agent", "all", "--project", str(project), "--apply"]
        for expected in ("create", "unchanged"):
            result = subprocess.run(args, cwd=elsewhere, capture_output=True, text=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual({item["action"] for item in json.loads(result.stdout)["registrations"]},
                             {expected})
        for directory in (".agents", ".claude"):
            destination = project / directory / "skills" / register.NAME
            marker = json.loads((destination / register.MARKER).read_text())
            self.assertEqual(marker["source_root"], str(register.KIT))
            self.assertEqual(sorted(p.name for p in destination.iterdir()),
                             [register.MARKER, "SKILL.md"])
        self.assertEqual(rules.read_text(), "Existing project rules")
        self.assertEqual(ignores.read_text(), "existing-ignore/\n")
        self.assertFalse((elsewhere / ".agents").exists())
        self.assertFalse((project / ".agent-workflow.json").exists())

    def test_project_registration_refuses_missing_target_and_custom_directory(self):
        with self.assertRaises(register.RegistrationError):
            register.destinations(agent="all", project=self.root / "missing")
        with self.assertRaises(register.RegistrationError):
            register.destinations(project=self.root, skills_dir=self.destination.parent)
        self.assertFalse(self.destination.exists())

    def test_project_registration_refuses_agent_directory_outside_project(self):
        project = self.root / "project"
        project.mkdir()
        outside = self.root / "outside"
        outside.mkdir()
        (project / ".agents").symlink_to(outside, target_is_directory=True)
        with self.assertRaises(register.RegistrationError):
            register.destinations(agent="all", project=project)
        self.assertEqual(list(outside.iterdir()), [])
        self.assertFalse((project / ".claude").exists())

    def test_project_aliases_register_one_shared_entry(self):
        project = self.root / "project"
        project.mkdir()
        (project / ".claude").mkdir()
        (project / ".agents").symlink_to(".claude", target_is_directory=True)
        paths = register.destinations(agent="all", project=project)
        self.assertEqual(paths, [project.resolve() / ".claude/skills/agent-workflow"])
        plan, body, marker = register.plan_registration(paths, register.KIT)
        register.apply_registration(plan, body, marker)
        self.assertTrue((project / ".agents/skills/agent-workflow/SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()
