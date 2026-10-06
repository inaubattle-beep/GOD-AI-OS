from typing import Dict, Any, List, Optional
import time
import json

from packages.models.provider import ProviderRouter, LLMResponse
from packages.agent-factory.factory import AgentFactory

class AgentExecutionTrace:
    def __init__(self, agent_id: str, prompt: str):
        self.agent_id = agent_id
        self.prompt = prompt
        self.steps: List[Dict[str, Any]] = []
        self.start_time = time.time()
        self.end_time: Optional[float] = None
        self.tokens_used = 0
        self.cost_usd = 0.0
        self.status = "RUNNING"
        self.result: Optional[str] = None
        self.error: Optional[str] = None

    def add_step(self, phase: str, details: Dict[str, Any]):
        self.steps.append({
            "timestamp": time.time(),
            "phase": phase,
            "details": details
        })

    def complete(self, result: str):
        self.end_time = time.time()
        self.status = "COMPLETED"
        self.result = result

    def fail(self, error: str):
        self.end_time = time.time()
        self.status = "FAILED"
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        duration = (self.end_time or time.time()) - self.start_time
        return {
            "agent_id": self.agent_id,
            "prompt": self.prompt,
            "status": self.status,
            "duration_sec": round(duration, 3),
            "tokens_used": self.tokens_used,
            "cost_usd": self.cost_usd,
            "steps": self.steps,
            "result": self.result,
            "error": self.error
        }

class MotherAgentEngine:
    def __init__(self, provider_name: str = "openai", api_key: Optional[str] = None):
        self.provider = ProviderRouter.get_provider(provider_name, api_key=api_key)

    async def execute_task(
        self,
        user_prompt: str,
        system_instructions: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        max_retries: int = 3
    ) -> AgentExecutionTrace:
        trace = AgentExecutionTrace(agent_id="mother-agent", prompt=user_prompt)
        
        # Step 1: OBSERVE & UNDERSTAND
        trace.add_step("OBSERVE", {"prompt": user_prompt})
        
        # Step 2: PLAN & TASK DECOMPOSITION
        planner_instructions = (
            "You are GOD AI OS — Mother Agent, the central orchestrator.\n"
            "Analyze the user prompt. Decompose into concrete steps. Identify required tools or specialized agents."
        )
        if system_instructions:
            planner_instructions += f"\n\nContext:\n{system_instructions}"

        plan_response = await self.provider.generate(
            prompt=f"Task: {user_prompt}\nProvide a structured step-by-step plan to accomplish this.",
            system_instructions=planner_instructions,
            temperature=0.3
        )
        trace.tokens_used += plan_response.input_tokens + plan_response.output_tokens
        trace.add_step("PLAN", {"plan": plan_response.content})

        # Step 3: ACT & EXECUTE
        act_instructions = (
            "Execute the task based on the plan. Return a detailed, structured final response."
        )
        act_response = await self.provider.generate(
            prompt=f"User Goal: {user_prompt}\nExecution Plan: {plan_response.content}\n\nExecute step-by-step and produce the final result.",
            system_instructions=act_instructions,
            temperature=0.4
        )
        trace.tokens_used += act_response.input_tokens + act_response.output_tokens
        trace.add_step("ACT", {"response": act_response.content})

        # Step 4: EVALUATE RESULT
        eval_instructions = "Evaluate the output for correctness, factual consistency, and goal completion. Grade PASS or FAIL."
        eval_response = await self.provider.generate(
            prompt=f"Goal: {user_prompt}\nResult Output: {act_response.content}\nDoes this satisfy the user goal cleanly?",
            system_instructions=eval_instructions,
            temperature=0.1
        )
        trace.tokens_used += eval_response.input_tokens + eval_response.output_tokens
        trace.add_step("EVALUATE", {"evaluation": eval_response.content})

        trace.complete(result=act_response.content)
        return trace

    async def understand_and_deploy_agent(self, user_prompt: str) -> Dict[str, Any]:
        """
        Natural Language System Administration:
        e.g. "Create a coding agent with GitHub access."
        Mother Agent determines goal, instructions, selects template or creates custom spec.
        """
        prompt_lower = user_prompt.lower()
        matched_template = None
        for t in AgentFactory.list_templates():
            if t["name"].lower() in prompt_lower or t["category"] in prompt_lower:
                matched_template = t
                break
        
        if not matched_template:
            spec = AgentFactory.create_agent_spec(name="Custom Agent", custom_instructions=user_prompt)
        else:
            spec = AgentFactory.create_agent_spec(name=matched_template["name"], custom_instructions=user_prompt)

        return {
            "status": "CREATED",
            "agent_spec": spec.model_dump(),
            "message": f"Mother Agent instantiated agent '{spec.name}' with role '{spec.role}' and goal '{spec.goal}'."
        }
