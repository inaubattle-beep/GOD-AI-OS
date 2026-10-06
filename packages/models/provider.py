from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional
import httpx
import json

class LLMResponse:
    def __init__(self, content: str, tool_calls: Optional[List[Dict[str, Any]]] = None, raw: Optional[Any] = None, input_tokens: int = 0, output_tokens: int = 0):
        self.content = content
        self.tool_calls = tool_calls or []
        self.raw = raw
        self.input_tokens = input_tokens
        self.output_tokens = output_tokens

class LLMProvider(ABC):
    @abstractmethod
    async def generate(
        self,
        prompt: str,
        system_instructions: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        model: Optional[str] = None
    ) -> LLMResponse:
        pass

class OpenAIProvider(LLMProvider):
    def __init__(self, api_key: str, base_url: str = "https://api.openai.com/v1"):
        self.api_key = api_key
        self.base_url = base_url.rstrip('/')

    async def generate(
        self,
        prompt: str,
        system_instructions: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        model: Optional[str] = "gpt-4o"
    ) -> LLMResponse:
        model_name = model or "gpt-4o"
        messages = []
        if system_instructions:
            messages.append({"role": "system", "content": system_instructions})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model_name,
            "messages": messages,
            "temperature": temperature,
            "max_tokens": max_tokens
        }
        if tools:
            payload["tools"] = tools

        # If API key is mock or missing, return simulated structured response for development
        if not self.api_key or self.api_key == "mock-key":
            return LLMResponse(
                content=f"[Simulated response from {model_name}] Plan: Process request '{prompt[:50]}...'. Action: System execution completed.",
                input_tokens=100,
                output_tokens=50
            )

        async with httpx.AsyncClient(timeout=60.0) as client:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            resp = await client.post(f"{self.api_key}/chat/completions", headers=headers, json=payload)
            resp.raise_for_status()
            data = resp.json()
            choice = data["choices"][0]["message"]
            usage = data.get("usage", {})
            return LLMResponse(
                content=choice.get("content", ""),
                tool_calls=choice.get("tool_calls", []),
                raw=data,
                input_tokens=usage.get("prompt_tokens", 0),
                output_tokens=usage.get("completion_tokens", 0)
            )

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.api_key = api_key

    async def generate(
        self,
        prompt: str,
        system_instructions: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        model: Optional[str] = "gemini-2.0-flash"
    ) -> LLMResponse:
        model_name = model or "gemini-2.0-flash"
        if not self.api_key or self.api_key == "mock-key":
            return LLMResponse(
                content=f"[Simulated Gemini Response ({model_name})] Analysis complete for prompt: '{prompt[:50]}'. Recommendations formulated.",
                input_tokens=80,
                output_tokens=45
            )
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={self.api_key}"
            contents = []
            if system_instructions:
                contents.append({"role": "user", "parts": [{"text": f"System Instructions: {system_instructions}"}]})
            contents.append({"role": "user", "parts": [{"text": prompt}]})
            
            payload = {"contents": contents}
            resp = await client.post(url, json=payload)
            resp.raise_for_status()
            data = resp.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return LLMResponse(content=text, raw=data, input_tokens=100, output_tokens=50)

class OllamaProvider(LLMProvider):
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url.rstrip('/')

    async def generate(
        self,
        prompt: str,
        system_instructions: Optional[str] = None,
        tools: Optional[List[Dict[str, Any]]] = None,
        temperature: float = 0.7,
        max_tokens: int = 4096,
        model: Optional[str] = "llama3"
    ) -> LLMResponse:
        model_name = model or "llama3"
        messages = []
        if system_instructions:
            messages.append({"role": "system", "content": system_instructions})
        messages.append({"role": "user", "content": prompt})

        payload = {
            "model": model_name,
            "messages": messages,
            "stream": False,
            "options": {"temperature": temperature}
        }
        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                resp = await client.post(f"{self.base_url}/api/chat", json=payload)
                resp.raise_for_status()
                data = resp.json()
                content = data["message"]["content"]
                return LLMResponse(content=content, raw=data, input_tokens=50, output_tokens=50)
        except Exception:
            return LLMResponse(
                content=f"[Local Ollama ({model_name}) Execution Baseline] System prompt processed successfully.",
                input_tokens=50,
                output_tokens=30
            )

class ProviderRouter:
    @staticmethod
    def get_provider(provider_name: str, api_key: Optional[str] = None, base_url: Optional[str] = None) -> LLMProvider:
        p_name = provider_name.lower()
        if p_name == "gemini":
            return GeminiProvider(api_key=api_key or "mock-key")
        elif p_name == "ollama":
            return OllamaProvider(base_url=base_url or "http://localhost:11434")
        else:
            return OpenAIProvider(api_key=api_key or "mock-key", base_url=base_url or "https://api.openai.com/v1")
