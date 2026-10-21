"""Integration contracts for the shipped package, using Hermes's real loader."""

import json
import os
from pathlib import Path
import re
import shutil
import tempfile
import unittest
from unittest.mock import patch

import httpx

from agent.secret_scope import reset_multiplex_context, reset_secret_scope, set_multiplex_context, set_secret_scope
from hermes_cli.agent_plugins import load_agent_plugin
from hermes_cli.plugin_validate import validate_plugin_dir
from tools.mcp_tool_config import _interpolate_env_vars, _load_mcp_config, _require_rendered_remote
from tools.mcp_tool_errors import _make_redirect_header_stripper

ROOT = Path(__file__).resolve().parents[1]
EXPECTED_SKILLS = {
    "academic-scientific-research", "investment-research-briefs",
    "product-competitor-intelligence", "sales-account-intelligence",
    "tavily-best-practices", "tavily-web", "threat-intelligence-enrichment",
    "vendor-risk-kyc-screening",
}


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="tavily-package-")
        self.addCleanup(self.temp.cleanup)
        self.package = load_agent_plugin(ROOT, Path(self.temp.name))

    def test_hermes_admission_has_no_warnings_or_skipped_components(self):
        report = validate_plugin_dir(ROOT)
        self.assertTrue(report.ok, report.to_dict())
        self.assertEqual(report.warnings, [])
        self.assertEqual(self.package.diagnostics, ())
        self.assertEqual(set(self.package.mcp_servers), {"tavily"})
        self.assertEqual({s.name for s in self.package.skills}, EXPECTED_SKILLS)

    def test_package_keeps_credentials_out_of_the_url_and_preserves_attribution(self):
        server = self.package.mcp_servers["tavily"]
        self.assertEqual(server["url"], "https://mcp.tavily.com/mcp/")
        self.assertEqual(server["headers"]["X-Client-Name"], "hermes plugin")
        self.assertEqual(server["headers"]["Authorization"], "Bearer ${TAVILY_API_KEY}")
        self.assertTrue(server["strict_redirect_headers"])
        self.assertNotIn("command", server)

    def test_profile_credentials_override_foreign_process_credentials(self):
        with patch.dict(os.environ, {"TAVILY_API_KEY": "foreign-profile-value"}):
            for key in ("profile-a-value", "profile-b-value"):
                with self.subTest(profile=key):
                    token = set_secret_scope({"TAVILY_API_KEY": key})
                    try:
                        server = _interpolate_env_vars(self.package.mcp_servers["tavily"])
                        self.assertEqual(server["headers"]["Authorization"], f"Bearer {key}")
                        self.assertEqual(server["headers"]["X-Client-Name"], "hermes plugin")
                    finally:
                        reset_secret_scope(token)

    def test_missing_profile_key_fails_before_a_network_request(self):
        with patch.dict(os.environ, {"TAVILY_API_KEY": "foreign-profile-value"}):
            multiplex = set_multiplex_context(True)
            token = set_secret_scope({})
            try:
                server = _interpolate_env_vars(self.package.mcp_servers["tavily"])
                with self.assertRaisesRegex(ValueError, "TAVILY_API_KEY"):
                    _require_rendered_remote("tavily", server)
            finally:
                reset_secret_scope(token)
                reset_multiplex_context(multiplex)

    def test_bundled_skill_meets_hermes_authoring_contract(self):
        required = ["When to Use", "Prerequisites", "How to Run", "Quick Reference",
                    "Procedure", "Pitfalls", "Verification"]
        for skill in self.package.skills:
            self.assertLessEqual(len(skill.description), 60)
            self.assertTrue(skill.description.endswith("."))
            self.assertIn("Mani Srinivasan", skill.frontmatter["author"])
            body = skill.skill_md.read_text(encoding="utf-8")
            positions = [body.index(f"## {heading}") for heading in required]
            self.assertEqual(positions, sorted(positions))
            for target in re.findall(r"\]\(((?:references|templates)/[^)]+)\)", body):
                self.assertTrue((skill.root / target).is_file(), target)

    def _load_connection_example(self, filename, secrets):
        from hermes_cli.plugins import PluginManager

        home = Path(self.temp.name) / "configured-home"
        installed = home / "plugins" / "tavily"
        shutil.copytree(ROOT, installed, ignore=shutil.ignore_patterns(".git", "__pycache__", "verification-results"))
        (home / "config.yaml").write_text(
            "plugins:\n  enabled: [tavily]\n" + (ROOT / "examples" / filename).read_text(encoding="utf-8"),
            encoding="utf-8",
        )
        bundled = home / "empty-bundled"
        bundled.mkdir()
        with patch.dict(os.environ, {"HERMES_HOME": str(home), "HERMES_BUNDLED_PLUGINS": str(bundled),
                                     "TAVILY_API_KEY": "foreign-profile-value"}):
            manager = PluginManager(scope_key=str(home))
            multiplex = set_multiplex_context(True)
            token = set_secret_scope(secrets)
            try:
                manager.discover_and_load()
                with patch("hermes_cli.plugins.get_plugin_manager", return_value=manager):
                    servers = _load_mcp_config()
                self.assertEqual(set(servers), {"tavily"})
                self.assertEqual(len(manager.list_plugin_skill_metadata()), len(EXPECTED_SKILLS))
                return _require_rendered_remote("tavily", servers["tavily"])
            finally:
                manager.unload()
                reset_secret_scope(token)
                reset_multiplex_context(multiplex)

    def test_oauth_setup_replaces_packaged_key_auth_without_requiring_a_key(self):
        server = self._load_connection_example("oauth.yaml", {})
        self.assertEqual(server["auth"], "oauth")
        self.assertEqual(server["headers"], {"X-Client-Name": "hermes plugin"})
        self.assertEqual(server["url"], "https://mcp.tavily.com/mcp/")
        self.assertEqual(server["timeout"], 900)
        self.assertTrue(server["strict_redirect_headers"])

    def test_api_key_setup_uses_only_the_selected_profile_key(self):
        server = self._load_connection_example("api-key.yaml", {"TAVILY_API_KEY": "profile-key"})
        self.assertNotEqual(server.get("auth"), "oauth")
        self.assertEqual(server["headers"]["Authorization"], "Bearer profile-key")
        self.assertEqual(server["headers"]["X-Client-Name"], "hermes plugin")
        self.assertEqual(server["timeout"], 900)
        self.assertTrue(server["strict_redirect_headers"])

    def test_installed_package_exposes_skill_and_mcp_only_when_enabled(self):
        from hermes_cli.plugins import PluginManager

        home = Path(self.temp.name) / "home"
        installed = home / "plugins" / "tavily"
        shutil.copytree(ROOT, installed, ignore=shutil.ignore_patterns(".git", "__pycache__", "verification-results"))
        bundled = home / "empty-bundled"
        bundled.mkdir()
        with patch.dict(os.environ, {"HERMES_HOME": str(home), "HERMES_BUNDLED_PLUGINS": str(bundled)}):
            for enabled in (False, True):
                with self.subTest(enabled=enabled):
                    (home / "config.yaml").write_text(
                        "plugins:\n  enabled: " + ("[tavily]" if enabled else "[]") + "\n",
                        encoding="utf-8",
                    )
                    manager = PluginManager(scope_key=str(home))
                    try:
                        manager.discover_and_load()
                        self.assertEqual(bool(manager.get_portable_mcp_servers()), enabled)
                        self.assertEqual(len(manager.list_plugin_skill_metadata()), len(EXPECTED_SKILLS) if enabled else 0)
                        if enabled:
                            row = next(p for p in manager.list_plugins() if p["name"] == "tavily")
                            self.assertIsNone(row["error"])
                            from tools.skills_tool import skill_view

                            with patch("hermes_cli.plugins.get_plugin_manager", return_value=manager):
                                for skill in manager.list_plugin_skill_metadata():
                                    skill_md = manager.find_plugin_skill(skill["name"])
                                    self.assertTrue(skill_md.is_file())
                                    viewed = json.loads(skill_view(skill["name"]))
                                    self.assertTrue(viewed["success"], viewed)
                                    for directory in ("references", "templates"):
                                        for path in (skill_md.parent / directory).rglob("*.md"):
                                            relative = path.relative_to(skill_md.parent).as_posix()
                                            resource = json.loads(skill_view(skill["name"], file_path=relative))
                                            self.assertTrue(resource["success"], resource)
                                            self.assertIn(path.read_text(encoding="utf-8").strip(), resource["content"])
                    finally:
                        manager.unload()


