import pytest
from httpx import AsyncClient, ASGITransport
from apps.api.main import app

@pytest.mark.asyncio
async def test_tools_and_mcp():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        # 1. List universal tools
        tools_resp = await ac.get("/api/v1/tools")
        assert tools_resp.status_code == 200
        tools = tools_resp.json()
        assert len(tools) >= 3

        # 2. Test tool execution (file_write & file_read)
        write_resp = await ac.post("/api/v1/tools/execute/file_write", json={"params": {"filepath": "c:/GOD AI OS/scratch/test_tool.txt", "content": "GOD AI OS Tool Execution Test"}})
        assert write_resp.status_code == 200
        assert write_resp.json()["success"] is True

        read_resp = await ac.post("/api/v1/tools/execute/file_read", json={"params": {"filepath": "c:/GOD AI OS/scratch/test_tool.txt"}})
        assert read_resp.status_code == 200
        assert read_resp.json()["output"] == "GOD AI OS Tool Execution Test"

        # 3. List MCP Servers and Discover tools
        mcp_resp = await ac.get("/api/v1/mcp/servers")
        assert mcp_resp.status_code == 200
        servers = mcp_resp.json()
        assert len(servers) >= 2

        disc_resp = await ac.get("/api/v1/mcp/servers/filesystem/discover")
        assert disc_resp.status_code == 200
        disc_data = disc_resp.json()
        assert len(disc_data["tools"]) >= 1
