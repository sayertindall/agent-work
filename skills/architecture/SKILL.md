---
name: architecture
description: "Resolve consequential decisions about system boundaries, contracts, and data models when designing or changing a system."
---

# Architecture

Inspect the affected consumers, authoritative schemas, compatibility constraints, and relevant project conventions. Define the behavior and invariants the design must preserve.

Compare alternatives only where the choice is unsettled and meaningful. Evaluate consumer experience, maintainability, failure modes, and migration cost. Use a bounded prototype when evidence would settle a consequential question and writes are authorized. Read [design principles](../steady/references/design-principles.md) when weighing structure.

Specify ownership, inputs/outputs, state transitions, errors, and integration boundaries at the detail needed for implementation. Retain compatibility when external users or deployment sequencing require it. Identify the verification path and any unresolved decision. A design request ends with a proposal; implementation requires its own authorization.
