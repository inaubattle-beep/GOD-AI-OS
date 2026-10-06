from typing import Dict, Any, List, Optional
import time

class MemoryEntry:
    def __init__(self, memory_type: str, content: str, agent_id: Optional[str] = None, scope: str = "global", importance: float = 1.0):
        self.memory_type = memory_type # working, short_term, episodic, semantic, agent
        self.content = content
        self.agent_id = agent_id
        self.scope = scope
        self.importance = importance
        self.timestamp = time.time()

class MultiLayerMemoryStore:
    def __init__(self):
        self._items: List[MemoryEntry] = []

    def store(self, memory_type: str, content: str, agent_id: Optional[str] = None, scope: str = "global", importance: float = 1.0) -> MemoryEntry:
        entry = MemoryEntry(memory_type=memory_type, content=content, agent_id=agent_id, scope=scope, importance=importance)
        self._items.append(entry)
        return entry

    def query(self, query_text: str, agent_id: Optional[str] = None, limit: int = 5) -> List[Dict[str, Any]]:
        query_words = set(query_text.lower().split())
        results = []
        for item in self._items:
            if agent_id and item.agent_id and item.agent_id != agent_id:
                continue
            match_score = len(query_words.intersection(set(item.content.lower().split())))
            results.append((match_score, item))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [
            {
                "memory_type": item.memory_type,
                "content": item.content,
                "agent_id": item.agent_id,
                "importance": item.importance,
                "timestamp": item.timestamp
            }
            for score, item in results[:limit]
        ]

memory_store = MultiLayerMemoryStore()
