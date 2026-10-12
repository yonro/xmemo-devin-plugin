# Verification evidence

## IMPLEMENTED

- Root Devin manifest at `.devin-plugin/plugin.json` with one HTTPS MCP server.
- Four Devin skills with explicit triggers, existing XMemo tool mappings, and safety boundaries.
- Package validator, unit tests, GitHub Actions validation, MIT license, changelog, and marketplace preparation notes.

## VERIFIED

- On 2026-10-13, local package validation, generated-source verification and six unit tests passed, including negative cases for credentials, path escape, broken links, upstream/generated drift and release tags. These are static checks, not model behavior or Devin E2E tests.
- GitHub repository creation and rc.1 validation/release workflows succeeded. The published rc.1 artifact is historical and is not changed by the rc.2 development work.
- `https://xmemo.dev/.well-known/oauth-authorization-server` returned HTTP 200 and advertised authorization, token, registration, and revocation endpoints with PKCE S256 support on 2026-10-12.
- `https://xmemo.dev/mcp` returned HTTP 401 without an access token on 2026-10-12, which is consistent with a protected endpoint.

## REAL RUNTIME PROGRESS (2026-10-13)

- Cloud installed the repository at Personal scope and indexed four skills and one HTTP MCP using commit `8d6fb98bc4064cb8f41cb17944f59be6b2c7d9c8`.
- Connect MCP reached XMemo login with Devin's HTTPS callback, PKCE S256 and the MCP resource URL. This proves initiation, not completed consent or authenticated tool access.
- Installed CLI `3000.10.48 (fcf7ba39)` generated an isolated local config with `oauthScopes` as a string array. Its OAuth initiation still requested both memory and knowledge read/write. The pending probe was stopped without granting access.
- CLI browser sign-in and `plugins install --local --yes` succeeded for rc.2. `plugins list` confirmed the installed version and `mcp list` exposed xmemo.
- Cloud reindex of `224e11f` completed, but Connect MCP failed with `OAuth scopes require an OAuth client ID`. The scopes-only override was therefore removed to retain DCR compatibility. This failed experiment is not runtime acceptance.
- Commit `224e11f` passed GitHub Actions run `38275435365` before the runtime scope incompatibility was found; a CI pass alone did not catch it.
- The unmodified official template validator at `dd46026e57a228050b34c25961cdf9b82d5415bd` passed with this package staged under `plugins/xmemo-devin`. This validator checks structure, not OAuth or model behavior.
- See [the itemized audit](devin-compatibility.md). Later manifest changes require Cloud reindexing; earlier install evidence does not prove those changes loaded.

## BLOCKED

- Completed OAuth consent, real `tools/list`, authorized recall/write, revocation and cross-session resume still require user authorization and a synthetic test session.
- Actual scope narrowing remains unresolved; declared scopes are not evidence of granted scopes.
- User/workspace isolation and revocation require separately authorized synthetic test identities. Follow [acceptance.md](acceptance.md); server metadata alone is insufficient.

## NOT STARTED

- No CognitionAI marketplace PR was submitted, by explicit task boundary. After owner review, use a fork, add the tested full SHA, run `python3 scripts/validate.py --fix` and `--fetch`, and submit only after CLA review.
- The local marketplace preparation branch still pins rc.1; update it only to a commit with the required acceptance evidence. No stable release is enabled by the current release gate.
