# Skill provenance

The source is [`tavily-ai/skills` at `778122e`](https://github.com/tavily-ai/skills/tree/778122e5f9c680f541eeceda5a5b36405eb7980c/skills).
The full source commit is `778122e5f9c680f541eeceda5a5b36405eb7980c`.
Tavily's MIT license and source attribution are retained. Skill frontmatter
credits the Hermes adaptation separately from Tavily's original material.

## Included skills

- `tavily-search`
- `tavily-extract`
- `tavily-map`
- `tavily-crawl`
- `tavily-research`
- `tavily-best-practices`

This is the user-selected MCP bundle. `tavily-cli` and
`tavily-dynamic-search` are excluded because their setup and disk-filtering
workflows depend on the Tavily CLI. No use-case skills are bundled.

## MCP adaptations

The operational skills preserve their source tasks: discover sources, extract
selected pages, map before broad collection, bound crawls, and reserve Research
for multi-source synthesis. Source selection, evidence verification, extraction
failure checks, and research model selection are retained.

CLI invocations are replaced with examples for Hermes's
`mcp__tavily__tavily_*` tools. Command flags become MCP arguments where the
advertised schema supports them: for example, `--depth` becomes
`search_depth`, hyphenated names become underscored argument names, domain/path
lists become JSON arrays, and external-link selection becomes a boolean.
The current hosted schemas were read on 2026-10-21; the examples are checked
against that interface in the package tests.

The source CLI's installation, keyless login, automatic skill refresh, output
files, and separate Research polling commands are not presented as MCP
features. OAuth and API-key instructions use Hermes's profile-aware connection
configuration. No Tavily CLI process or separate CLI authentication is required.
Only inputs in the live MCP schema are documented as operational controls.

Descriptions are shortened to at most 60 characters and end with a period.
Content follows Hermes's required section order. Qualified skill names are
discovered using `skills_list`; `skill_view` loads skills and references.
Rate/credit errors stop the workflow; failed attempts count against the user's
request budget. These are agent instructions rather than runtime quota guards.

## Developer references

`tavily-best-practices` keeps the official SDK/API material and explicitly
distinguishes application credentials and API parameters from the plugin's
MCP OAuth connection and advertised tool inputs.

Four guides are byte-identical to the selected source: `sdk.md`, `extract.md`,
`crawl.md`, and `research.md`. `search.md` has only two trailing spaces removed.
In `integrations.md`, the previously approved changes replace credential
assignments and `os.environ` examples with external application configuration
and SDK credential defaults, so Hermes's admission scanner passes.

SDK install commands and examples are developer documentation, executed only
within requested development work and Hermes approvals. The plugin has no
executable runtime or skill scripts.
