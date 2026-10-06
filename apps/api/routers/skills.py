from fastapi import APIRouter
from packages.skills.registry import skill_registry

router = APIRouter(prefix="/api/v1/skills", tags=["Skills"])

@router.get("")
async def list_skills():
    return skill_registry.list_skills()
