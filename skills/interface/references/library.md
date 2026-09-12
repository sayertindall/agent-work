# Interface library

These are conditional references beneath Interface, not additional globally discovered skills. Read only the guides relevant to the requested work. A request naming one of these skills selects its guide directly through this table; no installation or extra invocation is needed. Names mentioned inside a guide refer to this same table.

| Guide | Use when |
| --- | --- |
| [design-taste](library/design-taste/GUIDE.md) | Establishing a visual direction, redesigning, or polishing a generic interface; includes all five original reference files |
| [better-accessibility](library/jakubkrehel/better-accessibility/GUIDE.md) | Semantics, keyboard, focus, forms, screen readers, motion preferences |
| [better-colors](library/jakubkrehel/better-colors/GUIDE.md) | Palettes, semantic tokens, measured contrast |
| [better-layout](library/jakubkrehel/better-layout/GUIDE.md) | Grouping, alignment, density, responsive layout |
| [better-typography](library/jakubkrehel/better-typography/GUIDE.md) | Type selection, sizing, wrapping, font features |
| [better-ui](library/jakubkrehel/better-ui/GUIDE.md) | Surfaces, icons, optical alignment, motion, polish |
| [better-writing](library/jakubkrehel/better-writing/GUIDE.md) | Product copy, labels, errors, localization |
| [better-interface](library/jakubkrehel/better-interface/GUIDE.md) | A requested review across the interface disciplines |
| [interface-review](library/jakubkrehel/interface-review/GUIDE.md) | Changes to UI in a working copy, commit, branch, or pull request |
| [explain-interface](library/jakubkrehel/explain-interface/GUIDE.md) | Explaining a site's implementation or reconstructing an effect from an image |
| [variant](library/jakubkrehel/variant/GUIDE.md) | Requested alternatives and an interactive comparison |
| [break](library/jakubkrehel/break/GUIDE.md) | Requested component stress testing with realistic states and content |

## Apply within the shared workflow

The shared policy and Interface contract govern these imported references. Upstream frontmatter is provenance, not a second skill loader. Resolve named guides here automatically; do not ask the user to run another skill. Broad reviews use the relevant disciplines; narrow changes do not load every guide.

Preserve requested scope, project design systems, and existing authorization. Treat aesthetic bans, intensity dials, exact motion recipes, and fixed pass counts as design guidance where applicable, not universal constraints. Critique and refine meaningful visual work without manufacturing extra iterations for a trivial edit. Accessibility requirements take precedence over taste.

Use the actual applicable accessibility standard when a source makes a compliance claim. In particular, the old design-taste large-text threshold confuses points and pixels: 18pt is 24 CSS px, and 14pt bold is approximately 18.67 CSS px. Its 18px/14px thresholds must not be used to claim the lower contrast requirement. See [WCAG contrast guidance](https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html).

Report the requested coverage without arbitrary caps on findings or consumers, and do not silently narrow a broad assignment. Use `git dft` for inspection and OCR alongside it where the shared review contract applies. Strict no-write requests exclude fetches, scratch pages, saved screenshots, and service startup. Authorized fixes and runtime verification do not require a new permission question merely because a source says to stop or look once.

Variants and stress-test pages require a request that authorizes those artifacts. Retain their deliverables as requested; cleanup must preserve user and concurrent work. Keep explicit user choices, such as selecting a variant, with the user.

The full upstream text and supporting files are preserved in the library. Source revision, archive origin, and file hashes are recorded in `library/manifest.json`; Jakub Krehel's MIT notice is retained in `library/jakubkrehel/LICENSE`.
