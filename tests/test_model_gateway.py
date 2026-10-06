import pytest
from httpx import AsyncClient, ASGITransport
from apps.api.main import app

@pytest.mark.asyncio
async def test_model_gateway_and_providers():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. List available models
        models_resp = await ac.get("/api/v1/models")
        assert models_resp.status_code == 200
        models = models_resp.json()
        assert len(models) >= 4

        # 2. List model providers
        prov_resp = await ac.get("/api/v1/models/providers")
        assert prov_resp.status_code == 200
        providers = prov_resp.json()
        assert len(providers) >= 5

        # 3. Test Model Router for Coding Task (Routes to Claude / GPT-4o)
        route_code = await ac.post("/api/v1/models/route", json={
            "prompt": "Write a Python FastAPI async router",
            "task_type": "coding"
        })
        assert route_code.status_code == 200
        code_data = route_code.json()
        assert code_data["routed_model"] in ["claude-3-5-sonnet", "gpt-4o"]

        # 4. Test Model Router for Private Data Task (Routes to Local Ollama/Llama3)
        route_privacy = await ac.post("/api/v1/models/route", json={
            "prompt": "Process sensitive internal employee records",
            "task_type": "general",
            "require_privacy": True
        })
        assert route_privacy.status_code == 200
        privacy_data = route_privacy.json()
        assert privacy_data["is_local"] is True
        assert privacy_data["routed_model"] == "llama3-local"
