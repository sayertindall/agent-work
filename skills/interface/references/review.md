# Interface review

Resolve whether the subject is a screen, flow, prototype, or code change. For a change, identify the baseline and distinguish introduced defects from existing issues. Inspect only the requested scope and relevant affected surfaces.

Review the user's ability to complete the task, information hierarchy, interaction feedback, error recovery, accessibility, layout, typography, color, and motion as applicable. Do not load a separate manual for every visual property. Respect deliberate project choices unless they cause an evidenced problem.

Use the actual app when read-only interaction is safe and permitted. Do not submit forms, alter records, start services, or create screenshots on disk under a strict no-write instruction. Source-only review is useful but cannot prove rendered behavior.

Return prioritized findings with the affected state, user consequence, and evidence. Aesthetic alternatives are suggestions, not defects. Do not cap findings arbitrarily or silently narrow the requested coverage; identify any uninspected surface.

For a requested cross-discipline review, use better-interface and its domain references through the [interface library](library.md). For a UI diff, start with interface-review for scope and removed behavior, then assess the applicable disciplines. The library integration rules preserve this review contract.
