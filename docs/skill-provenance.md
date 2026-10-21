# Skill provenance

This package reuses all eight skills from
[`tavily-ai/tavily-grok-plugin` at `0cfd0c2`](https://github.com/tavily-ai/tavily-grok-plugin/tree/0cfd0c2be2df4a2a90c683abaadaf36ef7f2f59d/skills).
The full source commit is `0cfd0c2be2df4a2a90c683abaadaf36ef7f2f59d`.
Tavily's MIT license and original source metadata are retained. Frontmatter
credits the Hermes adaptation separately from the original Tavily skills.

| Source skill | Hermes skill |
| --- | --- |
| `tavily-web` | Same name and web-research workflow. |
| `tavily-best-practices` | Same name, SDK/API examples, and six reference guides. |
| `academic-scientific-research` | Same name, workflow, and evidence-brief template. |
| `investment-research-briefs` | Same name, workflow, and investment-brief template. |
| `product-competitor-intelligence` | Same name, workflow, and product-comparison template. |
| `sales-account-intelligence` | Same name, workflow, and account-brief template. |
| `threat-intelligence-enrichment` | Same name, workflow, and threat-brief template. |
| `vendor-risk-kyc-screening` | Same name, workflow, and risk-brief template. |

## Hermes adaptations

- Descriptions are at most 60 characters, end with a period, and describe the
  capability. The original longer descriptions remain in `When to Use`.
- Existing content is arranged into the required `When to Use`, `Prerequisites`,
  `How to Run`, `Quick Reference`, `Procedure`, `Pitfalls`, and `Verification`
  sections. Research budgets and source-selection guidance are preserved.
- Tool references use Hermes's `mcp__tavily__tavily_*` names. The web skill points
  to Hermes's OAuth login and profile configuration.
- The six specialized skills' original Markdown output templates are moved
  unchanged into `templates/brief.md`, linked from their skills, and readable
  through Hermes's `skill_view` tool.
- Added prerequisites and verification checks require the current MCP schema,
  source citations, bounded scope, and normal Hermes approval handling.
- The developer skill explicitly distinguishes application SDK/API credentials
  and parameters from the Hermes plugin's MCP OAuth connection and live schema.

Four developer reference files are copied byte for byte: `sdk.md`, `extract.md`,
`crawl.md`, and `research.md`. In `search.md`, two trailing spaces are removed;
its text and examples are unchanged. In `integrations.md`, the Hermes
admission scanner rejected illustrative key assignments and `os.environ`
access. Those credential examples now direct developers to configure credentials
externally and use SDK credential defaults. The integration workflows and
remaining examples are preserved.

The package contains no executable skill scripts. Reference code is developer
documentation; it is not executed during plugin installation or discovery.