class TransportTests(unittest.IsolatedAsyncioTestCase):
    async def test_all_rpc_requests_send_attribution_and_profile_key(self):
        with tempfile.TemporaryDirectory() as data:
            package = load_agent_plugin(ROOT, Path(data))
        token = set_secret_scope({"TAVILY_API_KEY": "fixture-key"})
        try:
            server = _require_rendered_remote("tavily", _interpolate_env_vars(package.mcp_servers["tavily"]))
        finally:
            reset_secret_scope(token)
        received = []

        def capture(request):
            received.append(request)
            return httpx.Response(200, json={"jsonrpc": "2.0", "id": 1, "result": {}})

        factory = _make_redirect_header_stripper(
            httpx, httpx.URL(server["url"]), strict=server["strict_redirect_headers"],
            configured_header_names={key.lower() for key in server["headers"]},
        )
        async with factory(headers=server["headers"], transport=httpx.MockTransport(capture)) as client:
            for method in ("initialize", "tools/list", "tools/call"):
                await client.post(server["url"], json={"jsonrpc": "2.0", "id": 1, "method": method})
        self.assertEqual(len(received), 3)
        for request in received:
            self.assertEqual(request.headers["X-Client-Name"], "hermes plugin")
            self.assertEqual(request.headers["Authorization"], "Bearer fixture-key")

    async def test_redirect_cannot_leak_credentials_or_attribution_to_another_origin(self):
        with tempfile.TemporaryDirectory() as data:
            server = load_agent_plugin(ROOT, Path(data)).mcp_servers["tavily"]
        received = []

        def redirect(request):
            received.append(request)
            if request.url.host == "mcp.tavily.com":
                return httpx.Response(307, headers={"Location": "https://other.example/mcp"})
            return httpx.Response(200)

        headers = {**server["headers"], "Authorization": "Bearer fixture-key"}
        factory = _make_redirect_header_stripper(
            httpx, httpx.URL(server["url"]), strict=server["strict_redirect_headers"],
            configured_header_names={key.lower() for key in headers},
        )
        async with factory(headers=headers, follow_redirects=True, transport=httpx.MockTransport(redirect)) as client:
            await client.post(server["url"], json={"method": "tools/list"})
        self.assertEqual(len(received), 2)
        self.assertNotIn("Authorization", received[-1].headers)
        self.assertNotIn("X-Client-Name", received[-1].headers)
