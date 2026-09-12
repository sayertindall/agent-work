# Naming and code quality rules

These rules apply whenever producing or reviewing an artifact, including small edits. They do not depend on whether a durable plan or principle is needed.

## Name the domain

Choose names for the responsibility or content. A person outside the current task should understand the name without its ticket, phase, agent, or conversation.

| Do not introduce | Prefer when it describes the actual responsibility |
| --- | --- |
| `k01-auth-check.ts` | `verify-access-token.ts` |
| `runR02Migration()` | `migrateSessionStorage()` |
| `phase3-results.json` | `permission-check-results.json` |
| `task17Bucket` | `auditArchiveBucket` |
| `final-v2-fixed.ts` | The module's domain responsibility |

Before creating a path, symbol, field, test title, image, or resource, choose its domain meaning. This includes work-plan filenames: put task IDs inside tracking metadata, not in the filename. Describe test behavior instead of naming the task that requested it.

Do not copy an existing violation. Rename owned violations within authorized scope with their callers. For external contracts, deployed resource identities, and sealed evidence, report the required migration; do not break compatibility or rewrite historical bytes. New evidence does not qualify as immutable merely because it lives under an evidence directory.

Semantic review, not a universal pattern matcher, determines whether a name describes its domain. Project-specific linters may enforce established identifiers or resource constraints, but legitimate protocol versions and externally owned names need evidence-based treatment rather than broad substring bans.

## Keep code useful and checkable

- Preserve known types and derive from authoritative schemas. Do not widen and cast back to hide a mismatch. Validate genuinely untrusted input at its boundary.
- Keep an abstraction when it owns a meaningful decision. Remove duplicate decisions and empty pass-through layers within the requested scope.
- Assert observable behavior and meaningful failure cases. Avoid tests that only restate implementation or their own fixtures.
- Keep necessary invariant and rationale comments. A comment is not evidence that an unsafe operation is safe; check the invariant itself.
- Use the project's formatter and targeted lint checks. Do not introduce competing formatting conventions or blanket bans on mocks, `unknown`, or runtime type checks.
- Preserve semantics when simplifying collection operations, error handling, or compatibility code. A shorter expression is not automatically a better implementation.

Before commit, inspect new paths, symbols, fields, test titles, images, and resources in the actual change. For branch review, use the real base and head. Report any name that still depends on task context and any language or artifact the review could not inspect.

A failed project check requires a fix or an explicit unresolved finding. Do not weaken severity, expand debt, bypass hooks, or rename a forbidden operation through indirection to make the check pass. A real project-policy defect needs a separately reviewed correction and a regression case.
