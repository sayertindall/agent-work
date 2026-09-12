"""Black-box tests for the naming checker using disposable Git repositories."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from typing import Any, Mapping, Optional


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "scripts/check_names.py"
DEFAULT_POLICY = {
    "version": 1,
    "task_prefixes": ["R", "K", "S"],
    "allowed_terms": [],
    "baseline": [],
    "immutable": [],
}


class CheckNamesTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_directory = tempfile.TemporaryDirectory(prefix="check-names-tests-")
        self.addCleanup(self.temp_directory.cleanup)
        self.repo = Path(self.temp_directory.name) / "repo"
        self.repo.mkdir()
        self.git("init", "-q", "-b", "main")
        self.git("config", "user.email", "checker-tests@example.invalid")
        self.git("config", "user.name", "Checker Tests")

    def git(
        self,
        *arguments: str,
        input_text: Optional[str] = None,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        result = subprocess.run(
            ["git", "-C", str(self.repo), *arguments],
            check=False,
            capture_output=True,
            text=True,
            input=input_text,
        )
        if check and result.returncode:
            self.fail(
                f"git {' '.join(arguments)} failed with {result.returncode}:\n"
                f"stdout={result.stdout}\nstderr={result.stderr}"
            )
        return result

    def write(self, relative_path: str, content: Any) -> Path:
        path = self.repo / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(content, bytes):
            path.write_bytes(content)
        else:
            path.write_text(str(content), encoding="utf-8")
        return path

    def write_policy(self, policy: Mapping[str, Any]) -> None:
        self.write("naming-policy.json", json.dumps(policy, indent=2) + "\n")

    def commit(self, message: str) -> str:
        self.git("add", "--all")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD").stdout.strip()

    def seed_base(
        self,
        files: Optional[Mapping[str, Any]] = None,
        policy: Optional[Mapping[str, Any]] = None,
    ) -> str:
        for path, content in (files or {}).items():
            self.write(path, content)
        self.write_policy(policy or DEFAULT_POLICY)
        return self.commit("seed naming checker fixture")

    def stage(self) -> None:
        self.git("add", "--all")

    def run_checker(
        self,
        *arguments: str,
        repo: Optional[Path] = None,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                "-B",
                str(SOURCE),
                "--repo",
                str(repo or self.repo),
                *arguments,
            ],
            check=False,
            capture_output=True,
            text=True,
        )

    @staticmethod
    def records(result: subprocess.CompletedProcess[str], stream: str = "stdout") -> list[dict[str, Any]]:
        output = getattr(result, stream)
        return [json.loads(line) for line in output.splitlines() if line.strip()]

    def violations(self, result: subprocess.CompletedProcess[str]) -> list[dict[str, Any]]:
        return [record["violation"] for record in self.records(result) if "violation" in record]

    def assert_status(self, result: subprocess.CompletedProcess[str], status: str) -> None:
        records = self.records(result)
        self.assertTrue(records, msg=f"no JSON stdout records:\n{result.stdout}")
        self.assertEqual(records[-1].get("status"), status, msg=result.stdout)

    def assert_error(self, result: subprocess.CompletedProcess[str], fragment: str) -> None:
        self.assertEqual(
            result.returncode,
            2,
            msg=f"stdout:\n{result.stdout}\nstderr:\n{result.stderr}",
        )
        records = self.records(result, "stderr")
        self.assertEqual(len(records), 1, msg=result.stderr)
        self.assertIn(fragment, records[0].get("error", ""), msg=result.stderr)

    def test_default_index_reports_staged_bad_file_when_worktree_is_clean(self) -> None:
        self.seed_base({"service.py": "def serve():\n    return 'ok'\n"})
        path = self.write("service.py", "def task7Serve():\n    return 'ok'\n")
        self.stage()
        path.write_text("def serve():\n    return 'ok'\n", encoding="utf-8")

        result = self.run_checker()

        self.assertEqual(path.read_text(encoding="utf-8"), "def serve():\n    return 'ok'\n")
        self.assertEqual(result.returncode, 1, msg=result.stderr)
        self.assert_status(result, "violations")
        self.assertEqual({item["name"] for item in self.violations(result)}, {"task7Serve"})

    def test_default_index_ignores_bad_worktree_when_staged_file_is_clean(self) -> None:
        self.seed_base({"service.py": "def serve():\n    return 'ok'\n"})
        path = self.write("service.py", "def serve():\n    return 'ok'\n")
        self.stage()
        path.write_text("def task8Serve():\n    return 'ok'\n", encoding="utf-8")

        result = self.run_checker()

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assert_status(result, "clean-within-coverage")
        self.assertEqual(self.violations(result), [])

    def test_clean_snapshot_has_zero_exit_and_complete_status(self) -> None:
        self.seed_base(
            {
                "src/service.py": "def serve(request):\n    return request\n",
                "docs/release-v1.2.3.md": "Task 7 is historical prose.\n",
            }
        )

        result = self.run_checker()

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assert_status(result, "clean-within-coverage")
        self.assertEqual(self.records(result)[-1]["violations"], 0)

    def test_tree_requires_an_explicit_base_revision(self) -> None:
        target = self.seed_base({"README.md": "fixture\n"})

        result = self.run_checker("--tree", target)

        self.assert_error(result, "--tree requires --base")

    def test_tree_revision_is_checked_against_the_named_base(self) -> None:
        base = self.seed_base({"README.md": "fixture\n"})
        self.write("new.py", "def task9Refresh():\n    return 1\n")
        target = self.commit("add target evidence")
        self.write("new.py", "def task10WorkingTreeOnly():\n    return 1\n")

        result = self.run_checker("--tree", target, "--base", base)

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        self.assert_status(result, "violations")
        self.assertEqual({item["name"] for item in self.violations(result)}, {"task9Refresh"})

    def test_python_owned_names_and_json_keys_and_resources_are_checked(self) -> None:
        self.seed_base()
        self.write(
            "src/records.py",
            """class R55Manifest:
    def __init__(self, task6_config):
        self.task7_state = task6_config

