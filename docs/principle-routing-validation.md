# Principle routing validation

The change adds portable instruction-driven loading. It does not implement a host hook or prove reliable behavior in all three hosts.

## Structural checks

On September 12, 2026, in the isolated codex/principle-routing worktree:

- `python3 -B scripts/validate.py`: passed; 17 skill identities and 305 description words remain unchanged.
- `python3 -B -m unittest discover -s scripts -p 'test_*.py'`: 26 tests passed. These exercise existing scaffold and validator behavior, not principle selection.
- A read-only heading-resolution check verified all 25 local section links outside the imported interface library.
- `git diff --check`: passed. Difftastic inspection and direct source assessment were used for this instruction-only change; OCR was not run because there is no code diff.

## Author scenario walkthrough

These are source-based decision walkthroughs, not independent model runs. Inputs and boundaries are recorded in [scenarios](../evals/scenarios.json).

| Cases | Decision traced through the revised instructions |
| --- | --- |
| tiny-edit, principle-no-preload | The shared policy excludes self-evident small edits from managed records; the index does not impose a principle step when no consequential decision exists. |
| read-only, proposal, principle-direct-entry | Direct architecture entry reads the relevant sections before selection; existing evidence supports a conversational proposal, with no prototype or plan creation. |
| repeat-init, uncertain-retry | Initialization and the operational lane read safe-retry guidance before mutation or repetition. Existing content and uncertain results must be reconciled. |
| handoff, concurrent-claim, principle-delegate-context | Coordination reconciles live ownership before replacement; assignments include principle paths and workers must read them themselves. |
| principle-mid-task | Repeated failed repairs trigger premise guidance before the next attempt, even after initial routing. |
| partial-ci, principle-completion | work-run and work-sync read outcome-proof guidance before completion. A missing runtime criterion stays unmet despite build or CI success. |
| retro, principle-retro-boundary | Evidence guidance is loaded before recommending a durable correction; read-only analysis cannot change global policy or memory. |

The migration preserves existing principle definitions, giving them addressable headings. It adds selection timing and section pointers rather than a new discoverable skill catalog. Installed policy copies and the live canonical checkout are outside this PR's activation scope.

## Behavioral evidence

A separate Luna/max worker performed a read-only forward test from a fresh assignment, using the branch skills and a supplied export-state fixture. The evaluator was told to follow the skills and report read order; this is a scoped compliance exercise, not a blinded comparison against the previous version.

For direct architecture entry, the fixture supplied `isRunning`, `isFinished`, an optional result URL, and four required states. The worker reported reading architecture, the index, then useful-model, intended-design, uncertainty, and consumer sections before returning a proposal. It chose a discriminated status union with a URL only on the finished variant, preserved boundary validation, and identified unresolved compatibility details. It created no prototype or plan. Supporting reads later included the scenario catalog, so this is not held-out evaluation evidence.

For a subsequent report that two repairs failed the same regression check, it read debug, reused the index, then read repair-the-cause and reconsider-the-premise guidance. It proposed correlating the same export ID across persistence, worker terminal events, and the API response to distinguish execution failure from stale read state. It did not pretend to execute this observation against the nonexistent application.

Both responses preserved proposal/read-only scope and reported the relevant definitions read before their recommendations. Read order and absence of side effects are worker-reported; no automated tool-event trace assertion was implemented. Cross-host loading, long-session retention, and actual delegated execution remain outside this validation.
