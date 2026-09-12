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
