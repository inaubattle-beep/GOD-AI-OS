import pytest
from httpx import AsyncClient, ASGITransport
from apps.api.main import app

@pytest.mark.asyncio
async def test_plugin_architecture():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. List installed plugins
        plugins_resp = await ac.get("/api/v1/plugins")
        assert plugins_resp.status_code == 200
        plugins = plugins_resp.json()
        assert len(plugins) >= 4
        assert any(p["plugin_id"] == "github-dev-kit" for p in plugins)

        # 2. Toggle plugin status
        toggle_resp = await ac.post("/api/v1/plugins/github-dev-kit/toggle", json={"enabled": False})
        assert toggle_resp.status_code == 200
        assert toggle_resp.json()["enabled"] is False

@pytest.mark.asyncio
async def test_skill_registry_expanded():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. List expanded AgenticSkills
        skills_resp = await ac.get("/api/v1/skills")
        assert skills_resp.status_code == 200
        skills = skills_resp.json()
        assert len(skills) >= 10
        assert any(s["skill_id"] == "owasp_security_auditor" for s in skills)

        # 2. Register custom skill
        reg_resp = await ac.post("/api/v1/skills", json={
            "skill_id": "quantum_encryption_audit",
            "name": "Quantum-Resistant Encryption Audit",
            "description": "Evaluate cryptographic suites against post-quantum lattice standards.",
            "instructions": "1. Scan cipher suites.\n2. Evaluate key length.\n3. Verify post-quantum fallback.",
            "category": "security",
            "required_tools": ["security_scanner"]
        })
        assert reg_resp.status_code == 200
        assert reg_resp.json()["status"] == "REGISTERED"

        # 3. Fetch custom skill details
        detail_resp = await ac.get("/api/v1/skills/quantum_encryption_audit")
        assert detail_resp.status_code == 200
        assert detail_resp.json()["name"] == "Quantum-Resistant Encryption Audit"
