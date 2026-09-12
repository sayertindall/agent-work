# Working with agents

Use this guide to drive work in Claude Code, Codex, or OMP. Give the agent an outcome, useful context, and clear limits. Steady handles the workflow and selects the skills. You do not need to invoke each step yourself.

This guide describes the workflow in this repository. After updating skills, follow [installation and activation](installation.md) and start a fresh session. Shared policy files are installed separately from the skill links.

## Start a task

Open the target project in your agent. Say what should change, how to check it, and where the agent should stop.

> Add CSV export to the activity table. Preserve the current filters and permissions. Verify the downloaded contents against the visible rows. Open a PR; do not merge or deploy.

For substantive work, expect the agent to inspect the project, locate or create a durable plan, implement the change, verify it, and deliver the requested result. A typo fix needs only the edit and a suitable check.

Add context that would change a decision: the affected screen, a reproduction, a requirement, a relevant file, or an existing plan. You can leave routine implementation choices to the agent.

## Choose the kind of work

These prompts work without host-specific command syntax. Skill names are optional shortcuts.

| You want | Say |
| --- | --- |
| An explanation | “Explain how export permissions work. Read only; no saved report.” |
| A diagnosis | “Find why this export fails after restart. Diagnose only; do not fix it.” |
| A proposal | “Compare approaches for this feature. Recommend one, but do not implement or create files.” |
| A fix | “Reproduce this bug, fix the cause, and verify the original case. Keep changes local.” |
| A review | “Review this branch against its PR base. Report actionable findings; do not fix or post them.” |
| UI work | “Use interface to improve this error state. Keep the design system and verify the interaction.” |
| Writing | “Use writing to simplify this guide for a new contributor. Edit only this file.” |

“Read only” includes incidental writes such as saved reports, caches, and Git metadata. The agent should use existing evidence and explain any checks it cannot perform within that limit.

## Keep plans somewhere predictable

The work directory holds plans and evidence. Source code stays in the project checkout or its worktree.

The agent chooses the work directory in this order:

1. The path you give it.
2. The project's instructions.
3. The configured default, `~/Dev/work` in this setup.

To choose another location:

> Implement this feature using ~/Dev/client-work for tracking. Reuse that work directory if it exists; scaffold missing structure through work-init.

The agent uses the initialization script to inspect and create missing structure. It preserves existing content and reports conflicts. New standalone work roots use Git unless you request directory-only tracking.

A work directory contains:

```text
README.md                    Index of tracked work
plans/drafts/                Ideas and unresolved plans
plans/ready/                 Actionable plans
plans/active/                Work in progress or awaiting acceptance
plans/done/                  Completed work with evidence
plans/discarded/             Cancelled work with a reason
projects/                    Project context
evidence/                    Retained checks and artifacts
```

To save an idea without starting it:

> Use work-add to capture “export audit history” in ~/Dev/work. Leave it as a draft. Do not implement.

To prepare and then execute it:

> Prepare the export audit history draft for execution. Record scope, dependencies, and acceptance criteria. Do not implement yet.

> Execute the ready export audit history plan. Verify its acceptance criteria and open a PR. Do not merge.

A ready plan is technically actionable; it still needs execution authorization. If you already asked for implementation, the agent should carry it through without another permission round for routine steps.

## Steer work while it runs

Send corrections in the same conversation. Name what changes and what remains required.

> Keep the existing API. Change only the internal implementation; the original acceptance criteria still apply.

For status without changing records:

> Use work-status for the export plan. What is complete, what is blocked, and what evidence is missing? Read only.

To reconcile records with results:

> Use work-sync to update the export plan from its actual checks and PR state. Do not change code or merge anything.

Completion depends on the requested outcome. If you asked for a PR, an opened PR can satisfy that delivery requirement. If you asked for a working packaged app, green CI alone cannot establish completion.

## Use workers deliberately

Keep one coordinator responsible for the task and its shared work records. Use workers when bounded assignments can progress independently or a separate assessment is useful.

> Split the API and UI work between two workers if their ownership can be separated. Give each a clear scope and acceptance criteria. You own integration and final verification. Use the configured worker models.

The coordinator supplies each worker with the baseline, owned paths, allowed actions, relevant guidance, and required evidence. Workers return artifacts; the coordinator inspects and integrates them. A worker's “done” message is not verification.

Do not start another coordinator against the same work directory while its owner is active. Separate worktrees isolate source changes; they do not lock a shared plan queue or isolate shared ports and databases.

## Let principles guide decisions

You do not need to select principles manually. The agent reads relevant guidance before consequential decisions and revisits it when the situation changes.

For example, repeated failed fixes should trigger a check of their shared assumption. An uncertain retry should trigger inspection of what already happened. Completion should trigger a check against the actual required behavior.

If a choice is unclear, ask:

> What evidence supports that decision, and which alternative did you rule out?

The [principle index](../skills/steady/references/principle-index.md) supplies the routing. This is instruction-driven loading; it is not a runtime hook that guarantees compliance.

## Review and deliver

For code changes, the workflow uses `git dft` for inspection alongside the configured Open Code Review CLI. The agent checks OCR findings against the source and reports incomplete coverage. Strict no-write or offline requests may require local inspection instead.

A useful handoff tells you what changed, what was checked, what remains uncertain, and where to review the result.

> Finish the implementation, verify it, and open a PR with the relevant evidence. Stop before merge or deployment.

If you want only local changes, say so. Permission to implement does not by itself authorize publishing, deployment, or messages to other people.

## Pause, resume, and learn

To pause with a durable handoff:

> Pause safely. Record the current state, running jobs, uncommitted changes, remaining checks, and next action in the plan. Reconcile workers before handing off.

In a fresh session:

> Resume the export plan in ~/Dev/work. Check its owner, checkout, live jobs, and current evidence before continuing. Keep the recorded authorization limits.

A timed-out status check does not prove the previous worker stopped. Resolve ownership before starting a replacement. Asking an agent to keep working later also requires an available scheduling mechanism; a promise in the conversation is insufficient.

After a difficult task:

> Use work-retro to explain what repeatedly slowed this down and propose the smallest useful correction. Do not edit skills or global instructions yet.

Use the [skill catalog](../CATALOG.md) for exact responsibilities and [shared policy](../policy/AGENTS.md) for scope and authority.
