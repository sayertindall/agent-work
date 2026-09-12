# Naming enforcement validation

Validated locally on September 12, 2026, in the isolated PR worktree. No live host installation or project-wide migration was performed.

## Automated checks

- Collection validation: 17 skills, 305 description words, policy under 500 words, all file links and scenario records valid.
- Full unittest discovery: 59 tests passed, including 32 new black-box naming tests written by a separate Luna/max worker and one metadata-discrimination regression added by the coordinator against disposable Git repositories.
- Naming tests include staged/working-tree disagreement in both directions, explicit tree selection, camel/snake/kebab naming, unusual filenames and renames, declarations and resource fields, duplicate JSON keys, exact debt counts, immutable pins, parse failures, invalid policy, invalid Git state, and unsupported coverage.
- A TypeScript fixture exposed missing resource detection for a literal element assignment. The implementation was repaired and the fixture passed without weakening its expectation.
- The staged repository snapshot reported zero violations and 18 unsupported content files (workflow/guide YAML and retained checksum files). Those files received path checks only. Markdown and presentation assets also receive path checks only by design.
- The final self-scan identified a false positive on exact historical-debt metadata. The checker now distinguishes that record from a new resource; a regression confirms that ordinary resource names remain rejected.
- Difftastic inspection and direct source review completed. No formatter migration or upstream anti-slop source copy was introduced.

## Instruction walkthroughs

The author traced the four new cases in [scenarios](../evals/scenarios.json): a small script requested with a task code, an existing violating helper, sealed evidence, and pressure to get a failed PR green. The always-loaded rule requires domain names in all four; the rules reference preserves external/immutable contracts and refuses exemption expansion. These are source walkthroughs, not cross-host behavioral tests.

The parser recognizes configured markers and selected syntax. It does not prove that every accepted name describes its domain or that all resource values are observable statically. [Coverage and adoption](naming-gate.md) remain part of the check result.

## Remaining review and activation

OCR preview selected code/configuration files and excluded Markdown. The full OCR call was rejected by automatic approval review because it would transmit the code diff to the configured provider without explicit approval for that payload. No OCR result is claimed; local assessment was used and approval was requested separately.

The PR adds a GitHub workflow but does not make its status required through repository protection. After adoption, repository administrators must require the Naming gate check and protect enforcement changes. This first introduction requires maintainer review because the base has no trusted checker yet. Host policy copies and project hook adoption are also separate activation steps.
