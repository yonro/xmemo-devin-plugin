# Devin adapter architecture

The XMemo service remains the sole OAuth, storage, authorization and state
implementation. This repository packages one HTTP MCP declaration, four skills,
a shared Devin policy and build-time validation. It runs no background writer.

Three workflow sources come from the immutable Claude commit in upstream-lock.json.
The deterministic adapter changes session naming and routes references to the
Devin policy. Original MIT sources are checked by SHA-256. Local modifications
belong in the adapter or Devin policy; CI rejects edits to generated output.
This keeps future upstream updates reviewable without changing the Claude repo.

The Devin override requires active tool discovery rather than assuming Claude's
signed profile. Claude hooks, profile identity, OAuth client IDs and automatic
checkpoint triggers are not installed. A session boundary alone grants no write
authorization. Named tool routes are conditional on the active connection.

The release line is candidate-only. VERSION and tag must match. A stable release
is rejected even when static tests pass. The acceptance checklist describes the
external evidence required before maintainers can review enabling stable releases.
No API, database schema, production deployment or Claude directory branch changes
are part of this adapter.
