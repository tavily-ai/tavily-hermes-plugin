---
name: tavily-best-practices
description: Build Tavily integrations using SDK and API guidance.
version: 1.0.0
author: Mani Srinivasan (@manisrinivasan2k1), Hermes adaptation; Tavily, original skills
license: MIT
compatibility: Requires the Tavily MCP connection supplied by this Hermes plugin.
metadata:
  source: https://github.com/tavily-ai/tavily-grok-plugin/tree/0cfd0c2be2df4a2a90c683abaadaf36ef7f2f59d/skills/tavily-best-practices
  grok_source: https://github.com/tavily-ai/tavily-grok-plugin/tree/0cfd0c2be2df4a2a90c683abaadaf36ef7f2f59d/skills/tavily-best-practices
  grok_commit: 0cfd0c2be2df4a2a90c683abaadaf36ef7f2f59d
---

# Tavily Best Practices Skill

Tavily is a search API designed for LLMs, enabling AI applications to access real-time web data.
This skill documents SDK and API development; inspect the connected MCP schema
when using the Hermes plugin's tools.

## When to Use

Build production-ready Tavily integrations with best practices baked in. Reference documentation for developers using coding assistants (Claude Code, Cursor, etc.) to implement web search, content extraction, crawling, and research in agentic workflows, RAG systems, or autonomous agents.

## Prerequisites

Use this guidance when the user asks to implement or review a Tavily integration.
SDK/API examples require the target application's own Tavily API credentials;
Hermes's MCP OAuth login authenticates its MCP connection. Never read Hermes
credential files or use its OAuth tokens in generated application code.

## How to Run

### Installation

**Python:**
```bash
pip install tavily-python
```

**JavaScript:**
```bash
npm install @tavily/core
```

See **[references/sdk.md](references/sdk.md)** for complete SDK reference.

### Client Initialization

```python
from tavily import TavilyClient

# Uses TAVILY_API_KEY env var (recommended)
client = TavilyClient()

#With project tracking (for usage organization)
client = TavilyClient(project_id="your-project-id")

# Async client for parallel queries
from tavily import AsyncTavilyClient
async_client = AsyncTavilyClient()
```

## Quick Reference

### Choosing the Right Method

**For custom agents/workflows:**

| Need | Method |
|------|--------|
| Web search results | `search()` |
| Content from specific URLs | `extract()` |
| Content from entire site | `crawl()` |
| URL discovery from site | `map()` |

**For out-of-the-box research:**

| Need | Method |
|------|--------|
| End-to-end research with AI synthesis | `research()` |

#### search() - Web Search

```python
response = client.search(
    query="quantum computing breakthroughs",  # Keep under 400 chars
    max_results=10,
    search_depth="advanced"
)
print(response)
```
Key parameters: `query`, `max_results`, `search_depth` (ultra-fast/fast/basic/advanced), `include_domains`, `exclude_domains`, `time_range`

See **[references/search.md](references/search.md)** for complete search reference.

#### extract() - URL Content Extraction

```python
# Simple one-step extraction
response = client.extract(
    urls=["https://docs.example.com"],
    extract_depth="advanced"
)
print(response)
```
Key parameters: `urls` (max 20), `extract_depth`, `query`, `chunks_per_source` (1-5)

See **[references/extract.md](references/extract.md)** for complete extract reference.

#### crawl() - Site-Wide Extraction

```python
response = client.crawl(
    url="https://docs.example.com",
    instructions="Find API documentation pages",  # Semantic focus
    extract_depth="advanced"
)
print(response)
```
Key parameters: `url`, `max_depth`, `max_breadth`, `limit`, `instructions`, `chunks_per_source`, `select_paths`, `exclude_paths`

See **[references/crawl.md](references/crawl.md)** for complete crawl reference.

#### map() - URL Discovery

```python
response = client.map(
    url="https://docs.example.com"
)
print(response)
```

#### research() - AI-Powered Research

```python
import time

# For comprehensive multi-topic research
result = client.research(
    input="Analyze competitive landscape for X in SMB market",
    model="pro"  # or "mini" for focused queries, "auto" when unsure
)
request_id = result["request_id"]

# Poll until completed
response = client.get_research(request_id)
while response["status"] not in ["completed", "failed"]:
    time.sleep(10)
    response = client.get_research(request_id)

print(response["content"])  # The research report
```

Key parameters: `input`, `model` ("mini"/"pro"/"auto"), `stream`, `output_schema`, `citation_format`

See **[references/research.md](references/research.md)** for complete research reference.

## Procedure

Read the relevant guide below before implementing the requested method. Check
current official documentation for version-specific behavior, keep credentials
in the target application's supported secret configuration, and test the
requested integration before reporting it as working.

### Detailed Guides

For complete parameters, response fields, patterns, and examples:

- **[references/sdk.md](references/sdk.md)** - Python & JavaScript SDK reference, async patterns, Hybrid RAG
- **[references/search.md](references/search.md)** - Query optimization, search depth selection, domain filtering, async patterns, post-filtering
- **[references/extract.md](references/extract.md)** - One-step vs two-step extraction, query/chunks for targeting, advanced mode
- **[references/crawl.md](references/crawl.md)** - Crawl vs Map, instructions for semantic focus, use cases, Map-then-Extract pattern
- **[references/research.md](references/research.md)** - Prompting best practices, model selection, streaming, structured output schemas
- **[references/integrations.md](references/integrations.md)** - LangChain, LlamaIndex, CrewAI, Vercel AI SDK, and framework integrations

## Pitfalls

These references describe Tavily SDKs and the direct API. They do not declare
additional parameters on the Hermes MCP connection. Use the live MCP schema
when invoking `mcp__tavily__tavily_search`, `mcp__tavily__tavily_extract`,
`mcp__tavily__tavily_map`, `mcp__tavily__tavily_crawl`, or
`mcp__tavily__tavily_research`.

Installation commands and example programs are development instructions. Run
them only within the user's requested work and Hermes approval rules. Bound
research polling to the application's deadline and handle failed tasks.

## Verification

- The chosen SDK/API method matches the target application's requirements.
- Installed versions and parameters were checked against current official docs.
- Authentication and failures were exercised without logging credentials.
- The requested application behavior was tested with representative input.
