from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from apps.api.database import get_db
from apps.api.schemas.schemas import MotherAgentChatRequest
from packages.agent_core.engine import MotherAgentEngine
from apps.api.models.entities import Agent

router = APIRouter(prefix="/api/v1/mother", tags=["Mother Agent"])
engine = MotherAgentEngine(provider_name="openai")

@router.post("/chat")
async def mother_agent_chat(request: MotherAgentChatRequest, db: AsyncSession = Depends(get_db)):
    """
    Primary Mother Agent Chat Endpoint:
    Receives user request -> OBSERVE -> PLAN -> SELECT AGENT/TOOLS -> ACT -> EVALUATE -> RETURN RESULT
    """
    prompt_lower = request.user_prompt.lower()
    intent_keywords = ["create", "build", "deploy", "instantiate", "make an agent", "agent for"]
    if any(k in prompt_lower for k in intent_keywords) and "agent" in prompt_lower:
        deployment_res = await engine.understand_and_deploy_agent(request.user_prompt)
        spec = deployment_res["agent_spec"]
        new_agent = Agent(**spec)
        db.add(new_agent)
        await db.commit()
        await db.refresh(new_agent)
        return {
            "status": "AGENT_CREATED",
            "message": deployment_res["message"],
            "agent": {
                "id": new_agent.id,
                "name": new_agent.name,
                "role": new_agent.role,
                "goal": new_agent.goal
            }
        }
    
    trace = await engine.execute_task(user_prompt=request.user_prompt)
    return {
        "status": trace.status,
        "result": trace.result,
        "trace": trace.to_dict()
    }
