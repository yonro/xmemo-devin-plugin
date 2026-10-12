# Devin compatibility audit

Audit date: 2026-10-13 (Asia/Tokyo). Scope: this repository's plugin,
four skills, hosted MCP declaration, Cloud/CLI installation and release path.
This is not certification of every Devin product feature. Optional features
not shipped here are explicitly excluded; absence is not a runtime pass.

## Sources and interpretation

The live official [plugin reference](https://docs.devin.ai/cli/extensibility/plugins/overview),
[Cloud plugin guide](https://docs.devin.ai/product-guides/plugins),
[ecosystem guide](https://docs.devin.ai/product-guides/plugin-ecosystem),
[skill reference](https://docs.devin.ai/cli/extensibility/skills/overview),
[skill authoring guide](https://docs.devin.ai/cli/extensibility/skills/creating-skills),
[MCP configuration](https://docs.devin.ai/cli/extensibility/mcp/configuration),
[rules](https://docs.devin.ai/cli/extensibility/rules) and
[hooks](https://docs.devin.ai/cli/extensibility/hooks) were reviewed.
The installed CLI also includes corresponding reference documents.

The [official template validator](https://github.com/CognitionAI/plugin-template/blob/dd46026e57a228050b34c25961cdf9b82d5415bd/scripts/validate-plugins.mjs)
was executed unchanged with this package copied under `plugins/xmemo-devin`.
The [marketplace validator](https://github.com/CognitionAI/devin-marketplace/blob/ad4d8ec5478ee07118a9899885960425692b1526/scripts/validate.py)
uses a narrower schema for marketplace-owned entries. That is not the universal
plugin manifest schema. In particular, Devin supports manifest `version`.

## Itemized checks

STATIC means inspected or tested without a model session. RUNTIME means an
observed product result. BLOCKED means acceptance remains incomplete.

| Area | Requirement / decision | Evidence and status |
| --- | --- | --- |
| Discovery | Preferred `.devin-plugin/plugin.json` location | STATIC pass; Cloud discovered package |
| Identity | Stable lowercase kebab-case name | STATIC pass: `xmemo-devin` |
| Metadata | Supported version and license | STATIC pass; version equals VERSION; MIT attribution retained |
| Presentation | Description, logo, homepage and repository | RUNTIME pass on earlier installed commit; logo path containment tested |
| Versioning | Manifest, VERSION and release tag agree | STATIC pass; mismatch negative test |
| Skill layout | Default `skills/<name>/SKILL.md` | STATIC pass; RUNTIME four skills indexed |
| Frontmatter | Name/description and directory agreement | STATIC pass, including official validator |
| Invocation | Namespaced slash commands | Documented; actual model invocation BLOCKED |
| Triggers | Default user/model triggers; no invented lifecycle | STATIC pass; model selection BLOCKED |
| Tool approval | `allowed-tools` is not an access restriction | Omitted; negative test prevents accidental auto-approval |
| Policy loading | Linked policy is not automatically always-on | Required before workflow operations; model compliance BLOCKED |
| Upstream reuse | Immutable source, license, reproducible adaptation | STATIC pass; SHA-256 and generated drift negative tests |
| MCP shape | Inline named server map | STATIC pass; RUNTIME one MCP indexed |
| Transport | HTTPS URL defaults to Streamable HTTP | RUNTIME Cloud shows HTTP; authenticated transport BLOCKED |
| MCP precedence | No competing `.mcp.json` or file override | STATIC pass |
| Credentials | No embedded token, header or client secret | STATIC pass; forbidden config negative test; regex is not a complete security audit |
| OAuth client | Use host DCR, do not impersonate Claude | RUNTIME Cloud and CLI authorization initiation observed |
| PKCE/resource | S256; resource is MCP URL | RUNTIME initiation pass; token exchange BLOCKED |
| Scope config | Memory read/write array | RUNTIME CLI writes supported array; manifest requests it |
| Actual scope | Declared scopes must match approved access | BLOCKED: CLI URL also requests knowledge read/write; Cloud update needs separate check |
| Cloud ownership | Personal authorization, no shared Org Access | RUNTIME Personal installation pass |
| Cloud indexing | Parse skills and MCP after repository fetch | RUNTIME pass for `8d6fb98`; new manifest reindex must be verified separately |
| CLI install | CLI sign-in then local installation | BLOCKED by CLI login; Desktop installation alone does not prove CLI authentication |
| Login separation | Cloud connection does not prove CLI connection | Documented; neither MCP consent completed |
| Discovery | Inspect actual tools/list and schemas | BLOCKED by OAuth; tool names in skills remain conditional |
| Identity | Server-derived user/tenant attribution | Policy inspected; actual server identity BLOCKED |
| Read/write | Exact synthetic fact and scoped checkpoint | BLOCKED; zero authenticated test writes so far |
| Resume | New session checks live Git against stale state | BLOCKED |
| Handoff | Recipient/scope/provenance and partial receipts | Static workflow present; runtime BLOCKED |
| Untrusted memory | Retrieved text is context, not instructions | Explicit upfront rule; adversarial runtime test BLOCKED |
| Isolation | Two users and workspaces cannot cross access | BLOCKED: separately authorized test identities needed |
| Revocation | Provider grant revoked; old credentials rejected | BLOCKED; CLI logout alone is insufficient |
| Hooks/rules/agents | Optional capabilities | Not shipped; no hook-based enforcement or subagent support claimed |
| Plugin governance | Required/optional/forbidden dependencies | Not used; cannot override an organization's denial policy |
| Packaging | Versioned ZIP/checksum and CI validation | Existing rc.1 release verified; rc.2 is development only |
| Marketplace | External URL pinned to full tested SHA | Prepared only; existing local preparation pins rc.1 |
| Legal/publication | Review CLA before third-party submission | No marketplace PR or CLA acceptance; GA gate remains closed |

## Reproducing checks

Run `python scripts/sync_skills.py --check`, `python scripts/validate_package.py`
and `python -m unittest discover -s tests -v` in this repository.
For the official template check, clone the pinned template commit into a
temporary directory, copy this package's `.devin-plugin` and `skills` directories
under `plugins/xmemo-devin`, and run `node scripts/validate-plugins.mjs` unchanged.
Its pass establishes structure only; it does not validate remote MCP behavior.

The CLI schema probe used an isolated temporary working directory and
`devin mcp add xmemo-scope-schema --url https://xmemo.dev/mcp --scope local --scopes memory:read,memory:write`.
This command initiates browser authorization automatically. The generated
config used `oauthScopes: ["memory:read", "memory:write"]`, but the authorization
URL included knowledge scopes too. No consent was approved and the waiting
probe was terminated. Full authorization URLs, state, cookies and tokens must
never be added to this repository. The observation does not identify whether
scope expansion originates in client discovery logic or server challenge policy.

## Remaining acceptance

Follow [acceptance.md](acceptance.md) after login and scope review. Record the
exact installed revision, host version, test identifiers and sanitized result
for each step. Missing consent, discovery, model behavior, isolation or revocation
evidence blocks a claim of full adaptation and the stable release.
