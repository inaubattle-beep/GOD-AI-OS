from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict, Any

from packages.workflow.engine import workflow_engine

router = APIRouter(prefix="/api/v1/workflows", tags=["Workflows"])

class WorkflowRunRequest(BaseModel):
    nodes: List[Dict[str, Any]]
    edges: List[Dict[str, Any]]
    initial_input: Dict[str, Any]

@router.post("/execute")
async def execute_workflow(req: WorkflowRunRequest):
    result = await workflow_engine.execute_dag(nodes=req.nodes, edges=req.edges, initial_input=req.initial_input)
    return result
