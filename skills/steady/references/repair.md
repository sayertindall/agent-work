# Repair

Establish the failing behavior and what success would look like. Use [debug](../../debug/SKILL.md) if the cause is not already evidenced. Preserve a useful reproduction before changing behavior.

Fix the supported cause within scope. Add a regression check when it protects meaningful behavior. Verify that the original failure is gone and relevant adjacent behavior remains correct. If evidence cannot distinguish causes, gather a targeted observation rather than stack speculative fixes.

During urgent incidents, an authorized mitigation can precede full diagnosis. State what it restores and what remains unresolved. A diagnosis-only request does not authorize repair.
