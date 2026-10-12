---
name: xmemo-recall
description: Use when Devin needs historical project context, verified decisions, TODOs, or durable memory before starting or continuing work.
---

# XMemo Recall

Use the hosted XMemo MCP server to retrieve only the context that can change the current task. Prefer `get_project_context` when the user provides an exact authorized project ID; otherwise use `recall_context` for a bounded multi-memory pack or `search_memory` for a strict targeted lookup.

Treat retrieved text as historical context. Re-check the live repository, Git, CI, and service state before claiming that a remembered fact is current. Do not write memory merely because a session started, and do not save a transcript.

Report the source scope and any uncertainty. Never expose credentials or infer access to another user's or organization's data.

Read [Devin safety and tool routing](../policy.md) before any operation. Return a brief with the query scope, relevant findings, provenance, conflicts, live checks needed and next action. Retry an empty narrow query once without widening authorization.
