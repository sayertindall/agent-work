---
name: performance
description: "Investigate a measured performance problem or optimize a specified metric with before-and-after evidence."
---

# Performance

Identify the metric, representative workload, environment, and acceptable behavior. Establish a repeatable baseline before choosing an optimization. If a benchmark is unavailable, distinguish a suspected bottleneck from a measured one.

Profile the relevant path and choose a hypothesis whose effect can be observed. Control material differences between baseline and treatment. Avoid production load generation or disruptive profiling outside authorization. Diagnosis-only requests do not authorize changes.

For authorized optimization, change the supported bottleneck and rerun representative measurements alongside correctness checks. Report variation, tradeoffs, and whether the target was met. Stop when the agreed target is satisfied or new evidence requires a decision; do not optimize indefinitely. Retain a reusable benchmark when it will guard meaningful behavior.
