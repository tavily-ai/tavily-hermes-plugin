# Verification record

Checked 2026-10-21 on macOS with Python 3.14.6.

## Current package

The bundle contains six MCP-adapted skills from `tavily-ai/skills` at
`778122e5f9c680f541eeceda5a5b36405eb7980c`: Search, Extract, Map, Crawl,
Research, and Best Practices. CLI setup, Dynamic Search, and use-case skills
are outside this bundle. See [provenance](skill-provenance.md).

## Package checks

Eleven integration checks pass against:

- Hermes stable 0.22.2: `d923a5eb487a17c0a68801bba9ef0f56c81040a8`.
- Hermes development: `baf24532a1b95a07fd5505aadbe1faf169b4586b`.
- Additional development checkout: `46b5cfde4f120485183f447a22a75735e5e0b0e2`
  (upstream base `3f2afed3eb813cb00bd381d29b084d0e01de048f` plus a local,
  data-only catalog entry; submission remains paused).

The suite uses the real Hermes admission validator, portable loader, plugin
manager, and `skill_view`. It verifies all six skill names, authoring metadata,
enabled/disabled discovery, every skill and reference file, the OAuth and
API-key examples, profile credential isolation, missing credentials under
multiplexing, attribution, and redirect boundaries.

A separate contract check validates the operational JSON examples against the
hosted MCP schemas captured on 2026-10-21. Schema discovery used the actual
OAuth connection and made no paid tool calls. The snapshot is test data, not
a runtime parameter allowlist; the connected server remains authoritative.

Independent review found no remaining correctness/security issue in the
adaptations or package tests. Four SDK/API guides match the selected source
byte for byte; Search has only trailing-whitespace cleanup, and Integrations
contains the previously approved credential-example adaptations.

## Existing authentication and transport evidence

The MCP connection and authentication examples are unchanged from the
previously live-tested package. That verification covered real browser OAuth
login, fresh-process cached-token reuse, a real successful refresh after
simulated local expiry, and successful calls to all five tools. Every captured
MCP RPC used the stored OAuth token and exact `X-Client-Name: hermes plugin`
header. API-key Search, Extract, Map, and Research also returned useful content;
its earlier Crawl run encountered empty results and HTTP 429, while the OAuth
Crawl run returned content.

The user's manual test independently completed OAuth login and discovered all
five remote tools. Plugin enablement then failed because this machine's private
package index returned HTTP 401; it did not establish a package dependency
conflict. The separately configured MCP connection still worked, but a disabled
plugin did not expose its skills. The local manual launcher now selects the
public index for that dedicated test process. Global index settings are unchanged.

## Evidence limits

- Check the draft PR's exact commit and CI status before release.
- A successful MCP connection test does not prove plugin enablement or skill
  discovery; verify those separately in a fresh session.
- Revoked-token/consent-denial behavior and long `pro` Research were not live-tested.
- Attribution is verified on outgoing requests; production analytics ingestion
  was not queried.
- Skills guide model behavior; they do not enforce deterministic request quotas.
- SDK/API references are developer guidance. Every integration example has not
  been executed as an application test.

The repository remains internal. The public-clone prerequisite and maintainer
catalog review are not complete, so catalog submission remains paused.
