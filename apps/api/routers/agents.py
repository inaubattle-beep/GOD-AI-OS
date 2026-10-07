from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from apps.api.database import get_db
from apps.api.models.entities import Agent, AgentRun
from apps.api.schemas.schemas import AgentCreate, AgentResponse, AgentUpdate, AgentRunCreate, AgentRunResponse, AgentTemplateCreate, AgentTemplateUpdate
from packages.agent_factory.factory import AgentFactory

router = APIRouter(prefix="/api/v1/agents", tags=["Agents"])

@router.get("", response_model=List[AgentResponse])
async def list_agents(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Agent))
    return result.scalars().all()

@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(agent_in: AgentCreate, db: AsyncSession = Depends(get_db)):
    agent = Agent(**agent_in.model_dump())
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    return agent

@router.get("/templates")
async def list_agent_templates():
    return AgentFactory.list_templates()

@router.post("/templates")
async def create_agent_template(tpl_in: AgentTemplateCreate):
    tpl = AgentFactory.add_template(tpl_in.model_dump())
    return tpl

@router.put("/templates/{template_name}")
async def update_agent_template(template_name: str, tpl_in: AgentTemplateUpdate):
    updated = AgentFactory.update_template(template_name, tpl_in.model_dump(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail=f"Template '{template_name}' not found.")
    return updated

@router.post("/templates/{template_name}/instantiate", response_model=AgentResponse)
async def instantiate_template(template_name: str, db: AsyncSession = Depends(get_db)):
    spec = AgentFactory.create_agent_spec(template_name)
    agent = Agent(**spec.model_dump())
    db.add(agent)
    await db.commit()
    await db.refresh(agent)
    return agent

@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(agent_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Agent).where(Agent.id == agent_id))
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: str, agent_in: AgentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Agent).where(Agent.id == agent_id))
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    update_data = agent_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(agent, key, value)
    
    await db.commit()
    await db.refresh(agent)
    return agent

@router.delete("/{agent_id}")
async def delete_agent(agent_id: str, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Agent).where(Agent.id == agent_id))
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    await db.delete(agent)
    await db.commit()
    return {"status": "deleted", "agent_id": agent_id}
