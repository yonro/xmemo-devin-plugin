---
name: xmemo-handoff
description: Use when handing verified project context from Devin to another authorized agent or session, including Claude Code, Codex, or Cursor.
---

# XMemo Handoff

Prepare a compact handoff with the project identifier, current objective, exact files or artifacts changed, tests actually run, confirmed decisions, unresolved questions, blockers, and one exact next action. Save it through `update_state` or `record_event` only after the user authorizes the handoff or explicitly requests it.

Mention the receiving agent and session boundary in provenance. Do not include credentials, private conversation transcripts, or claims that a snapshot reproduces the full environment. The receiving agent must independently verify repository, Git, CI, and deployment state after `recall_context` or `get_project_context`.
