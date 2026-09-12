---
name: work-sync
description: "Reconcile durable plan records with observed delivery results when the user requests synchronization or an authorized execution reaches a checkpoint."
---

# Reconcile outcomes

Read [plan format](../work-plan/references/plan-format.md). As the single work-repository writer, compare the selected plan's requirements with its actual artifacts and current relevant state. If another owner is active, return evidence to that owner rather than modify shared records.

Before changing completion state, read [outcome proof](../steady/references/delivery-principles.md#prove-the-outcome), unless already in context. For each acceptance criterion, identify evidence at the revision or environment it describes. Verify recorded PRs belong to the planned work; merge status alone does not prove scope or behavior. Preserve failed checks and unverified requirements.

Move `active/` to `done/` only when every required criterion is evidenced. Otherwise retain `active/`, record the blocker or remaining work, and update the next action. Use other transitions only under their documented conditions. A closed unmerged PR does not automatically cancel a plan.

Update the README index from authoritative plan locations. Repeated sync should not duplicate records or evidence. Do not change product code, merge PRs, redeploy, dispatch, or expand authorization as part of synchronization. Report what changed and why.
