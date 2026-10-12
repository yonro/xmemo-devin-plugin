---
name: xmemo-checkpoint
description: Use when the user explicitly asks to save progress, record a decision, or create a restart-ready checkpoint at a meaningful task boundary.
---

# XMemo Checkpoint

First summarize the bounded state: objective, verified changes, decisions, open TODOs, blockers, and one next action. Ask for authorization before a durable write unless the user already requested the checkpoint.

Use `update_state` for the resumable working state. Use `record_event` only for a significant milestone or decision, and use `remember` only for a concise durable fact. A checkpoint is not a copy of the conversation and does not restore an executable environment. Include agent identity, project scope, provenance, and evidence in the write metadata when the server contract permits it.

After writing, report exactly what was saved and what remains unverified. Never claim a checkpoint succeeded if the MCP call failed.
