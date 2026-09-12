"""Exercise user-level synchronization in disposable homes."""
import importlib.util
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('agent_updater', ROOT / 'scripts/update_agents.py')
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


class UpdateAgentsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='agent-update-')
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name) / 'home'
        self.home.mkdir()
        self.source = (Path(self.temp.name) / 'source').resolve()
        shutil.copytree(ROOT, self.source, ignore=shutil.ignore_patterns('.git', 'node_modules', '__pycache__'))

    def run_update(self, *args):
        return subprocess.run([sys.executable, '-B', str(ROOT / 'scripts/update_agents.py'),
                               '--home', str(self.home), '--source', str(self.source), *args],
                              capture_output=True, text=True)

    def install(self):
        result = self.run_update()
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_check_creates_nothing(self):
        result = self.run_update('--check')
        self.assertEqual(result.returncode, 1)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_install_links_all_hosts_and_repeat_is_noop(self):
        self.install()
        for relative, folder in updater.LINKS.items():
            self.assertEqual((self.home / relative).resolve(), self.source / folder)
        for relative in updater.POLICIES:
            self.assertIn('Name the domain', (self.home / relative).read_text())
        archives = list((self.home / '.skills-archive/updates').iterdir())
        times = {p: p.stat().st_mtime_ns for p in self.home.rglob('*') if p.is_file() and not p.is_symlink()}
        self.install()
        self.assertEqual(list((self.home / '.skills-archive/updates').iterdir()), archives)
        self.assertEqual({p: p.stat().st_mtime_ns for p in times}, times)
        self.assertEqual(self.run_update('--check').returncode, 0)

    def test_new_policy_preserves_host_preferences_and_modes(self):
        self.install()
        path = self.home / '.claude/CLAUDE.md'
        path.write_text(path.read_text() + '\nShow full diff before committing.\n')
        path.chmod(0o640)
        policy = self.source / 'policy/AGENTS.md'
        policy.write_text(policy.read_text() + '\nUse the project vocabulary.\n')
        self.install()
        self.assertIn('Use the project vocabulary.', path.read_text())
        self.assertTrue(path.read_text().endswith('\nShow full diff before committing.\n'))
        self.assertEqual(path.stat().st_mode & 0o777, 0o640)

    def test_local_managed_edits_are_not_overwritten(self):
        self.install()
        path = self.home / '.codex/AGENTS.md'
        path.write_text(path.read_text().replace('Name the domain', 'My locally changed rule'))
        before = {p: (self.home / p).read_bytes() for p in updater.POLICIES}
        result = self.run_update()
        self.assertEqual(result.returncode, 2)
        self.assertIn('local edits', result.stderr)
        self.assertEqual({p: (self.home / p).read_bytes() for p in updater.POLICIES}, before)

    def test_legacy_current_policy_adopts_without_receipt(self):
        policy = (self.source / 'policy/AGENTS.md').read_text().rstrip() + '\n'
        for relative in updater.POLICIES:
            path = self.home / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(policy + updater.MARKER + '\nThe canonical skill collection is old.\n\nKeep this preference.\n')
        self.install()
        for relative in updater.POLICIES:
            self.assertTrue((self.home / relative).read_text().endswith('\nKeep this preference.\n'))

    def test_existing_directory_blocks_before_policy_changes(self):
        path = self.home / '.claude/skills'
        path.mkdir(parents=True)
        (path / 'owned.txt').write_text('preserve')
        result = self.run_update()
        self.assertEqual(result.returncode, 2)
        self.assertEqual((path / 'owned.txt').read_text(), 'preserve')
        self.assertFalse((self.home / '.codex/AGENTS.md').exists())

    def test_symlinked_instruction_or_parent_is_refused(self):
        elsewhere = Path(self.temp.name) / 'external'
        elsewhere.mkdir()
        (self.home / '.claude').symlink_to(elsewhere)
        self.assertEqual(self.run_update().returncode, 2)
        self.assertEqual(list(elsewhere.iterdir()), [])

    def test_invalid_source_does_not_touch_home(self):
        (self.source / 'policy/AGENTS.md').unlink()
        self.assertEqual(self.run_update().returncode, 2)
        self.assertEqual(list(self.home.iterdir()), [])

    def test_failed_write_rolls_back_previous_changes(self):
        self.install()
        before = {p: (self.home / p).read_bytes() for p in updater.POLICIES}
        policy = self.source / 'policy/AGENTS.md'
        policy.write_text(policy.read_text() + '\nUse the project vocabulary.\n')
        original = updater.replace_file
        calls = 0
        def fail_once(path, content, mode):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError('simulated write failure')
            return original(path, content, mode)
        with patch.object(updater, 'replace_file', fail_once):
            with self.assertRaises(OSError):
                updater.apply(self.home, self.source)
        self.assertEqual({p: (self.home / p).read_bytes() for p in updater.POLICIES}, before)


if __name__ == '__main__':
    unittest.main()
