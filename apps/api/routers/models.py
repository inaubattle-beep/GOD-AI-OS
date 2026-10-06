from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from packages.models.gateway import model_gateway

router = APIRouter(prefix="/api/v1/models", tags=["Model Gateway & Router"])

class RouteRequest(BaseModel):
    prompt: str
    system_instructions: Optional[str] = None
    task_type: str = "general"
    require_privacy: bool = False
    prefer_low_cost: bool = False

@router.get("")
async def list_available_models():
    return model_gateway.list_models()

@router.get("/providers")
async def list_providers():
    return [
        {"provider": "openai", "name": "OpenAI", "type": "cloud", "status": "ACTIVE"},
        {"provider": "gemini", "name": "Google Gemini", "type": "cloud", "status": "ACTIVE"},
        {"provider": "anthropic", "name": "Anthropic Claude", "type": "cloud", "status": "ACTIVE"},
        {"provider": "ollama", "name": "Ollama / Local LLM", "type": "local", "status": "ACTIVE"},
        {"provider": "lm_studio", "name": "LM Studio (OpenAI Compatible)", "type": "local", "status": "ACTIVE"},
        {"provider": "vllm", "name": "vLLM High-Throughput Engine", "type": "local", "status": "ACTIVE"}
    ]

@router.post("/route")
async def route_and_generate(req: RouteRequest):
    result = await model_gateway.generate_with_router(
        prompt=req.prompt,
        system_instructions=req.system_instructions,
        task_type=req.task_type,
        require_privacy=req.require_privacy
    )
    return result
