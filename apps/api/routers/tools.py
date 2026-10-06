from fastapi import APIRouter, HTTPException, Body
from typing import List, Dict, Any

from packages.tools.registry import tool_registry, ToolResult

router = APIRouter(prefix="/api/v1/tools", tags=["Tools"])

@router.get("")
async def list_tools():
    return tool_registry.list_tools()

@router.post("/execute/{tool_name}")
async def execute_tool(tool_name: str, payload: Dict[str, Any] = Body(...)):
    params = payload.get("params", payload)
    result: ToolResult = await tool_registry.execute_tool(tool_name, params)
    if not result.success:
        raise HTTPException(status_code=400, detail=result.error)
    return result.to_dict()
