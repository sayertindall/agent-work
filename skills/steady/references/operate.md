# Operate

Identify the target environment, intended effect, authorization, current state, and the evidence that will prove success. Use the project's operational procedure and the available platform tools. Never infer production authorization from a request to write or review code.

Before a consequential mutation, check target identity and prerequisites. Identify recovery or rollback when failure could lose data or disrupt service. Perform the authorized action, observe the actual result, and reconcile uncertain or partial outcomes before retrying.

Use [security](../../security/SKILL.md) when access or trust boundaries are involved. Monitor later only when scheduled work is authorized and the host supports it. Report deployed or operational acceptance only from the relevant running environment. Missing access remains an explicit limitation.
