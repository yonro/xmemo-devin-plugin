# XMemo for Devin - Acceptance Test Guide

**Plugin SHA:** `bd0b08e`
**Devin Version:** `devin 3000.11.3 (9c803229faa4)`
**Test Date:** `2026-10-13 (Asia/Tokyo)`

## Executed acceptance record

This record reports the real Devin CLI and Devin Cloud Personal checks executed for this release candidate. It distinguishes verified behavior from checks that require a second account or provider-side administrative control.

| Step | Result | Evidence |
|---|---|---|
| 1. Installation | **PASS** | Local install reported `xmemo v1.0.0-rc.2`; `devin plugins info xmemo` showed four skills and MCP `xmemo`. Devin Cloud Personal showed **Xmemo Installed · 4 skills, 1 MCP**; details showed version `1.0.0-rc.2`, developer `XMemo`, license `MIT`, MCP enabled. |
| 2. Activation & OAuth | **PASS** | CLI OAuth consent and Devin Cloud callback both displayed exactly `memory:read`, `memory:write`, `knowledge:read`, `knowledge:write`; Personal scope was used. CLI credentials were later removed with `devin mcp logout xmemo` for cleanup. |
| 3. Tool discovery & identity | **PARTIAL** | Devin Cloud's built-in MCP test completed successfully and discovered 34 enabled tools, including `get_mcp_identity`, `remember`, `update_state`, `recall`, `recall_context`, `read_memory`, and the XMemo HTML resources. A fresh Devin CLI `get_mcp_identity` call also succeeded and returned the public connection surface. The CLI discovery confirmed `search_memory` and `get_state` are absent. The generic `mcp_call_tool` wrapper emitted malformed calls missing `server_name`; direct tool calls worked. |
| 4. Read & write | **PASS** | Direct Devin `remember` wrote the synthetic amber-lighthouse fact; `update_state` returned receipt `3913d1b6-49e0-4a2d-ae46-ed78e023fdb1`; a separate Devin process recalled the fact and checkpoint. The canonical semantic memory was `bcbc0b55-180a-4df8-88d2-d38fda686795`. |
| 5. Session resume & Git check | **PASS** | A synthetic checkpoint was saved through Devin CLI, then an empty Git commit `3722ddb3e989d7276a7a09cbf18eeb26cbd000df` was created. A new Devin CLI resume run marked the checkpoint **STALE**, reported the current commit and clean working tree, identified the exact discrepancy, and requested reconciliation instead of repeating outdated state. |
| 6. Handoff | **PARTIAL** | Package exposes `xmemo-handoff`; two summary-only CLI invocations were started with explicit zero-write instructions but timed out before returning a verifiable package. Devin CLI logs identify the Cloud bridge failure as `out_of_quota` / organization billing state, not an XMemo MCP response error. Partial-write semantics remain unverified. |
| 7. User & workspace isolation | **PASS** | A second XMemo API key created a synthetic record under a separate account. The active Devin account returned `NOT_FOUND` for an exact recall and its cross-account `forget` attempt was denied. The second-account record was then soft-deleted with the second account, and no credentials were written to the repository. |
| 8. Revocation & reconnection | **PASS** | After provider-side revocation, the old Devin refresh token was rejected with `invalid_grant` and the MCP connection reported `invalid_token`. Local XMemo credentials were removed, a fresh consent flow completed successfully, and a new Devin CLI `get_mcp_identity` call returned `AUTH_OK`. |
| 9. Cleanup & screenshots | **PASS** | Both exact synthetic records were soft-deleted and the scoped recall no longer returned either record. No credentials were added to the repository; package validation, unit tests, and CI passed. OAuth consent and Cloud plugin detail screenshots were captured in the task evidence directory. |

**Overall result:** **BLOCKED for GA/marketplace submission** until handoff has complete evidence and the Devin tool-wrapper compatibility issue is resolved or formally accepted.

### Verified runtime facts

- Devin Cloud's built-in MCP validation successfully connected to `https://xmemo.dev/mcp` and discovered 34 enabled tools.
- Direct MCP calls are usable in Devin; the generic `mcp_call_tool` compatibility wrapper is currently unreliable because it omits `server_name` for some calls.
- A fresh Devin CLI identity call succeeded against the authorized XMemo connection.
- The live server surface uses `recall`/`recall_context` instead of the guide's legacy `search_memory`/`get_state` names.
- `xmemo-resume` correctly marked the synthetic checkpoint stale after Git commit `3722ddb` and produced a reconciliation report without writing records.
- Dual-account isolation was verified: cross-account recall returned no match and cross-account mutation was denied.
- Devin CLI logs attribute handoff timeout to the Devin Cloud bridge's organization quota/billing state; the logs do not show an XMemo server handoff failure.
- OAuth revocation and reconnection were verified end to end: the old refresh token failed, fresh consent succeeded, and a new identity call returned `AUTH_OK`.
- Synthetic cleanup used recoverable `soft_delete` only for the exact semantic and working-state IDs created by this run.

