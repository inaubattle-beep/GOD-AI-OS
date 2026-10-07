from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from packages.plugins.manager import plugin_manager, PluginManifest
from apps.api.schemas.schemas import PluginCreate, PluginUpdate

router = APIRouter(prefix="/api/v1/plugins", tags=["Plugin System"])

class TogglePluginRequest(BaseModel):
    enabled: bool

@router.get("")
async def list_plugins():
    return plugin_manager.list_plugins()

@router.post("")
async def create_plugin(req: PluginCreate):
    manifest = PluginManifest(
        plugin_id=req.plugin_id,
        name=req.name,
        version=req.version,
        description=req.description,
        author=req.author,
        category=req.category,
        permissions=req.permissions,
        tools=req.tools,
        skills=req.skills,
        mcp_servers=req.mcp_servers
    )
    plugin_manager.register_plugin(manifest)
    return {"status": "REGISTERED", "plugin_id": req.plugin_id}

@router.put("/{plugin_id}")
async def update_plugin(plugin_id: str, req: PluginUpdate):
    updated = plugin_manager.update_plugin(plugin_id, req.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_id}' not found.")
    return {"status": "UPDATED", "plugin_id": plugin_id}

@router.delete("/{plugin_id}")
async def delete_plugin(plugin_id: str):
    success = plugin_manager.delete_plugin(plugin_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_id}' not found.")
    return {"status": "DELETED", "plugin_id": plugin_id}

@router.post("/{plugin_id}/toggle")
async def toggle_plugin(plugin_id: str, req: TogglePluginRequest):
    success = plugin_manager.toggle_plugin(plugin_id, req.enabled)
    if not success:
        raise HTTPException(status_code=404, detail=f"Plugin '{plugin_id}' not found.")
    return {"plugin_id": plugin_id, "enabled": req.enabled}
