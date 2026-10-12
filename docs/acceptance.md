# Real Devin acceptance

Status: PARTIAL: Cloud installation passed; authenticated MCP acceptance is blocked. Static validation does
not establish runtime acceptance. Record plugin SHA, Devin version, date and
redacted evidence for each case. Never commit tokens or personal memory content.

For a detailed step-by-step test guide with evidence templates, see [scripts/acceptance_test.md](../scripts/acceptance_test.md).

## Test Summary

1. **Installation** - Install plugin locally or from repository at personal scope
2. **Activation & OAuth** - Complete OAuth in browser, inspect scopes and destination
3. **Tool Discovery** - Inspect tools/list and live input schemas, check identity
4. **Read & Write** - Save, recall, and update checkpoints in synthetic project
5. **Session Resume** - Resume in new session after Git change, verify staleness detection
6. **Handoff** - Request handoff, verify evidence, partial writes, and zero-write summary
7. **Isolation** - Demonstrate user/workspace isolation with two test accounts
8. **Revocation** - Revoke grant, verify old credentials fail, reconnect with new consent
9. **Cleanup** - Capture screenshots, soft-delete synthetic records, verify no credentials

Record PASS/FAIL/BLOCKED for installation, activation, discovery, OAuth, identity,
read, write, user isolation, workspace isolation, revocation and session resume.
Missing cases block GA and marketplace submission. Review the Marketplace CLA
before opening a PR; preparation is not authorization to submit.
