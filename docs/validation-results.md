# Validation results

Repository creation and evaluation date: September 12, 2026.

The initial collection had sixteen skills and a shared policy. The workflow is named Steady. No live agent configuration has been installed or replaced.

## Evidence under evaluation

- `python3 -B scripts/validate.py`: passed for all 16 skills, 284 description words, catalog, policy, relative links, and evaluation records.
- `python3 -B scripts/test_validate.py`: 7 regression tests passed, including missing references, wrong identities, invalid scenario contracts, unknown lanes, escaping links, and nonportable metadata.
- `python3 -B scripts/test_init_work.py`: 17 behavioral tests passed for scaffold creation, repeatability, content preservation, read-only checks, conflict refusal, and Git initialization and reuse.
- The installed Codex skill-creator `quick_validate.py` passed all 16 skills in the earlier authoring pass. The final rerun could not start because both available Python runtimes lacked PyYAML. The current metadata passed the collection validator; a fresh upstream validation remains unverified.
- The first structural pass correctly detected the absent validation-results document before this file was created.

The author also ran the disposable CLI fixture's help, list, and show commands and compared their output with the generated reference. The commands and examples agreed.

A separate Luna worker at maximum reasoning completed eight decision simulations and a disposable lifecycle from draft through ready, active, and done. The author inspected the report, plan, and fixture, independently ran the CLI, and verified matching before/after manifests for repeat init (18 non-Git file hashes), repeat sync (19), and read-only status (19). Retained evidence is in [the lifecycle fixture](../evals/observed/lifecycle/README.md).

The lifecycle used the Markdown work procedures before the user's subsequent request for a deterministic scaffold script. The script is evaluated separately by the 17 behavioral tests above; these receipts do not prove its behavior.

After the shared policy made the workflow automatic, a Luna worker also simulated an implementation request with a project-defined work directory and no explicit skill invocation. It selected Steady, the Implement lane, the project directory, script-based initialization, a durable plan, and verification. This was a decision simulation and created no directory. The scenario is retained as `automatic-workflow` in `evals/scenarios.json`.

## Live host acceptance

Claude Code: not installed or exercised in a fresh session.
Codex: not installed; authoring and independent evaluation occur in this host, which does not prove native installed discovery.
OMP: not installed or exercised in a fresh session.

These checks belong to the subsequent backup and activation stage.

## Open Code Review and Difftastic integration

Added the seventeenth skill, `open-code-review`, and connected it to the shared review contract. The agent uses the existing `git dft` alias alongside OCR. Installed OCR v1.12.0 help confirmed the documented flags; its configured provider was not changed or called for this integration.

The collection validator and all 7 validator regression tests passed after the addition. A disposable Git fixture confirmed that `git dft --cached` selects staged changes only, while `ocr review --preview --audience agent` selects staged, unstaged, and untracked files. Preview did not perform an LLM review.

Author walkthroughs covered default branch review, staged-only scope, and partial results despite exit zero. The instructions resolve the actual branch baseline, reject widening a staged-only request, and leave skipped coverage incomplete. These are author assessments, not independent agent evaluations. Live discovery in all three hosts and a full provider-backed OCR review remain untested.
