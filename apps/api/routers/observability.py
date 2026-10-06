from fastapi import APIRouter
from packages.observability.tracer import telemetry_tracker

router = APIRouter(prefix="/api/v1/observability", tags=["Observability & Telemetry"])

@router.get("/metrics")
async def get_system_metrics():
    return telemetry_tracker.get_summary_metrics()