def K88FetchManifest(task9_input):
    task_10_state = task9_input
    return {"task-13-route": "route", "name": "S33Bucket"}

def computed_resource():
    descriptor = {}
    descriptor["name"] = "S66Computed"
    return descriptor
""",
        )
        self.write(
            "fixtures/routes.json",
            '{"task-11-route": "description", "name": "R12Resource"}\n',
        )
        self.stage()

        result = self.run_checker()

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        names = {item["name"] for item in self.violations(result)}
        self.assertTrue(
            {
                "R55Manifest",
                "task6_config",
                "task7_state",
                "K88FetchManifest",
                "task9_input",
                "task_10_state",
                "task-13-route",
                "S33Bucket",
                "S66Computed",
                "task-11-route",
                "R12Resource",
            }.issubset(names),
            msg=result.stdout,
        )

    def test_typescript_owned_names_and_resource_fields_are_checked(self) -> None:
        self.seed_base()
        self.write(
            "src/records.ts",
            """export function K88FetchManifest(task77Input: string) {
  const task_99_state = task77Input;
  const descriptor = {
    name: "S44Bucket",
    task_11_route: "route",
    "task-12-route": "route",
    prose: "task 13 docs",
  };
  descriptor["task_14_route"] = "route";
  descriptor["name"] = "S55Computed";
  const external = client.task17External;
  return { descriptor, external };
}
""",
        )
        self.stage()

        result = self.run_checker()

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        names = {item["name"] for item in self.violations(result)}
        self.assertTrue(
            {
                "K88FetchManifest",
                "task77Input",
                "task_99_state",
                "S44Bucket",
                "task_11_route",
                "task-12-route",
                "task_14_route",
                "S55Computed",
            }.issubset(names),
            msg=result.stdout,
        )
        self.assertNotIn("task17External", names, msg=result.stdout)

    def test_malformed_typescript_is_reported_as_json_error(self) -> None:
        self.seed_base()
        self.write("broken.ts", "export function K88Broken(\n")
        self.stage()

        result = self.run_checker()

        self.assert_error(result, "cannot parse 'broken.ts'")

    def test_python_fixture_literals_are_scanned_only_as_keys_or_resources(self) -> None:
        self.seed_base()
        self.write(
            "fixtures/data.py",
            """fixture_values = ["R42", "task 7", "phase eight", "S2"]
