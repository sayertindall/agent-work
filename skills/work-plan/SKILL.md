---
name: work-plan
description: "Prepare a durable work plan with scope, decisions, dependencies, and acceptance criteria when the user requests execution planning."
---

# Prepare a plan

Read [plan format](references/plan-format.md) and use [the template](assets/plan.md) for the relevant fields. Inspect the draft, target project instructions, and affected evidence. Reuse existing requirements rather than restating them inconsistently.

Before the first record edit, establish that you are the single coordinator writing this work repository. If another coordinator owns it, return the proposed update to that owner; do not edit a competing copy.

Define the outcome, exclusions, completion artifact, and checks that demonstrate acceptance. Resolve consequential uncertainties through authorized inspection. Use [architecture](../architecture/SKILL.md), [research](../research/SKILL.md), or [interface](../interface/SKILL.md) only when those questions arise. Do not require every implementation detail to be decided.

Record dependencies and the authorization actually supplied. Readiness is technical; it does not grant execution permission. Keep unresolved product choices or missing acceptance criteria in `drafts/`. When the plan is actionable, move it to `ready/` and update the index as its single writer. Blocked prerequisites may remain declared dependencies, but must be satisfied before execution starts.

Planning alone does not authorize implementation, external messages, or a PR. Report what is ready, what remains undecided, and the intended completion evidence.
