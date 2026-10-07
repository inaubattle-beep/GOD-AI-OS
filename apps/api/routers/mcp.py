from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any

from packages.mcp.gateway import mcp_gateway, MCPServerConfig
from apps.api.schemas.schemas import MCPServerCreate, MCPServerResponse, MCPServerUpdate

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

@router.put("/servers/{server_name}")
async def update_mcp_server(server_name: str, server_in: MCPServerUpdate):
    updated = mcp_gateway.update_server(server_name, server_in.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail=f"MCP Server '{server_name}' not found.")
    return {"status": "UPDATED", "server": server_name}

@router.delete("/servers/{server_name}")
async def delete_mcp_server(server_name: str):
    success = mcp_gateway.delete_server(server_name)
    if not success:
        raise HTTPException(status_code=404, detail=f"MCP Server '{server_name}' not found.")
    return {"status": "DELETED", "server": server_name}

@router.get("/servers/{server_name}/discover")
async def discover_mcp_tools(server_name: str):
    try:
        tools = await mcp_gateway.discover_tools(server_name)
        return {"server": server_name, "tools": tools}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
