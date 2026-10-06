import pytest
from httpx import AsyncClient, ASGITransport
from apps.api.main import app

@pytest.mark.asyncio
async def test_mother_agent_chat_and_dynamic_creation():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Test Natural Language System Admin agent creation
        create_prompt = "Create a DevOps agent that monitors server health."
        resp = await ac.post("/api/v1/mother/chat", json={"user_prompt": create_prompt})
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "AGENT_CREATED"
        assert "agent" in data

        # 2. Test Mother Agent Task Execution
        task_prompt = "Analyze system performance and suggest optimization."
        task_resp = await ac.post("/api/v1/mother/chat", json={"user_prompt": task_prompt})
        assert task_resp.status_code == 200
        task_data = task_resp.json()
        assert task_data["status"] == "COMPLETED"
        assert "result" in task_data
        assert "trace" in task_data
