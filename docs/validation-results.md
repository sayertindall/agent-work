# Validation results

Repository creation and evaluation date: September 12, 2026.

The collection has sixteen skills and a shared policy. The workflow is named Steady. No live agent configuration has been installed or replaced.

## Evidence under evaluation

- `python3 -B scripts/validate.py`: passed for all 16 skills, 289 description words, catalog, policy, relative links, and evaluation records.
- `python3 -B scripts/test_validate.py`: 7 regression tests passed, including missing references, wrong identities, invalid scenario contracts, unknown lanes, escaping links, and nonportable metadata.
- The installed Codex skill-creator `quick_validate.py`: all 16 skills passed independently of the collection validator.
- The first structural pass correctly detected the absent validation-results document before this file was created.

The author also ran the disposable CLI fixture's help, list, and show commands and compared their output with the generated reference. The commands and examples agreed.

A separate Luna worker at maximum reasoning completed eight decision simulations and a disposable lifecycle from draft through ready, active, and done. The author inspected the report, plan, and fixture, independently ran the CLI, and verified matching before/after manifests for repeat init (18 non-Git file hashes), repeat sync (19), and read-only status (19). Retained evidence is in [the lifecycle fixture](../evals/observed/lifecycle/README.md).

The lifecycle used the Markdown work procedures before the user's subsequent request for a deterministic scaffold script. The script is evaluated separately; these receipts do not prove its behavior.

## Live host acceptance

Claude Code: not installed or exercised in a fresh session.
Codex: not installed; authoring and independent evaluation occur in this host, which does not prove native installed discovery.
OMP: not installed or exercised in a fresh session.

These checks belong to the subsequent backup and activation stage.
