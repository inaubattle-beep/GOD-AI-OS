from typing import Dict, Any, List, Optional
import time

from packages.models.provider import ProviderRouter, LLMProvider, LLMResponse

class ModelSpec:
    def __init__(
        self,
        model_id: str,
        name: str,
        provider: str,
        context_window: int,
        coding_score: float,
        reasoning_score: float,
        speed_score: float,
        cost_per_1k_input: float,
        is_local: bool = False,
        supports_tools: bool = True
    ):
        self.model_id = model_id
        self.name = name
        self.provider = provider
        self.context_window = context_window
        self.coding_score = coding_score
        self.reasoning_score = reasoning_score
        self.speed_score = speed_score
        self.cost_per_1k_input = cost_per_1k_input
        self.is_local = is_local
        self.supports_tools = supports_tools

class ModelGateway:
    def __init__(self):
        self._models: Dict[str, ModelSpec] = {}
        self._register_default_models()

    def _register_default_models(self):
        self.register_model(ModelSpec(
            model_id="gpt-4o",
            name="OpenAI GPT-4o",
            provider="openai",
            context_window=128000,
            coding_score=0.95,
            reasoning_score=0.96,
            speed_score=0.90,
            cost_per_1k_input=0.0025,
            is_local=False
        ))
        self.register_model(ModelSpec(
            model_id="gemini-2.0-flash",
            name="Google Gemini 2.0 Flash",
            provider="gemini",
            context_window=1000000,
            coding_score=0.92,
            reasoning_score=0.93,
            speed_score=0.99,
            cost_per_1k_input=0.0001,
            is_local=False
        ))
        self.register_model(ModelSpec(
            model_id="claude-3-5-sonnet",
            name="Anthropic Claude 3.5 Sonnet",
            provider="anthropic",
            context_window=200000,
            coding_score=0.98,
            reasoning_score=0.97,
            speed_score=0.88,
            cost_per_1k_input=0.003,
            is_local=False
        ))
        self.register_model(ModelSpec(
            model_id="llama3-local",
            name="Ollama Llama 3 (Local)",
            provider="ollama",
            context_window=32000,
            coding_score=0.85,
            reasoning_score=0.84,
            speed_score=0.95,
            cost_per_1k_input=0.0,
            is_local=True
        ))
        self.register_model(ModelSpec(
            model_id="deepseek-r1-local",
            name="DeepSeek R1 Reasoning (Local)",
            provider="ollama",
            context_window=64000,
            coding_score=0.94,
            reasoning_score=0.97,
            speed_score=0.85,
            cost_per_1k_input=0.0,
            is_local=True
        ))

    def register_model(self, model_spec: ModelSpec):
        self._models[model_spec.model_id] = model_spec

    def list_models(self) -> List[Dict[str, Any]]:
        return [
            {
                "model_id": m.model_id,
                "name": m.name,
                "provider": m.provider,
                "context_window": m.context_window,
                "coding_score": m.coding_score,
                "reasoning_score": m.reasoning_score,
                "speed_score": m.speed_score,
                "cost_per_1k_input": m.cost_per_1k_input,
                "is_local": m.is_local,
                "supports_tools": m.supports_tools
            }
            for m in self._models.values()
        ]

    def route_task_to_model(self, task_type: str, require_privacy: bool = False, prefer_low_cost: bool = False) -> ModelSpec:
        """
        Model Router Logic:
        Selects optimal model based on task intent, cost, speed, reasoning, or privacy constraints.
        """
        if require_privacy:
            # Route to local model
            return self._models.get("llama3-local") or self._models["gpt-4o"]
        
        task_lower = task_type.lower()
        if "code" in task_lower or "developer" in task_lower or "bug" in task_lower:
            return self._models.get("claude-3-5-sonnet") or self._models["gpt-4o"]
        elif "reason" in task_lower or "math" in task_lower or "logic" in task_lower:
            return self._models.get("deepseek-r1-local") or self._models["gpt-4o"]
        elif prefer_low_cost or "quick" in task_lower or "fast" in task_lower:
            return self._models.get("gemini-2.0-flash") or self._models["gpt-4o"]
        
        return self._models["gpt-4o"]

    async def generate_with_router(
        self,
        prompt: str,
        system_instructions: Optional[str] = None,
        task_type: str = "general",
        require_privacy: bool = False,
        api_keys: Optional[Dict[str, str]] = None
    ) -> Dict[str, Any]:
        target_model = self.route_task_to_model(task_type, require_privacy=require_privacy)
        keys = api_keys or {}
        provider = ProviderRouter.get_provider(
            provider_name=target_model.provider,
            api_key=keys.get(target_model.provider, "mock-key")
        )

        response: LLMResponse = await provider.generate(
            prompt=prompt,
            system_instructions=system_instructions,
            model=target_model.model_id
        )

        return {
            "routed_model": target_model.model_id,
            "provider": target_model.provider,
            "is_local": target_model.is_local,
            "content": response.content,
            "input_tokens": response.input_tokens,
            "output_tokens": response.output_tokens,
            "estimated_cost_usd": round((response.input_tokens / 1000.0) * target_model.cost_per_1k_input, 6)
        }

model_gateway = ModelGateway()
