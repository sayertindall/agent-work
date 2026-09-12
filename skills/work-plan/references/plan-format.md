# Durable plan format

This format is used only for managed work. Do not read all project plans or history to execute one bounded task.

## Location and identity

Use the chosen work repository with `plans/{drafts,ready,active,done,discarded}/`. Each plan is one Markdown file named `<area>-<slug>.md`; choose a collision-free name and keep its ID stable through moves. The directory is the lifecycle state. The README links plans but cannot override their state. Project context lives in `projects/<project>/context.md`; evidence goes under `evidence/<plan-id>/` when a retained artifact is useful. External evidence can be linked without copying it.

## Fields

Use [the template](../assets/plan.md). A draft may be incomplete. A ready plan identifies its target repository, outcome, scope, acceptance, decisions or safe assumptions, dependencies, completion artifact, and authorization boundary. Links to authoritative requirements can replace duplicated content.

An active plan additionally records its owner, host, session handle if available, checkout, branch/base revision, and next action. Evidence entries identify the command or observation, date, artifact/revision checked, result, and material limitations. Do not put credentials in plans.

## Transitions

| Transition | Required evidence or authority |
| --- | --- |
| New to drafts | User asked to capture or plan work |
| Drafts to ready | Actionable outcome, scope, acceptance, and consequential decisions |
| Ready to active | Execution authorized, dependencies satisfied, exclusive owner and workspace established |
| Active remains active | Review, merge, verification, or external prerequisite still outstanding; record blocker and next action |
| Active to ready | Execution safely suspended for reassignment, no unreconciled worker, ownership released |
| Active to drafts | New information invalidates the plan; preserve work and record the unresolved decision |
| Active to done | Every completion criterion has matching evidence at the relevant final state |
| Any unfinished state to discarded | User cancels, or previously authorized cancellation criteria are met; retain reason and evidence |

Do not mark an unfinished implementation done merely because a worker stopped, a PR opened, or CI passed. A merge is required only when specified; a report can finish without a PR. Corrections to a done plan retain prior evidence and explain the change rather than erasing the historical outcome.

## Ownership and recovery

One coordinator writes each work repository. Workers return isolated artifacts. Do not launch two coordinators against separate clones of the same shared plan repository and assume Git prevents duplicate claims. Multiple concurrent coordinators are unsupported without a separately implemented authoritative claim service.

Before moving a plan, verify its current location and state. If a previous attempt already completed the move, reconcile the record and index rather than create another copy. Stop on conflicting copies or owners and resolve the actual state. Record owner release or transfer explicitly. Read-only status never repairs records.

Update the index after the authoritative plan. If interrupted, rebuild the index from the plan locations. Commit work records at meaningful checkpoints only when authorized; do not commit after every observation or publish implicitly.
