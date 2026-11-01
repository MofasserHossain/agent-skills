import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

SPEC = importlib.util.spec_from_file_location("workspaces", Path(__file__).resolve().parents[1] / "tools/workspaces.py")
workspace = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workspace)


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.base = Path(self.temporary.name).resolve()
        self.source = self.base / "source project"
        self.source.mkdir()
        self.root = self.base / "managed workspaces"
        self.git(self.source, "init", "-b", "main")
        (self.source / "file.txt").write_text("original\n")
        self.commit(self.source)
        self.original = self.git(self.source, "rev-parse", "HEAD")

    def git(self, directory, *arguments):
        result = subprocess.run(["git", "-c", "core.hooksPath=" + workspace.os.devnull,
                                 "-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                                 *arguments], cwd=directory, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stderr)
        return result.stdout.strip()

    def commit(self, directory):
        self.git(directory, "add", "--all")
        self.git(directory, "commit", "-m", "Fixture")

    def create(self, name="feature", **options):
        result = workspace.create(self.root, self.source, name, execute=True, **options)
        return result, Path(result["checkout"])

    def test_preview_and_list_have_no_filesystem_effects(self):
        result = workspace.create(self.root, self.source, "feature")
        self.assertFalse(result["executed"])
        self.assertFalse(self.root.exists())
        self.assertEqual(workspace.list_workspaces(self.root)["workspaces"], [])
        self.assertFalse(self.root.exists())

    def test_creates_independent_checkout_without_changing_source_or_publishing(self):
        result, checkout = self.create()
        self.assertEqual(result["state"], "ready")
        self.assertEqual(self.git(checkout, "branch", "--show-current"), "workspace/feature")
        self.assertEqual(self.git(checkout, "remote"), "")
        (checkout / "file.txt").write_text("workspace only\n")
        self.assertEqual((self.source / "file.txt").read_text(), "original\n")
        self.assertEqual(self.git(self.source, "rev-parse", "HEAD"), self.original)
        self.assertEqual(self.git(self.source, "branch", "--show-current"), "main")
        listing = workspace.list_workspaces(self.root)["workspaces"]
        self.assertEqual(len(listing), 1)
        self.assertGreater(listing[0]["checkout_bytes"], 0)
        with self.assertRaises(workspace.WorkspaceError):
            self.create()

    def test_dirty_source_requires_explicit_committed_only(self):
        (self.source / "untracked.txt").write_text("do not silently copy")
        with self.assertRaises(workspace.WorkspaceError):
            self.create()
        self.assertFalse(self.root.exists())
        result, checkout = self.create(committed_only=True)
        self.assertTrue(result["source_had_changes"])
        self.assertFalse((checkout / "untracked.txt").exists())

    def test_same_named_projects_get_distinct_keys_and_multiple_workspaces(self):
        first, _ = self.create()
        second, _ = self.create("another-task")
        self.assertEqual(first["project"], second["project"])
        other = self.base / "another owner" / self.source.name
        other.parent.mkdir()
        self.git(self.source, "clone", "--", str(self.source), str(other))
        third = workspace.create(self.root, other, "feature", execute=True)
        self.assertNotEqual(first["project"], third["project"])
        self.assertEqual(len(workspace.list_workspaces(self.root)["workspaces"]), 3)

    def test_archive_purge_restore_round_trip_retains_branches_tags_and_binary_work(self):
        result, checkout = self.create()
        (checkout / "new.bin").write_bytes(bytes(range(256)))
        self.commit(checkout)
        self.git(checkout, "tag", "saved-version")
        self.git(checkout, "branch", "other-branch")
        expected = workspace.clean_snapshot(checkout)
        self.assertFalse(workspace.archive_workspace(self.root, result["project"], "feature")["executed"])
        self.assertFalse((self.root / result["project"] / "archives/feature").exists())
        workspace.archive_workspace(self.root, result["project"], "feature", execute=True)
        archive = self.root / result["project"] / "archives/feature"
        self.assertTrue(list(archive.glob("*.bundle")))
        self.assertFalse(workspace.purge(self.root, result["project"], "feature")["executed"])
        self.assertTrue(checkout.exists())
        workspace.purge(self.root, result["project"], "feature", execute=True)
        self.assertFalse(checkout.exists())
        self.assertTrue(archive.exists())
        self.assertEqual(workspace.list_workspaces(self.root)["workspaces"][0]["state"], "purged")
        workspace.restore(self.root, result["project"], "feature", execute=True)
        self.assertEqual(workspace.clean_snapshot(checkout), expected)
        self.assertEqual((checkout / "new.bin").read_bytes(), bytes(range(256)))
        self.assertEqual((self.source / "file.txt").read_text(), "original\n")

    def test_archive_refuses_changed_untracked_and_ignored_files(self):
        result, checkout = self.create()
        (checkout / ".gitignore").write_text("cache/\n")
        self.commit(checkout)
        for kind in ("tracked", "untracked", "ignored"):
            with self.subTest(kind=kind):
                target = checkout / ("file.txt" if kind == "tracked" else
                                     "extra.txt" if kind == "untracked" else "cache/keep")
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_text("unique work")
                with self.assertRaises(workspace.WorkspaceError):
                    workspace.archive_workspace(self.root, result["project"], "feature", execute=True)
                self.assertTrue(target.exists())
                if kind == "tracked":
                    target.write_text("original\n")
                else:
                    target.unlink()
                    if kind == "ignored":
                        target.parent.rmdir()

    def test_purge_refuses_new_work_and_corrupt_archive(self):
        result, checkout = self.create()
        workspace.archive_workspace(self.root, result["project"], "feature", execute=True)
        (checkout / "file.txt").write_text("new edits")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.purge(self.root, result["project"], "feature", execute=True)
        (checkout / "file.txt").write_text("original\n")
        _, bundle = workspace.verified_archive(self.root / result["project"] / "archives/feature", result["project"], "feature")
        bundle.write_bytes(bundle.read_bytes() + b"corrupted")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.purge(self.root, result["project"], "feature", execute=True)
        self.assertTrue(checkout.exists())

    def test_lock_and_path_substitution_prevent_removal(self):
        result, checkout = self.create()
        workspace.archive_workspace(self.root, result["project"], "feature", execute=True)
        record = self.root / result["project"] / "records/feature"
        (record / "operation.lock").write_text("interrupted")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.purge(self.root, result["project"], "feature", execute=True)
        (record / "operation.lock").unlink()
        preserved = checkout.with_name("preserved")
        checkout.rename(preserved)
        checkout.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(workspace.WorkspaceError):
            workspace.purge(self.root, result["project"], "feature", execute=True)
        self.assertTrue(preserved.exists())
        self.assertTrue(self.source.exists())

    def test_claims_hidden_changes_and_new_commits_block_cleanup(self):
        result, checkout = self.create()
        record = self.root / result["project"] / "records/feature"
        (record / "worker.lock").write_text("active")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.archive_workspace(self.root, result["project"], "feature", execute=True)
        (record / "worker.lock").unlink()
        self.git(checkout, "update-index", "--assume-unchanged", "file.txt")
        (checkout / "file.txt").write_text("hidden work")
        with self.assertRaises(workspace.WorkspaceError):
            workspace.archive_workspace(self.root, result["project"], "feature", execute=True)
        self.git(checkout, "update-index", "--no-assume-unchanged", "file.txt")
        self.commit(checkout)
        workspace.archive_workspace(self.root, result["project"], "feature", execute=True)
        (checkout / "file.txt").write_text("another commit")
        self.commit(checkout)
        with self.assertRaises(workspace.WorkspaceError):
            workspace.purge(self.root, result["project"], "feature", execute=True)
        workspace.archive_workspace(self.root, result["project"], "feature", execute=True)
        self.assertEqual(len(list((self.root / result["project"] / "archives/feature").glob("*.bundle"))), 2)
        workspace.purge(self.root, result["project"], "feature", execute=True)
        workspace.restore(self.root, result["project"], "feature", execute=True)
        self.assertEqual((checkout / "file.txt").read_text(), "another commit")

    def test_failed_restore_verification_preserves_checkout_and_failure_record(self):
        result, checkout = self.create()
        with mock.patch.object(workspace, "restore_checkout", side_effect=workspace.WorkspaceError("bad export")):
            with self.assertRaises(workspace.WorkspaceError):
                workspace.archive_workspace(self.root, result["project"], "feature", execute=True)
        value, _, _, _ = workspace.load(self.root, result["project"], "feature")
        self.assertEqual(value["state"], "failed")
        self.assertTrue(checkout.exists())
        with self.assertRaises(workspace.WorkspaceError):
            workspace.purge(self.root, result["project"], "feature", execute=True)

    def test_invalid_names_overlapping_roots_and_symlink_roots_are_rejected(self):
        for name in ("../escape", "", "Uppercase", "--flag"):
            with self.subTest(name=name), self.assertRaises(workspace.WorkspaceError):
                workspace.create(self.root, self.source, name, execute=True)
        with self.assertRaises(workspace.WorkspaceError):
            workspace.create(self.source / "workspaces", self.source, "feature", execute=True)
        self.root.symlink_to(self.source, target_is_directory=True)
        with self.assertRaises(workspace.WorkspaceError):
            workspace.list_workspaces(self.root)

    def test_cli_preview_emits_json_without_creating_directories(self):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = workspace.main(["--root", str(self.root), "create", "feature", "--project", str(self.source)])
        self.assertEqual((code, err.getvalue()), (0, ""))
        self.assertFalse(json.loads(out.getvalue())["executed"])
        self.assertFalse(self.root.exists())


if __name__ == "__main__":
    unittest.main()