metadata = {
    "description": "K8",
    "notes": "task-9-route",
}
""",
        )
        self.stage()

        result = self.run_checker()

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assert_status(result, "clean-within-coverage")

    def test_hashes_versions_and_prose_are_legitimate_values(self) -> None:
        self.seed_base(
            {
                "fixtures/values.py": (
                    'examples = {"sha256": "R42", "version": "K7", '
                    '"description": "Task 4 and S3 are prose"}\n'
                ),
                "fixtures/values.json": (
                    '{"sha256": "R42", "version": "S3", '
                    '"description": "phase seven is prose"}\n'
                ),
                "checksums/sha256.txt": "R42 and task 8 are documented checksums.\n",
            }
        )

        result = self.run_checker()

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assert_status(result, "clean-within-coverage")

    def test_seeded_allowed_term_is_honored_for_a_resource_value(self) -> None:
        policy = dict(DEFAULT_POLICY)
        policy["allowed_terms"] = ["R42"]
        self.seed_base(policy=policy)
        self.write("fixture.py", 'descriptor = {"name": "R42"}\n')
        self.stage()

        result = self.run_checker()

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assert_status(result, "clean-within-coverage")

    def test_duplicate_json_keys_remain_independent_evidence(self) -> None:
        self.seed_base()
        self.write("fixtures/duplicate.json", '{"name": "R42", "name": "K03Bucket"}\n')
        self.stage()

        result = self.run_checker()

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        self.assertEqual(
            {item["name"] for item in self.violations(result)}, {"R42", "K03Bucket"}
        )

    def test_paths_with_spaces_and_newlines_and_staged_renames_are_checked(self) -> None:
        old_name = "docs/meeting notes\n2026.md"
        new_name = "docs/task 7\nnotes.md"
        self.seed_base({old_name: "meeting notes\n"})
        self.assertEqual(self.run_checker().returncode, 0)
        self.git("mv", old_name, new_name)

        result = self.run_checker()

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        path_findings = [item for item in self.violations(result) if item["kind"] == "path"]
        self.assertEqual(len(path_findings), 1, msg=result.stdout)
        self.assertEqual(path_findings[0]["path"], new_name)
        self.assertEqual(path_findings[0]["name"], new_name)

    def test_exact_debt_metadata_is_not_a_resource_but_other_names_are(self) -> None:
        self.seed_base()
        self.write("metadata.py", """record = {"path": "legacy.py", "kind": "symbol", "name": "task7Legacy", "count": 1}
