from typing import Dict, Any, List, Optional
import os
import re

class KnowledgeChunk:
    def __init__(self, chunk_id: str, source_id: str, content: str, metadata: Optional[Dict[str, Any]] = None):
        self.chunk_id = chunk_id
        self.source_id = source_id
        self.content = content
        self.metadata = metadata or {}

class KnowledgeRAGPipeline:
    def __init__(self):
        self._chunks: List[KnowledgeChunk] = []

    def ingest_text(self, source_id: str, text: str, chunk_size: int = 500, overlap: int = 50) -> List[KnowledgeChunk]:
        paragraphs = text.split("\n\n")
        new_chunks = []
        chunk_counter = 0
        
        for para in paragraphs:
            para = para.strip()
            if not para:
                continue
            words = para.split()
            for i in range(0, len(words), chunk_size - overlap):
                chunk_text = " ".join(words[i:i + chunk_size])
                chunk_id = f"{source_id}-chunk-{chunk_counter}"
                chunk = KnowledgeChunk(chunk_id=chunk_id, source_id=source_id, content=chunk_text)
                self._chunks.append(chunk)
                new_chunks.append(chunk)
                chunk_counter += 1
                
        return new_chunks

    def search_context(self, query: str, top_k: int = 3) -> List[Dict[str, Any]]:
        query_terms = set(re.findall(r'\w+', query.lower()))
        scored = []
        for chunk in self._chunks:
            chunk_terms = set(re.findall(r'\w+', chunk.content.lower()))
            overlap_score = len(query_terms.intersection(chunk_terms))
            scored.append((overlap_score, chunk))
        
        scored.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "chunk_id": item.chunk_id,
                "source_id": item.source_id,
                "content": item.content,
                "relevance_score": score
            }
            for score, item in scored[:top_k]
        ]

rag_pipeline = KnowledgeRAGPipeline()
