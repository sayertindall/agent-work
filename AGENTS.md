# Working on Agent Work

Use normal Git. Keep all changes scoped to this repository unless installation or migration is explicitly requested. Do not alter live agent configuration while developing skills here.

This repository maintains portable instructions. Skill frontmatter uses only `name` and `description`; host mechanics belong in `adapters/`. Keep descriptions short and specific. Store conditional detail in references, with working relative links.

Read the relevant skill and its callers before changing a workflow. Run `python3 -B scripts/validate.py` after structural changes. For decision-boundary changes, exercise the relevant cases from `evals/scenarios.json` and report what was actually tested. Structural checks do not prove agent behavior.

Name artifacts for domain responsibilities, never local tasks or phases. Read [shared rules](skills/steady/references/rules.md) before introducing names. Inspect new names before committing. Run `python3 -B scripts/validate.py` and `python3 -B -m unittest discover -s scripts -p 'test_*.py'` after structural changes.

Do not add a workflow, principle, or unconditional rule without a concrete decision it improves. Preserve the shared policy's scope and authorization rules.
