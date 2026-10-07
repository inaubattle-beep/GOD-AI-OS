import pytest
from httpx import AsyncClient, ASGITransport
from apps.api.main import app

@pytest.mark.asyncio
async def test_hermes_full_crud_lifecycle():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. Skills CRUD
        create_skill = await ac.post("/api/v1/skills", json={
            "skill_id": "test_hermes_skill",
            "name": "Hermes Test Skill",
            "description": "Test skill description",
            "instructions": "Step 1: Test Hermes skill",
            "category": "test"
        })
        assert create_skill.status_code == 200
        
        update_skill = await ac.put("/api/v1/skills/test_hermes_skill", json={
            "description": "Updated description for Hermes skill"
        })
        assert update_skill.status_code == 200
        assert update_skill.json()["description"] == "Updated description for Hermes skill"

        delete_skill = await ac.delete("/api/v1/skills/test_hermes_skill")
        assert delete_skill.status_code == 200

        # 2. MCP Servers CRUD
        create_mcp = await ac.post("/api/v1/mcp/servers", json={
            "name": "test-hermes-mcp",
            "transport": "stdio",
            "command": "npx",
            "args": ["-y", "@modelcontextprotocol/server-memory"]
        })
        assert create_mcp.status_code == 200

        update_mcp = await ac.put("/api/v1/mcp/servers/test-hermes-mcp", json={
            "command": "node"
        })
        assert update_mcp.status_code == 200

        delete_mcp = await ac.delete("/api/v1/mcp/servers/test-hermes-mcp")
        assert delete_mcp.status_code == 200

        # 3. Plugins CRUD
        create_plugin = await ac.post("/api/v1/plugins", json={
            "plugin_id": "test-hermes-plugin",
            "name": "Hermes Test Plugin",
            "description": "Test plugin description",
            "category": "test"
        })
        assert create_plugin.status_code == 200

        update_plugin = await ac.put("/api/v1/plugins/test-hermes-plugin", json={
            "description": "Updated plugin description"
        })
        assert update_plugin.status_code == 200

        delete_plugin = await ac.delete("/api/v1/plugins/test-hermes-plugin")
        assert delete_plugin.status_code == 200

        # 4. Communications Channels CRUD
        create_chan = await ac.post("/api/v1/communications/channels", json={
            "channel_id": "test-hermes-chan",
            "name": "Hermes Signal Bot",
            "channel_type": "signal",
            "provider": "signal"
        })
        assert create_chan.status_code == 200

        update_chan = await ac.put("/api/v1/communications/channels/test-hermes-chan", json={
            "name": "Updated Hermes Signal Bot"
        })
        assert update_chan.status_code == 200

        delete_chan = await ac.delete("/api/v1/communications/channels/test-hermes-chan")
        assert delete_chan.status_code == 200

        # 5. Model Providers & Models CRUD
        create_model = await ac.post("/api/v1/models", json={
            "model_id": "hermes-local-v1",
            "name": "Hermes Local AI v1",
            "provider": "ollama",
            "context_window": 32000,
            "is_local": True
        })
        assert create_model.status_code == 200

        update_model = await ac.put("/api/v1/models/hermes-local-v1", json={
            "context_window": 64000
        })
        assert update_model.status_code == 200

        delete_model = await ac.delete("/api/v1/models/hermes-local-v1")
        assert delete_model.status_code == 200
