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

## Activating principle routing after review

The shared policy source directs agents to Steady's principle index. Specialist skills also route at relevant decisions, including direct entry without the router. All three hosts use the same Markdown references; no host hook, model setting, or new discoverable skill is needed. This is instruction-driven loading, whose timing requires behavioral evaluation.

Development in an isolated worktree does not update the installed skills. After review and a separately authorized merge/installation, update the canonical checkout and synchronize `policy/AGENTS.md` into each host's installed global instruction file, preserving host-specific preferences and the canonical source pointer. Those policy files are copies, so a Git update alone does not refresh them. The existing skill links then expose the canonical references. Begin fresh sessions and verify selective loading in each host before claiming cross-host behavioral acceptance.

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
