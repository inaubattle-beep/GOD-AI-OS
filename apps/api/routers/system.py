from fastapi import APIRouter
import time

router = APIRouter(tags=["System Health"])
start_time = time.time()

@router.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "system": "GOD AI OS — Mother Agent",
        "version": "1.0.0",
        "uptime_sec": round(time.time() - start_time, 2)
    }

@router.get("/api/v1/system/status")
async def system_status():
    return {
        "mother_agent": "ONLINE",
        "agent_factory": "ONLINE",
        "mcp_gateway": "ONLINE",
        "tool_registry": "ONLINE",
        "memory_store": "ONLINE",
        "active_providers": ["openai", "gemini", "ollama"]
    }
