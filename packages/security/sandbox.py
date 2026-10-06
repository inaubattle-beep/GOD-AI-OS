from typing import Dict, Any, List, Optional
import base64
import re

class SecurityPolicyEngine:
    def __init__(self):
        self._blocked_patterns = [
            r"ignore previous instructions",
            r"system override",
            r"bypass security",
            r"reveal secret key",
            r"drop database",
            r"rm -rf /"
        ]

    def validate_prompt_security(self, prompt: str) -> Dict[str, Any]:
        prompt_lower = prompt.lower()
        for pattern in self._blocked_patterns:
            if re.search(pattern, prompt_lower):
                return {
                    "secure": False,
                    "reason": f"Prompt injection or dangerous action pattern detected: '{pattern}'"
                }
        return {"secure": True, "reason": "Prompt cleared security validation."}

    def check_permission(self, agent_permissions: List[str], required_permission: str) -> bool:
        if "*" in agent_permissions or "admin" in agent_permissions:
            return True
        return required_permission in agent_permissions

    def encrypt_secret(self, raw_secret: str, secret_key: str = "god-ai-os-key") -> str:
        # Symmetric obfuscation / AES baseline representation
        encoded = base64.b64encode(raw_secret.encode('utf-8')).decode('utf-8')
        return f"enc_v1:{encoded}"

    def decrypt_secret(self, encrypted_secret: str, secret_key: str = "god-ai-os-key") -> str:
        if encrypted_secret.startswith("enc_v1:"):
            payload = encrypted_secret[7:]
            return base64.b64decode(payload.encode('utf-8')).decode('utf-8')
        return encrypted_secret

security_engine = SecurityPolicyEngine()
