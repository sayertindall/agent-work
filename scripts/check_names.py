#!/usr/bin/env python3
"""Check names in Git index/tree blobs. Exit 0 clean, 1 violations, 2 incomplete/error."""
import argparse
import ast
from collections import Counter
import hashlib
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tokenize

POLICY = 'naming-policy.json'
DEFAULT = {'version': 1, 'task_prefixes': ['R', 'K', 'S'], 'allowed_terms': [],
           'baseline': [], 'immutable': []}
RESOURCE_FIELDS = {'name', 'prefix', 'image', 'bucket', 'resource', 'resource_name',
                   'image_name', 'bucket_name', 'container_name'}
TEXT_ONLY = {'.md', '.txt', '.csv', '.lock', '.svg', '.html', '.css'}


def git(repo, *args):
    result = subprocess.run(['git', '-C', str(repo), *args], capture_output=True)
    if result.returncode:
        raise ValueError('git ' + args[0] + ': ' + result.stderr.decode(errors='replace').strip())
    return result.stdout


def snapshot(repo, revision):
    """Use object ids rather than rev:path expressions, including for unusual paths."""
    if revision is None:
        data = git(repo, 'ls-files', '--stage', '-z')
    else:
        revision = git(repo, 'rev-parse', '--verify', revision + '^{tree}').decode().strip()
        data = git(repo, 'ls-tree', '-r', '-z', revision)
    files = {}
    for entry in data.split(b'\0'):
        if not entry:
            continue
        meta, path = entry.split(b'\t', 1)
        fields = meta.decode().split()
        if revision is None:
            mode, oid, stage = fields
            if stage != '0':
                raise ValueError('unmerged index: ' + repr(path))
        else:
            mode, _, oid = fields
        files[path.decode('utf-8', errors='surrogateescape')] = (mode, oid)
    return files


def blob(repo, files, path):
    return git(repo, 'cat-file', 'blob', files[path][1])


