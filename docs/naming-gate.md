# Naming gate

Name artifacts for their domain responsibility. Task IDs belong in tracking metadata and explanatory prose, not paths, symbols, test names, images, or resources. The [shared rules](../skills/steady/references/rules.md) apply even when a mechanical check cannot recognize the violation.

## Run it

From a checkout of this repository, install the pinned JavaScript/TypeScript parser once:

```sh
npm ci --ignore-scripts
```

Check the index without changing files or staging:

```sh
python3 -B scripts/check_names.py --staged
```

Check another repository or an explicit pair of revisions:

```sh
python3 -B /path/to/agent-work/scripts/check_names.py --repo /path/to/project --staged
python3 -B scripts/check_names.py --tree HEAD --base origin/main
```

`--base` identifies the trusted policy snapshot, not a diff filter. The checker scans every file in the target snapshot, so inherited violations need exact baseline records. Staged checks default to HEAD as the policy baseline. Unborn repositories need an initial trusted commit before running this gate. Invalid refs, unmerged indexes, missing parsers, malformed source and invalid policy exit with an error instead of a clean result.

The driver reads Git blob IDs with NUL-delimited paths. Staged mode reads index contents, not working files. Tree mode reads the selected committed tree. Spaces, tabs, newlines, renames, and partial staging do not change which bytes are checked. Nothing is rewritten automatically.

Output is JSON lines with paths, names, locations where available, and coverage limits. Exit codes:

| Code | Meaning |
| --- | --- |
| 0 | No violations within the reported coverage |
| 1 | Naming violations |
| 2 | Checker error, or unsupported content with `--require-complete` |

Use `--require-complete` when every selected file must have content analysis. A path-only result for an unsupported language is never reported as full content acceptance.

## What it catches

The default markers are R, K and S followed by at least two digits, separated by path punctuation, snake/kebab separators, or camel/Pascal case boundaries. Examples include `k01-export.ts`, `runK01Export`, and `K01_EXPORT`. Numbered task, ticket, phase, and step names, including common spelled numbers, are also detected. Versions, hexadecimal digests and ordinary `s3` usage are not blanket-banned.

- Every tracked path is checked, including new evidence and audit directories.
- Python uses its AST for declarations, bindings, parameters, assigned fields, dictionary keys, and selected literal resource fields.
- JavaScript/TypeScript uses the pinned TypeScript parser for declarations, local binding names, member definitions, object keys, and selected literal resource fields. Imported aliases are checked locally; ordinary member reads are not treated as new definitions.
- JSON checks keys, including duplicate keys, and selected literal resource fields. Locations are file-level rather than exact JSON lines.
- Selected resource fields include `name`, `prefix`, `image`, `bucket`, `resource`, and their documented variants in the checker. Dynamically constructed values need project-specific checks at their actual consumption boundary.

Prose, comments and ordinary fixture strings are not treated as identifiers. An exact Python debt-record dictionary (`path`, `kind`, `name`, `count`) describes a historical finding; its name value is metadata, not a new resource. Its keys are still checked. Markdown and common presentation/text assets receive path checks only. Other languages, YAML/Terraform contents, binary contents, symlinks and submodules are explicitly reported as unsupported content. Test descriptions and computed names still require semantic review. This gate does not claim whole-program ownership analysis, cloud inspection, or detection of every task nickname.

## Debt and immutable evidence

[naming-policy.json](../naming-policy.json) is read from the same Git snapshot as source. It records literal project prefixes, exact allowed names, exact debt entries, and immutable blob pins. The initial repository policy has no exceptions.

A debt entry identifies `path`, `kind`, `name`, and `count`. It cannot exempt a whole file. A new name or additional occurrence fails. Resolved entries must be removed. Against the base snapshot, counts may only shrink; allowed terms and prefix policy cannot change through a routine code patch.

An immutable entry identifies an exact path and SHA-256 content hash. The content must remain byte-identical and present. Pins cannot be removed, repointed or expanded through an ordinary change. An evidence directory is not an exemption.

Introducing legitimate exceptions or migrating protected policy requires a separately reviewed adoption decision establishing a new trusted baseline. The checker has no bypass flag or automatic baseline generator. Do not rename sealed data or externally owned contracts to satisfy the gate. Report the migration instead.

## CI and project adoption

The [repository workflow](../.github/workflows/checks.yml) runs structural checks, regression tests and the naming gate. On later PRs it runs the checker and parser from the trusted base revision against proposed blobs. That prevents a PR from passing simply by rewriting its own checker. The first introduction necessarily uses the proposed checker and needs maintainer review.

GitHub must require the `Naming gate` status check through repository protection or a ruleset to make it a merge barrier. This PR adds the workflow; it does not alter repository protection. Workflow changes themselves also need trusted review or an organization-managed required workflow. A workflow stored in a PR is not a tamper-proof security boundary.

For another project, adopt the checker, parser dependency and reviewed policy in that project's tooling layout, or invoke a trusted complete checkout. Add the command to its existing pre-commit mechanism and CI; preserve existing hooks. Do not change every project's hooks or formatter as an incidental skill installation. Add language/resource adapters where that project needs coverage, and test them with real violations and valid cases.

The agent instructions are portable across Claude Code, Codex and OMP. Activating them still requires the policy synchronization described in [installation](installation.md). No live host configuration or other project has been changed by this implementation.

## Anti-slop approach

The [anti-slop project](https://github.com/dmmulroy/anti-slop) demonstrates repository-owned lint rules with diagnostics, regression cases, local customization and recorded provenance. This implementation follows that approach; no upstream rule code was copied. It does not require Oxlint or Oxfmt, and keeps formatter choice with each project. Its semantic code-quality rules remain in the shared guidance until an appropriate project-specific check exists.
