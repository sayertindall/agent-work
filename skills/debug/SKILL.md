---
name: debug
description: "Diagnose a reproducible or difficult failure through causal evidence. Repair only when the user requested a fix."
---

# Debug

Establish expected and observed behavior, the relevant environment, and a reproduction or retained failure trace. Check the failing path and state, including persistence or environment differences where relevant. Avoid assuming that a source change caused a runtime symptom.

Choose an observation that discriminates between plausible causes. Instrument or experiment only within authorization; a read-only diagnosis cannot modify code, clear caches, restart services, or launch writing tools. Record confidence and remaining alternatives.

Before choosing a repair, read the cause guidance selected by the [principle index](../steady/references/principle-index.md). When repeated fixes fail, load its premise guidance before another attempt and test their shared assumption. Once supported, repair the cause if authorized and verify the original case plus meaningful regression behavior. If only a mitigation is feasible, label it. Before retry or proof decisions, read the matching delivery sections from the index unless already in context. Return the cause, evidence, correction if made, and remaining uncertainty.
