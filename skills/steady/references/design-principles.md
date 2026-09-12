# Design principles

Use the principles relevant to an actual decision. They do not mandate a redesign, prototype, or abstraction.

## Simplify the responsibility

Remove redundant decisions and indirection when doing so serves the requested change. A small diff is useful only when it solves the full problem. Preserve useful abstractions even when they have one caller.
## Choose a useful model

Represent states and transitions so contradictory combinations are difficult to construct. Prefer authoritative schemas and types to parallel definitions. Stronger types should prevent a real error, not make ordinary code ceremonial.
## Validate where trust changes

Parse external input before relying on it. Avoid duplicate validation of established invariants, but retain checks for state that can change, untyped boundaries, concurrency, or corrupted persistence. Types do not prove those conditions safe.
## Reduce reader effort

Keep decisions near their owners, derive values instead of synchronizing copies, and limit mutable state. Judge abstraction by the complexity it hides, not a fixed number of files or lines.
## Reconsider the premise

Repeated unsuccessful fixes are a reason to test the assumption they share. Gather a discriminating observation before trying another variation.
## Consider the intended design

Ask how a new requirement changes the underlying model. Improve the relevant boundary without turning a bounded task into an unsolicited rewrite.
## Explore where uncertainty matters

Compare plausible alternatives or build a disposable probe when the decision is costly and evidence can settle it. No fixed number of candidates is required. Read-only work uses existing evidence unless experimentation is separately authorized.
## Design for the consumer

Judge a UI by the user's task, a library by its callers, and a change by its maintainers. Keep explicit requirements; propose scope tradeoffs rather than silently shipping less.
## Isolate mutable ownership

Prefer independent outputs for independent workers. When shared mutation is essential, use enforced serialization or transactions rather than relying on polite instructions.
