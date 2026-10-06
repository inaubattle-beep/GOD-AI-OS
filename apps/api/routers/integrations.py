from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, Optional

from packages.integrations.adapters import integration_manager

router = APIRouter(prefix="/api/v1/integrations", tags=["Business Integrations"])

class CallViciDialRequest(BaseModel):
    phone_number: str
    prompt: str
    language: str = "en"

class TriggerN8nRequest(BaseModel):
    workflow_id: str
    payload: Dict[str, Any]

@router.get("/erpnext/sales-report")
async def get_erpnext_sales():
    erp = integration_manager["erpnext"]
    return await erp.fetch_sales_report()

@router.post("/vicidial/call")
async def trigger_vicidial_call(req: CallViciDialRequest):
    vici = integration_manager["vicidial"]
    return await vici.trigger_outbound_call(phone_number=req.phone_number, text_prompt=req.prompt, language=req.language)

@router.post("/n8n/trigger")
async def trigger_n8n_workflow(req: TriggerN8nRequest):
    n8n = integration_manager["n8n"]
    return await n8n.trigger_workflow(workflow_id=req.workflow_id, payload=req.payload)
