from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from packages.communications.hub import comm_hub, CommunicationChannel

router = APIRouter(prefix="/api/v1/communications", tags=["Communications Hub"])

class ChannelCreateRequest(BaseModel):
    channel_id: str
    name: str
    channel_type: str
    provider: str = "custom"
    status: str = "ONLINE"

class ChannelUpdateRequest(BaseModel):
    name: str | None = None
    channel_type: str | None = None
    provider: str | None = None
    status: str | None = None

class DispatchMessageRequest(BaseModel):
    channel_id: str
    recipient: str
    message_text: str
    media_url: str | None = None

@router.get("/channels")
async def list_communication_channels():
    return comm_hub.list_channels()

@router.post("/channels")
async def create_communication_channel(req: ChannelCreateRequest):
    channel = CommunicationChannel(
        channel_id=req.channel_id,
        name=req.name,
        channel_type=req.channel_type,
        provider=req.provider,
        status=req.status
    )
    comm_hub.register_channel(channel)
    return {"status": "REGISTERED", "channel_id": req.channel_id}

@router.put("/channels/{channel_id}")
async def update_communication_channel(channel_id: str, req: ChannelUpdateRequest):
    updated = comm_hub.update_channel(channel_id, req.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail=f"Channel '{channel_id}' not found.")
    return {"status": "UPDATED", "channel_id": channel_id}

@router.delete("/channels/{channel_id}")
async def delete_communication_channel(channel_id: str):
    success = comm_hub.delete_channel(channel_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Channel '{channel_id}' not found.")
    return {"status": "DELETED", "channel_id": channel_id}

@router.post("/dispatch")
async def dispatch_message(req: DispatchMessageRequest):
    try:
        log = comm_hub.dispatch_message(
            channel_id=req.channel_id,
            recipient=req.recipient,
            message_text=req.message_text,
            media_url=req.media_url
        )
        return log
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/logs")
async def get_dispatch_logs():
    return comm_hub.get_logs()
