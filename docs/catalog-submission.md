# Catalog submission

A Tavily owner or major contributor submits a PR to `NousResearch/hermes-agent`.
Nous maintainers review and merge the entry; there is no self-service publishing.

1. Run package tests and `hermes plugins validate /path/to/plugin --install-deps`.
2. Push the reviewed package commit and resolve its full 40-character SHA.
3. In a separate Hermes branch, add `plugin-catalog/tavily.yaml` using the
   metadata below and the **real pushed SHA**. Never submit a branch, tag,
   short SHA, or placeholder.
4. Run Hermes's catalog schema check and plugin validation at that exact commit.
   Review every scanner warning.
5. Include the disclosures below and verification evidence in the PR. Request
   vendor verification in prose; only Nous maintainers set `tier: verified`.

```yaml
name: tavily
repo: https://github.com/tavily-ai/tavily-hermes-plugin
# sha: insert the reviewed, pushed 40-character commit SHA
description: Web search, extraction, website mapping and crawling, and research through Tavily MCP, with a web research skill.
maintainer: tavily-ai
tier: community
category: web
requires_hermes: ">=0.22.2"
docs_url: https://github.com/tavily-ai/tavily-hermes-plugin
version: "1.0.0"
platforms: []
capabilities:
  provides_tools: []
  provides_hooks: []
  provides_middleware: []
  requires_env: [TAVILY_API_KEY]
```

The tool, hook, and middleware lists are empty because the package does not
register native Python capabilities. The default MCP connection requires
`TAVILY_API_KEY`, so declare it in `requires_env`. Disclose the remotely
discovered tools and the recommended native OAuth setup explicitly. OAuth users
do not need an API key; the declaration describes the packaged fallback. Do not put
remote MCP tool names in the native `provides_tools` list.

## Disclosures for the PR

- Tavily-maintained portable package inspired by `tavily-ai/tavily-grok-plugin`;
  no fork of a Hermes bundled provider.
- HTTPS requests to `mcp.tavily.com`; Tavily processes queries, URLs, and research
  instructions, using account credits.
- Fixed attribution: `X-Client-Name: hermes plugin`.
- Recommended interactive setup uses Hermes-managed OAuth. The portable package
  supplies API-key authentication when no native connection overrides it; the
  README and examples explicitly separate the two methods.
- No runtime dependencies, local executables, shell commands, background
  workers, credential-file reads, core overrides, or self-updater.
- Five remotely discovered tools and one bundled skill; no Desktop renderer code.
- Research may take minutes; stable Hermes needs the documented native timeout
  override for longer calls. The hosted service updates separately from this pin.
- Link capability coverage and identify the live calls, auth modes, and
  attribution checks that were actually tested.

Updates require a new SHA-bump PR and review of the commit range. Keep the
manifest version and catalog label aligned and the SemVer floor truthful.

See the authoritative [catalog policy](https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/catalog-submission).
