#!/usr/bin/env python3
"""Synchronize the local Claude, Codex and OMP installation from a chosen checkout."""
import argparse
from datetime import datetime, timezone
import fcntl
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

MARKER = '\n## Installed collection\n'
RECEIPT = '.agents/agent-work-install.json'
POLICIES = ('.claude/CLAUDE.md', '.codex/AGENTS.md', '.omp/agent/AGENTS.md')
LINKS = {f'{host}/{folder}': folder for host in ('.agents', '.claude')
         for folder in ('skills', 'policy', 'adapters')}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def safe_path(home, relative):
    path = home / relative
    for parent in path.parents:
        if parent == home:
            break
        if parent.is_symlink():
            raise ValueError('symlinked parent requires explicit reconciliation: ' + str(parent))
        if parent.exists() and not parent.is_dir():
            raise ValueError('installation parent is not a directory: ' + str(parent))
    return path


def read_receipt(home):
    path = safe_path(home, RECEIPT)
    if path.is_symlink():
        raise ValueError('receipt must not be a symlink')
    if not path.exists():
        return {}
    value = json.loads(path.read_text())
    if not isinstance(value, dict) or value.get('version') != 1 or not isinstance(value.get('policies'), dict):
        raise ValueError('invalid installation receipt')
    return value['policies']


def prepare(home, source):
    policy = (source / 'policy/AGENTS.md').read_text().rstrip() + '\n'
    managed_hash = digest(policy.encode())
    recorded = read_receipt(home)
    changes = []
    receipt = {'version': 1, 'source': str(source), 'policies': {}}
    for relative in POLICIES:
        path = safe_path(home, relative)
        if path.is_symlink() or (path.exists() and not path.is_file()):
            raise ValueError('instruction destination is not a regular file: ' + str(path))
        if path.exists():
            current = path.read_text()
            if current.count(MARKER) != 1:
                raise ValueError('unrecognized instruction layout; reconcile before updating: ' + str(path))
            prefix, suffix = current.split(MARKER, 1)
            prefix_hash = digest((prefix.rstrip() + '\n').encode())
            if prefix_hash not in {managed_hash, recorded.get(relative)}:
                raise ValueError('local edits in managed policy; refusing to overwrite: ' + str(path))
            lines = suffix.splitlines(keepends=True)
            if not lines or not lines[0].startswith('The canonical skill collection is '):
                raise ValueError('unrecognized source pointer; reconcile before updating: ' + str(path))
            # Only the managed pointer line changes; host preferences follow verbatim.
            tail = ''.join(lines[1:])
        else:
            tail = ''
        pointer = (f'The canonical skill collection is `{source}/skills`. Resolve skill symlinks before '
                   f'following relative references. Load `{source}/skills/steady/SKILL.md` '
                   'automatically for substantive work.\n')
        desired = (policy + MARKER + pointer + tail).encode()
        if not path.exists() or path.read_bytes() != desired:
            changes.append((relative, 'file', desired))
        receipt['policies'][relative] = managed_hash
    for relative, folder in LINKS.items():
        path = safe_path(home, relative)
        target = str(source / folder)
        if path.is_symlink():
            if os.readlink(path) != target:
                changes.append((relative, 'link', target))
        elif path.exists():
            raise ValueError('refusing to replace an existing discovery directory: ' + str(path))
        else:
            changes.append((relative, 'link', target))
    desired = (json.dumps(receipt, indent=2, sort_keys=True) + '\n').encode()
    receipt_path = safe_path(home, RECEIPT)
    if not receipt_path.exists() or receipt_path.read_bytes() != desired:
        changes.append((RECEIPT, 'file', desired))
    return changes


def replace_file(path, content, mode):
    descriptor, temporary = tempfile.mkstemp(prefix='.agent-work-', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(content)
        os.chmod(temporary, mode)
        os.replace(temporary, path)
    finally:
        if os.path.lexists(temporary):
            os.unlink(temporary)


def replace_link(path, target):
    descriptor, temporary = tempfile.mkstemp(prefix='.agent-work-', dir=path.parent)
    os.close(descriptor)
    os.unlink(temporary)
    try:
        os.symlink(target, temporary)
        os.replace(temporary, path)
    finally:
        if os.path.lexists(temporary):
            os.unlink(temporary)


def apply(home, source):
    changes = prepare(home, source)
    if not changes:
        print('Already current; no files changed.')
        return
    archive = safe_path(home, '.skills-archive/updates')
    if archive.is_symlink():
        raise ValueError('update archive must not be a symlink')
    archive.mkdir(parents=True, exist_ok=True, mode=0o700)
    backup = Path(tempfile.mkdtemp(prefix=datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%SZ-'), dir=archive))
    originals = []
    for relative, _, _ in changes:
        path = safe_path(home, relative)
        saved = backup / relative
        if path.is_symlink():
            originals.append((relative, 'link', os.readlink(path), None))
        elif path.exists():
            saved.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(path, saved)
            originals.append((relative, 'file', str(saved), path.stat().st_mode & 0o777))
        else:
            originals.append((relative, 'absent', None, None))
    (backup / 'manifest.json').write_text(json.dumps({'source': str(source), 'originals': originals}, indent=2) + '\n')
    attempted = []
    try:
        for relative, kind, value in changes:
            path = safe_path(home, relative)
            path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            attempted.append(relative)
            if kind == 'link':
                replace_link(path, value)
            else:
                mode = path.stat().st_mode & 0o777 if path.exists() else 0o600
                replace_file(path, value, mode)
        if prepare(home, source):
            raise ValueError('installation verification failed')
    except Exception:
        for relative, kind, value, mode in reversed(originals):
            if relative not in attempted:
                continue
            path = home / relative
            if kind == 'file':
                replace_file(path, Path(value).read_bytes(), mode)
            elif kind == 'link':
                replace_link(path, value)
            elif os.path.lexists(path):
                path.unlink()
        raise
    print('Updated Claude, Codex and OMP from ' + str(source))
    print('Backup: ' + str(backup))
    print('Start fresh agent sessions to load updated instructions.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--home', type=Path, default=Path.home(), help='Installation home; use a disposable home for tests')
    parser.add_argument('--check', action='store_true', help='Inspect only; exit 1 if synchronization is needed')
    args = parser.parse_args()
    try:
        source = args.source.resolve(strict=True)
        home = args.home.resolve(strict=True)
        result = subprocess.run([sys.executable, '-B', str(source / 'scripts/validate.py'), '--root', str(source)],
                                capture_output=True, text=True)
        if result.returncode:
            raise ValueError('source validation failed: ' + result.stdout + result.stderr)
        if args.check:
            changes = prepare(home, source)
            for relative, kind, _ in changes:
                print('Needs update: ' + relative + ' (' + kind + ')')
            print('Synchronization needed.' if changes else 'All three agents are current.')
            return 1 if changes else 0
        lock = safe_path(home, '.agents/agent-work-update.lock')
        if lock.is_symlink():
            raise ValueError('update lock must not be a symlink')
        lock.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
        with lock.open('a') as stream:
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
            apply(home, source)
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print('Update refused: ' + str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
