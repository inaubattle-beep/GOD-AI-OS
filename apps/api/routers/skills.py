from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from packages.skills.registry import skill_registry, SkillDefinition

router = APIRouter(prefix="/api/v1/skills", tags=["Skill Registry"])

class SkillCreateRequest(BaseModel):
    skill_id: str
    name: str
    description: str
    instructions: str
    category: str = "general"
    required_tools: List[str] = []
    author: str = "User"

@router.get("")
async def list_skills():
    return skill_registry.list_skills()

@router.post("")
async def create_skill(req: SkillCreateRequest):
    skill = SkillDefinition(
        skill_id=req.skill_id,
        name=req.name,
        description=req.description,
        instructions=req.instructions,
        category=req.category,
        required_tools=req.required_tools,
        author=req.author
    )
    skill_registry.register_skill(skill)
    return {"status": "REGISTERED", "skill_id": req.skill_id}

@router.get("/{skill_id}")
async def get_skill(skill_id: str):
    skill = skill_registry.get_skill(skill_id)
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found")
    return {
        "skill_id": skill.skill_id,
        "name": skill.name,
        "description": skill.description,
        "instructions": skill.instructions,
        "category": skill.category,
        "required_tools": skill.required_tools,
        "author": skill.author,
        "version": skill.version,
        "enabled": skill.enabled
    }
