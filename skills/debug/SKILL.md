---
name: debug
description: "Diagnose a reproducible or difficult failure through causal evidence. Repair only when the user requested a fix."
---

# Debug

Establish expected and observed behavior, the relevant environment, and a reproduction or retained failure trace. Check the failing path and state, including persistence or environment differences where relevant. Avoid assuming that a source change caused a runtime symptom.

Choose an observation that discriminates between plausible causes. Instrument or experiment only within authorization; a read-only diagnosis cannot modify code, clear caches, restart services, or launch writing tools. Record confidence and remaining alternatives.

When repeated fixes fail, test their shared premise. Once supported, repair the cause if authorized and verify the original case plus meaningful regression behavior. If only a mitigation is feasible, label it. Read [delivery principles](../steady/references/delivery-principles.md) for retry or proof decisions. Return the cause, evidence, correction if made, and remaining uncertainty.
