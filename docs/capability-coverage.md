# Tavily MCP capabilities

This plugin connects Hermes to Tavily's hosted MCP server and includes a skill
for web research with source citations.

| Tool | Capability |
| --- | --- |
| `tavily_search` | Find sources on the web with the search controls advertised by the server. |
| `tavily_extract` | Read content from specified URLs. |
| `tavily_map` | Discover URLs on a website. |
| `tavily_crawl` | Collect content from a bounded website section. |
| `tavily_research` | Produce a report using multiple sources. |

Hermes discovers the tool schemas directly from Tavily. The plugin does not
maintain a parameter allowlist; server additions become available when Hermes
refreshes its connection. Availability may differ from Tavily's direct API.

OAuth and API-key connections use the same hosted MCP service. Authentication
does not add parameters to the tool schemas. Choose one connection method using
the [setup instructions](../README.md#install-and-connect).

Research can take several minutes. See the README's
[research deadlines](../README.md#research-deadlines) before running long tasks.
The catalog commit pins the plugin's configuration and instructions. Tavily
operates and updates the hosted service separately.

See [Tavily MCP documentation](https://docs.tavily.com/documentation/mcp) for
the service and [verification](verification.md) for the tested package behavior.
