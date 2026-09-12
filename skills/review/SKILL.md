---
name: review
description: "Review a specified change or artifact for actionable defects and unmet requirements. Do not edit the subject unless fixes are requested."
---

# Review

Resolve the requested baseline, artifact, and review scope. Read the applicable requirements and changed paths, then trace relevant callers and consequences. Do not turn a bounded review into an entire-repository audit.

Inspect Git changes with the user's `git dft` command (Difftastic). Use `git dft --cached` for staged changes, `git dft` for unstaged tracked changes, and `git dft <base>...<head>` for branch changes since their merge base. Use two explicit refs without three dots for an endpoint comparison. Inspect untracked files separately; never change staging to select a review scope. Do not persist `diff.external` in Git configuration.

For Git code diffs, use [open-code-review](../open-code-review/SKILL.md) as the default automated review pass unless the user selects another method or task constraints prohibit it. Validate its findings yourself. For non-code artifacts, use direct assessment.

Before assessing maintainability or test adequacy, use the [principle index](../steady/references/principle-index.md) to read reader-effort or behavior-test guidance as applicable. Principles support evidence-backed findings, not preference-only objections.

Read [naming and code quality rules](../steady/references/rules.md) when reviewing new paths, symbols, or resources. Assess semantic names as well as the gate result. Existing violations do not justify new ones; preserve immutable and external contracts.

Prioritize defects with a concrete trigger and observable impact. Check correctness, compatibility, failure handling, and maintainability where relevant. Separate introduced defects, regressions, and pre-existing issues. Prefer evidence to style preferences. Load [security](../security/SKILL.md) or [interface](../interface/SKILL.md) only when that review surface is requested or material.

Use read-only inspection when required; tests can write caches or fixtures. Do not fix a finding during a review-only request. Report each actionable finding with severity, location, trigger, consequence, and supporting evidence. Report coverage and unverified surfaces even when no findings remain.

For an explicitly independent review, use a separate permitted reviewer and inspect its actual findings. If unavailable, label the assessment as self-review and leave the independence requirement unmet.
