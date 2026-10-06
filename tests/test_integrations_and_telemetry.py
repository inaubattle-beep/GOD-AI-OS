import pytest
from httpx import AsyncClient, ASGITransport
from apps.api.main import app

@pytest.mark.asyncio
async def test_business_integrations():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. ERPNext Sales Report
        erp_resp = await ac.get("/api/v1/integrations/erpnext/sales-report")
        assert erp_resp.status_code == 200
        assert erp_resp.json()["adapter"] == "ERPNext"
        assert erp_resp.json()["sales_count"] == 42

        # 2. ViciDial Outbound Call Trigger
        vici_resp = await ac.post("/api/v1/integrations/vicidial/call", json={
            "phone_number": "+18005550199",
            "prompt": "Hello from GOD AI OS Voice Agent",
            "language": "en"
        })
        assert vici_resp.status_code == 200
        assert vici_resp.json()["status"] == "CALL_INITIATED"

        # 3. n8n Workflow Trigger
        n8n_resp = await ac.post("/api/v1/integrations/n8n/trigger", json={
            "workflow_id": "wf-sales-report",
            "payload": {"key": "val"}
        })
        assert n8n_resp.status_code == 200
        assert n8n_resp.json()["status"] == "WORKFLOW_TRIGGERED"

@pytest.mark.asyncio
async def test_observability_metrics():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        metrics_resp = await ac.get("/api/v1/observability/metrics")
        assert metrics_resp.status_code == 200
        data = metrics_resp.json()
        assert "total_agent_runs" in data
        assert "total_tokens_consumed" in data
