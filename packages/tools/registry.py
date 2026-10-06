from typing import Dict, Any, List, Optional, Callable
import subprocess
import os
import httpx
import json
import asyncio

class ToolResult:
    def __init__(self, success: bool, output: Any, error: Optional[str] = None):
        self.success = success
        self.output = output
        self.error = error

    def to_dict(self) -> Dict[str, Any]:
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error
        }

class ToolRegistry:
    def __init__(self):
        self._tools: Dict[str, Dict[str, Any]] = {}
        self._register_defaults()

    def register_tool(self, name: str, description: str, category: str, risk_level: str, handler: Callable, input_schema: Dict[str, Any]):
        self._tools[name] = {
            "name": name,
            "description": description,
            "category": category,
            "risk_level": risk_level,
            "handler": handler,
            "input_schema": input_schema,
            "enabled": True
        }

    def list_tools(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": meta["name"],
                "description": meta["description"],
                "category": meta["category"],
                "risk_level": meta["risk_level"],
                "input_schema": meta["input_schema"],
                "enabled": meta["enabled"]
            }
            for meta in self._tools.values()
        ]

    async def execute_tool(self, name: str, params: Dict[str, Any]) -> ToolResult:
        if name not in self._tools:
            return ToolResult(success=False, output=None, error=f"Tool '{name}' not found in registry.")
        
        tool = self._tools[name]
        if not tool["enabled"]:
            return ToolResult(success=False, output=None, error=f"Tool '{name}' is currently disabled.")

        try:
            handler = tool["handler"]
            if asyncio.iscoroutinefunction(handler):
                result = await handler(**params)
            else:
                result = handler(**params)
            return ToolResult(success=True, output=result)
        except Exception as e:
            return ToolResult(success=False, output=None, error=str(e))

    def _register_defaults(self):
        # 1. HTTP Request Tool
        async def http_request(url: str, method: str = "GET", headers: Optional[Dict[str, str]] = None, body: Optional[Dict[str, Any]] = None):
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.request(method=method, url=url, headers=headers, json=body)
                return {"status_code": resp.status_code, "text": resp.text[:2000]}

        self.register_tool(
            name="http_request",
            description="Send an HTTP request (GET, POST, PUT, DELETE) to a target URL.",
            category="web",
            risk_level="MEDIUM",
            handler=http_request,
            input_schema={"url": "string", "method": "string"}
        )

        # 2. File Read Tool
        def file_read(filepath: str) -> str:
            if not os.path.exists(filepath):
                raise FileNotFoundError(f"File not found: {filepath}")
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                return f.read(50000)

        self.register_tool(
            name="file_read",
            description="Read the contents of a text file.",
            category="files",
            risk_level="LOW",
            handler=file_read,
            input_schema={"filepath": "string"}
        )

        # 3. File Write Tool
        def file_write(filepath: str, content: str) -> str:
            os.makedirs(os.path.dirname(os.path.abspath(filepath)), exist_ok=True)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            return f"File successfully written to {filepath}"

        self.register_tool(
            name="file_write",
            description="Write text content to a specified file path.",
            category="files",
            risk_level="MEDIUM",
            handler=file_write,
            input_schema={"filepath": "string", "content": "string"}
        )

        # 4. Shell Exec Tool
        def shell_exec(command: str, cwd: Optional[str] = None) -> Dict[str, Any]:
            res = subprocess.run(
                command,
                shell=True,
                cwd=cwd or os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=30
            )
            return {
                "exit_code": res.returncode,
                "stdout": res.stdout[:5000],
                "stderr": res.stderr[:5000]
            }

        self.register_tool(
            name="shell_exec",
            description="Execute a shell command within the workspace directory.",
            category="system",
            risk_level="HIGH",
            handler=shell_exec,
            input_schema={"command": "string"}
        )

tool_registry = ToolRegistry()
