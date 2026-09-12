---
name: open-code-review
description: "Use the configured OCR CLI for Git diff reviews selected by Steady or review, or when Open Code Review is requested."
---

# Open Code Review

Use the installed `ocr` CLI and its existing provider configuration. Follow the [shared policy](../../policy/AGENTS.md) and [review contract](../review/SKILL.md). Do not install, upgrade, or reconfigure the CLI as an incidental review step. Check `ocr version` and `ocr review --help` when capabilities are uncertain.

## Select the actual diff

Resolve the repository and baseline from the task and Git state. Run from the repository or pass `--repo`. Provide concise requirements through `--background`, or `--background-file` for an existing document. Quote arguments safely.

| Scope | Arguments to `ocr review --audience agent` |
| --- | --- |
| Entire working copy | No revision arguments |
| One commit against its parent | `--commit <verified-ref>` |
| Branch changes since their common ancestor | `--from <verified-base> --to <verified-head>` |
| Inspect file selection without an LLM call | Add `--preview` to the chosen scope |

Workspace mode includes staged, unstaged, and untracked files. Staging selected files does not narrow it. For staged-only or exact endpoint requests, verify supported diff semantics and use an authorized isolated snapshot or another review method if necessary. Do not silently widen scope or change the index. Resolve a PR's actual base and head instead of assuming `main`.

Preview the selection before a substantial run. An empty preview means no selected coverage, not a clean review. Full-file audits use `ocr scan` only within an explicitly requested audit scope; inspect its help first.

## Run and assess

Use `--audience agent --format json --output <unique-evidence-path>` for a full review and read the complete result. Choose a task-owned evidence path when records are authorized. OCR sends code to its configured provider and may persist session data. For strict no-write or offline requests, use permitted local inspection unless those effects have been explicitly allowed. Review-only permits assessment, not source fixes or publishing comments.

Inspect exit status, stderr, and coverage. The installed CLI can exit zero with partial results when a token budget skips files. Failed, skipped, or truncated coverage must remain visible in the verdict. Do not retry connection failures blindly, expose configuration secrets, or change providers to conceal failure. If a required flag is missing, report the limitation and use a compatible, scope-preserving method when possible.

Inspect the matching changes with `git dft` as described in the review contract, alongside OCR's automated pass. OCR generates its own diff internally; do not pipe Difftastic output into an undocumented input flag. Verify candidate findings against the source, requirements, and callers. Resolve missing line positions manually before citing them. Prioritize supported impact rather than accepting or discarding findings solely by severity label. Retain limitations even when no findings survive validation.

OCR provides a separate automated review pass. It does not establish human approval, model diversity, runtime acceptance, or any stronger independence requirement without evidence. Fix validated defects when the task already authorizes fixes, then run relevant checks. Report using the review contract.
