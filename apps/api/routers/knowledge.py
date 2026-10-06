from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from packages.knowledge.rag import rag_pipeline

router = APIRouter(prefix="/api/v1/knowledge", tags=["Knowledge & RAG"])

class IngestRequest(BaseModel):
    source_id: str
    text: str

class SearchRequest(BaseModel):
    query: str
    top_k: int = 3

@router.post("/ingest")
async def ingest_document(req: IngestRequest):
    chunks = rag_pipeline.ingest_text(source_id=req.source_id, text=req.text)
    return {"status": "INGESTED", "chunk_count": len(chunks)}

@router.post("/search")
async def search_knowledge(req: SearchRequest):
    results = rag_pipeline.search_context(query=req.query, top_k=req.top_k)
    return {"query": req.query, "results": results}
