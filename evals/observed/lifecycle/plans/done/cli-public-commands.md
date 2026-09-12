# Document this CLI public commands

- ID: cli-public-commands
- Project and repository: `/tmp/agent-work-validation.Ve4PmT/fixture`
- Source: Validation request to document the fixture CLI's public commands
- Completion artifact: `/tmp/agent-work-validation.Ve4PmT/fixture/COMMANDS.md`

## Outcome

Provide a concise Markdown reference for the fixture CLI's public `list` and
`show` commands.

## Scope and exclusions

Document only commands exposed by `python3 fixture/cli.py --help`. The
reference will live beside the fixture as `fixture/COMMANDS.md`. Do not add
commands, change CLI behavior, create a PR, commit, configure a remote, or
install anything.

## Acceptance

- `fixture/COMMANDS.md` names both public commands, `list` and `show`.
- The reference describes each command's arguments and observed output.
- The reference is checked against the fixture's `--help`, `list`, and
  `show beta` behavior, with the checked outputs retained under `evidence/`.

## Decisions and unknowns

Use the CLI help output as the command-name source of truth. Use a short
Markdown page with invocation examples and observed output; no generated
documentation tool is needed.

## Dependencies

None.

## Authorization

The user authorized this disposable validation lifecycle, including local
implementation and verification of the command reference. There is no
authorization to create a PR, commit, configure a remote, or install anything.

## Ownership

- Coordinator: Luna validation agent in the current Codex task
- Checkout: `/tmp/agent-work-validation.Ve4PmT`
- Branch/base: `main` (local disposable repository; no commit or remote)
- Worker scopes: none; this coordinator is the sole work-repository writer
- Ownership released after successful sync; no active worker remains.

## Progress and evidence

- Baseline help and command outputs were captured under `evidence/` before
  planning.
- Dependencies are satisfied: the fixture exists and its help exposes `list`
  and `show`.
- 2026-09-12T11:55:03-05:00: `python3 fixture/cli.py --help` confirms the
  public `list` and `show` commands; output is in
  `evidence/cli-public-commands/final-help.txt`.
- 2026-09-12T11:55:03-05:00: `python3 fixture/cli.py list` returns `alpha` and
  `beta`; output is in `evidence/cli-public-commands/final-list.txt`.
- 2026-09-12T11:55:03-05:00: `python3 fixture/cli.py show beta` returns
  `beta: Second fixture record`; output is in
  `evidence/cli-public-commands/final-show-beta.txt`.
- 2026-09-12T11:55:03-05:00: the reference contains the `list` and
  `show <record_id>` sections, and the baseline/final CLI outputs compare
  byte-identically with `cmp`.
- 2026-09-12T11:55:03-05:00: repeated work-init created no missing setup; the
  pre/post non-Git file hash manifests compare byte-identically at
  `/tmp/agent-work-validation.Ve4PmT.before-repeat-init.sha256` and
  `/tmp/agent-work-validation.Ve4PmT.after-repeat-init.sha256`.
- 2026-09-12: work-sync checked every acceptance criterion; the detailed
  reconciliation is in `evidence/cli-public-commands/sync-report.md`.

## Next action

All acceptance criteria are evidenced and the plan is complete in
`plans/done/`. Read-only work-status may report the completed state.
