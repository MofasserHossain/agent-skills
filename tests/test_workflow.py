import contextlib
import importlib.util
import io
import json
from pathlib import Path
import sys
import tempfile
import time
import unittest

SPEC = importlib.util.spec_from_file_location("workflow", Path(__file__).resolve().parents[1] / "tools/workflow.py")
workflow = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(workflow)


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.project = self.root / "project with spaces"
        self.project.mkdir()
        self.call("init", str(self.project))
        self.issues = self.project / "docs/work/example/issues"
        self.issues.mkdir(parents=True)
        self.task = self.write_task("01-example")

    def call(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = workflow.main(list(args))
        return code, out.getvalue(), err.getvalue()

    def write_task(self, task_id, **changes):
        metadata = {
            "schema_version": 1, "id": task_id, "status": "ready",
            "execution": "afk", "review": "human", "blocked_by": [],
        }
        metadata.update(changes)
        path = self.issues / (task_id + ".md")
        path.write_text(
            "---\n" + json.dumps(metadata) + "\n---\n"
            "# Preserve a setting\n\n## Expected behavior\n"
            "The saved choice survives restart.\n\n## Acceptance criteria\n"
            "- [ ] Restart retains the choice.\n\n## Verification\n"
            "Run the persistence test.\n"
        )
        return path

    def registry(self, command):
        path = self.root / "executor-overrides.json"
        path.write_text(json.dumps({
            "schema_version": 1,
            "agents": {"codex": {"label": "Local fake executor", "command": command}}
        }))
        return path

    def run_args(self, *extra):
        return ("run", str(self.task), "--project", str(self.project), *extra)

    def test_init_preserves_existing_instructions_and_configuration(self):
        instructions = self.project / "AGENTS.md"
        instructions.write_text("Existing rules.")
        config = self.project / workflow.CONFIG
        original = config.read_bytes()
        code, _, _ = self.call("init", str(self.project))
        self.assertEqual(code, 2)
        self.assertEqual(config.read_bytes(), original)
        self.assertEqual(instructions.read_text(), "Existing rules.")
        self.assertEqual(sorted(p.name for p in self.project.iterdir()),
                         [workflow.CONFIG, "AGENTS.md", "docs"])

    def test_preview_does_not_start_executor(self):
        marker = self.root / "should-not-exist"
        registry = self.registry([sys.executable, "-c", f"open({str(marker)!r}, 'w').write('ran')"])
        code, out, _ = self.call(*self.run_args("--agent", "codex", "--registry", str(registry)))
        self.assertEqual(code, 0)
        self.assertFalse(json.loads(out)["executed"])
        self.assertFalse(marker.exists())
        self.assertFalse((self.project / ".workflow-runs").exists())

    def test_executor_override_receives_prompt_and_project_without_accepting_task(self):
        registry = self.registry([
            sys.executable, "-c",
            "import json,sys,pathlib; text=sys.stdin.read(); "
            "print(json.dumps({'cwd':str(pathlib.Path.cwd()),'prompt':text,'args':sys.argv[1:]}))",
            "$(this-is-literal)", "an argument with spaces",
        ])
        before = self.task.read_bytes()
        code, _, err = self.call(*self.run_args(
            "--agent", "codex", "--registry", str(registry), "--execute"))
        self.assertEqual((code, err), (0, ""))
        output = next((self.project / ".workflow-runs").iterdir())
        response = json.loads((output / "stdout.txt").read_text())
        self.assertEqual(Path(response["cwd"]).resolve(), self.project.resolve())
        self.assertIn("Restart retains the choice.", response["prompt"])
        self.assertIn("Required report", response["prompt"])
        self.assertEqual(response["args"], ["$(this-is-literal)", "an argument with spaces"])
        result = json.loads((output / "result.json").read_text())
        self.assertEqual(result["status"], "process-completed")
        self.assertFalse(result["accepted"])
        self.assertEqual(self.task.read_bytes(), before)

    def test_failed_executor_keeps_failure_evidence(self):
        registry = self.registry([sys.executable, "-c", "import sys; print('failure details',file=sys.stderr); sys.exit(7)"])
        code, _, _ = self.call(*self.run_args("--agent", "codex", "--registry", str(registry), "--execute"))
        self.assertEqual(code, 7)
        output = next((self.project / ".workflow-runs").iterdir())
        result = json.loads((output / "result.json").read_text())
        self.assertEqual(result["status"], "failed")
        self.assertFalse(result["accepted"])
        self.assertIn("failure details", (output / "stderr.txt").read_text())

    def test_timeout_stops_executor(self):
        output = self.root / "timeout-run"
        started = time.monotonic()
        code = workflow.dispatch([sys.executable, "-c", "import time; time.sleep(10)"],
                                 "task", self.project, output, 0.1)
        self.assertEqual(code, 124)
        self.assertLess(time.monotonic() - started, 3)
        self.assertEqual(json.loads((output / "result.json").read_text())["status"], "timed-out")

    @unittest.skipUnless(sys.platform != "win32", "POSIX process-group behavior")
    def test_timeout_stops_child_processes_too(self):
        marker = self.root / "child-finished"
        child = f"import time,pathlib; time.sleep(0.5); pathlib.Path({str(marker)!r}).write_text('finished')"
        parent = f"import subprocess,sys,time; subprocess.Popen([sys.executable,'-c',{child!r}]); time.sleep(10)"
        code = workflow.dispatch([sys.executable, "-c", parent], "task", self.project,
                                 self.root / "tree-timeout", 0.15)
        self.assertEqual(code, 124)
        time.sleep(0.6)
        self.assertFalse(marker.exists())

    def test_hitl_and_nonready_tasks_are_not_dispatched(self):
        for change in ({"execution": "hitl"}, {"status": "blocked"}, {"status": "done"}):
            self.write_task("01-example", **change)
            code, _, _ = self.call(*self.run_args())
            self.assertEqual(code, 2)

    def test_dependencies_must_be_done(self):
        self.write_task("01-example", blocked_by=["02-prerequisite"])
        self.write_task("02-prerequisite", status="review")
        code, _, err = self.call(*self.run_args())
        self.assertEqual(code, 2)
        self.assertIn("Unfinished blockers", err)
        self.write_task("02-prerequisite", status="done")
        self.assertEqual(self.call(*self.run_args())[0], 0)

    def test_unknown_or_duplicate_dependencies_are_refused(self):
        self.write_task("01-example", blocked_by=["missing"])
        self.assertEqual(self.call(*self.run_args())[0], 2)
        self.write_task("01-example", blocked_by=["missing", "missing"])
        self.assertEqual(self.call(*self.run_args())[0], 2)

    def test_duplicate_task_ids_are_refused(self):
        (self.issues / "duplicate.md").write_bytes(self.task.read_bytes())
        self.assertEqual(self.call(*self.run_args())[0], 2)

    def test_task_cannot_leave_project_work_directory(self):
        outside = self.root / "outside.md"
        outside.write_bytes(self.task.read_bytes())
        code, _, _ = self.call("prompt", str(outside), "--project", str(self.project))
        self.assertEqual(code, 2)

    def test_symlink_cannot_smuggle_external_task_into_context(self):
        outside = self.root / "outside.md"
        outside.write_bytes(self.task.read_bytes())
        (self.issues / "external.md").symlink_to(outside)
        self.assertEqual(self.call(*self.run_args())[0], 2)

    def test_work_directory_cannot_escape_project(self):
        config = json.loads((self.project / workflow.CONFIG).read_text())
        config["work_dir"] = "../outside"
        (self.project / workflow.CONFIG).write_text(json.dumps(config))
        self.assertEqual(self.call(*self.run_args())[0], 2)

    def test_github_owned_work_is_not_dispatched_as_local(self):
        path = self.project / workflow.CONFIG
        config = json.loads(path.read_text())
        config["tracker"] = "github"
        path.write_text(json.dumps(config))
        self.assertEqual(self.call(*self.run_args())[0], 2)

    def test_registry_cannot_turn_command_into_shell_string(self):
        registry = self.registry("echo hello")
        code, _, _ = self.call("agents", "--registry", str(registry))
        self.assertEqual(code, 2)

    def test_nonfinite_timeouts_are_refused(self):
        for timeout in ("nan", "inf", "0", "-1"):
            self.assertEqual(self.call(*self.run_args("--timeout", timeout))[0], 2)

    def test_malformed_metadata_returns_a_useful_failure(self):
        for changes in ({"status": {}}, {"execution": []}, {"review": {}}):
            self.write_task("01-example", **changes)
            self.assertEqual(self.call(*self.run_args())[0], 2)

    def test_output_directory_cannot_be_redirected_outside_project(self):
        registry = self.registry([sys.executable, "-c", "print('ran')"])
        outside = self.root / "outside-logs"
        outside.mkdir()
        (self.project / ".workflow-runs").symlink_to(outside, target_is_directory=True)
        code, _, _ = self.call(*self.run_args("--agent", "codex", "--registry", str(registry), "--execute"))
        self.assertEqual(code, 2)
        self.assertEqual(list(outside.iterdir()), [])

    def test_context_is_executor_neutral_and_loads_only_active_procedure(self):
        code, prompt, _ = self.call("prompt", str(self.task), "--project", str(self.project))
        self.assertEqual(code, 0)
        self.assertIn("Portable implementation request", prompt)
        self.assertIn("Read the selected task", prompt)
        self.assertNotIn("Turn meeting notes", prompt)
        self.assertNotIn("claude exec", prompt)
        self.assertNotIn("codex exec", prompt)

    def test_missing_executor_fails_without_changing_task(self):
        registry = self.registry(["not-a-real-agent-workflow-executor"])
        before = self.task.read_bytes()
        code, _, err = self.call(*self.run_args("--agent", "codex", "--registry", str(registry), "--execute"))
        self.assertEqual(code, 2)
        self.assertIn("not installed", err)
        self.assertEqual(self.task.read_bytes(), before)

    def test_registry_and_project_reject_other_agents(self):
        registry = self.root / "unsupported-agent.json"
        registry.write_text(json.dumps({"schema_version": 1, "agents": {
            "other-agent": {"label": "Unsupported", "command": ["unused"]}
        }}))
        self.assertEqual(self.call("agents", "--registry", str(registry))[0], 2)
        config = self.project / workflow.CONFIG
        data = json.loads(config.read_text())
        data["default_agent"] = "other-agent"
        config.write_text(json.dumps(data))
        self.assertEqual(self.call(*self.run_args())[0], 2)
        self.assertFalse((self.project / ".workflow-runs").exists())

    def test_manual_is_context_only_and_agent_listing_has_two_targets(self):
        code, output, err = self.call("agents")
        self.assertEqual((code, err), (0, ""))
        self.assertEqual({line.split(":", 1)[0] for line in output.splitlines()},
                         {"claude", "codex"})
        code, output, err = self.call(*self.run_args("--execute"))
        self.assertEqual((code, err), (0, ""))
        self.assertIn("Portable implementation request", output)
        self.assertFalse((self.project / ".workflow-runs").exists())
        registry = self.registry(None)
        self.assertEqual(self.call("agents", "--registry", str(registry))[0], 2)
        registry.write_text(json.dumps({"schema_version": 1, "agents": {
            "manual": {"command": ["unused"]}
        }}))
        self.assertEqual(self.call("agents", "--registry", str(registry))[0], 2)

    def test_named_checks_reject_malformed_commands_and_names(self):
        config = self.project / workflow.CONFIG
        original = json.loads(config.read_text())
        for checks in ([], None, {"test": "npm test"}, {"test": []},
                       {"test": ["", "test"]}, {"test": ["runner", 3]},
                       {"test suite": ["runner"]}, {"Test": ["runner"]}):
            with self.subTest(checks=checks):
                config.write_text(json.dumps({**original, "checks": checks}))
                code, _, err = self.call("prompt", str(self.task), "--project", str(self.project))
                self.assertEqual(code, 2)
                self.assertIn("checks must map", err)
        self.assertFalse((self.project / ".workflow-runs").exists())

    def test_changed_project_commands_reach_next_prompt_without_running_checks(self):
        config = self.project / workflow.CONFIG
        original = json.loads(config.read_text())
        # A check with an observable side effect must only be passed as context.
        marker = self.root / "check-was-run"
        first = {"test-unit": [sys.executable, "-c",
                              f"open({str(marker)!r}, 'w').write('ran')"]}
        second = {"test-unit": ["different-runner", "tests with spaces", "--once"],
                  "types": ["project-types"]}
        for checks in (first, second):
            config.write_text(json.dumps({**original, "checks": checks}))
            code, prompt, err = self.call("prompt", str(self.task), "--project", str(self.project))
            self.assertEqual((code, err), (0, ""))
            supplied = prompt.split("## Project configuration\n", 1)[1].split("\n\n## Active procedure", 1)[0]
            self.assertEqual(json.loads(supplied)["checks"], checks)
            self.assertFalse(marker.exists())
        self.assertNotIn(str(marker), prompt)
        self.assertFalse((self.project / ".workflow-runs").exists())

    def test_legacy_config_without_named_checks_remains_supported(self):
        config = self.project / workflow.CONFIG
        original = json.loads(config.read_text())
        original.pop("checks", None)
        config.write_text(json.dumps(original))
        code, _, err = self.call("prompt", str(self.task), "--project", str(self.project))
        self.assertEqual((code, err), (0, ""))


if __name__ == "__main__":
    unittest.main()
