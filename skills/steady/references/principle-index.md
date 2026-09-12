# Principle selection

Use this index before a consequential decision, including when entering a specialist directly. Match the situation, then read the linked section before the action it informs. The index is a routing map, not a substitute for the definition. Read only applicable sections; do not preload the library or require every principle on every task. If no trigger fits, continue without adding a principle step.

| Situation, before acting | Guidance to read | Decision it informs |
| --- | --- | --- |
| Choosing a state model or integrating a requirement | [Useful model](design-principles.md#choose-a-useful-model), [intended design](design-principles.md#consider-the-intended-design) | Represent valid states and change the relevant boundary. |
| Choosing an abstraction or reviewing maintainability | [Simplify responsibility](design-principles.md#simplify-the-responsibility), [reader effort](design-principles.md#reduce-reader-effort) | Keep a boundary only when it hides useful complexity. |
| Placing validation or handling changing state | [Trust changes](design-principles.md#validate-where-trust-changes) | Validate where the invariant actually needs protection. |
| Comparing an unsettled consequential design | [Uncertainty](design-principles.md#explore-where-uncertainty-matters), [consumer](design-principles.md#design-for-the-consumer) | Choose proportionate evidence and preserve requirements. |
| Diagnosing a failure; repeated fixes share an assumption | [Repair the cause](delivery-principles.md#repair-the-cause); on repetition, [reconsider the premise](design-principles.md#reconsider-the-premise) | Test the causal explanation before another fix. |
| Introducing concurrent writers or handing off | [Mutable ownership](design-principles.md#isolate-mutable-ownership), [coordination](coordination.md) | Separate outputs and reconcile live ownership. |
| Designing initialization or repeating an uncertain mutation | [Safe retries](delivery-principles.md#make-retries-safe) | Inspect actual state and reconcile partial completion. |
| Sequencing a migration or removing an old path | [Checkpoints](delivery-principles.md#sequence-useful-checkpoints), [end state](delivery-principles.md#converge-on-the-requested-end-state), [retirement](delivery-principles.md#retire-superseded-paths-deliberately) | Select verifiable units and preserve required compatibility. |
| Choosing tests or declaring completion | [Behavior tests](delivery-principles.md#test-behavior), [outcome proof](delivery-principles.md#prove-the-outcome) | Observe the required behavior and expose missing acceptance. |
| Repeated manual work or fragile verification | [Reusable proof](delivery-principles.md#automate-repeated-proof) | Build a small tool only when it earns its cost. |
| Large evidence or a context handoff | [Selective context](delivery-principles.md#keep-context-selective) | Preserve useful state and evidence pointers. |
| Proposing a correction for a recurring failure | [Improve from evidence](delivery-principles.md#improve-from-evidence) | Choose code, checks, templates, or judgment guidance. |

Reevaluate at these events, not after every tool call. If the relevant guidance is already in current context, use it; after compaction or transfer, reread what is missing. New evidence can make another principle relevant midway through execution.

When delegating, include the applicable reference paths and section names with the assignment. Workers read those sections before their affected decisions; they do not assume the parent's loaded context is inherited. They select additional guidance if their evidence changes. The coordinator retains scope and integration responsibility.

Record a consequential choice and its evidence in the existing plan when managed tracking applies. Do not create a separate principle log or plan for read-only, proposal-only, or trivial work. Mention a principle in the handoff only when it explains a material decision, and only if its definition was read. Report the choice and evidence, not a checklist of principle names.

These are instruction-driven reads, not host hooks or guaranteed runtime injection. User scope, project constraints, and host permissions govern every suggested action. For read-only work, use available evidence and explain uncertainty; a principle never authorizes a probe, file, external action, or worker by itself.
