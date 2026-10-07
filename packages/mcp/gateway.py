from typing import Dict, Any, List, Optional
import json

class MCPServerConfig:
    def __init__(
        self,
        name: str,
        transport: str = "stdio",
        command: Optional[str] = None,
        args: Optional[List[str]] = None,
        url: Optional[str] = None,
        env_vars: Optional[Dict[str, str]] = None
    ):
        self.name = name
        self.transport = transport # stdio, sse, http
        self.command = command
        self.args = args or []
        self.url = url
        self.env_vars = env_vars or {}
        self.enabled = True
        self.status = "CONNECTED"

class MCPGateway:
    def __init__(self):
        self._servers: Dict[str, MCPServerConfig] = {}
        self._register_default_servers()

    def _register_default_servers(self):
        self.register_server(MCPServerConfig(
            name="filesystem",
            transport="stdio",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-filesystem", "./"]
        ))
        self.register_server(MCPServerConfig(
            name="github",
            transport="stdio",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-github"]
        ))
        self.register_server(MCPServerConfig(
            name="postgresql",
            transport="stdio",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-postgres", "postgresql://god_user:god_password@localhost:5432/god_ai_os"]
        ))
        self.register_server(MCPServerConfig(
            name="docker",
            transport="stdio",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-docker"]
        ))
        self.register_server(MCPServerConfig(
            name="puppeteer",
            transport="stdio",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-puppeteer"]
        ))
        self.register_server(MCPServerConfig(
            name="slack",
            transport="sse",
            url="http://localhost:3001/mcp/slack/sse"
        ))
        self.register_server(MCPServerConfig(
            name="notion",
            transport="http",
            url="http://localhost:3002/mcp/notion/api"
        ))
        self.register_server(MCPServerConfig(
            name="fetch",
            transport="stdio",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-fetch"]
        ))
        self.register_server(MCPServerConfig(
            name="memory",
            transport="stdio",
            command="npx",
            args=["-y", "@modelcontextprotocol/server-memory"]
        ))
        self.register_server(MCPServerConfig(
            name="erpnext",
            transport="http",
            url="http://localhost:8000/mcp/erpnext"
        ))

    def register_server(self, config: MCPServerConfig):
        self._servers[config.name] = config

    def update_server(self, name: str, updated_fields: Dict[str, Any]) -> Optional[MCPServerConfig]:
        if name not in self._servers:
            return None
        server = self._servers[name]
        for k, v in updated_fields.items():
            if hasattr(server, k):
                setattr(server, k, v)
        return server

    def delete_server(self, name: str) -> bool:
        if name in self._servers:
            del self._servers[name]
            return True
        return False

    def list_servers(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": s.name,
                "transport": s.transport,
                "command": s.command,
                "args": s.args,
                "url": s.url,
                "enabled": s.enabled,
                "status": s.status
            }
            for s in self._servers.values()
        ]

    async def discover_tools(self, server_name: str) -> List[Dict[str, Any]]:
        if server_name not in self._servers:
            raise ValueError(f"MCP Server '{server_name}' not found.")
        
        if server_name == "filesystem":
            return [
                {"name": "mcp_read_file", "description": "Read file contents via MCP Filesystem"},
                {"name": "mcp_write_file", "description": "Write file contents via MCP Filesystem"},
                {"name": "mcp_list_directory", "description": "List directory contents via MCP Filesystem"}
            ]
        elif server_name == "github":
            return [
                {"name": "mcp_github_create_issue", "description": "Create issue on GitHub repository"},
                {"name": "mcp_github_get_repo", "description": "Fetch GitHub repository details"},
                {"name": "mcp_github_create_pr", "description": "Create pull request on GitHub"}
            ]
        elif server_name == "postgresql":
            return [
                {"name": "mcp_pg_query", "description": "Execute read-only SQL query on PostgreSQL"},
                {"name": "mcp_pg_inspect_schema", "description": "Inspect PostgreSQL tables and indexes"}
            ]
        elif server_name == "docker":
            return [
                {"name": "mcp_docker_list_containers", "description": "List running Docker containers"},
                {"name": "mcp_docker_inspect_logs", "description": "Fetch container log stream"}
            ]
        elif server_name == "puppeteer":
            return [
                {"name": "mcp_puppeteer_navigate", "description": "Navigate browser to target URL"},
                {"name": "mcp_puppeteer_click", "description": "Click element on web page"},
                {"name": "mcp_puppeteer_screenshot", "description": "Capture page screenshot"}
            ]
        elif server_name == "fetch":
            return [
                {"name": "mcp_fetch_url", "description": "Fetch raw HTML/Markdown content from URL"}
            ]
        elif server_name == "memory":
            return [
                {"name": "mcp_memory_create_graph", "description": "Store knowledge graph entity/relation"},
                {"name": "mcp_memory_read_graph", "description": "Query knowledge graph entities"}
            ]
        elif server_name == "slack":
            return [
                {"name": "mcp_slack_post_message", "description": "Post message to target Slack channel"}
            ]
        elif server_name == "notion":
            return [
                {"name": "mcp_notion_search", "description": "Search Notion workspace pages"},
                {"name": "mcp_notion_create_page", "description": "Create page in Notion database"}
            ]
        elif server_name == "erpnext":
            return [
                {"name": "mcp_erp_get_doc", "description": "Get ERPNext document by doctype and name"}
            ]
        return []

mcp_gateway = MCPGateway()
