from typing import Dict, Any, List, Optional
import json

class MCPServerConfig:
    def __init__(self, name: str, transport: str = "stdio", command: Optional[str] = None, args: Optional[List[str]] = None, url: Optional[str] = None):
        self.name = name
        self.transport = transport
        self.command = command
        self.args = args or []
        self.url = url
        self.enabled = True

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

    def register_server(self, config: MCPServerConfig):
        self._servers[config.name] = config

    def list_servers(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": s.name,
                "transport": s.transport,
                "command": s.command,
                "args": s.args,
                "url": s.url,
                "enabled": s.enabled
            }
            for s in self._servers.values()
        ]

    async def discover_tools(self, server_name: str) -> List[Dict[str, Any]]:
        if server_name not in self._servers:
            raise ValueError(f"MCP Server '{server_name}' not found.")
        
        # Baseline mock discovery return for standard MCP tools
        if server_name == "filesystem":
            return [
                {"name": "mcp_read_file", "description": "Read file via MCP Filesystem server"},
                {"name": "mcp_list_directory", "description": "List directory contents via MCP"}
            ]
        elif server_name == "github":
            return [
                {"name": "mcp_github_create_issue", "description": "Create issue on GitHub via MCP"},
                {"name": "mcp_github_get_repo", "description": "Get repository details via MCP"}
            ]
        return []

mcp_gateway = MCPGateway()
