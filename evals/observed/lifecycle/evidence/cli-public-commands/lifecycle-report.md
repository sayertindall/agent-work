# Disposable lifecycle validation

- Work repository: `/tmp/agent-work-validation.Ve4PmT`
- Fixture: `/tmp/agent-work-validation.Ve4PmT/fixture/cli.py`
- Completion artifact: `/tmp/agent-work-validation.Ve4PmT/fixture/COMMANDS.md`
- Final plan: `/tmp/agent-work-validation.Ve4PmT/plans/done/cli-public-commands.md`

## Transitions

1. `work-init`: initialized the empty local Git repository, created the seven
   tracking directories, `.gitkeep` files where needed, and the README.
2. `work-add`: captured `Document this CLI public commands` at
   `plans/drafts/cli-public-commands.md` with scope, acceptance, and the
   capture-only boundary.
3. `work-plan`: resolved the artifact path and checks, then moved the plan to
   `plans/ready/cli-public-commands.md`.
4. `work-run`: confirmed the fixture, authorization, and sole coordinator,
   moved the plan to `plans/active/cli-public-commands.md`, and created
   `fixture/COMMANDS.md`.
5. `work-sync`: checked every acceptance criterion and moved the plan to
   `plans/done/cli-public-commands.md`.
6. `work-status`: reported one done plan, no ready or active Markdown plans,
   and left all non-Git file hashes unchanged.

## Commands and checks

- `python3 fixture/cli.py --help`: exposes `list` and `show`.
- `python3 fixture/cli.py list`: returns `alpha` and `beta`.
- `python3 fixture/cli.py show beta`: returns `beta: Second fixture record`.
- `rg` checks confirm both reference sections and the documented outputs.
- `cmp` confirms baseline and final help, list, and show outputs are identical.
- Repeat `work-init`: pre/post non-Git manifests compare identically at
  `/tmp/agent-work-validation.Ve4PmT.before-repeat-init.sha256` and
  `/tmp/agent-work-validation.Ve4PmT.after-repeat-init.sha256`.
- Repeat `work-sync`: done state and evidence remain unchanged; manifests
  compare identically at
  `/tmp/agent-work-validation.Ve4PmT.before-repeat-sync.sha256` and
  `/tmp/agent-work-validation.Ve4PmT.after-repeat-sync.sha256`.
- Read-only `work-status`: manifests compare identically at
  `/tmp/agent-work-validation.Ve4PmT.before-status.sha256` and
  `/tmp/agent-work-validation.Ve4PmT.after-status.sha256`.

Detailed command outputs are under
`evidence/cli-public-commands/`; `sync-report.md` records the acceptance
reconciliation.

## Observed issues and boundaries

No functional issues occurred. The collection supplies Markdown skills rather
than executable `work-*` commands, so this validation applied each documented
operation directly to the disposable records. The repository remains local
and uncommitted with no remote, PR, or installation, as authorized. The hash
comparisons intentionally exclude `.git/` internals and cover every other
regular file present at each checkpoint.
