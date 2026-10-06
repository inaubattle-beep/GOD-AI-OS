from typing import Dict, Any, List, Optional
import time

class SystemTelemetryTracker:
    def __init__(self):
        self._total_runs = 0
        self._total_tokens = 0
        self._total_cost_usd = 0.0
        self._execution_history: List[Dict[str, Any]] = []

    def record_run(self, agent_id: str, prompt: str, duration_sec: float, tokens: int, cost_usd: float, status: str):
        self._total_runs += 1
        self._total_tokens += tokens
        self._total_cost_usd += cost_usd
        
        record = {
            "timestamp": time.time(),
            "agent_id": agent_id,
            "prompt_snippet": prompt[:60],
            "duration_sec": round(duration_sec, 3),
            "tokens": tokens,
            "cost_usd": round(cost_usd, 4),
            "status": status
        }
        self._execution_history.append(record)

    def get_summary_metrics(self) -> Dict[str, Any]:
        return {
            "total_agent_runs": self._total_runs,
            "total_tokens_consumed": self._total_tokens,
            "total_estimated_cost_usd": round(self._total_cost_usd, 4),
            "recent_runs": self._execution_history[-10:]
        }

telemetry_tracker = SystemTelemetryTracker()