def read_policy(repo, files):
    def unique_object(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('duplicate naming policy key: ' + key)
            result[key] = value
        return result
    policy = json.loads(blob(repo, files, POLICY), object_pairs_hook=unique_object) if POLICY in files else dict(DEFAULT)
    if not isinstance(policy, dict) or set(policy) != set(DEFAULT) or type(policy['version']) is not int or policy['version'] != 1:
        raise ValueError('invalid naming policy schema')
    for key in ('task_prefixes', 'allowed_terms', 'baseline', 'immutable'):
        if not isinstance(policy[key], list):
            raise ValueError('policy field must be a list: ' + key)
    if not policy['task_prefixes'] or any(not isinstance(x, str) or not re.fullmatch('[A-Za-z]+', x)
                                           for x in policy['task_prefixes']):
        raise ValueError('task_prefixes must contain literal alphabetic prefixes')
    if any(not isinstance(x, str) or not x for x in policy['allowed_terms']):
        raise ValueError('allowed_terms must contain nonempty exact names')
    for item in policy['baseline']:
        if (not isinstance(item, dict) or set(item) != {'path', 'kind', 'name', 'count'}
                or any(not isinstance(item[k], str) or not item[k] for k in ('path', 'kind', 'name'))
                or type(item['count']) is not int or item['count'] < 1):
            raise ValueError('invalid exact baseline record')
    for item in policy['immutable']:
        if (not isinstance(item, dict) or set(item) != {'path', 'sha256'}
                or not isinstance(item['path'], str) or not item['path']
                or not isinstance(item['sha256'], str)
                or not re.fullmatch('[0-9a-f]{64}', item['sha256'])):
            raise ValueError('invalid immutable blob pin')
    pin_paths = [item['path'] for item in policy['immutable']]
    if len(pin_paths) != len(set(pin_paths)):
        raise ValueError('duplicate immutable path')
    for key in ('baseline', 'immutable'):
        records = [json.dumps(x, sort_keys=True) for x in policy[key]]
        if len(records) != len(set(records)):
            raise ValueError('duplicate policy records')
    return policy


def counts(policy):
    result = Counter()
    for item in policy['baseline']:
        key = (item['path'], item['kind'], item['name'])
        if key in result:
            raise ValueError('duplicate baseline identity')
        result[key] = item['count']
    return result


def validate_policy_change(old, new):
    for key in ('version', 'task_prefixes', 'allowed_terms'):
        if old[key] != new[key]:
            raise ValueError('protected naming policy changed: ' + key)
    if counts(new) - counts(old):
        raise ValueError('naming baseline expanded')
    if old['immutable'] != new['immutable']:
        raise ValueError('immutable exemptions changed; require a separately reviewed policy migration')


def forbidden(name, policy):
    if name in policy['allowed_terms']:
        return False
    # Separate camel/Pascal words before matching literal project markers.
    words = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', name)
    words = re.sub(r'([A-Z])([A-Z][a-z])', r'\1 \2', words)
    parts = re.split(r'[^A-Za-z0-9]+', words)
    prefixes = '|'.join(re.escape(x) for x in policy['task_prefixes'])
    code = re.compile(r'(?:' + prefixes + r')[0-9]{2,}', re.I)
    for i, part in enumerate(parts):
        if code.fullmatch(part):
            return True
        if re.fullmatch(r'(?:task|phase|ticket|step)[0-9]+', part, re.I):
            return True
        if part.lower() in {'task', 'phase', 'ticket', 'step'} and i + 1 < len(parts):
            if re.fullmatch(r'[0-9]+|one|two|three|four|five|six|seven|eight|nine|ten', parts[i + 1], re.I):
                return True
    return False


def is_debt_record(value):
    # An exact debt record describes an existing name; it does not create a resource.
    return (isinstance(value, dict) and set(value) == {'path', 'kind', 'name', 'count'}
            and value['kind'] in {'path', 'symbol', 'field', 'key', 'resource'}
            and isinstance(value['path'], str) and isinstance(value['name'], str)
            and type(value['count']) is int and value['count'] > 0)


def python_names(text):
    tree = ast.parse(text)
    for node in ast.walk(tree):
        line = getattr(node, 'lineno', 1)
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            yield 'symbol', node.name, line
        elif isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store):
            yield 'symbol', node.id, line
        elif isinstance(node, ast.ExceptHandler) and node.name:
            yield 'symbol', node.name, line
        elif type(node).__name__ in {'MatchAs', 'MatchStar'} and node.name:
            yield 'symbol', node.name, line
        elif type(node).__name__ == 'MatchMapping' and node.rest:
            yield 'symbol', node.rest, line
        elif isinstance(node, ast.arg):
            yield 'symbol', node.arg, line
        elif isinstance(node, ast.Attribute) and isinstance(node.ctx, ast.Store):
            yield 'field', node.attr, line
        elif isinstance(node, ast.Subscript) and isinstance(node.ctx, ast.Store):
            if isinstance(node.slice, ast.Constant) and isinstance(node.slice.value, str):
                yield 'field', node.slice.value, line
        elif isinstance(node, ast.alias):
            yield 'symbol', node.asname or node.name.split('.')[0], line
        elif isinstance(node, (ast.Global, ast.Nonlocal)):
            for name in node.names:
                yield 'symbol', name, line
        if isinstance(node, ast.Dict):
            try:
                debt_record = is_debt_record(ast.literal_eval(node))
            except (ValueError, TypeError):
                debt_record = False
            for key, value in zip(node.keys, node.values):
                if isinstance(key, ast.Constant) and isinstance(key.value, str):
                    yield 'key', key.value, key.lineno
                    if not debt_record and key.value in RESOURCE_FIELDS and isinstance(value, ast.Constant) and isinstance(value.value, str):
                        yield 'resource', value.value, value.lineno
        pairs = []
        if isinstance(node, ast.Assign):
            pairs = [(t.id if isinstance(t, ast.Name) else t.attr, node.value)
                     for t in node.targets if isinstance(t, (ast.Name, ast.Attribute))]
            pairs.extend((t.slice.value, node.value) for t in node.targets
                         if isinstance(t, ast.Subscript) and isinstance(t.slice, ast.Constant)
                         and isinstance(t.slice.value, str))
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            pairs = [(node.target.id, node.value)]
        elif isinstance(node, ast.keyword):
            pairs = [(node.arg, node.value)]
            if node.arg:
                yield 'field', node.arg, line
        for name, value in pairs:
            if name and re.sub(r'([a-z])([A-Z])', r'\1_\2', name).lower() in RESOURCE_FIELDS and isinstance(value, ast.Constant) and isinstance(value.value, str):
                yield 'resource', value.value, value.lineno


