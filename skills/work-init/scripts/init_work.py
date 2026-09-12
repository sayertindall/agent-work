#!/usr/bin/env python3
"""Initialize or inspect a durable work-tracking repository."""

from __future__ import annotations

import argparse
from dataclasses import dataclass, field
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
from typing import Iterable, List, Optional, Sequence

DIRS = (
    "plans", "plans/drafts", "plans/ready", "plans/active", "plans/done",
    "plans/discarded", "projects", "evidence",
)
KEEP_DIRS = DIRS[1:]
README = """# Work tracking

Plans move through [drafts](plans/drafts/), [ready](plans/ready/),
[active](plans/active/), [done](plans/done/), and [discarded](plans/discarded/).
Use the work-plan format for each Markdown plan.

Project context lives in [projects](projects/); retained artifacts live in
[evidence](evidence/).

This repository follows a single-writer rule: one coordinator writes shared
plans while workers return isolated artifacts. Authorization to execute work is
recorded separately from plan readiness.

To begin, create a plan in [plans/drafts](plans/drafts/).
"""


class InitError(Exception):
    pass


@dataclass
class Scan:
    root: Path
    root_exists: bool = False
    missing: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    dirs: List[Path] = field(default_factory=list)
    files: List[Path] = field(default_factory=list)

    def name(self, path: Path) -> str:
        return "." if path == self.root else path.relative_to(self.root).as_posix()

    def miss(self, path: Path) -> None:
        name = self.name(path)
        if name not in self.missing:
            self.missing.append(name)

    def conflict(self, path: Path, reason: str) -> None:
        message = f"{self.name(path)}: {reason}"
        if message not in self.conflicts:
            self.conflicts.append(message)


def status(path: Path):
    try:
        return path.lstat()
    except (FileNotFoundError, NotADirectoryError):
        return None
    except OSError as exc:
        raise InitError(f"cannot inspect {path}: {exc}") from exc


def scan(root: Path, check_only: bool) -> Scan:
    result = Scan(root)
    root_stat = status(root)
    if root_stat is None:
        result.miss(root)
        if check_only:
            for name in DIRS:
                result.miss(root / name)
            result.miss(root / "README.md")
            for name in KEEP_DIRS:
                result.miss(root / name / ".gitkeep")
            return result
        result.dirs = [root] + [root / name for name in DIRS]
        result.files = [root / "README.md"] + [root / name / ".gitkeep" for name in KEEP_DIRS]
        return result
    if stat.S_ISLNK(root_stat.st_mode):
        result.conflict(root, "target is a symlink")
        return result
    if not stat.S_ISDIR(root_stat.st_mode):
        result.conflict(root, "target is not a directory")
        return result
    result.root_exists = True

    invalid = set()
    for name in DIRS:
        path = root / name
        parent = name.rsplit("/", 1)[0] if "/" in name else ""
        if parent and parent in invalid:
            continue
        path_stat = status(path)
        if path_stat is None:
            result.miss(path)
            result.dirs.append(path)
            if name in KEEP_DIRS:
                keeper = path / ".gitkeep"
                result.miss(keeper)
                result.files.append(keeper)
            continue
        if stat.S_ISLNK(path_stat.st_mode):
            result.conflict(path, "symlink is not allowed")
            invalid.add(name)
            continue
        if not stat.S_ISDIR(path_stat.st_mode):
            result.conflict(path, "expected a directory")
            invalid.add(name)
            continue
        if name not in KEEP_DIRS:
            continue
        keeper = path / ".gitkeep"
        keeper_stat = status(keeper)
        if keeper_stat is not None:
            if stat.S_ISLNK(keeper_stat.st_mode):
                result.conflict(keeper, "symlink is not allowed")
            elif not stat.S_ISREG(keeper_stat.st_mode):
                result.conflict(keeper, "expected a regular file")
        else:
            try:
                with os.scandir(path) as entries:
                    is_empty = next(entries, None) is None
            except OSError as exc:
                raise InitError(f"cannot inspect directory {path}: {exc}") from exc
            if is_empty:
                result.miss(keeper)
                result.files.append(keeper)

    readme = root / "README.md"
    readme_stat = status(readme)
    if readme_stat is None:
        result.miss(readme)
        result.files.append(readme)
    elif stat.S_ISLNK(readme_stat.st_mode):
        result.conflict(readme, "symlink is not allowed")
    elif not stat.S_ISREG(readme_stat.st_mode):
        result.conflict(readme, "expected a regular file")
    return result


def git_run(executable: str, arguments: Sequence[str]) -> subprocess.CompletedProcess:
    try:
        environment = os.environ.copy()
        environment["LC_ALL"] = "C"
        environment["LANG"] = "C"
        return subprocess.run(
            [executable] + list(arguments), check=False, capture_output=True, text=True,
            env=environment,
        )
    except OSError as exc:
        raise InitError(f"cannot execute Git: {exc}") from exc


def git_available() -> str:
    for variable in ("GIT_DIR", "GIT_WORK_TREE", "GIT_COMMON_DIR", "GIT_INDEX_FILE"):
        if variable in os.environ:
            raise InitError(f"{variable} is set; unset it before using --git")
    executable = shutil.which("git")
    if executable is None:
        raise InitError("Git is unavailable; --git cannot initialize the target")
    result = git_run(executable, ("--version",))
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown error"
        raise InitError(f"Git preflight failed: {detail}")
    return executable


