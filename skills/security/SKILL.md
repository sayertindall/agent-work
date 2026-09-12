---
name: security
description: "Assess or implement a material security boundary, or perform an explicitly requested security review."
---

# Security

Establish the asset, actor, trust boundary, intended permissions, and authorized review or repair scope. Trace attacker-controlled input to the relevant access check or sensitive effect. Distinguish a concrete exploit path from generic hardening advice.

Use bounded evidence and safe fixtures where authorized. Do not probe third-party systems, expose secrets, rotate credentials, or modify production access without the corresponding authorization. A security review remains read-only unless repairs are requested.

For a finding, report prerequisites, affected boundary, trigger, impact, location, and evidence. For a repair, verify allowed behavior still works and unauthorized behavior is denied at the actual boundary. Treat provider, cloud, and deployment verification as separate evidence when not exercised. Follow project security requirements rather than inventing blanket gates for unrelated work.
