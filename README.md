# Tavily for Hermes Agent

Search the web, extract pages, discover URLs, crawl websites, and run research
through [Tavily's hosted MCP server](https://docs.tavily.com/documentation/mcp).
Includes a Tavily research skill. No local Tavily server, Node.js, additional
runtime dependencies, or changes to Hermes core are required.

## Install

Requires **Hermes Agent 0.22.2 or later** and a [Tavily API key](https://app.tavily.com).
This repository is installable directly; it is not yet an approved catalog listing.

1. Configure `TAVILY_API_KEY` for your active Hermes profile using Hermes's
   API-key settings or `hermes setup`. An existing key in that profile works.
   Keep keys out of chat, this repository, and `mcp.json`.
2. Install and enable:

   ```bash
   hermes plugins install tavily-ai/tavily-hermes-plugin --no-enable
   hermes plugins list
   hermes plugins enable tavily
   ```

3. Start a fresh session. Ask Hermes to find and load the plugin's `tavily-web`
   skill with `skills_list` and `skill_view`, then try:

   > Search Tavily's official documentation for search-depth options and cite the sources.

Hermes qualifies skill names to avoid collisions; discover the full name with
`skills_list`. If `plugins list` shows a different installed key, use that key
for enable/disable. Use the same profile for setup, installation, and chat.

## Tools and skills

| Hermes tool | Use |
| --- | --- |
| `mcp__tavily__tavily_search` | Web search with depth, domain, and date controls |
| `mcp__tavily__tavily_extract` | Extract content from known URLs |
| `mcp__tavily__tavily_map` | Discover URLs on a website |
| `mcp__tavily__tavily_crawl` | Collect content from a bounded website section |
| `mcp__tavily__tavily_research` | Produce a multi-source research report |

Hermes discovers schemas from the hosted server without a plugin-side allowlist.
The MCP exposes fewer parameters than Tavily's direct API; see the verified
[capability coverage](docs/capability-coverage.md). This plugin does not change
Hermes's built-in `web_search` or `web_extract` provider selection.

The [tavily-web skill](skills/tavily-web/SKILL.md) covers tool selection, source
verification, bounded crawls, citations, partial results, and errors. It adapts
the workflow approach from the [Tavily Grok plugin](https://github.com/tavily-ai/tavily-grok-plugin)
to Hermes's tools and skill format.

Example prompts:

- “Extract the API parameters from these documentation URLs.”
- “Map this documentation site and identify its authentication pages.”
- “Crawl up to five pages in this section; stay on this site.”
- “Use Tavily Research mini to compare these products using primary sources.”

## Research deadlines

Research can take several minutes. Hermes 0.22.2 does not support per-server
timeouts inside portable manifests. For longer calls, merge this entry into
the active profile's `config.yaml`:

```yaml
mcp_servers:
  tavily:
    url: https://mcp.tavily.com/mcp/
    timeout: 900
    strict_redirect_headers: true
    headers:
      Authorization: "Bearer ${TAVILY_API_KEY}"
      X-Client-Name: "hermes plugin"
```

A native `tavily` entry overrides the package's connection **as a whole**.
Keep both headers when changing the timeout, then restart the session. A timeout
does not prove the server-side research task was cancelled; do not automatically
submit a duplicate paid task.
The HTTP transport also has a 300-second read-inactivity limit; a longer tool
deadline does not prevent disconnects if the server sends no intervening events.

## Authentication

The default API key is resolved by Hermes for the active profile. This package
contains only a placeholder and never reads credential files, stores keys, or
refreshes tokens. The key travels in an HTTPS header, not the URL.

For OAuth, replace the native `tavily` entry with:

```yaml
mcp_servers:
  tavily:
    url: https://mcp.tavily.com/mcp/
    auth: oauth
    timeout: 900
    strict_redirect_headers: true
    headers:
      X-Client-Name: "hermes plugin"
```

Run `hermes mcp login tavily` interactively, then start a new session. Hermes
owns token storage and refresh. Complete login before unattended jobs; failures
require reauthorization, not a background browser prompt.
See [Hermes MCP authentication](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp#oauth-authentication)
and [Tavily authentication](https://docs.tavily.com/documentation/mcp#oauth-authentication).

## Data flow and attribution

- Requests go to `https://mcp.tavily.com/mcp/`. Queries, URLs, filters, and research
  instructions are sent to Tavily for processing. Calls use your Tavily plan.
- Every request includes **`X-Client-Name: hermes plugin`**, the HTTP equivalent
  of the Python SDK's `client_name="hermes plugin"`. This identifies the
  integration to Tavily. No separate analytics endpoint or collector is added.
- OAuth additionally contacts authorization endpoints discovered by Hermes.
- No local tool processes, background workers, or reads of local user files
  are implemented by this package. Hermes manages its configuration, secrets,
  logs, and MCP runtime.
- Catalog SHA pins cover this package. Tavily operates and updates the hosted
  service separately. The package never downloads replacement plugin code.
- Web content is untrusted evidence. The skill preserves task scope and
  rejects instructions embedded in retrieved pages.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| Missing key or HTTP 401 | Set a valid key for the active profile, or reauthorize OAuth. |
| No tools | Confirm the plugin is enabled, restart the session, and check MCP connection status. |
| Duplicate server warning | An existing native `tavily` entry wins over this package. Check its configuration. |
| Wrong attribution after override | Keep `X-Client-Name: "hermes plugin"` in the native entry. |
| Rate or credit limit | Check account limits; avoid repeated retries. |
| Research timeout | Configure the deadline above and investigate the existing request before rerunning. |
| Missing API parameter | Check the live MCP schema and capability coverage. Skills cannot add server inputs. |

## Development

The installed plugin is data and Markdown. Test dependencies are separate and
hash-pinned. With Python 3.14 and a Hermes checkout:

```bash
python -m venv .venv
# Activate .venv for your shell, then:
python -m pip install --require-hashes -r requirements-dev.txt
python scripts/test.py --hermes-source /path/to/hermes-agent
hermes plugins validate . --install-deps
```

Tests use temporary homes and synthetic keys to exercise Hermes admission,
skill discovery, profile isolation, missing credentials, attribution, and
redirect security. CI targets pinned stable/development Hermes revisions on
Linux, macOS, and Windows without paid calls or repository secrets.

See [catalog submission](docs/catalog-submission.md). Release evidence must
distinguish package tests, live tool execution, OAuth, and server-side attribution.

## License

[MIT](LICENSE), copyright Tavily AI.
