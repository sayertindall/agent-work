#!/usr/bin/env python3
"""Validate the portable skill collection without modifying it."""
import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote, urlsplit


def validate(root):
    errors = []
    names = set()
    expected = {
        'steady', 'work-init', 'work-add', 'work-plan', 'work-run',
        'work-status', 'work-sync', 'work-retro', 'architecture', 'debug',
        'review', 'open-code-review', 'research', 'interface', 'writing', 'security', 'performance',
    }
    total_description_words = 0
    skill_paths = sorted((root / 'skills').glob('*/SKILL.md'))
    for path in skill_paths:
        text = path.read_text()
        label = str(path.relative_to(root))
        parts = text.split('---', 2)
        if len(parts) != 3 or parts[0]:
            errors.append(f'{label}: missing frontmatter')
            continue
        metadata = {}
        for line in parts[1].strip().splitlines():
            key, sep, value = line.partition(':')
            if not sep or key in metadata:
                errors.append(f'{label}: malformed or repeated frontmatter key')
                continue
            metadata[key] = value.strip()
        if set(metadata) != {'name', 'description'}:
            errors.append(f'{label}: use only name and description')
            continue
        name = metadata['name']
        if not re.fullmatch(r'[a-z][a-z0-9-]{0,63}', name) or name != path.parent.name:
            errors.append(f'{label}: name must match the folder')
        if name in names:
            errors.append(f'{label}: duplicate name {name}')
        names.add(name)
        try:
            description = json.loads(metadata['description'])
            if not isinstance(description, str) or not description.strip():
                raise ValueError('description must be a nonempty quoted string')
        except (ValueError, TypeError) as exc:
            errors.append(f'{label}: invalid description ({exc})')
            continue
        words = len(description.split())
        total_description_words += words
        if words > 40:
            errors.append(f'{label}: description has {words} words; maximum 40')
        body_words = len(parts[2].split())
        if body_words > 600 or body_words < 40:
            errors.append(f'{label}: body has {body_words} words; expected 40..600')
        if re.search(r'\b(?:gpt-\d|claude-[a-z]+-\d|spawn_agent|AskUserQuestion|TaskCreate)\b', parts[2]):
            errors.append(f'{label}: host mechanics belong in adapters')
    if names != expected:
        errors.append(f'catalog identity mismatch: missing={sorted(expected-names)}, extra={sorted(names-expected)}')
    catalog = root / 'CATALOG.md'
    if not catalog.is_file():
        errors.append('missing CATALOG.md')
    else:
        for name in names:
            if f'(skills/{name}/SKILL.md)' not in catalog.read_text():
                errors.append(f'CATALOG.md: missing {name}')
    for path in sorted(root.rglob('*.md')):
        if '.git' in path.parts:
            continue
        text = path.read_text()
        label = str(path.relative_to(root))
        if re.search(r'\b(?:TODO|FIXME|TBD)\b', text):
            errors.append(f'{label}: unfinished marker')
        if '\u2014' in text:
            errors.append(f'{label}: em dash conflicts with shared style policy')
        for target in re.findall(r'\[[^\]]*\]\(([^)]+)\)', text):
            target = target.strip('<>')
            parsed = urlsplit(target)
            if parsed.scheme or not parsed.path:
                continue
            destination = (path.parent / unquote(parsed.path)).resolve()
            if not destination.is_relative_to(root.resolve()):
                errors.append(f'{label}: link escapes repository: {target}')
            elif not destination.is_file():
                errors.append(f'{label}: broken file link: {target}')
    policy = root / 'policy/AGENTS.md'
    if not policy.is_file():
        errors.append('missing shared policy')
    elif len(policy.read_text().split()) > 500:
        errors.append('shared policy exceeds 500 words')
    try:
        cases = json.loads((root / 'evals/scenarios.json').read_text())
        ids = set()
        required = {'id', 'request', 'entry', 'allowed_effects', 'expected', 'forbidden'}
        if not isinstance(cases, list) or len(cases) < 12:
            raise ValueError('expected at least 12 scenario records')
        for case in cases:
            if not isinstance(case, dict) or set(case) != required:
                raise ValueError('invalid scenario fields')
            if any(not isinstance(v, str) or not v.strip() for v in case.values()):
                raise ValueError('empty or non-string scenario field')
            if case['id'] in ids:
                raise ValueError('duplicate scenario id')
            ids.add(case['id'])
            entry = case['entry']
            base, _, lane = entry.partition('/')
            if entry != 'direct' and base not in names:
                raise ValueError(f'unknown scenario skill: {entry}')
            if lane and not (root / 'skills' / base / 'references' / f'{lane}.md').is_file():
                raise ValueError(f'unknown scenario lane: {entry}')
    except (OSError, ValueError) as exc:
        errors.append(f'evals/scenarios.json: {exc}')
    return errors, len(skill_paths), total_description_words


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors, count, words = validate(args.root)
    if errors:
        for error in errors:
            print(f'FAIL: {error}', file=sys.stderr)
        return 1
    print(f'PASS: {count} skills; {words} description words; catalog, policy, links, and scenarios valid.')
    print('Structural validation only. Host discovery and agent behavior require separate evidence.')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
