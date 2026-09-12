# Host adapters

The canonical skill tree uses plain `SKILL.md` frontmatter and relative references. It contains no model identifiers or host-specific tool schemas. Read only the adapter for the active host when installation, delegation, or scheduling mechanics matter.

| Host | Adapter | Global policy destination |
| --- | --- | --- |
| Claude Code | [Claude](claude.md) | `~/.claude/CLAUDE.md` |
| Codex | [Codex](codex.md) | `~/.codex/AGENTS.md` |
| OMP | [OMP](omp.md) | `~/.omp/agent/AGENTS.md` |

These are the audited local defaults. Respect a configured home or project-specific override at installation time. Existing global files must be backed up and reconciled rather than blindly overwritten.

## One source, one discovery path

Expose the canonical `skills/` tree through each host's supported discovery mechanism after backup. Prefer the shared discovery root where all three installed versions demonstrably support it. Otherwise use host-specific links without also leaving a second discoverable copy for that host. Do not simply add links to all roots.

Some references intentionally cross skill folders and reach this repository's policy or adapters. Install the complete repository, preserving its layout. If linking individual skill directories, test that the host resolves references against the canonical real path. If it instead resolves against the alias, use a supported additional skill root or a whole-tree installation that preserves the adjacent directories. Do not distribute individual skill folders as standalone packages.

At activation, inspect each host's actual discovered inventory. Directory contents alone cannot establish precedence or duplicate suppression. Confirm canonical paths, descriptions, and references. Run [behavioral cases](../docs/validation.md) before declaring all three hosts accepted.

## Common role contract

Use the current session for coordination. Optional roles are worker, reviewer, and researcher; an existing explorer can handle narrow read-only discovery. The host may use different names. Choose a suitable configured role, not a hardcoded provider. Pass outcome, baseline, ownership, allowed actions, acceptance, and required returned evidence.

If a tool or independent reviewer is unavailable, say so. Continue useful local work when allowed, but do not label a self-review independent or promise unavailable scheduling.
