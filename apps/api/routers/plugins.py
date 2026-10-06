from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from packages.plugins.manager import plugin_manager

router = APIRouter(prefix="/api/v1/plugins", tags=["Plugin System"])

class TogglePluginRequest(BaseModel):
    enabled: bool

@router.get("")
async def list_plugins():
    return plugin_manager.list_plugins()

@router.post("/{plugin_id}/toggle")
async def toggle_plugin(plugin_id: str, req: TogglePluginRequest):
    success = plugin_manager.toggle_plugin(plugin_id, req.enabled)
    if not success:
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_id}' not found.")
    return {"plugin_id": plugin_id, "enabled": req.enabled}
