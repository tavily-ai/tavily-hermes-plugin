# Tavily for Hermes Agent

Tavily gives Hermes Agent current information from the web. With this plugin, Hermes can search the web and cite its sources, read the full text of any page, map and crawl a documentation site, and run multi-source research that returns a cited report.

The plugin connects Hermes to Tavily's hosted MCP server, so nothing runs on your machine. It also bundles Tavily skills that tell Hermes which tool fits a task, how to apply domain and date filters, and how to verify what it retrieved before relying on it.

## Install

```bash
hermes plugins install tavily-ai/tavily-hermes-plugin
```

The plugin requires Hermes Agent 0.22.2 or later with MCP support installed. After installing, connect your Tavily account with one of the two methods below. Use the same Hermes profile for installation, configuration, login, and chat.

### OAuth (recommended)

OAuth lets you sign in to Tavily in the browser while Hermes stores and refreshes the tokens. Merge [this connection](examples/oauth.yaml) into your active profile's `config.yaml`, replacing any existing `mcp_servers.tavily` entry and keeping the other servers in the file:

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

Then sign in from a terminal:

```bash
hermes mcp login tavily
```

You do not need a `TAVILY_API_KEY` for this connection. Do not add an `Authorization` header, because Hermes supplies the OAuth bearer token.

The config step is needed because the portable plugin format in Hermes 0.22.2 cannot declare OAuth. A native `tavily` entry in `config.yaml` takes precedence over the API-key connection packaged with the plugin. The plugin never edits your profile or handles tokens itself.

For unattended runs, complete the login first. If a token refresh is rejected, run `hermes mcp login tavily` again, since background jobs cannot complete browser consent. See [Hermes OAuth](https://hermes-agent.nousresearch.com/docs/user-guide/features/mcp#oauth-authenticated-http-servers) and [Tavily OAuth](https://docs.tavily.com/documentation/mcp#oauth-authentication) for details.

### API key

Use an API key for automation or when you want requests billed to a specific project key. Set `TAVILY_API_KEY` through Hermes's API-key settings for the active profile, and keep the key out of chat, URLs, and this repository.

The plugin's `mcp.json` uses this key whenever there is no native `tavily` entry in `config.yaml`. To get the longer research timeout, or to switch from OAuth, replace the native entry with [the API-key connection](examples/api-key.yaml):

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

Replace the whole entry when switching methods so that `auth: oauth` is removed. Hermes resolves the placeholder from the active profile.

### Verify the connection

If you added a native `mcp_servers.tavily` entry, run `hermes mcp test tavily`. It should discover five Tavily tools. Hermes 0.22.2 cannot test the packaged API-key connection this way, so check that setup in a fresh chat instead. If Hermes reports that the MCP SDK or HTTP transport is unavailable, install the MCP optional feature following your Hermes version's instructions.

Start a new session, ask Hermes to find and load `tavily-search` with `skills_list` and `skill_view`, and then try a prompt such as:

> Search Tavily's official documentation for search-depth options and cite the sources.

Hermes prefixes skill names to avoid collisions, so use `skills_list` to find the full name.

## Tools and skills

| Hermes tool | Use |
| --- | --- |
| `mcp__tavily__tavily_search` | Find sources on the web |
| `mcp__tavily__tavily_extract` | Read content from known URLs |
| `mcp__tavily__tavily_map` | Discover URLs on a website |
| `mcp__tavily__tavily_crawl` | Collect content from a bounded website section |
| `mcp__tavily__tavily_research` | Produce a multi-source research report |

| Skill | Use |
| --- | --- |
| [tavily-search](skills/tavily-search/SKILL.md) | Find web sources with supported domain and date controls. |
| [tavily-extract](skills/tavily-extract/SKILL.md) | Read clean content from selected URLs. |
| [tavily-map](skills/tavily-map/SKILL.md) | Discover URLs before choosing pages to read. |
| [tavily-crawl](skills/tavily-crawl/SKILL.md) | Collect content from a bounded website section. |
| [tavily-research](skills/tavily-research/SKILL.md) | Produce multi-source research with citations. |
| [tavily-best-practices](skills/tavily-best-practices/SKILL.md) | Plan reliable MCP retrieval and verification workflows. |

The skills are adapted from [tavily-ai/skills](https://github.com/tavily-ai/skills) to call the MCP tools above, so none of them needs the Tavily CLI, an SDK, or a separate login. The CLI setup and Dynamic Search skills are not included because they depend on the CLI. [Skill provenance](docs/skill-provenance.md) lists the source commit and every adaptation.

The plugin exposes the tools and parameters that Tavily's hosted MCP server advertises, which can differ from Tavily's direct API; see [capability coverage](docs/capability-coverage.md). It does not change which provider Hermes's built-in `web_search` and `web_extract` use.

## Research timeouts

Both native connection examples set a 900-second tool timeout. Hermes 0.22.2 does not support per-server timeouts in portable manifests, so the packaged API-key connection uses Hermes's default timeout.

The HTTP transport also disconnects after 300 seconds without data, regardless of the tool timeout. A client-side timeout does not cancel the research task on Tavily's side, so check the existing task before submitting another paid request.

## Data flow and attribution

- Requests go to `https://mcp.tavily.com/mcp/`, where Tavily processes your queries, URLs, filters, and research instructions under your Tavily account.
- Both connection examples send the header `X-Client-Name: hermes plugin`, which matches the Python SDK's `client_name="hermes plugin"`.
- With OAuth, Hermes also contacts the authorization endpoints it discovers. Hermes owns configuration, credential storage, token refresh, and the MCP runtime.
- The plugin runs no local processes, background workers, credential-file readers, self-updaters, or analytics collectors.
- The skills treat retrieved web content as untrusted and ignore instructions embedded in pages.

## Troubleshooting

| Symptom | Action |
| --- | --- |
| OAuth authorization fails or expires | Run `hermes mcp login tavily` interactively in the correct profile. |
| Missing API key or HTTP 401 with API-key setup | Configure a valid key in that profile. |
| No tools | Confirm the connection and plugin are enabled, then restart the session. |
| Duplicate server warning | This is expected, because a native `tavily` entry takes precedence over the packaged connection. |
| Wrong attribution after changing configuration | Keep `X-Client-Name: "hermes plugin"` in the native entry. |
| Rate or credit limit | Check account limits and avoid repeated retries. |
| Research timeout | See the timeouts above and check the existing request before rerunning. |

## Development

The installed plugin contains only data and Markdown. Test dependencies are separate and hash-pinned. With Python 3.14 and a Hermes checkout:

```bash
python -m venv .venv
# Activate .venv for your shell, then:
python -m pip install --require-hashes -r requirements-dev.txt
python scripts/test.py --hermes-source /path/to/hermes-agent
hermes plugins validate . --install-deps
```

Tests use temporary profiles and synthetic credentials to cover admission, skill discovery, both connection configurations, profile isolation, attribution, and redirect handling. CI runs against pinned stable and development Hermes revisions on Linux, macOS, and Windows without paid calls or repository secrets.

See [verification](docs/verification.md) for live test evidence and [catalog submission](docs/catalog-submission.md) for the listing process.

## License

[MIT](LICENSE), copyright Tavily AI.
