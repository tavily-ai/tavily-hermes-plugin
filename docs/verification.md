# Verification record

Checked 2026-10-20–21 on macOS with Python 3.14.6.

## Package compatibility

Ten integration checks pass against these Hermes checkouts:

- Hermes stable 0.22.2: `d923a5eb487a17c0a68801bba9ef0f56c81040a8`.
- Hermes development: `baf24532a1b95a07fd5505aadbe1faf169b4586b`.
- Current tested development checkout: `46b5cfde4f120485183f447a22a75735e5e0b0e2`
  (upstream base `3f2afed3eb813cb00bd381d29b084d0e01de048f` plus the local
  data-only catalog entry). Both the ten local checks and OAuth token-reuse
  call used this checkout.

The tests exercise the actual Hermes admission validator and security scanner,
portable loader, enabled/disabled discovery, skill resolution, credential
interpolation, missing credentials under multiplexing, and redirect handling.
The two connection-example checks also verify that native OAuth replaces the
packaged API-key configuration without inheriting its Authorization header or
requiring a key, and that the API-key alternative uses the active profile's key.
Admission returns `safe`, with no warnings or skipped components. The suite
also passes in a clean environment containing only `requirements-dev.txt`.

[GitHub Actions run 39625518923](https://github.com/tavily-ai/tavily-hermes-plugin/actions/runs/39625518923)
passed all six jobs at package commit
`3a9e913b5ff946795c7fdff80730cfab2a8642b0`: Linux, macOS, and Windows,
each against the stable and development Hermes revisions above. Each job ran
the same ten integration checks. Check the PR's latest run before release.

An independent review found no package correctness/security blocker. Its
research read-inactivity caveat is documented in the README.

## Live API-key execution

The package was copied into an isolated Hermes profile, enabled, discovered
through `PluginManager`, and connected through Hermes's `MCPServerTask` and
MCP SDK 2.3.0. The authenticated hosted server advertised all five tools.

| Tool | Observed result |
| --- | --- |
| Search | One source returned for a bounded IANA query. |
| Extract | One extracted page returned for `https://example.com`. |
| Map | One URL returned from the Tavily documentation site. |
| Research | `mini` reached `completed` and returned a nonempty report. |
| Crawl | Requests completed with empty result sets for two targets; a subsequent two-page check on Tavily's site returned HTTP 429. Useful crawl content remains unverified. |

Actual HTTP requests from Hermes were captured without recording credentials.
All ten captured requests in the five-tool run carried the exact header
`X-Client-Name: hermes plugin` and the intended bearer credential. The current
shared MCP source at `835129d1a9f6d7a03c9a569234ea4f5be4cedc7c` also preserves
that header in `get_client_name()` and `build_request_headers()`.

## Remaining release evidence

- Useful Crawl content passed in the OAuth run below. The earlier API-key Crawl
  run remains limited to empty responses and a provider HTTP 429.
- OAuth login, cached-token reuse, and successful refresh passed. Revoked refresh
  tokens and consent denial were not tested against the live service.
- Stored attribution in Tavily's production analytics was not queried.
  Client-side header capture plus source inspection does not prove ingestion.
- Long `pro` research spanning the HTTP read-inactivity deadline was not tested.

## Live OAuth execution (2026-10-21)

Used an isolated Hermes profile with the installed plugin and the configuration
in `examples/oauth.yaml`. No `TAVILY_API_KEY` or static Authorization header was
configured. Hermes stable 0.22.2 and MCP SDK 2.3.0 performed the authentication;
the package did not implement its own OAuth client.

1. Ran the same Hermes login implementation used by `hermes mcp login tavily`.
   The real browser callback displayed **Authorization Successful**. Hermes
   verified that tokens were stored and reported all five available tools.
2. Started a fresh process with browser interaction disabled. The cached OAuth
   token authenticated a Search call that returned a source.
3. Marked only the isolated profile's cached token expiry as past due, then
   started another process with browser interaction disabled. Hermes sent a real
   `grant_type=refresh_token` request to Tavily's `/token` endpoint, received
   HTTP 200, stored a different access token, and completed the calls below.
4. Started a fresh process against the current development checkout using the
   updated package and its OAuth example. It reused the refreshed token and
   returned a Search result without an API key or another browser login.

| OAuth tool call after refresh | Result |
| --- | --- |
| Search | One source for a bounded IANA query. |
| Extract | One extracted page from `https://example.com`. |
| Map | One URL from the Tavily documentation site. |
| Crawl | One page from `https://www.tavily.com`. |
| Research | `mini` reached `completed` with a nonempty report. |

HTTP request hooks captured authentication checks after the SDK injected the
bearer token. Every captured MCP RPC used the stored OAuth access token and
`X-Client-Name: hermes plugin`. Evidence records only boolean token comparisons
and non-secret request metadata; access and refresh token values were not logged.
This verifies client-side attribution, not its storage in Tavily analytics.

## Live agent conversation (2026-10-21)

Ran the actual Hermes `AIAgent.run_conversation()` loop with the installed
package at `3a9e913b5ff946795c7fdff80730cfab2a8642b0`, Hermes development
`baf24532a1b95a07fd5505aadbe1faf169b4586b`, and the real `z-ai/glm-5.2`
model through Nous. The isolated profile used `examples/oauth.yaml`, the cached
OAuth token, and no Tavily API key. Missing Hermes development dependencies were
installed into an isolated test environment.

The prompt asked the agent to load the Tavily skill, find IANA's explanation of
example.com with one Search result restricted to `iana.org`, Extract the returned
page, and answer with a citation. The model loaded the installed skill, requested
the live tool schemas, and called Search and Extract through Hermes's normal
deferred-tool dispatcher. It finished normally after four model calls with a
cited answer using `https://www.iana.org/help/example-domains`.

Both Tavily tool requests returned HTTP 200. Search returned one source; Extract
returned one page with 939 characters of content and no failed results. Assertions
checked the actual response payloads, provider request IDs, the selected URL,
the final citation, and successful conversation completion. Every captured MCP
RPC used the stored OAuth token and exact `X-Client-Name: hermes plugin` header.
The request hooks observed real traffic; model and Tavily responses were not
mocked.

This covers the agent conversation through Search and Extract. Map, Crawl, and
Research were exercised directly through Hermes's MCP runtime in the OAuth run
above. Terminal UI interactions and production analytics ingestion were not
part of this conversation test.

Do not describe these remaining checks as passed or describe this package as
an approved Hermes catalog listing until the corresponding evidence exists.
