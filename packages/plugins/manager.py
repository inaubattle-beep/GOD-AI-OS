from typing import Dict, Any, List, Optional

class PluginManifest:
    def __init__(
        self,
        plugin_id: str,
        name: str,
        version: str,
        description: str,
        author: str,
        category: str,
        permissions: List[str],
        tools: List[str],
        skills: List[str],
        mcp_servers: List[str]
    ):
        self.plugin_id = plugin_id
        self.name = name
        self.version = version
        self.description = description
        self.author = author
        self.category = category
        self.permissions = permissions
        self.tools = tools
        self.skills = skills
        self.mcp_servers = mcp_servers
        self.enabled = True

class PluginManager:
    def __init__(self):
        self._plugins: Dict[str, PluginManifest] = {}
        self._register_default_plugins()

    def _register_default_plugins(self):
        self.register_plugin(PluginManifest(
            plugin_id="github-dev-kit",
            name="GitHub Developer & CI/CD Suite",
            version="1.2.0",
            description="Complete GitHub integration with issue tracking, pull request review, and repository management.",
            author="GOD AI OS Core Team",
            category="developer",
            permissions=["github.write", "repository.read"],
            tools=["mcp_github_create_issue", "mcp_github_get_repo"],
            skills=["code_refactoring", "unit_testing"],
            mcp_servers=["github"]
        ))
        self.register_plugin(PluginManifest(
            plugin_id="erp-suite-plugin",
            name="Enterprise ERP & Logistics Pack",
            version="2.0.1",
            description="Interface with ERPNext, Odoo, WooCommerce, and supply chain inventory management.",
            author="Enterprise AI Solutions",
            category="business",
            permissions=["erp.read", "erp.write"],
            tools=["erp_fetch_orders", "erp_update_stock"],
            skills=["erpnext_integration", "inventory_management"],
            mcp_servers=["erpnext"]
        ))
        self.register_plugin(PluginManifest(
            plugin_id="voice-telephony-pack",
            name="Bengali & Omnichannel Telephony Suite",
            version="1.0.4",
            description="Real-time IVR voice agent integration with ViciDial, Asterisk, and Telegram notifications.",
            author="OmniVoice AI",
            category="communication",
            permissions=["telephony.dial", "audio.stream"],
            tools=["audio_stream", "tts_generate"],
            skills=["voice_synthesis", "conversational_flow"],
            mcp_servers=["vicidial"]
        ))
        self.register_plugin(PluginManifest(
            plugin_id="security-auditor-pack",
            name="AppSec & Cloud Security Scanner",
            version="1.1.0",
            description="Continuous RBAC audit, vulnerability detection, secrets scanner, and zero-trust sandbox engine.",
            author="Security Operations",
            category="security",
            permissions=["security.audit", "sandbox.manage"],
            tools=["security_scanner", "prompt_checker"],
            skills=["vulnerability_scanning", "rbac_auditing"],
            mcp_servers=["security"]
        ))

    def register_plugin(self, manifest: PluginManifest):
        self._plugins[manifest.plugin_id] = manifest

    def list_plugins(self) -> List[Dict[str, Any]]:
        return [
            {
                "plugin_id": p.plugin_id,
                "name": p.name,
                "version": p.version,
                "description": p.description,
                "author": p.author,
                "category": p.category,
                "enabled": p.enabled,
                "permissions": p.permissions,
                "tools": p.tools,
                "skills": p.skills,
                "mcp_servers": p.mcp_servers
            }
            for p in self._plugins.values()
        ]

    def toggle_plugin(self, plugin_id: str, enabled: bool) -> bool:
        if plugin_id in self._plugins:
            self._plugins[plugin_id].enabled = enabled
            return True
        return False

plugin_manager = PluginManager()
