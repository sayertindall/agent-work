# Validation

## Structural checks

Run `python3 -B scripts/validate.py` from the repository root. It checks every skill's required frontmatter, unique identity, description and body size, catalog coverage, relative file links, portable text, and evaluation record shape. It also flags unfinished edit markers. It performs no writes and needs only Python's standard library.

Run `python3 -B scripts/test_validate.py` to exercise the validator against damaged disposable copies. Those regression tests write only to temporary directories and must not run under a strict no-write instruction.

These checks prove the collection's structure. They do not prove that the host loader selects the right skill or that an agent follows it.

## Work-directory scaffolding

Run `python3 -B scripts/test_init_work.py` to check fresh creation, reuse, preservation, read-only inspection, Git ownership, and conflict handling in disposable directories. These tests intentionally write temporary fixtures. The scaffold itself has a read-only `--check` mode.

## Behavioral evaluation

`evals/scenarios.json` contains realistic requests, allowed effects, expected decisions, and disallowed behavior. Give a fresh evaluator the request and relevant skill paths without showing it the expected outcome. Use an isolated disposable workspace if executing code or writing plans. Read-only cases must not write there either.

Assess actual tool calls and artifacts, not just a claimed intended behavior. For routing-only evaluation, have the evaluator state the chosen entry point, first action, required authority, and completion predicate; label that evidence as a decision simulation, not a full execution.

Evaluate relevant cases after changing a decision boundary. For initial activation run the complete set separately in fresh Claude, Codex, and OMP sessions. Record model/host, source revision, observed effects, result, and limitations. Do not ask a worker to validate the intended answer supplied by its author.

## Acceptance boundaries

Repository acceptance requires structural validity, reviewed policy/routing, and relevant scenario evaluation. Live-host acceptance additionally requires an installed inventory with no duplicate entries, working references, reconciled global instructions, and actual scenario execution on that host. Do not launch or reconfigure live hosts during a repository-only build.

The initial evidence is recorded in [validation results](validation-results.md). Update it only after observing a new result. Saved expectations are not evidence.
