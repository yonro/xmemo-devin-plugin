# Devin runtime evidence — 2026-10-13

This record contains only synthetic acceptance data. No personal memory,
project record, knowledge item, token, cookie, or credential is included.

## Environment

- Devin CLI `3000.10.48 (fcf7ba39)` on Windows.
- Plugin revision tested: `dbbcc524dead48a2508f6bb71fe73e954f00f2dd` (rc.2).
- Cloud Personal scope: plugin showed **Enabled**, 4 skills, 1 MCP after reindex.
- CLI OAuth callback: localhost. Cloud OAuth callback: `api.devin.ai`.
- Consent showed four scopes: memory read/write and knowledge read/write.

## Results

| Test | Result | Evidence |
| --- | --- | --- |
| OAuth | PASS | Both Cloud and CLI completed XMemo consent; CLI reported successful authentication. |
| Tool discovery | PASS | Devin called `mcp_list_tools`; live server exposed `get_mcp_identity`, `remember`, `update_state`, `recall`, `recall_context`, `read_memory` and other tools. `search_memory` and `get_state` were absent. |
| Synthetic write | PASS | Direct Devin `remember` returned semantic-memory ID `62ecc904-0e4d-41b6-8891-06ecc313fd93`; a later exact read resolved the stored memory as `bcbc0b55-180a-4df8-88d2-d38fda686795`. Content was the amber lighthouse fact under `acceptance/devin-20261013-a7c9`. |
| Synthetic checkpoint | PASS | `update_state` created state key `devin-20261013-a7c9`; wrapper receipt ID `3913d1b6-49e0-4a2d-ae46-ed78e023fdb1`. Recall later returned state ID `e40871af-98c8-4b3f-9a5e-2b5dfde9ec7d`. |
| New-session resume | PASS | A separate `devin -p` process used the exact query/path filter and found both synthetic records, including “verify lighthouse color in a new session”. |
| Scope discipline | PASS | Recall was restricted to the exact synthetic path. No knowledge tools or unrelated MCP servers were used. |
| Generic wrapper | FAIL / compatibility issue | Devin's `mcp_call_tool` wrapper repeatedly emitted malformed calls missing `server_name` for `remember`/`update_state`. Direct `mcp__xmemo__remember` and `mcp__xmemo__update_state` worked. The plugin policy therefore must route through live direct tools, not the wrapper. |
| Local credential removal | PASS | `devin mcp logout xmemo` removed local OAuth credentials. This does not prove provider-side grant revocation. |
| Provider revocation | BLOCKED | No provider-side revoke was performed because the XMemo account UI was not used to delete the grant. Old-token rejection therefore remains unverified. |
| Two-user isolation | BLOCKED | A second separately authorized synthetic identity was not available. |

The direct-memory read returned a different canonical ID than the initial
receipt ID. This is preserved as observed behavior and is not treated as a
plugin success bug without server-side correlation evidence. The test did not
create additional records after the successful direct write.

## Release impact

OAuth, discovery, direct synthetic write, checkpoint, and new-session recall
are now runtime-proven. Provider revocation, two-user isolation, model-level
skill invocation, and the generic wrapper failure remain open. Stable GA and
marketplace submission remain disabled.
