---
name: review
description: "Review a specified change or artifact for actionable defects and unmet requirements. Do not edit the subject unless fixes are requested."
---

# Review

Resolve the requested baseline, artifact, and review scope. Read the applicable requirements and changed paths, then trace relevant callers and consequences. Do not turn a bounded review into an entire-repository audit.

Prioritize defects with a concrete trigger and observable impact. Check correctness, compatibility, failure handling, and maintainability where relevant. Separate introduced defects, regressions, and pre-existing issues. Prefer evidence to style preferences. Load [security](../security/SKILL.md) or [interface](../interface/SKILL.md) only when that review surface is requested or material.

Use read-only inspection when required; tests can write caches or fixtures. Do not fix a finding during a review-only request. Report each actionable finding with severity, location, trigger, consequence, and supporting evidence. Report coverage and unverified surfaces even when no findings remain.

For an explicitly independent review, use a separate permitted reviewer and inspect its actual findings. If unavailable, label the assessment as self-review and leave the independence requirement unmet.
