# Agent Work

One workflow and skill collection for Claude Code, Codex, and OMP. Small tasks stay small. Substantial work gets explicit outcomes, relevant investigation, and evidence of completion. Substantive authorized work uses durable plans, driven by the agent.

## Start here

- [Shared policy](policy/AGENTS.md) defines scope, authorization, and completion.
- [Steady](skills/steady/SKILL.md) selects a workflow when one is useful.
- [Catalog](CATALOG.md) lists the seventeen skills and their boundaries.
- [Host setup](adapters/README.md) explains how to expose the same source in each host.
- [Validation](docs/validation.md) separates structural checks, scenario evaluation, and live-host acceptance.

The collection is installed at user level in Claude Code, Codex, and OMP. Old user skills and plugin packages are archived under `~/.skills-archive/20260912T173619Z`, with a verified one-command restore. Project-local files were not changed. See [installation and recovery](docs/installation.md).

## Examples

Say `Implement this export and verify it in the app`; the agent drives Steady, including its plan lifecycle. Say `Use work-add to capture this idea` to save a draft without implementing it. Use `work-plan` to prepare it, `work-run` to execute authorized work, `work-status` for a read-only report, and `work-sync` to reconcile completion.

Steady is the required workflow for substantive work. The agent selects the lane and invokes its work skills automatically; manual skill calls remain useful shortcuts. Simple answers and self-evident small edits stay proportionate. Informational and read-only requests create no plan files.

## Choose a work directory

`work-init` accepts any explicit location. Otherwise the agent uses the project's documented location, then the configured default (`~/Dev/work` for this setup). That default can be changed during installation; it has not been created by this build. To inspect or scaffold one after selecting its path:

```sh
python3 -B skills/work-init/scripts/init_work.py /path/to/work --check
python3 -B skills/work-init/scripts/init_work.py /path/to/work
```

Run these commands from this repository. The first is read-only; the second creates only missing structure and preserves existing content. Add `--git` to the second command when a local Git repository is wanted. It reuses an existing owning repository instead of nesting another one. Nothing installs skills, commits, or publishes.

## Repository layout

```text
policy/       Shared global policy, installed separately from skills
skills/       Canonical skill folders and conditional references
adapters/     Host mechanics and setup guidance
docs/         Design rationale, validation, and migration guidance
evals/        Portable requests and expected behavior
scripts/      Read-only collection validator
```

This repository contains reusable instructions. Actual project plans belong in a separate work repository chosen by the user. No background service, database, auto-learning hook, model router, or scheduler is required.

Use Python 3.9 or newer. Run `python3 -B scripts/validate.py` from this repository. The command reads the collection and reports structural failures without changing files. It does not claim that any host has loaded the skills.

See [sources and adaptations](docs/sources.md) for the ideas retained from pstack and the two articles.
