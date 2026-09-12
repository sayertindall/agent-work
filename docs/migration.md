# Backup and activation: next stage

Building this repository does not activate it. Do not run this procedure unless the user has requested the backup and installation stage. No existing skill, plugin, hook, global policy, or memory should be changed as a side effect of validating this repository.

## Establish the actual installation

Inventory all active discovery roots, enabled workflow plugins, startup hooks, global instruction files, configured home overrides, and linked targets for Claude, Codex, and OMP. Inspect live inventories where available. Separate custom workflow skills from application capabilities and vendor-managed system skills.

Create a dated backup outside the discovery roots. Preserve file content, permissions, symlink targets, enabled-plugin state, relevant configuration, and a manifest mapping originals to backups. Back up the canonical content of linked custom skills as well as their link metadata. Do not bundle unrelated credentials, conversation histories, or databases into a skills backup.

Verify the backup by reading selected originals and retained copies and comparing content hashes across the full selected write set. Record missing targets separately; an archive containing only a broken link cannot restore its former content. Keep enough information to restore exact paths and enabled state.

## Reconcile and expose

Review the exact replacement set. Retire overlapping legacy workflow triggers and the old pstack startup mandate for the selected hosts. Preserve app-specific capabilities and useful project instructions. Reconcile genuine global preferences into the shared policy without restoring the conflicts identified in the audit.

Choose one discovery route per host using [the adapters](../adapters/README.md). Preserve the repository layout for cross-skill references. Do not install into every known root. Update only the reviewed paths; record each change for rollback. Restart or open a fresh session when necessary to refresh discovery.

## Accept or restore

Inspect each host's actual inventory and loaded global rules. Run the shared behavioral cases, particularly no-write, authorization, full completion, and handoff. Mark acceptance separately for Claude, Codex, and OMP. If one fails, correct its adapter or restore that host's backup; do not claim universal activation.

Keep verified backups through the migration. Ordinary operation after acceptance should use this repository and native app capabilities, not the backup directories. The user decides when old backups can be removed.
