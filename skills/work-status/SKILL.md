---
name: work-status
description: "Report the current state of tracked plans, dependencies, and recorded delivery artifacts without changing records or external systems."
---

# Read work status

Read [plan format](../work-plan/references/plan-format.md) when interpreting lifecycle state. Inspect only the requested project or queue. Treat plan locations as recorded state and timestamps as freshness clues, not proof.

Check relevant PR, process, or artifact state through read-only tools when available. If live inspection is unavailable or could write in a no-write task, report the recorded state and its date. Distinguish a recorded claim from current observation.

Report active work, actionable ready work, dependency blockers, items awaiting a decision or merge, and stale ownership only where relevant. Cite plan paths and supporting artifacts. Do not repair the index, move files, commit, schedule monitoring, post messages, or dispatch workers. Recommend `work-sync` when reconciliation is needed.
