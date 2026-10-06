from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

from packages.security.sandbox import security_engine

router = APIRouter(prefix="/api/v1/security", tags=["Security & Sandbox"])

class PromptCheckRequest(BaseModel):
    prompt: str

class PermissionCheckRequest(BaseModel):
    agent_permissions: List[str]
    required_permission: str

@router.post("/validate-prompt")
async def validate_prompt(req: PromptCheckRequest):
    return security_engine.validate_prompt_security(req.prompt)

@router.post("/check-permission")
async def check_permission(req: PermissionCheckRequest):
    allowed = security_engine.check_permission(req.agent_permissions, req.required_permission)
    return {"allowed": allowed, "required_permission": req.required_permission}
