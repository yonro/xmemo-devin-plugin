# Real Devin acceptance

Status: PARTIAL: Cloud installation passed; authenticated MCP acceptance is blocked. Static validation does
not establish runtime acceptance. Record plugin SHA, Devin version, date and
redacted evidence for each case. Never commit tokens or personal memory content.

1. Install locally using the README command, or use Customize > Plugins > Add
   plugin > From repository at personal scope. Start a new session.
2. Activate XMemo and complete OAuth in the browser. Inspect the account, scopes
   and destination. Do not distribute personal authorization at organization scope.
3. Inspect tools/list and live input schemas. Check identity with an exposed
   identity tool. Missing tools must produce an unavailable-capability response;
   do not claim Devin uses Claude's signed 16-tool profile.
4. In an explicitly authorized synthetic project, save a unique test fact,
   recall it and update a task-specific checkpoint. Verify scope and attribution.
5. Resume in a new session after changing a synthetic local commit. Verify Devin
   checks Git and labels stale checkpoint claims instead of repeating them.
6. Request a handoff to another authorized agent. Check evidence, recipient and
   next action. A summary-only request must perform zero writes. Failed partial
   writes must produce a partial receipt and must not replay successful records.
7. With two separately authorized test users and workspaces, demonstrate that
   neither can read or modify the other's synthetic records.
8. Revoke the test grant. Verify old access and refresh credentials cannot access
   protected resources. Reconnect only through a new consent flow.
9. Capture redacted install, recall and handoff screenshots. Soft-delete only the
   exact synthetic records approved for cleanup.

Record PASS/FAIL/BLOCKED for installation, activation, discovery, OAuth, identity,
read, write, user isolation, workspace isolation, revocation and session resume.
Missing cases block GA and marketplace submission. Review the Marketplace CLA
before opening a PR; preparation is not authorization to submit.
