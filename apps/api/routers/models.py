from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from packages.models.gateway import model_gateway, ModelSpec
from fastapi import HTTPException

router = APIRouter(prefix="/api/v1/models", tags=["Model Gateway & Router"])

class ModelCreateRequest(BaseModel):
    model_id: str
    name: str
    provider: str
    context_window: int = 128000
    coding_score: float = 0.90
    reasoning_score: float = 0.90
    speed_score: float = 0.90
    cost_per_1k_input: float = 0.001
    is_local: bool = False

class ModelUpdateRequest(BaseModel):
    name: str | None = None
    provider: str | None = None
    context_window: int | None = None
    coding_score: float | None = None
    reasoning_score: float | None = None
    speed_score: float | None = None
    cost_per_1k_input: float | None = None
    is_local: bool | None = None

class ProviderCreateRequest(BaseModel):
    provider: str
    name: str
    type: str = "cloud"
    status: str = "ACTIVE"
    api_base: str | None = None

SYSTEM_PROVIDERS = [
    {"provider": "openai", "name": "OpenAI", "type": "cloud", "status": "ACTIVE"},
    {"provider": "gemini", "name": "Google Gemini", "type": "cloud", "status": "ACTIVE"},
    {"provider": "anthropic", "name": "Anthropic Claude", "type": "cloud", "status": "ACTIVE"},
    {"provider": "ollama", "name": "Ollama / Local LLM", "type": "local", "status": "ACTIVE"},
    {"provider": "lm_studio", "name": "LM Studio (OpenAI Compatible)", "type": "local", "status": "ACTIVE"},
    {"provider": "vllm", "name": "vLLM High-Throughput Engine", "type": "local", "status": "ACTIVE"}
]

class RouteRequest(BaseModel):
    prompt: str
    system_instructions: Optional[str] = None
    task_type: str = "general"
    require_privacy: bool = False
    prefer_low_cost: bool = False

@router.get("")
async def list_available_models():
    return model_gateway.list_models()

@router.post("")
async def register_model(req: ModelCreateRequest):
    spec = ModelSpec(
        model_id=req.model_id,
        name=req.name,
        provider=req.provider,
        context_window=req.context_window,
        coding_score=req.coding_score,
        reasoning_score=req.reasoning_score,
        speed_score=req.speed_score,
        cost_per_1k_input=req.cost_per_1k_input,
        is_local=req.is_local
    )
    model_gateway.register_model(spec)
    return {"status": "REGISTERED", "model_id": req.model_id}

@router.put("/{model_id}")
async def update_model(model_id: str, req: ModelUpdateRequest):
    updated = model_gateway.update_model(model_id, req.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found.")
    return {"status": "UPDATED", "model_id": model_id}

@router.delete("/{model_id}")
async def delete_model(model_id: str):
    success = model_gateway.delete_model(model_id)
    if not success:
        raise HTTPException(status_code=404, detail=f"Model '{model_id}' not found.")
    return {"status": "DELETED", "model_id": model_id}

@router.get("/providers")
async def list_providers():
    return SYSTEM_PROVIDERS

@router.post("/providers")
async def create_provider(req: ProviderCreateRequest):
    for p in SYSTEM_PROVIDERS:
        if p["provider"].lower() == req.provider.lower():
            p.update(req.model_dump())
            return {"status": "UPDATED", "provider": req.provider}
    SYSTEM_PROVIDERS.append(req.model_dump())
    return {"status": "REGISTERED", "provider": req.provider}

@router.delete("/providers/{provider_name}")
async def delete_provider(provider_name: str):
    for i, p in enumerate(SYSTEM_PROVIDERS):
        if p["provider"].lower() == provider_name.lower():
            del SYSTEM_PROVIDERS[i]
            return {"status": "DELETED", "provider": provider_name}
    raise HTTPException(status_code=404, detail=f"Provider '{provider_name}' not found.")

@router.post("/route")
async def route_and_generate(req: RouteRequest):
    result = await model_gateway.generate_with_router(
        prompt=req.prompt,
        system_instructions=req.system_instructions,
        task_type=req.task_type,
        require_privacy=req.require_privacy
    )
    return result
