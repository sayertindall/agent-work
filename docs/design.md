# Design decisions

The system has sixteen discoverable skills. Seven manage durable work, Steady selects the execution lane, and eight cover distinct specialist decisions. The shared policy is installed once per host. Principles are read on demand, not advertised as separate skills.

This retains pstack's emphasis on simple structures, real evidence, root causes, consumer experience, and accountable delegation. It removes mandatory principle citations, automatic panel reviews, fixed prototype quotas, automatic external actions, and workflow-triggered PR creation.

The managed-work lifecycle borrows the useful idea of durable Markdown plans in Git. It is required for substantive authorized changes and multi-session execution, and supports reports and operational work as well as code. Informational and no-write requests remain non-mutating; trivial work stays lightweight. Technical readiness is separate from execution authorization. Completion is defined by the plan's acceptance criteria, not by a universal PR milestone.

One coordinator owns each work repository. Workers own separate code workspaces and report evidence. The design does not pretend that moving a Markdown file is a cross-machine lock. Concurrent coordinators sharing one queue would require a real claim mechanism; this collection does not implement one.

The collection uses a deliberately small frontmatter subset accepted as ordinary skill metadata: a name and a quoted description. No host-only opt-in flags are relied on for authorization. Descriptions define narrow intent triggers; the shared policy and task request define permissible actions.

The principles are rewritten guidance, not copies of the installed pstack implementation. Model names, plugin routers, and runtime commands are not vendored. The adapters describe how to select the live host capability and document what must be verified at activation.

Structural budgets in the validator keep descriptions and entrypoints small. They are repository-maintenance limits, not a requirement that agents omit necessary evidence from answers. Change a budget deliberately when a demonstrated use case requires it, rather than padding guidance to reach the maximum.

The user explicitly chose Steady as the required agent-driven workflow after the initial proposal. Its entry rule lives once in shared policy; it does not mandate rereading every lane or principle. Work-root precedence is explicit request, project instructions, then host default. The initial default is `~/Dev/work`, configurable at installation. Building these skills does not create or install that global work directory.
