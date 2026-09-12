---
name: work-init
description: "Inspect, reuse, or scaffold the selected work directory before managed execution or when work tracking setup is requested."
---

# Initialize work tracking

Read [plan format](../work-plan/references/plan-format.md). Resolve the location from the explicit request, project instructions, then the configured default in the [shared policy](../../policy/AGENTS.md). Ask only if that resolution leaves a material conflict. Do not infer that this skills repository should hold project plans.

Use [the scaffold script](scripts/init_work.py) for filesystem operations. Resolve its location from this skill's canonical directory. Given a selected target:

```sh
python3 -B /path/to/agent-work/skills/work-init/scripts/init_work.py /path/to/work --check
python3 -B /path/to/agent-work/skills/work-init/scripts/init_work.py /path/to/work
```

`--check` inspects without creating or changing anything. The normal command reuses existing content and creates only missing structure. It preserves existing README and plan bytes, refuses conflicting files or internal symlinks, and reports the canonical work path. Do not run the normal command during a read-only task.

Add `--git` for a new standalone work root under the shared policy, or when Git setup is explicitly requested. Omit it for directory-only tracking. It initializes a local repository if needed, or reuses an existing owning repository. It does not create remotes, commit, or publish. The check and Git flags are mutually exclusive.

Before initialization can mutate state, read [safe retries](../steady/references/delivery-principles.md#make-retries-safe); reuse it if already in context. Before mutation, inspect existing plan layout and establish that no other coordinator is writing this work directory. A different legacy layout needs an explicit migration decision; do not create a parallel queue silently. The script is repeatable initialization, not a distributed claim lock. Resolve reported conflicts rather than delete or replace them. Do not manually work around refusal by overwriting user content.

After scaffolding, run `--check` and report the actual location and Git result if requested. Existing content stays authoritative; index maintenance and plan creation belong to the other work skills.
