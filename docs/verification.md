# Verification record

Checked 2026-10-20–21 on macOS with Python 3.14.6.

## Package compatibility

Eight integration checks pass against both:

- Hermes stable 0.22.2: `d923a5eb487a17c0a68801bba9ef0f56c81040a8`.
- Hermes development: `baf24532a1b95a07fd5505aadbe1faf169b4586b`.

The tests exercise the actual Hermes admission validator and security scanner,
portable loader, enabled/disabled discovery, skill resolution, credential
interpolation, missing credentials under multiplexing, and redirect handling.
Admission returns `safe`, with no warnings or skipped components. The suite
also passes in a clean environment containing only `requirements-dev.txt`.

An independent review found no package correctness/security blocker. Its
research read-inactivity caveat is documented in the README.

## Live execution

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

- Check useful Crawl results after the account's provider limits permit it.
- OAuth browser login, refresh, and unattended expiry behavior were not
  exercised. The default API-key route was exercised.
- Stored attribution in Tavily's production analytics was not queried.
  Client-side header capture plus source inspection does not prove ingestion.
- Long `pro` research spanning the HTTP read-inactivity deadline was not tested.
- CI defines Linux, macOS, and Windows jobs; local results prove macOS only.
  Review the actual workflow results for the final pushed commit.
- Full direct-API parameter coverage requires a shared MCP update; see
  [capability coverage](capability-coverage.md).

Do not describe these remaining checks as passed or describe this package as
an approved Hermes catalog listing until the corresponding evidence exists.
