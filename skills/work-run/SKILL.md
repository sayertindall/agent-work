---
name: work-run
description: "Execute an authorized durable plan, including scoped delegation, verification, and handoff. A ready plan alone is not execution authorization."
---

# Execute managed work

Read [plan format](../work-plan/references/plan-format.md). Load the selected plan, relevant project context, and actual repository state. Confirm acceptance criteria, dependencies, authorization, and exclusive ownership. Resolve existing workers before starting replacements. Do not take over another active owner's work from a stale record alone.

As the single coordinator, establish a branch/worktree or clone appropriate to the task, record ownership, and move the plan to `active/`. Preserve unrelated dirt. Use [Steady](../steady/SKILL.md) for the task lane, or enter the already selected specialist directly. Read [coordination](../steady/references/coordination.md) when delegating or handing off.

Before concurrent work, retries, or a changed design decision, revisit the [principle index](../steady/references/principle-index.md) and read the applicable guidance before acting. Include relevant reference paths and section names in worker assignments; workers read them themselves.

Apply [naming and code quality rules](../steady/references/rules.md) before introducing artifacts. Before commit and completion, inspect new names in the actual change and report unresolved naming issues or review-coverage limits.

Execute to the plan's full acceptance criteria. Keep decisions and evidence in the plan at meaningful checkpoints, not after every tool call. If new evidence invalidates scope or design, record it and resolve the decision rather than implement the wrong plan. Continue independent authorized work while a real blocker remains.

Before selecting final checks or declaring completion, read [outcome proof](../steady/references/delivery-principles.md#prove-the-outcome) and, when tests are involved, [behavior tests](../steady/references/delivery-principles.md#test-behavior), unless already in context. Inspect artifacts and run relevant checks on the integrated result. A worker's success, opened PR, or green CI is not the plan's completion by itself. Use [work-sync](../work-sync/SKILL.md) to reconcile evidence and state. If the outcome requires a merge or operational result outside current authorization, prepare the concrete result and ask only for that remaining action.

On interruption, preserve the next action, owner/session, live jobs, dirty state, evidence, and boundaries. On resumption, recheck actual state. Report what is complete and what acceptance remains.
