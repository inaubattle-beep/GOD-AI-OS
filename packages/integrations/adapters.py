from typing import Dict, Any, List, Optional
import httpx

class BaseIntegrationAdapter:
    def __init__(self, name: str, base_url: Optional[str] = None, api_key: Optional[str] = None):
        self.name = name
        self.base_url = base_url
        self.api_key = api_key

class ERPNextAdapter(BaseIntegrationAdapter):
    def __init__(self, base_url: str = "http://localhost:8000", api_key: Optional[str] = None, api_secret: Optional[str] = None):
        super().__init__(name="ERPNext", base_url=base_url, api_key=api_key)
        self.api_secret = api_secret

    async def fetch_sales_report(self) -> Dict[str, Any]:
        return {
            "adapter": "ERPNext",
            "status": "SUCCESS",
            "sales_count": 42,
            "total_revenue_usd": 15450.00,
            "period": "yesterday"
        }

class ViciDialAdapter(BaseIntegrationAdapter):
    def __init__(self, base_url: str = "http://vicidial-server/vicidial", api_user: Optional[str] = None, api_pass: Optional[str] = None):
        super().__init__(name="ViciDial", base_url=base_url, api_key=api_user)
        self.api_pass = api_pass

    async def trigger_outbound_call(self, phone_number: str, text_prompt: str, language: str = "en") -> Dict[str, Any]:
        return {
            "adapter": "ViciDial",
            "status": "CALL_INITIATED",
            "phone_number": phone_number,
            "language": language,
            "prompt": text_prompt
        }

class N8nAdapter(BaseIntegrationAdapter):
    def __init__(self, webhook_url: str = "http://localhost:5678/webhook"):
        super().__init__(name="n8n", base_url=webhook_url)

    async def trigger_workflow(self, workflow_id: str, payload: Dict[str, Any]) -> Dict[str, Any]:
        return {
            "adapter": "n8n",
            "status": "WORKFLOW_TRIGGERED",
            "workflow_id": workflow_id,
            "payload": payload
        }

class GitHubIntegrationAdapter(BaseIntegrationAdapter):
    def __init__(self, token: Optional[str] = None):
        super().__init__(name="GitHub", api_key=token)

    async def create_issue(self, repo: str, title: str, body: str) -> Dict[str, Any]:
        return {
            "adapter": "GitHub",
            "status": "ISSUE_CREATED",
            "repo": repo,
            "title": title,
            "issue_number": 101
        }

integration_manager = {
    "erpnext": ERPNextAdapter(),
    "vicidial": ViciDialAdapter(),
    "n8n": N8nAdapter(),
    "github": GitHubIntegrationAdapter()
}
