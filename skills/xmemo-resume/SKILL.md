---
name: xmemo-resume
description: Use when Devin starts a new session, resumes interrupted work, or takes over a task from another agent.
---

# XMemo Resume

Retrieve a bounded restart context with `recall_context`, or an exact project pack with `get_project_context` when an authorized project ID is known. Reconcile every remembered claim against the current checkout, Git history, tests, CI, and service state before acting.

Return the latest verified state, stale or conflicting items, active blockers, and one next action. If no trustworthy checkpoint exists, say so and inspect the live workspace. Do not write a new checkpoint simply because a session began.
