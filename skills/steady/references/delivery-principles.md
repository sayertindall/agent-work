# Delivery principles

- **Prove the outcome.** Choose evidence that observes the required behavior. A build proves buildability; a mock proves a bounded contract; neither alone proves the deployed user path. Identify each missing acceptance surface.
- **Test behavior.** Prefer checks through the public interface and meaningful negative cases. Avoid tests that assert only their own fixtures or mirror implementation details. Use a fault probe when test sensitivity is uncertain and the experiment is safe.
- **Repair the cause.** Reproduce or retain existing failure evidence, test a causal explanation, and verify the fix. A mitigation can be appropriate during an incident, but label it and retain the unresolved cause.
- **Sequence useful checkpoints.** Verify cohesive increments where a failure would change the next decision. Do not rerun every global suite after every mechanical edit. Respect required project gates and run integrated checks at the final relevant state.
- **Converge on the requested end state.** A planned local migration may have temporary breakage. Never treat it as completed or allow it into a shared release unintentionally. Preserve compatibility required by external users or deployment order.
- **Retire superseded paths deliberately.** Migrate owned callers and remove obsolete paths when scope and compatibility permit. Keep a documented removal condition for genuinely necessary adapters.
- **Make retries safe.** Before repeating a mutation, inspect its actual result. Reconcile partial completion; use existing idempotency keys or transactions. Never infer that a timeout means nothing happened.
- **Automate repeated proof.** Build a small reusable check or transformation when it reduces repeated work or makes a fragile operation reliable. A one-off edit need not produce a new tool.
- **Keep context selective.** Read relevant references and summarize large evidence with pointers. A handoff should preserve decisions, current state, and the next action rather than duplicate a transcript.
- **Improve from evidence.** Prefer eliminating a recurring failure in the responsible code, validator, or template. Propose skill changes when judgment guidance is the right layer. Do not autonomously harden every lesson into a global rule.
