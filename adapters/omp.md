# OMP

At installation, inspect `~/.omp/agent/config.yml`, the active global `AGENTS.md`, and OMP's actual skill inventory. The audited setup has native skills, managed skills, and an installed `list_skills` extension that reports the session's loaded inventory after deduplication and filtering. Prefer that live inventory to a filesystem count. Do not assume native skills are the only discovery source.

Use the live skill-loading mechanism, or read a canonical skill path. Do not copy a Claude or Codex invocation schema into OMP.

For delegation, inspect the current `task` tool's agent inventory and schema. Select roles that exist now. If batch tasks or isolated workspaces are exposed, use them when appropriate and inspect returned metadata to learn where the work actually ran. Otherwise manage isolated checkouts explicitly. Do not rely on old fixed agent names, effort spellings, or model IDs.

Workers return artifact paths, checks, and unresolved concerns. The root coordinator verifies and integrates. Use current job-control tools to observe or resume a live worker. Do not infer failure from a missing notification or timeout.

OMP's global policy currently has per-action authorization rules that conflict with task completion. Reconcile those during installation; adding skills alone does not remove the conflict. Preserve required project-specific constraints and the user's model-role configuration.

Activation acceptance: inspect the loaded inventory in a fresh session, resolve canonical references, check the reconciled policy, and exercise shared cases. Do not launch OMP solely to inspect skills during a no-write audit because startup may write runtime state.