resource = {"name": "task7Bucket"}
""")
        self.stage()
        result = self.run_checker()
        self.assertEqual(result.returncode, 1, msg=result.stderr)
        self.assertEqual({item["name"] for item in self.violations(result)}, {"task7Bucket"})

    def historical_policy(self) -> dict[str, Any]:
        policy = dict(DEFAULT_POLICY)
        policy["baseline"] = [
            {"path": "legacy.py", "kind": "symbol", "name": "task7Legacy", "count": 1},
        ]
        return policy

    def test_existing_baseline_debt_is_seeded_in_base_and_consumed(self) -> None:
        self.seed_base(
            {"legacy.py": "def task7Legacy():\n    return 1\n"},
            self.historical_policy(),
        )

        result = self.run_checker()

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assert_status(result, "clean-within-coverage")

    def test_historical_debt_does_not_cover_a_new_file_in_target_evidence(self) -> None:
        self.seed_base(
            {"legacy.py": "def task7Legacy():\n    return 1\n"},
            self.historical_policy(),
        )
        self.write("fresh.py", "def task8Fresh():\n    return 1\n")
        self.stage()

        result = self.run_checker()

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        findings = self.violations(result)
        self.assertEqual({(item["path"], item["name"]) for item in findings}, {("fresh.py", "task8Fresh")})

    def test_baseline_debt_does_not_cover_a_new_name_on_the_same_path(self) -> None:
        self.seed_base(
            {"legacy.py": "def task7Legacy():\n    return 1\n"},
            self.historical_policy(),
        )
        self.write(
            "legacy.py",
            "def task7Legacy():\n    return 1\n\ndef task8Fresh():\n    return 2\n",
        )
        self.stage()

        result = self.run_checker()

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        self.assertEqual({item["name"] for item in self.violations(result)}, {"task8Fresh"})

    def test_baseline_count_cannot_cover_an_increased_occurrence_count(self) -> None:
        self.seed_base(
            {"legacy.py": "def task7Legacy():\n    return 1\n"},
            self.historical_policy(),
        )
        self.write(
            "legacy.py",
            "def task7Legacy():\n    return 1\n\ndef task7Legacy():\n    return 2\n",
        )
        self.stage()

        result = self.run_checker()

        self.assertEqual(result.returncode, 1, msg=result.stderr)
        findings = self.violations(result)
        self.assertEqual(len(findings), 1, msg=result.stdout)
        self.assertEqual(findings[0]["name"], "task7Legacy")

    def test_resolved_baseline_debt_is_a_complete_error(self) -> None:
        self.seed_base(
            {"legacy.py": "def task7Legacy():\n    return 1\n"},
            self.historical_policy(),
        )
        self.write("legacy.py", "def useful_name():\n    return 1\n")
        self.stage()

        result = self.run_checker()

        self.assert_error(result, "stale naming baseline entries")

    def test_policy_baseline_expansion_is_rejected(self) -> None:
        self.seed_base()
        policy = dict(DEFAULT_POLICY)
        policy["baseline"] = [
            {"path": "legacy.py", "kind": "symbol", "name": "task7Legacy", "count": 1}
        ]
        self.write_policy(policy)
        self.stage()

        result = self.run_checker()

        self.assert_error(result, "naming baseline expanded")

    def test_policy_prefix_change_is_rejected(self) -> None:
        self.seed_base()
        policy = dict(DEFAULT_POLICY)
        policy["task_prefixes"] = ["R", "K", "S", "T"]
        self.write_policy(policy)
        self.stage()

        result = self.run_checker()

        self.assert_error(result, "protected naming policy changed: task_prefixes")

    def test_policy_allowed_terms_change_is_rejected(self) -> None:
        self.seed_base()
        policy = dict(DEFAULT_POLICY)
        policy["allowed_terms"] = ["R42"]
        self.write_policy(policy)
        self.stage()

        result = self.run_checker()

        self.assert_error(result, "protected naming policy changed: allowed_terms")

    def test_immutable_pin_change_is_rejected(self) -> None:
        artifact = b"immutable release manifest\n"
        policy = dict(DEFAULT_POLICY)
        policy["immutable"] = [
            {"path": "release/manifest.txt", "sha256": hashlib.sha256(artifact).hexdigest()}
        ]
        self.seed_base({"release/manifest.txt": artifact}, policy)
        changed = dict(policy)
        changed["immutable"] = [
            {"path": "release/manifest.txt", "sha256": "0" * 64}
        ]
        self.write_policy(changed)
        self.stage()

        result = self.run_checker()

        self.assert_error(result, "immutable exemptions")

    def test_immutable_artifact_change_is_rejected(self) -> None:
        artifact = b"immutable release manifest\n"
        policy = dict(DEFAULT_POLICY)
        policy["immutable"] = [
            {"path": "release/manifest.txt", "sha256": hashlib.sha256(artifact).hexdigest()}
        ]
        self.seed_base({"release/manifest.txt": artifact}, policy)
        self.write("release/manifest.txt", b"modified release manifest\n")
        self.stage()

        result = self.run_checker()

        self.assert_error(result, "immutable artifact changed")

    def test_missing_immutable_artifact_is_rejected(self) -> None:
        artifact = b"immutable release manifest\n"
        policy = dict(DEFAULT_POLICY)
        policy["immutable"] = [
            {"path": "release/manifest.txt", "sha256": hashlib.sha256(artifact).hexdigest()}
        ]
        self.seed_base({"release/manifest.txt": artifact}, policy)
        self.git("rm", "-q", "release/manifest.txt")

        result = self.run_checker()

        self.assert_error(result, "immutable artifact missing")

    def test_malformed_python_is_reported_as_json_error(self) -> None:
        self.seed_base()
        self.write("broken.py", "def task7Broken(\n")
        self.stage()

        result = self.run_checker()

        self.assert_error(result, "cannot parse 'broken.py'")

    def test_malformed_json_is_reported_as_json_error(self) -> None:
        self.seed_base()
        self.write("broken.json", '{"name":\n')
        self.stage()

        result = self.run_checker()

        self.assert_error(result, "cannot parse 'broken.json'")

    def test_malformed_policy_is_reported_as_json_error(self) -> None:
        self.seed_base()
        self.write("naming-policy.json", '{"version": 1, "task_prefixes": []}\n')
        self.stage()

        result = self.run_checker()

        self.assert_error(result, "invalid naming policy schema")

    def test_unsupported_content_is_clean_by_default_with_coverage_record(self) -> None:
        self.seed_base({"notes.yaml": "task 7 is prose in an unsupported format\n"})

        result = self.run_checker()

        self.assertEqual(result.returncode, 0, msg=result.stderr)
        self.assert_status(result, "clean-within-coverage")
        coverage = [record["coverage"] for record in self.records(result) if "coverage" in record]
        self.assertEqual(len(coverage), 1)
        self.assertEqual(coverage[0]["path"], "notes.yaml")

    def test_require_complete_turns_unsupported_coverage_into_error_status(self) -> None:
        self.seed_base({"notes.yaml": "task 7 is prose in an unsupported format\n"})

        result = self.run_checker("--require-complete")

        self.assertEqual(result.returncode, 2, msg=result.stderr)
        self.assert_status(result, "incomplete")
        coverage = [record["coverage"] for record in self.records(result) if "coverage" in record]
        self.assertEqual(coverage[0]["path"], "notes.yaml")

    def test_unmerged_index_is_a_complete_error(self) -> None:
        self.seed_base({"conflict.py": "value = 1\n"})
        self.git("checkout", "-q", "-b", "side")
        self.write("conflict.py", "value = 2\n")
        self.commit("side change")
        self.git("checkout", "-q", "main")
        self.write("conflict.py", "value = 3\n")
        self.commit("main change")
        merge = self.git("merge", "--no-commit", "--no-ff", "side", check=False)
        self.assertNotEqual(merge.returncode, 0, msg=merge.stderr)

        result = self.run_checker()

        self.assert_error(result, "unmerged index")

    def test_non_repository_is_a_complete_error(self) -> None:
        missing = Path(self.temp_directory.name) / "missing-repository"

        result = self.run_checker(repo=missing)

        self.assert_error(result, "git rev-parse")

    def test_unknown_tree_revision_is_a_complete_error(self) -> None:
        self.seed_base()

        result = self.run_checker("--tree", "missing-tree", "--base", "HEAD")

        self.assert_error(result, "git rev-parse")


if __name__ == "__main__":
    unittest.main()
