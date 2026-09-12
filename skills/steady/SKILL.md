---
name: steady
description: "Choose and complete a proportionate workflow for substantial engineering work, or when the user asks for Steady mode. Skip ordinary questions and trivial edits."
---

# Steady

Establish the requested outcome, scope, and evidence of completion. Read only enough context to choose the next useful action. Carry authorized work through verification and repair. These are responsibilities, not a mandatory visible checklist.

The [shared policy](../../policy/AGENTS.md) governs this collection; read it if it is not already supplied in the session. Honor stricter task boundaries and host instructions. The agent drives this workflow automatically. A clearly selected specialist can serve the matching lane without rereading this router when it is already in context.

Apply the shared naming rule even on small edits. Read [rules](references/rules.md) before introducing or reviewing names or resolving code-quality findings, unless already in context.

## Choose the lane

Read only the matching reference:

| Request | Lane |
| --- | --- |
| Explain, investigate, diagnose, audit | [Investigate](references/investigate.md) |
| Propose an approach or design | [Plan](references/plan.md) |
| Implement, refactor, or migrate | [Implement](references/implement.md) |
| Fix a reported failure | [Repair](references/repair.md) |
| Assess existing work | [Review](references/review.md) |
| Release or change an operational system | [Operate](references/operate.md) |

For substantive authorized changes or multi-session execution, locate the work directory using the shared policy's precedence. Use [work-init](../work-init/SKILL.md) to check it and scaffold missing structure through its script. Create or resume an actionable plan with [work-plan](../work-plan/SKILL.md), execute with [work-run](../work-run/SKILL.md), and reconcile with [work-sync](../work-sync/SKILL.md). Do not wait for the user to invoke each skill. Record clear existing decisions directly; do not invent an interview or approval gate for an actionable task.

Simple answers and self-evident small edits need no durable records. Informational, proposal-only, and no-write tasks stay within their requested mode; the required workflow never authorizes record creation against those boundaries.

## Apply judgment

Keep the required plan proportionate to the work. Add sequencing detail when it helps; do not duplicate the durable record in a ceremonial visible checklist. Investigate before choosing a fix. Explore alternatives when a consequential decision remains open, not every time a function boundary is crossed. Use a script when repetition or reproducibility warrants it. Avoid introducing infrastructure merely to satisfy a workflow.

Before a consequential choice, consult the [principle index](references/principle-index.md) and read the selected sections before acting. Apply the same routing when entering a specialist directly. Revisit selection when evidence changes, repeated fixes fail, work becomes concurrent, or retry and completion decisions arise. Guidance already read in the current context need not be reread unless it changes. Principles inform choices; they are not separate skills or required citations.

Delegation is optional. Read [coordination](references/coordination.md) only when using workers or handing off. Keep scope and authorization with the coordinating agent.

Finish against the original outcome. Report the result, meaningful checks, and remaining limitations. If acceptance is unmet and progress remains possible, continue.
