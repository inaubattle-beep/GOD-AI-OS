from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from apps.api.config import settings
from apps.api.database import init_db
from apps.api.routers import agents, mother, tools, mcp, skills, system, knowledge, workflows, security, integrations, observability, models, plugins, communications

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield

app = FastAPI(
    title="GOD AI OS — Mother Agent API",
    description="Extensible AI Agent Operating System & Agent Factory Runtime",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(system.router)
app.include_router(mother.router)
app.include_router(agents.router)
app.include_router(tools.router)
app.include_router(mcp.router)
app.include_router(skills.router)
app.include_router(knowledge.router)
app.include_router(workflows.router)
app.include_router(security.router)
app.include_router(integrations.router)
app.include_router(observability.router)
app.include_router(models.router)
app.include_router(plugins.router)
app.include_router(communications.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("apps.api.main:app", host=settings.API_HOST, port=settings.API_PORT, reload=True)
