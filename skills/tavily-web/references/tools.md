# Tavily MCP tool guidance

Use the current tool schema to validate arguments. These examples match the
hosted server observed on 2026-10-20 (server version 4.1.0).

## Search

`mcp__tavily__tavily_search` accepts `query`, `max_results`, `search_depth`,
`topic`, `time_range`, `start_date`, `end_date`, `include_domains`,
`exclude_domains`, `country`, `exact_match`, `include_images`,
`include_image_descriptions`, `include_raw_content`, and `include_favicon`.

Choose `basic` for ordinary questions, `advanced` for deeper source discovery,
`fast` for lower latency with relevance, or `ultra-fast` when latency dominates.
Use the schema's supported `topic` values (`general` and `news` at verification).
Date inputs use `YYYY-MM-DD`; time ranges are `day`, `week`, `month`, or `year`.

Example arguments for official documentation discovery:

```json
{
  "query": "Tavily API search filters documentation",
  "search_depth": "advanced",
  "max_results": 5,
  "include_domains": ["docs.tavily.com"]
}
```

## Extract

`mcp__tavily__tavily_extract` accepts `urls`, `query`, `extract_depth`,
`format`, `include_images`, and `include_favicon`.

Use `query` to focus content on a question. Start with `basic` extraction;
`advanced` can help with complex pages and tables. Choose `markdown` to retain
structure or `text` for plain text. Inspect failed results as well as successes.

```json
{
  "urls": ["https://docs.tavily.com/documentation/api-reference/endpoint/search"],
  "query": "Search depth and domain filtering",
  "format": "markdown"
}
```

## Map and crawl

Both tools accept `url`, `instructions`, `max_depth`, `max_breadth`, `limit`,
`select_paths`, `select_domains`, and `allow_external`.
`mcp__tavily__tavily_crawl` additionally accepts `extract_depth`, `format`, and
`include_favicon`; `mcp__tavily__tavily_map` returns URL discovery results.

Use map followed by extract for a few selected pages. Use crawl when the task
needs content across a section. Keep traversal and output bounded:

```json
{
  "url": "https://docs.tavily.com",
  "instructions": "Find the search and extract API reference pages",
  "max_depth": 1,
  "max_breadth": 5,
  "limit": 5,
  "select_paths": ["/documentation/api-reference/.*"],
  "allow_external": false
}
```

Do not invent `exclude_paths` or `exclude_domains` if they are absent from the
MCP schema. A selection regex is not always equivalent to an exclusion rule.

## Research

`mcp__tavily__tavily_research` currently accepts `input` and `model`.
Choose `mini`, `pro`, or `auto`. The server manages research submission and
polling; the tool returns a report or an error, rather than a caller-managed
stream. The client must allow sufficient time for the selected model.

```json
{
  "input": "Compare Tavily Search and Extract using official documentation. Explain when to use each, cite sources, and distinguish findings from inference.",
  "model": "mini"
}
```

Research instructions can request sections and sources, but cannot guarantee
the enforcement of an unavailable API-level output schema or domain filter.
For strict source restrictions, use search/extract with supported filters and
verify the returned source domains before synthesis.

## Sources

- [Tavily MCP](https://docs.tavily.com/documentation/mcp)
- [Search API](https://docs.tavily.com/documentation/api-reference/endpoint/search)
- [Extract API](https://docs.tavily.com/documentation/api-reference/endpoint/extract)
- [Crawl API](https://docs.tavily.com/documentation/api-reference/endpoint/crawl)
- [Map API](https://docs.tavily.com/documentation/api-reference/endpoint/map)
- [Research API](https://docs.tavily.com/documentation/api-reference/endpoint/research)
