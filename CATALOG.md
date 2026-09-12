# Skill catalog

Use one entry point for the actual request. The following are canonical names, not aliases for the legacy pstack collection.

| Skill | Purpose | Boundary |
| --- | --- | --- |
| [steady](skills/steady/SKILL.md) | Proportionate engineering workflow | Skip ordinary questions and trivial edits |
| [work-init](skills/work-init/SKILL.md) | Initialize durable tracking | Only when setup is requested |
| [work-add](skills/work-add/SKILL.md) | Capture an idea | No implementation |
| [work-plan](skills/work-plan/SKILL.md) | Make a durable plan actionable | Readiness does not authorize execution |
| [work-run](skills/work-run/SKILL.md) | Execute an authorized plan | Honor ownership, dependencies, and acceptance |
| [work-status](skills/work-status/SKILL.md) | Report recorded and live work state | No mutation |
| [work-sync](skills/work-sync/SKILL.md) | Reconcile records with evidence | No implicit merge, repair, or deployment |
| [work-retro](skills/work-retro/SKILL.md) | Propose evidence-backed improvements | No automatic policy or memory edits |
| [architecture](skills/architecture/SKILL.md) | Consequential design decisions | No compulsory redesign or implementation |
| [debug](skills/debug/SKILL.md) | Causal diagnosis | Repair only when requested |
| [review](skills/review/SKILL.md) | Bounded artifact assessment | No unsolicited fixes |
| [open-code-review](skills/open-code-review/SKILL.md) | Configured OCR diff review | Preserve diff scope; validate findings and coverage |
| [research](skills/research/SKILL.md) | Attributable external evidence | No automatic report files or installs |
| [interface](skills/interface/SKILL.md) | UI design, implementation, review | Preserve requested mode and project language |
| [writing](skills/writing/SKILL.md) | Writing as a deliverable | Drafting is not sending |
| [security](skills/security/SKILL.md) | Security boundaries and explicit reviews | No unrequested probes or access changes |
| [performance](skills/performance/SKILL.md) | Measured performance work | No unsupported speedup claims |

There are no separately discoverable principle skills, mandatory cleanup skills, or competing HTML routers. Principles are conditional references inside Steady. Interface guidance covers both app work and standalone artifacts without prescribing a visual style. Existing app-specific tools and skills can remain available after the separate migration.