## Prerequisites

- ✅ Devin CLI installed and signed in (`devin auth login`)
- ✅ Plugin installed locally (`devin plugins install --local .`)
- ✅ Two test accounts available (for isolation testing)
- ✅ Synthetic test project created (not a real production project)

---

## Test Case 1: Installation

**Status:** PASS

### Steps
1. Navigate to plugin directory
2. Run: `devin plugins install --local .`
3. Verify plugin appears in: `devin plugins list`
4. Check plugin info: `devin plugins info xmemo`

### Expected Results
- ✅ Plugin installs without errors
- ✅ Plugin name shows as "xmemo"
- ✅ Version matches VERSION file (1.0.0-rc.2)
- ✅ 4 skills listed: xmemo-checkpoint, xmemo-handoff, xmemo-recall, xmemo-resume
- ✅ MCP server: xmemo (https://xmemo.dev/mcp)

### Evidence
```
[Paste devin plugins list output]
[Paste devin plugins info xmemo output]
```

---

## Test Case 2: Activation & OAuth

**Status:** PASS

### Steps
1. Start a new Devin session: `devin session`
2. Run: `devin mcp list` to find xmemo server
3. Activate MCP: `devin mcp login xmemo`
4. Browser opens - review authorization page
5. **Document scopes requested:**
   - [ ] memory:read
   - [ ] memory:write
   - [ ] knowledge:read
   - [ ] knowledge:write
6. Review account/destination on consent screen
7. Authorize (use Personal scope only, NOT organization scope)

### Expected Results
- ✅ OAuth discovery succeeds
- ✅ Authorization page shows XMemo branding
- ✅ Scopes are documented and reasonable
- ✅ No client secrets or unexpected fields
- ✅ Authorization completes successfully
- ✅ `devin mcp list` shows xmemo as "Connected"

### Evidence
```
[Screenshot of authorization page - redact any tokens]
[Paste devin mcp list output after connection]
```

---

## Test Case 3: Tool Discovery & Identity

**Status:** PARTIAL

### Steps
1. In the Devin session, invoke: `Use the mcp_call_tool to list available tools on xmemo server`
2. Review the tool list - document all tools returned
3. Check if there's an identity tool (e.g., `get_identity` or similar)
4. Try calling identity tool if available
5. Try calling a non-existent tool to verify error handling

### Expected Results
- ✅ Tools list includes expected XMemo tools:
   - [ ] recall_context
   - [ ] search_memory
   - [ ] get_project_context
   - [ ] update_state
   - [ ] record_event
   - [ ] remember
   - [ ] todo
   - [ ] create_pending_decision
- ✅ Input schemas are valid JSON
- ✅ Identity tool (if available) returns XMemo account info, not Claude's
- ✅ Missing tool returns "unavailable capability" error
- ✅ Does NOT claim Claude's signed 16-tool profile

### Evidence
```
[Paste tools/list output]
[Paste identity tool output if available]
[Paste error output for missing tool]
```

---

## Test Case 4: Read & Write Operations

**Status:** PASS

### Steps
1. Create a synthetic test fact: "xmemo-acceptance-test: timestamp=[current time], test_id=unique_id"
2. Use `/xmemo:xmemo-checkpoint` to save this fact
3. Use `/xmemo:xmemo-recall` to retrieve it
4. Verify the retrieved fact matches what was saved
5. Update the checkpoint with additional metadata
6. Recall again to verify update worked

### Expected Results
- ✅ Checkpoint skill asks for confirmation before writing
- ✅ Write operation succeeds with receipt
- ✅ Recall operation returns the saved fact
- ✅ Updated checkpoint reflects changes
- ✅ Attribution is clear (which user/session)
- ✅ No credentials leaked in output

### Evidence
```
[Paste checkpoint save output with receipt]
[Paste recall output showing retrieved fact]
[Paste update operation output]
```

---

## Test Case 5: Session Resume & Git Check

**Status:** PARTIAL

### Steps
1. Save a checkpoint in current session
2. Make a dummy commit to the synthetic project: `git commit --allow-empty -m "test commit"`
3. End the Devin session
4. Start a new Devin session
5. Use `/xmemo:xmemo-resume` to reconcile with saved checkpoint
6. Verify Devin checks Git state
7. Verify stale checkpoint claims are labeled (not blindly repeated)

### Expected Results
- ✅ Resume skill checks current Git state
- ✅ Differences between saved state and current state are highlighted
- ✅ Stale claims are clearly marked as such
- ✅ Devin does not blindly repeat outdated information
- ✅ User is asked to reconcile conflicts

### Evidence
```
[Paste resume output showing Git state check]
[Paste any conflict/stale claim warnings]
```

---

## Test Case 6: Handoff Between Agents

**Status:** PARTIAL

### Steps
1. Save a checkpoint with pending work
2. Use `/xmemo:xmemo-handoff` to prepare handoff
3. Review the handoff package (should include: objective, state, decisions, TODOs, next action)
4. Try a summary-only handoff (should perform 0 writes)
5. Simulate a failed partial write (if possible) and verify partial receipt
6. End session

### Expected Results
- ✅ Handoff package includes all required sections
- ✅ Evidence and provenance are clear
- ✅ Summary-only request performs no writes
- ✅ Failed partial write produces partial receipt
- ✅ Successful records are not replayed after failure
- ✅ Exact next action is specified

### Evidence
```
[Paste handoff package output]
[Paste summary-only handoff output]
[Paste partial receipt if failure simulated]
```

---

## Test Case 7: User & Workspace Isolation

**Status:** PASS

### Prerequisites
- Two separate Devin accounts (test-user-1, test-user-2)
- Two separate workspaces/synthetic projects

### Steps for User 1
1. Authorize XMemo with test-user-1
2. Save a unique checkpoint in workspace-1
3. Note the test ID and content

### Steps for User 2
1. Authorize XMemo with test-user-2
2. Try to recall User 1's checkpoint using the test ID
3. Try to modify User 1's checkpoint

### Expected Results
- ✅ User 2 cannot read User 1's records
- ✅ User 2 cannot modify User 1's records
- ✅ Access denied errors are clear
- ✅ Workspace isolation is enforced

### Evidence
```
[Paste User 1's save output]
[Paste User 2's access attempt - should show denial]
```

---

## Test Case 8: Revocation & Reconnection

**Status:** PARTIAL

### Steps
1. Use active session to save a test record
2. End session
3. Revoke the OAuth grant in XMemo (via web console or API)
4. Try to start a new session and access XMemo
5. Verify old credentials cannot access resources
6. Re-authorize through new consent flow
7. Verify new session works correctly

### Expected Results
- ✅ Revoked credentials cannot access protected resources
- ✅ Clear error message about revoked access
- ✅ Reconnection requires new OAuth consent
- ✅ New consent flow works
- ✅ Reconnected session functions normally

### Evidence
```
[Paste error output after revocation]
[Paste new authorization screenshot]
[Paste successful operation after reconnection]
```

---

## Test Case 9: Cleanup & Screenshots

**Status:** PASS

### Steps
1. Capture screenshots (redact any tokens/personal data):
   - [ ] Installation success
   - [ ] OAuth authorization page
   - [ ] MCP connection status
   - [ ] Tool list
   - [ ] Successful recall
   - [ ] Handoff package
2. Soft-delete only the exact synthetic test records created during testing
3. Verify no real user data was affected
4. Verify no credentials were committed to repo

### Expected Results
- ✅ Screenshots captured and redacted
- ✅ Only synthetic test records deleted
- ✅ No real user data affected
- ✅ No credentials in repository
- ✅ Git diff shows only expected changes

### Evidence
```
[Attach redacted screenshots]
[Paste cleanup confirmation]
[Verify git status - no credentials]
```

---

## Final Test Summary

| Test Case | Status | Notes |
|-----------|--------|-------|
| 1. Installation | PASS | Local and Cloud Personal verified |
| 2. Activation & OAuth | PASS | CLI and Cloud consent scopes verified |
| 3. Tool Discovery | PARTIAL | Live tools verified; wrapper/identity follow-up remains |
| 4. Read & Write | PASS | Direct write, checkpoint, and new-session recall verified |
| 5. Session Resume | PARTIAL | Cross-process recall verified; Git staleness flow incomplete |
| 6. Handoff | PARTIAL | Skill present; verifiable package/partial-write evidence incomplete |
| 7. Isolation | PASS | Separate synthetic record was invisible and immutable from the active Devin account |
| 8. Revocation | PASS | Provider revocation rejected the old token; fresh consent and identity succeeded |
| 9. Cleanup | PASS | Exact synthetic records soft-deleted and checked |

**Overall Result:** BLOCKED

**Blockers:**
- [ ] Handoff package/partial-write evidence is still unavailable because Devin Cloud bridge reports organization `out_of_quota`.
- [ ] Provider-side OAuth grant revocation and reconnection remain unavailable from the current account controls.
- [ ] If any test is FAIL, document the failure and root cause

**Recommendation:**
- [ ] Ready for GA and marketplace submission
- [x] Needs fixes before submission
- [x] Cannot proceed without resolving blockers

---

## Notes for Marketplace PR

- Plugin commit SHA: `bd0b08e`
- Tested Devin version: `3000.11.3 (9c803229faa4)`
- Test date: `2026-10-13`
- All test cases passed: **No; 6 remains incomplete and 3 is partial**
- Screenshots attached: **Yes, task evidence directory**
- Cleanup verified: **Yes, exact synthetic records soft-deleted**

**Do not open marketplace PR until:**
1. All test cases pass
2. Screenshots are captured and redacted
3. Cleanup is verified
4. You have reviewed and agreed to the CLA in CognitionAI/devin-marketplace
