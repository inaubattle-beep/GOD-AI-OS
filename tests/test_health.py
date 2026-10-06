import pytest
from httpx import AsyncClient, ASGITransport
from apps.api.main import app

@pytest.mark.asyncio
async def test_health_check():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "uptime_sec" in data

@pytest.mark.asyncio
async def test_system_status():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/api/v1/system/status")
    assert response.status_code == 200
    data = response.json()
    assert data["mother_agent"] == "ONLINE"
    assert data["agent_factory"] == "ONLINE"