def json_names(text):
    # Preserve duplicate keys: a later value must not hide an earlier bad name.
    class Pairs(list):
        pass
    def walk(value):
        if isinstance(value, Pairs):
            for key, child in value:
                yield 'key', key, 1
                if key in RESOURCE_FIELDS and isinstance(child, str):
                    yield 'resource', child, 1
                yield from walk(child)
        elif isinstance(value, list):
            for child in value:
                yield from walk(child)
    yield from walk(json.loads(text, object_pairs_hook=Pairs))


def check(repo, files, policy):
    violations = []
    incomplete = []
    pins = {x['path']: x['sha256'] for x in policy['immutable']}
    if any(path not in files for path in pins):
        raise ValueError('immutable artifact missing')
    for path, (mode, _) in files.items():
        if path in pins:
            if mode not in {'100644', '100755'} or hashlib.sha256(blob(repo, files, path)).hexdigest() != pins[path]:
                raise ValueError('immutable artifact changed: ' + repr(path))
            continue
        if forbidden(path, policy):
            violations.append((path, 'path', path, 0))
        if mode not in {'100644', '100755'}:
            incomplete.append((path, 'non-regular Git entry; path checked only'))
            continue
        if path == POLICY:
            continue
        suffix = Path(path).suffix.lower()
        raw = blob(repo, files, path)
        if b'\0' in raw:
            incomplete.append((path, 'binary content; path checked only'))
            continue
        try:
            text = raw.decode('utf-8') if suffix != '.py' else ''
            if suffix == '.py':
                # Honour source encoding declarations, just like Python does.
                encoding, _ = tokenize.detect_encoding(io.BytesIO(raw).readline)
                names = python_names(raw.decode(encoding))
            elif suffix == '.json':
                names = json_names(text)
            elif suffix in {'.js', '.jsx', '.mjs', '.cjs', '.ts', '.tsx', '.mts', '.cts'}:
                result = subprocess.run(
                    ['node', str(Path(__file__).with_name('naming-js.cjs'))],
                    input=json.dumps({'path': path, 'text': text, 'resourceFields': sorted(RESOURCE_FIELDS)}),
                    text=True, capture_output=True)
                if result.returncode:
                    raise ValueError('JavaScript/TypeScript parser failed: ' + result.stderr.strip())
                names = json.loads(result.stdout)
            else:
                if suffix not in TEXT_ONLY and Path(path).name not in {'LICENSE', '.gitignore', '.gitattributes'}:
                    incomplete.append((path, 'no parser; path checked only'))
                continue
            for kind, name, line in names:
                if forbidden(name, policy):
                    violations.append((path, kind, name, line))
        except (SyntaxError, UnicodeError, ValueError) as exc:
            raise ValueError('cannot parse ' + repr(path) + ': ' + str(exc)) from exc
    debt = counts(policy)
    findings = []
    for path, kind, name, line in violations:
        key = (path, kind, name)
        if debt[key]:
            debt[key] -= 1
        else:
            findings.append({'path': path, 'line': line, 'kind': kind, 'name': name,
                             'message': 'Name the domain responsibility, not the local task.'})
    if any(debt.values()):
        raise ValueError('stale naming baseline entries; remove resolved debt')
    return findings, incomplete


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', default='.')
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument('--staged', action='store_true')
    mode.add_argument('--tree', help='Check all files at this commit/tree')
    parser.add_argument('--base', help='Trusted policy baseline revision; defaults to HEAD for staged checks')
    parser.add_argument('--require-complete', action='store_true', help='Fail on unsupported content coverage')
    args = parser.parse_args()
    try:
        repo = git(args.repo, 'rev-parse', '--show-toplevel').decode('utf-8', errors='surrogateescape').removesuffix('\n')
        files = snapshot(repo, args.tree)
        policy = read_policy(repo, files)
        if args.tree and not args.base:
            raise ValueError('--tree requires --base for policy ratcheting')
        base = args.base or 'HEAD'
        old = read_policy(repo, snapshot(repo, base))
        validate_policy_change(old, policy)
        findings, incomplete = check(repo, files, policy)
        for finding in findings:
            print(json.dumps({'violation': finding}, ensure_ascii=True))
        for path, reason in incomplete:
            print(json.dumps({'coverage': {'path': path, 'limitation': reason}}, ensure_ascii=True))
        code = 2 if incomplete and args.require_complete else 1 if findings else 0
        print(json.dumps({'status': 'incomplete' if code == 2 else 'violations' if code else 'clean-within-coverage',
                          'files': len(files), 'violations': len(findings), 'unsupported': len(incomplete)}))
        return code
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'error': str(exc)}, ensure_ascii=True), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
