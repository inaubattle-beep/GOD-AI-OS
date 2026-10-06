from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from packages.mcp.gateway import mcp_gateway, MCPServerConfig
from apps.api.schemas.schemas import MCPServerCreate, MCPServerResponse

router = APIRouter(prefix="/api/v1/mcp", tags=["MCP Subsystem"])

@router.get("/servers")
async def list_mcp_servers():
    return mcp_gateway.list_servers()

@router.post("/servers")
async def register_mcp_server(server_in: MCPServerCreate):
    config = MCPServerConfig(
        name=server_in.name,
        transport=server_in.transport,
        command=server_in.command,
        args=server_in.args,
        url=server_in.url
    )
    mcp_gateway.register_server(config)
    return {"status": "REGISTERED", "server": server_in.name}

@router.get("/servers/{server_name}/discover")
async def discover_mcp_tools(server_name: str):
    try:
        tools = await mcp_gateway.discover_tools(server_name)
        return {"server": server_name, "tools": tools}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
