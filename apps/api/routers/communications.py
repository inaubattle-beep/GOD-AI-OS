from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any

from packages.communications.hub import comm_hub

router = APIRouter(prefix="/api/v1/communications", tags=["Communications Hub"])

class DispatchMessageRequest(BaseModel):
    channel_id: str
    recipient: str
    message_text: str

@router.get("/channels")
async def list_communication_channels():
    return comm_hub.list_channels()

@router.post("/dispatch")
async def dispatch_message(req: DispatchMessageRequest):
    try:
        log = comm_hub.dispatch_message(
            channel_id=req.channel_id,
            recipient=req.recipient,
            message_text=req.message_text
        )
        return log
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

@router.get("/logs")
async def get_dispatch_logs():
    return comm_hub.get_logs()
