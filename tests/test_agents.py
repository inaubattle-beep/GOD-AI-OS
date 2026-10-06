import pytest
from httpx import AsyncClient, ASGITransport
from apps.api.main import app

@pytest.mark.asyncio
async def test_agent_lifecycle_and_templates():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. List agent templates
        templates_resp = await ac.get("/api/v1/agents/templates")
        assert templates_resp.status_code == 200
        templates = templates_resp.json()
        assert len(templates) >= 25
        
        # 2. Instantiate Coding Agent template
        instantiate_resp = await ac.post("/api/v1/agents/templates/Coding Agent/instantiate")
        assert instantiate_resp.status_code == 200
        agent = instantiate_resp.json()
        assert agent["name"] == "Coding Agent"
        assert agent["role"] == "Senior Full-Stack AI Engineer"
        agent_id = agent["id"]

        # 3. Fetch agent by ID
        get_resp = await ac.get(f"/api/v1/agents/{agent_id}")
        assert get_resp.status_code == 200
        assert get_resp.json()["id"] == agent_id

        # 4. List all active agents
        list_resp = await ac.get("/api/v1/agents")
        assert list_resp.status_code == 200
        agents_list = list_resp.json()
        assert any(a["id"] == agent_id for a in agents_list)
