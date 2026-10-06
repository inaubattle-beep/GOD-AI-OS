import pytest
from httpx import AsyncClient, ASGITransport
from apps.api.main import app

@pytest.mark.asyncio
async def test_communications_hub():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. List channels
        channels_resp = await ac.get("/api/v1/communications/channels")
        assert channels_resp.status_code == 200
        channels = channels_resp.json()
        assert len(channels) >= 5
        assert any(c["channel_type"] == "telegram" for c in channels)

        # 2. Dispatch test message via Telegram channel
        disp_resp = await ac.post("/api/v1/communications/dispatch", json={
            "channel_id": "telegram-bot",
            "recipient": "@admin_dev",
            "message_text": "GOD AI OS Alert: Server uptime healthy"
        })
        assert disp_resp.status_code == 200
        disp_data = disp_resp.json()
        assert disp_data["status"] == "SENT"
        assert disp_data["recipient"] == "@admin_dev"

        # 3. Get dispatch logs
        logs_resp = await ac.get("/api/v1/communications/logs")
        assert logs_resp.status_code == 200
        logs = logs_resp.json()
        assert len(logs) >= 1
