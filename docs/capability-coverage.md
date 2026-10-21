# Hosted MCP capability coverage

Verified on 2026-10-20 using an authenticated `initialize` and `tools/list`
against `https://mcp.tavily.com/mcp/`. The server reported version `4.1.0`.
This is an observation of the hosted interface, not a guarantee that a server
version uniquely identifies every deployment.

All five tools are connected without a plugin-side parameter allowlist.
Hermes discovers their schemas from the server, so supported additions become
available on reconnection. The catalog commit pins this package's configuration
and instructions; it does not pin the hosted service's implementation.

## API options absent from the observed MCP inputs

| Tool | Options in API documentation but absent from the MCP schema |
| --- | --- |
| Search | `chunks_per_source`, `include_published_date`, `filter_by_published_date`, `include_answer`, `include_domains_mode`, `language`, `filter_by_language`, `auto_parameters`, `include_usage`, `safe_search`; `topic="finance"` is not an allowed MCP topic. |
| Extract | `chunks_per_source`, `timeout`, `include_usage`. |
| Crawl | `chunks_per_source`, `exclude_paths`, `exclude_domains`, `include_images`, `timeout`, `include_usage`. |
| Map | `exclude_paths`, `exclude_domains`, `timeout`, `include_usage`. |
| Research | `stream`, `output_schema`, `citation_format`, `include_domains`, `exclude_domains`, `output_length`, `files`. Only `input` and `model` are exposed. |

Search already exposes all four depths: `basic`, `advanced`, `fast`, and
`ultra-fast`. It also exposes `exact_match`, date ranges, and domain filters.
The current MCP does not advertise standalone usage, logs, feedback, or
research-status tools.

These are per-call schema gaps. A server's `DEFAULT_PARAMETERS` header is not a
substitute for exposing typed arguments, particularly for research, and this
package does not inject undocumented defaults. Full API parity requires changes
to the shared Tavily MCP server and a deployment followed by a new schema check.

## Verification boundaries

- Package tests exercise the real Hermes loader, admission scanner, secret
  interpolation, and HTTP redirect boundary with synthetic credentials.
- The fixed outgoing header is `X-Client-Name: hermes plugin`, corresponding to
  the Python SDK's `client_name="hermes plugin"` transport value.
- A client-side capture proves what leaves Hermes. Verifying the final stored
  attribution requires a Tavily-side trace or analytics lookup for a real
  request; do not claim that from a successful search alone.
- Authentication here uses an API key managed by Hermes. OAuth is a separate
  native MCP configuration option described in the README.

## Official sources

- [MCP](https://docs.tavily.com/documentation/mcp)
- [Search](https://docs.tavily.com/documentation/api-reference/endpoint/search)
- [Extract](https://docs.tavily.com/documentation/api-reference/endpoint/extract)
- [Crawl](https://docs.tavily.com/documentation/api-reference/endpoint/crawl)
- [Map](https://docs.tavily.com/documentation/api-reference/endpoint/map)
- [Research](https://docs.tavily.com/documentation/api-reference/endpoint/research)