def git_owner(executable: str, root: Path) -> Optional[Path]:
    probe = root
    while True:
        probe_stat = status(probe)
        if probe_stat is not None:
            break
        if probe == probe.parent:
            return None
        probe = probe.parent
    if not stat.S_ISDIR(probe_stat.st_mode):
        return None
    result = git_run(executable, ("-C", str(probe), "rev-parse", "--show-toplevel"))
    if result.returncode == 0 and result.stdout.strip():
        try:
            return Path(result.stdout.strip()).expanduser().resolve(strict=False)
        except (OSError, RuntimeError):
            return Path(result.stdout.strip())
    current = probe
    while True:
        if status(current / ".git") is not None:
            detail = result.stderr.strip() or "Git ownership probe failed"
            raise InitError(f"cannot safely inspect Git repository at {current}: {detail}")
        if current == current.parent:
            break
        current = current.parent
    bare = git_run(executable, ("-C", str(probe), "rev-parse", "--is-bare-repository"))
    if bare.returncode == 0 and bare.stdout.strip() == "true":
        raise InitError(f"target is a bare Git repository at {probe}; cannot scaffold it")
    if "not a git repository" in result.stderr.lower():
        return None
    detail = result.stderr.strip() or result.stdout.strip() or "Git ownership probe failed"
    raise InitError(f"cannot determine Git ownership at {probe}: {detail}")


def initialize_git(executable: str, root: Path) -> None:
    result = git_run(executable, ("init", "-b", "main", str(root)))
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or "unknown error"
        raise InitError(f"Git initialization failed: {detail}")


def apply(result: Scan) -> List[str]:
    created = []
    if not result.root_exists:
        try:
            result.root.mkdir(parents=True, exist_ok=False)
        except OSError as exc:
            raise InitError(f"cannot create target {result.root}: {exc}") from exc
        result.root_exists = True
        created.append(".")
    for path in result.dirs:
        if path == result.root:
            continue
        try:
            path.mkdir(exist_ok=False)
        except OSError as exc:
            raise InitError(f"cannot create directory {path}: {exc}") from exc
        created.append(result.name(path))
    for path in result.files:
        try:
            with path.open("x", encoding="utf-8", newline="") as handle:
                if path.name == "README.md":
                    handle.write(README)
        except OSError as exc:
            raise InitError(f"cannot create file {path}: {exc}") from exc
        created.append(result.name(path))
    return created


def report(root: Path, mode: str, success: bool, result: Optional[Scan] = None,
           created: Iterable[str] = (), git_message: Optional[str] = None,
           error: Optional[str] = None) -> None:
    print(f"Work root: {root}\nMode: {mode}")
    if result is not None:
        for title, values in (("Missing", result.missing), ("Conflicts", result.conflicts)):
            if values:
                print(f"{title}:")
                for value in values:
                    print(f"  {value}")
        if not result.missing and not result.conflicts:
            print("Structure: complete")
    created = list(created)
    if created:
        print("Created:")
        for value in created:
            print(f"  {value}")
    elif mode == "initialize" and success:
        print("Created: none")
    if git_message:
        print(f"Git: {git_message}")
    if error:
        print(f"Error: {error}")
    print(f"Result: {'success' if success else 'failure'}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Initialize or inspect work tracking.")
    parser.add_argument("path", help="work repository root")
    flags = parser.add_mutually_exclusive_group()
    flags.add_argument("--check", action="store_true", help="read-only structure check")
    flags.add_argument("--git", action="store_true", help="initialize Git on main if needed")
    args = parser.parse_args(argv)
    try:
        root = Path(args.path).expanduser().resolve(strict=False)
    except (OSError, RuntimeError) as exc:
        print(f"Error: cannot resolve target path: {exc}", file=sys.stderr)
        return 1
    if args.check:
        try:
            result = scan(root, True)
        except InitError as exc:
            report(root, "check", False, error=str(exc))
            return 1
        success = result.root_exists and not result.missing and not result.conflicts
        report(root, "check", success, result=result)
        return 0 if success else 1

    executable = None
    if args.git:
        try:
            executable = git_available()
        except InitError as exc:
            report(root, "initialize", False, error=str(exc))
            return 1
    result = None
    try:
        result = scan(root, False)
        if result.conflicts:
            report(root, "initialize", False, result=result)
            return 1
        git_message = None
        if args.git:
            assert executable is not None
            owner = git_owner(executable, root)
            if owner is None:
                if not result.root_exists:
                    try:
                        root.mkdir(parents=True, exist_ok=False)
                    except OSError as exc:
                        raise InitError(f"cannot create target {root}: {exc}") from exc
                    result.root_exists = True
                    result.dirs = [path for path in result.dirs if path != root]
                initialize_git(executable, root)
                git_message = "initialized repository on main"
            else:
                git_message = f"reusing repository at {owner}"
        created = apply(result)
    except InitError as exc:
        report(root, "initialize", False, result=result, error=str(exc))
        return 1
    report(root, "initialize", True, result=result, created=created, git_message=git_message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
