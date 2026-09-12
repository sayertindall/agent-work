# Claude Code

At installation, inspect the active global `CLAUDE.md`, project instructions, skills inventory, and enabled plugin hooks. The audited local skill directory is `~/.claude/skills`; some entries link to `~/.agents/skills`. Resolve real paths before changing links. The existing pstack startup hook can override the intended lightweight entry behavior until it is explicitly retired during migration.

Use Claude's native skill invocation when available. When invoked from a file pointer, read the canonical `SKILL.md` and its selected references. Shared skill text does not require Claude-only metadata.

Use the live native agent/delegation tool for authorized workers. Inspect its available types and schema before dispatch. Choose configured models and permission modes rather than embedding them in shared prose. Give concurrent writers isolated worktrees or clones and ensure their permission mode does not exceed the assignment.

Use available read/search/edit/shell tools directly for ordinary work. Use the current browser or native-app capability for UI verification. Do not assume that a built-in skill called `run` or `verify` exists.

Recurring continuation requires an explicitly available scheduler and user authorization. A background worker is not an indefinite monitor. Inspect its real state before resuming or replacing it.

Activation acceptance: one canonical entry per skill, no competing legacy pstack startup mandate, global policy reconciled, relative references resolved, and the shared evaluation cases exercised in a fresh session. Those live checks are deferred until installation.
