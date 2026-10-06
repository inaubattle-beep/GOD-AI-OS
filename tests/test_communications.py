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

        # 2b. Dispatch test message via Facebook Messenger
        fb_resp = await ac.post("/api/v1/communications/dispatch", json={
            "channel_id": "facebook-messenger",
            "recipient": "fb_user_102938",
            "message_text": "GOD AI OS: Hello from Facebook channel!"
        })
        assert fb_resp.status_code == 200
        assert fb_resp.json()["channel_type"] == "facebook"

        # 2c. Dispatch test message via WhatsApp Cloud API
        wa_resp = await ac.post("/api/v1/communications/dispatch", json={
            "channel_id": "whatsapp-business",
            "recipient": "+18005550199",
            "message_text": "GOD AI OS: WhatsApp dispatch test"
        })
        assert wa_resp.status_code == 200
        assert wa_resp.json()["channel_type"] == "whatsapp"

        # 2d. Dispatch test message via Executive Email Gateway
        email_resp = await ac.post("/api/v1/communications/dispatch", json={
            "channel_id": "email-gateway",
            "recipient": "executive@company.org",
            "message_text": "GOD AI OS: Executive Briefing Email"
        })
        assert email_resp.status_code == 200
        assert email_resp.json()["channel_type"] == "email"

        # 2e. Dispatch test message via SMS Gateway
        sms_resp = await ac.post("/api/v1/communications/dispatch", json={
            "channel_id": "sms-gateway",
            "recipient": "+15550192834",
            "message_text": "GOD AI OS SMS Security Token: 981240"
        })
        assert sms_resp.status_code == 200
        assert sms_resp.json()["channel_type"] == "sms"

        # 2f. Dispatch test message via Local Desktop Message
        local_resp = await ac.post("/api/v1/communications/dispatch", json={
            "channel_id": "local-message",
            "recipient": "Local Workstation",
            "message_text": "Desktop Alert: High memory utilization detected"
        })
        assert local_resp.status_code == 200
        assert local_resp.json()["channel_type"] == "local_message"

        # 3. Get dispatch logs
        logs_resp = await ac.get("/api/v1/communications/logs")
        assert logs_resp.status_code == 200
        logs = logs_resp.json()
        assert len(logs) >= 6

