# Coordination and handoff

Use one coordinating agent for an active plan and one writer for the shared work repository. A second coordinator must use a distinct work repository until enforced shared ownership is implemented. Git commits and Markdown owner fields are not locks.

Delegate a bounded task only when independent work can progress or an independent assessment is useful. Check the live host tools, available roles, and session restrictions. Read the matching [host adapter](../../../adapters/README.md) when mechanics are needed. Keep ordinary work in the current session when delegation is unavailable or uneconomical. If independent review is required but unavailable, record the unmet gate.

Give each worker the outcome, exact repository and baseline, owned paths, allowed actions, acceptance criteria, and a return format: artifact locations, observed checks, unresolved concerns. Include applicable [principle references](principle-index.md) and section names; workers read the definitions before affected decisions and revisit selection when evidence changes. Do not assume parent context transfers. Tell workers they are not alone and must preserve others' changes. Concurrent writers get separate worktrees or clones and unique outputs. Isolate runtime state too when sockets, ports, databases, or caches could collide.

Workers complete their assignment directly; nested delegation requires an explicit coordinating assignment. Workers return evidence to the coordinator rather than editing the shared plan index. Model and effort selection follows current host configuration or explicit user instruction.

Inspect returned artifacts, reconcile contracts, integrate changes, and run checks on the integrated state. Do not accept a completion message as proof. A reviewer assesses the actual artifact and relevant baseline, with enough context to know the requirements but without being coached toward the desired verdict.

On pause or handoff, record the plan, baseline and dirty state, owner/session handle, completed checks, unresolved issues, next action, and authorization boundaries. Reconcile any running workers before transfer. A replacement agent checks current Git/process state before resuming. Do not restart a job merely because a status observation timed out.

Scheduled continuation requires explicit authorization and a supported scheduler. Save the outcome and stopping condition; notify on meaningful changes. Do not promise to watch something after the session ends without an actual scheduled mechanism.

If the prior owner is unreachable, inspect the recorded session/job and checkout. Transfer only after its work is confirmed stopped or the user explicitly authorizes a takeover that safely terminates or fences the old writer. A stale timestamp, unavailable status service, or timeout is insufficient. Preserve uncommitted artifacts and record the new owner before resuming. If liveness cannot be established, leave the claim unresolved and continue unrelated work.
