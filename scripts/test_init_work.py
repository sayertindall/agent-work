#!/usr/bin/env python3
"""Behavioral tests for the work-init scaffold CLI in disposable directories."""

from __future__ import annotations

import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from typing import Dict, Optional, Tuple


SOURCE = Path(__file__).resolve().parents[1] / "skills/work-init/scripts/init_work.py"


def run_cli(
    target: Path,
    *flags: str,
    environment: Optional[Dict[str, str]] = None,
) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    if environment is not None:
        env.update(environment)
    return subprocess.run(
        [sys.executable, "-B", str(SOURCE), str(target), *flags],
        check=False,
        capture_output=True,
        text=True,
        env=env,
    )


def git(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments], check=False, capture_output=True, text=True
    )


def filesystem_snapshot(root: Path) -> Tuple[Tuple[str, int, int, int, bytes], ...]:
    """Capture names, types, timestamps, and bytes without following links."""

    if not os.path.lexists(root):
        return ()
    paths = [root]
    for current, directories, files in os.walk(root, topdown=True, followlinks=False):
        directories.sort()
        files.sort()
        paths.extend(Path(current) / name for name in directories)
        paths.extend(Path(current) / name for name in files)

    snapshot = []
    for path in paths:
        metadata = os.lstat(path)
        relative = "." if path == root else path.relative_to(root).as_posix()
        content = b""
        if stat.S_ISREG(metadata.st_mode):
            content = path.read_bytes()
        elif stat.S_ISLNK(metadata.st_mode):
            content = os.readlink(path).encode()
        snapshot.append(
            (
                relative,
                stat.S_IFMT(metadata.st_mode),
                metadata.st_size,
                metadata.st_mtime_ns,
                content,
            )
        )
    return tuple(snapshot)


class WorkInitTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory(prefix="work-init-tests-")
        self.addCleanup(self.temp_directory.cleanup)
        self.temp_root = Path(self.temp_directory.name)

    def assertSuccess(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def assertFailure(self, result: subprocess.CompletedProcess[str]) -> None:
        self.assertNotEqual(
            result.returncode,
            0,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )

    def test_fresh_create_has_only_scaffold_paths(self) -> None:
        target = self.temp_root / "work"
        result = run_cli(target)
        self.assertSuccess(result)

        directories = {
            "plans",
            "plans/drafts",
            "plans/ready",
            "plans/active",
            "plans/done",
            "plans/discarded",
            "projects",
            "evidence",
        }
        files = {
            "README.md",
            *(f"{directory}/.gitkeep" for directory in directories if directory != "plans"),
        }
        actual_directories = set()
        actual_files = set()
        for current, child_directories, child_files in os.walk(target):
            current_path = Path(current)
            for name in child_directories:
                actual_directories.add((current_path / name).relative_to(target).as_posix())
            for name in child_files:
                actual_files.add((current_path / name).relative_to(target).as_posix())
        self.assertEqual(actual_directories, directories)
        self.assertEqual(actual_files, files)
        readme = (target / "README.md").read_text(encoding="utf-8")
        self.assertIn("plans/drafts/", readme)
        self.assertIn("single-writer rule", readme)
        self.assertIn(f"Work root: {target.resolve()}", result.stdout)
        self.assertIn("Result: success", result.stdout)

    def test_repeat_preserves_user_readme_plan_and_keeper_bytes(self) -> None:
        target = self.temp_root / "work"
        self.assertSuccess(run_cli(target))
        readme_bytes = b"User README\nwith local notes\xff\n"
        plan_bytes = b"# User plan\n\nDo not replace this record.\n"
        keeper_bytes = b"user keeper marker\n"
        (target / "README.md").write_bytes(readme_bytes)
        (target / "plans/drafts/user-plan.md").write_bytes(plan_bytes)
        (target / "plans/ready/.gitkeep").write_bytes(keeper_bytes)

        result = run_cli(target)
        self.assertSuccess(result)
        self.assertEqual((target / "README.md").read_bytes(), readme_bytes)
        self.assertEqual((target / "plans/drafts/user-plan.md").read_bytes(), plan_bytes)
        self.assertEqual((target / "plans/ready/.gitkeep").read_bytes(), keeper_bytes)
        self.assertIn("Created: none", result.stdout)

    def test_existing_directory_keeps_unrelated_files(self) -> None:
        target = self.temp_root / "existing"
        target.mkdir()
        unrelated = target / "notes.txt"
        unrelated.write_text("owned by the user\n", encoding="utf-8")
        result = run_cli(target)
        self.assertSuccess(result)
        self.assertEqual(unrelated.read_text(encoding="utf-8"), "owned by the user\n")
        self.assertTrue((target / "plans/active").is_dir())

    def test_check_missing_target_is_read_only_failure(self) -> None:
        target = self.temp_root / "missing"
        before = filesystem_snapshot(target)
        result = run_cli(target, "--check")
        self.assertFailure(result)
        self.assertEqual(filesystem_snapshot(target), before)
        self.assertFalse(os.path.lexists(target))
        self.assertIn("Missing:", result.stdout)
        self.assertIn("plans/drafts", result.stdout)
        self.assertIn("README.md", result.stdout)
        self.assertIn("Result: failure", result.stdout)

    def test_check_incomplete_existing_directory_is_read_only(self) -> None:
        target = self.temp_root / "incomplete"
        target.mkdir()
        (target / "user.txt").write_bytes(b"keep\n")
        before = filesystem_snapshot(target)
        result = run_cli(target, "--check")
        self.assertFailure(result)
        self.assertEqual(filesystem_snapshot(target), before)
        self.assertIn("plans", result.stdout)
        self.assertIn("README.md", result.stdout)

    def test_check_complete_structure_is_read_only_success(self) -> None:
        target = self.temp_root / "complete"
        self.assertSuccess(run_cli(target))
        before = filesystem_snapshot(target)
        result = run_cli(target, "--check")
        self.assertSuccess(result)
        self.assertEqual(filesystem_snapshot(target), before)
        self.assertIn("Structure: complete", result.stdout)

    def test_check_reports_regular_file_conflict_without_writes(self) -> None:
        target = self.temp_root / "conflict"
        target.mkdir()
        (target / "plans").write_bytes(b"this is a conflicting file\n")
        before = filesystem_snapshot(target)
        result = run_cli(target, "--check")
        self.assertFailure(result)
        self.assertEqual(filesystem_snapshot(target), before)
        self.assertIn("Conflicts:", result.stdout)
        self.assertIn("plans: expected a directory", result.stdout)

    def test_git_initializes_new_target_on_main_without_remote_or_commit(self) -> None:
        target = self.temp_root / "git-work"
        result = run_cli(target, "--git")
        self.assertSuccess(result)
        self.assertTrue((target / ".git").is_dir())
        branch = git("-C", str(target), "branch", "--show-current")
        self.assertEqual(branch.stdout.strip(), "main")
        remote = git("-C", str(target), "remote")
        self.assertEqual(remote.stdout.strip(), "")
        head = git("-C", str(target), "rev-parse", "--verify", "HEAD")
        self.assertNotEqual(head.returncode, 0)
        self.assertIn("initialized repository on main", result.stdout)

    def test_git_reuses_existing_parent_without_nested_repository(self) -> None:
        parent = self.temp_root / "parent"
        parent.mkdir()
        initialized = git("init", "-b", "main", str(parent))
        self.assertEqual(initialized.returncode, 0, initialized.stderr)
        target = parent / "nested-work"
        result = run_cli(target, "--git")
        self.assertSuccess(result)
        self.assertFalse((target / ".git").exists())
        owner = git("-C", str(target), "rev-parse", "--show-toplevel")
        self.assertEqual(owner.returncode, 0, owner.stderr)
        self.assertEqual(Path(owner.stdout.strip()).resolve(), parent.resolve())
        self.assertIn("reusing repository", result.stdout)

    def test_git_preflight_failure_does_not_create_target(self) -> None:
        target = self.temp_root / "no-git"
        result = run_cli(target, "--git", environment={"PATH": ""})
        self.assertFailure(result)
        self.assertFalse(os.path.lexists(target))
        self.assertIn("Git is unavailable", result.stdout)

    def test_git_rejects_environment_overrides_before_writes(self) -> None:
        for variable in ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE"):
            with self.subTest(variable=variable):
                target = self.temp_root / variable.lower()
                result = run_cli(target, "--git", environment={variable: "/tmp/redirect"})
                self.assertFailure(result)
                self.assertFalse(os.path.lexists(target))
                self.assertIn(variable, result.stdout)

    def test_symlinked_managed_paths_are_refused_before_writes(self) -> None:
        outside = self.temp_root / "outside"
        outside.mkdir()
        (outside / "sentinel.txt").write_bytes(b"outside\n")

        target = self.temp_root / "symlink-directory"
        target.mkdir()
        (target / "plans").symlink_to(outside, target_is_directory=True)
        before = filesystem_snapshot(target)
        result = run_cli(target)
        self.assertFailure(result)
        self.assertEqual(filesystem_snapshot(target), before)
        self.assertFalse((outside / "drafts").exists())
        self.assertIn("plans: symlink is not allowed", result.stdout)

        target_file = self.temp_root / "symlink-file"
        target_file.mkdir()
        (target_file / "README.md").symlink_to(outside / "sentinel.txt")
        before_file = filesystem_snapshot(target_file)
        result_file = run_cli(target_file)
        self.assertFailure(result_file)
        self.assertEqual(filesystem_snapshot(target_file), before_file)
        self.assertIn("README.md: symlink is not allowed", result_file.stdout)

    def test_git_conflict_is_rejected_before_git_initialization(self) -> None:
        target = self.temp_root / "git-conflict"
        target.mkdir()
        (target / "projects").write_bytes(b"conflict\n")
        before = filesystem_snapshot(target)
        result = run_cli(target, "--git")
        self.assertFailure(result)
        self.assertEqual(filesystem_snapshot(target), before)
        self.assertFalse((target / ".git").exists())
        self.assertIn("projects: expected a directory", result.stdout)

    def test_git_invalid_existing_marker_fails_closed(self) -> None:
        target = self.temp_root / "invalid-git"
        target.mkdir()
        (target / ".git").write_text("invalid marker\n", encoding="utf-8")
        result = run_cli(target, "--git")
        self.assertFailure(result)
        self.assertFalse((target / "plans").exists())
        self.assertIn("cannot safely inspect Git repository", result.stdout)

    def test_git_unexpected_probe_failure_fails_closed_without_marker(self) -> None:
        fake_bin = self.temp_root / "fake-bin"
        fake_bin.mkdir()
        fake_git = fake_bin / "git"
        fake_git.write_text(
            "#!/bin/sh\n"
            "if [ \"$1\" = \"--version\" ]; then echo 'git version fake'; exit 0; fi\n"
            "echo 'fatal: synthetic probe failure' >&2\n"
            "exit 17\n",
            encoding="utf-8",
        )
        fake_git.chmod(0o755)
        target = self.temp_root / "probe-failure"
        result = run_cli(target, "--git", environment={"PATH": str(fake_bin)})
        self.assertFailure(result)
        self.assertFalse(os.path.lexists(target))
        self.assertIn("cannot determine Git ownership", result.stdout)

    def test_git_rejects_existing_bare_repository_without_writes(self) -> None:
        target = self.temp_root / "bare.git"
        initialized = git("init", "--bare", str(target))
        self.assertEqual(initialized.returncode, 0, initialized.stderr)
        before = filesystem_snapshot(target)
        result = run_cli(target, "--git")
        self.assertFailure(result)
        self.assertEqual(filesystem_snapshot(target), before)
        self.assertFalse((target / ".git").exists())
        bare = git("-C", str(target), "rev-parse", "--is-bare-repository")
        self.assertEqual(bare.stdout.strip(), "true")
        self.assertIn("bare Git repository", result.stdout)

    def test_flags_are_mutually_exclusive(self) -> None:
        target = self.temp_root / "flags"
        result = run_cli(target, "--check", "--git")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(os.path.lexists(target))
        self.assertIn("not allowed with argument", result.stderr)


if __name__ == "__main__":
    unittest.main()
