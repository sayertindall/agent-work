# Retained lifecycle evidence

This disposable exercise was run by a Luna worker at maximum reasoning on September 12, 2026. Original workspace: `/tmp/agent-work-validation.Ve4PmT`.

The author inspected the done plan and command reference, reran the fixture, compared baseline/final command outputs, and compared the retained hash pairs. Repeat init, repeat sync, and read-only status preserved the non-Git files at their respective checkpoints. The manifests retain original absolute paths as historical evidence; the relevant fixture, plan, and outputs are copied here for inspection.

Run `python3 -B fixture/cli.py --help` from this directory to inspect the retained input. The example is an evaluation fixture, not a live project plan.

The eight decision simulations are recorded in [the decision report](evidence/decision-simulation.md). They are decision simulations, not executed live-host acceptance tests. The lifecycle applied the Markdown procedures directly before the deterministic init script was added; script behavior is covered separately by its executable tests.
