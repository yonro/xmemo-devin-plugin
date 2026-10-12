# XMemo for Devin

XMemo for Devin is a Devin plugin that connects Devin to the hosted XMemo MCP service at `https://xmemo.dev/mcp` and provides four focused workflows for durable project memory and cross-agent continuity.

> **Release status:** v1.0.0 package candidate. Devin account/session validation and marketplace admission remain separate gates and are not claimed here.

## What is included

- **XMemo Recall** — bounded retrieval of authorized memory and project context.
- **XMemo Checkpoint** — user-authorized progress and decision checkpoints.
- **XMemo Handoff** — evidence-based transfer to another agent or session.
- **XMemo Resume** — reconciliation of a saved checkpoint with the live workspace.

The plugin contains no memory backend and no credentials. Devin handles MCP OAuth and stores authorization outside this repository. The skills map to existing XMemo tools such as `recall_context`, `search_memory`, `get_project_context`, `update_state`, `record_event`, and `remember`; they do not invent new server tools.

## Install locally

```bash
devin plugins install --local ./xmemo-devin-plugin
```

Start a new Devin session after installation. When Devin activates the MCP connection, authorize XMemo in the browser for the scopes requested by the service. The repository cannot complete an OAuth login or a Devin Cloud installation on your behalf.

## Security boundaries

- No API keys, OAuth tokens, client secrets, cookies, or user data are committed.
- Memory writes are user-authorized and bounded; a session start does not trigger a write.
- Retrieved memories are historical context and must be checked against live repository state.
- Project and organization isolation is enforced by XMemo; the plugin does not accept client-supplied owner claims.
- Checkpoints and handoffs do not claim to restore a complete executable environment.

## Validation

```powershell
python scripts/validate_package.py
python -m unittest discover -s tests -p 'test_*.py' -v
```

The live endpoint currently responds with `401 Unauthorized` without authorization, while OAuth discovery is available. See [docs/verification.md](docs/verification.md) for the evidence matrix and the blocked Devin steps.

## Marketplace preparation

The official marketplace accepts a third-party plugin as a URL pinned to a full 40-character commit SHA. After this repository is pushed and tested, add an object like this to a fork of `CognitionAI/devin-marketplace`:

```json
{
  "source": "url",
  "url": "https://github.com/yonro/xmemo-devin-plugin.git",
  "sha": "<tested-40-character-commit-sha>"
}
```

Do not open that marketplace pull request until the owner reviews the prepared diff and accepts the marketplace CLA terms.

## License

MIT, © 2026 Yonro.
