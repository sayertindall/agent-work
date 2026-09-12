# Sources and adaptations

This is an independently written collection informed by:

- OpenAI, [Rethinking skills and prompts for GPT-6 Astra](https://developers.openai.com/blog/rethinking-skills-and-prompts-for-gpt-6-astra), September 11, 2026. Applied narrow triggers, conditional context, proportional procedures, and explicit completion.
- Fatih Arslan, [How I manage my agents](https://arslan.io/2026/09/11/how-i-manage-my-agents/), September 11, 2026. Adapted durable plan lifecycle, coordinator continuity, and evidence-backed retrospectives. Did not copy a supplied skill implementation; the article publishes no downloadable collection.
- The locally installed open-pstack pstack 1.4.1 Poteto router and principle skills. Reviewed their design and delivery principles, then rewrote a smaller set of conditional guidance. No pstack scripts, provider launcher, agent definitions, or source skill text are vendored.
- The user's read-only audit of Claude, Codex, OMP, and shared skill installations in this conversation. Addressed conflicting authorization, duplicate routing, host drift, excessive trigger breadth, and stale references.

## Principle mapping

| Prior ideas | New home and adjustment |
| --- | --- |
| Laziness, subtraction, reader load | Design principles; simplify relevant responsibilities without arbitrary line or layer limits |
| Foundations, domain modeling, types, boundaries | Design principles; protect real invariants without unconditional trust in mutable runtime state |
| Premise testing, root causes | Design and delivery principles; use discriminating evidence and distinguish mitigation |
| First-principles redesign, design exploration, experience | Design principles; proportional exploration and preserved user scope |
| Idempotency, ownership isolation | Delivery principles and coordination; reconcile partial mutations and isolate writers |
| Migration, outcome focus, verifiable units | Delivery principles; preserve required compatibility and verify coherent increments |
| Behavioral tests, real proof, reusable tools | Delivery principles; meaningful checks without universal script creation |
| Context management, autonomy, structural learning | Shared policy and delivery principles; selective reads, scoped authority, requested retrospectives |

No claim is made that this collection matches every behavior of upstream Poteto or replaces app-specific skills. It is intentionally an owned workflow with a smaller contract.

## Open Code Review integration

The [Open Code Review CLI](https://github.com/alibaba/open-code-review) and the user's project-local skill informed the new, independently rewritten CLI instructions. The source skill identifies Alibaba as author, version 1.0.0, and Apache-2.0 as its license. No source prose or implementation is vendored. The replacement uses the installed CLI and configuration, corrects staged-only scope assumptions, and treats partial coverage separately from successful process exit. CLI flags were checked against installed v1.12.0.

## Interface library

All eleven skills from [Jakub Krehel's collection](https://github.com/jakubkrehel/skills) at commit `267330e1adfc66a718fb65fa6918c1f06d0a689e` are included beneath Interface, together with the user's archived design-taste skill and its five references. Original guidance and upstream MIT attribution are preserved. Skill entrypoints become `GUIDE.md` so hosts do not discover duplicates; two documented link repairs fix a renamed entrypoint and identify a pre-existing missing brand reference. The [library router](../skills/interface/references/library.md) defines scope, permission, reporting, and design-system precedence. The source clone is at `~/Dev/agent-work-sources/jakubkrehel-skills`; updating it does not silently change the pinned installed copy.
