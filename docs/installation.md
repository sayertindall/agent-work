# Installation and recovery

Agent Work was installed at user level on September 12, 2026. The canonical source is `~/Dev/agent-work`. Project-local skills and configuration were not edited.

## Discovery

| Host | User skill source | Verified result |
| --- | --- | --- |
| Claude Code | `~/.claude/skills` links to the canonical skills directory | Initialization reports exactly 17 user skills |
| Codex | `~/.agents/skills` links to the canonical skills directory | Fresh app-server inventory reports exactly 17 enabled skills and no discovery errors |
| OMP | `~/.agents/skills`, through its native shared-agent provider | Installed discovery loader reports exactly 17 skills and no warnings |

The adjacent `policy` and `adapters` links preserve relative references for hosts that retain alias paths. Codex resolves the canonical paths. Both alias layouts were checked for valid skill references.

Shared policy was installed in each host's global instruction file. Claude's existing preference to show the diff before committing was retained. Model settings and credentials were not changed. OMP automatic skill creation was disabled so it does not regenerate retired managed skills. Native host commands remain available. Codex regenerates built-in system skill files; the archived system skills are explicitly disabled in its user configuration.

These checks validate discovery and configuration. They do not establish full behavioral acceptance across all three models. Existing conversations can retain old context; restart the hosts or begin fresh sessions before using the new workflow.

## Update all three agents

After choosing the revision in the canonical checkout, run this from any directory:

```sh
python3 -B ~/Dev/agent-work/scripts/update_agents.py
```

Check whether synchronization is needed without writing anything:

```sh
python3 -B ~/Dev/agent-work/scripts/update_agents.py --check
```

The script validates the source, synchronizes the three global instruction files, and checks or updates the shared skill, policy, and adapter links. It preserves host-specific text after the managed source pointer and existing file permissions. It backs up changed files and previous link targets under `~/.skills-archive/updates/` and rolls back attempted replacements if a write fails. Repeating a successful update changes nothing and creates no additional backup.

A receipt at `~/.agents/agent-work-install.json` records the installed policy hashes. Local edits inside a managed policy block cause refusal rather than silent replacement. Keep personal preferences after the Installed collection pointer. A matching older installation can be adopted without a receipt; an unknown layout or changed managed text needs reconciliation first. Existing skill directories are never replaced automatically. Updates use a process lock; do not edit instruction files concurrently.

`--source /path/to/agent-work` selects another complete checkout. `--home /path/to/disposable-home` supports isolated tests. `--check` exits 0 when current, 1 when an update is needed, and 2 on invalid source or a conflict. A normal successful update exits 0.

This command synchronizes the selected checkout. It does not fetch, switch branches, merge, install parser dependencies, change models, restore old plugins, alter project hooks, or configure required CI checks. The naming parser setup remains `npm ci --ignore-scripts` in that checkout when dependencies need installation. The original full-stack archive and its `latest` pointer remain untouched.

The shared policy directs agents to Steady's principle index and always-loaded naming rule. All three hosts use the same Markdown references. Start fresh sessions after an update; synchronization does not replace instructions already loaded in an active conversation or establish behavioral acceptance by itself.

## Archive and restore

The archive is `~/.skills-archive/20260912T173619Z`; `~/.skills-archive/latest` points to it. It includes 6,171 regular files, 70 symlinks, plugin packages and install records, relevant settings, and snapshots of external linked skill targets. Twenty skill links were already broken; their missing content could not be recovered and is identified in the manifest.

The original user plugin registries and configuration are recoverable. Claude's explicitly project-local plugin record and supporting cache were retained. Codex user plugin entries were disabled and its old cache retired. OMP's user plugin directory was retired. Conversations, authentication stores, and project files were outside the archive scope. Configuration snapshots are private and should not be published.

Restore the old user-level skills and plugin installation with one command:

```sh
~/.skills-archive/latest/restore.sh
```

The command verifies archived hashes, permissions, and link targets before restoring. It preserves the displaced current installation under the archive, then restores the original directories and settings. Existing external symlink targets are never overwritten. Restart all three hosts afterward.

Verify the archive without restoring it:

```sh
~/.skills-archive/latest/restore.sh --verify
```

Both a synthetic migration and a restoration of the real archive into an isolated temporary home passed. Recovery requires no download or fresh plugin installation. The retained packages restore their archived versions.
