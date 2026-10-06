from typing import Dict, Any, List, Optional
import os
import re

class SkillDefinition:
    def __init__(self, name: str, description: str, instructions: str, category: str = "general", required_tools: Optional[List[str]] = None):
        self.name = name
        self.description = description
        self.instructions = instructions
        self.category = category
        self.required_tools = required_tools or []

class SkillRegistry:
    def __init__(self):
        self._skills: Dict[str, SkillDefinition] = {}
        self._register_default_skills()

    def register_skill(self, skill: SkillDefinition):
        self._skills[skill.name.lower()] = skill

    def list_skills(self) -> List[Dict[str, Any]]:
        return [
            {
                "name": s.name,
                "description": s.description,
                "category": s.category,
                "required_tools": s.required_tools,
                "instructions_snippet": s.instructions[:150] + "..."
            }
            for s in self._skills.values()
        ]

    def get_skill(self, name: str) -> Optional[SkillDefinition]:
        return self._skills.get(name.lower())

    def _register_default_skills(self):
        self.register_skill(SkillDefinition(
            name="code_refactoring",
            description="Refactor existing source code to improve modularity, type safety, and readability.",
            instructions="1. Inspect source module.\n2. Preserve existing API signatures.\n3. Add type annotations and async/await handlers.\n4. Run test suite.",
            category="coding",
            required_tools=["file_read", "file_write"]
        ))
        self.register_skill(SkillDefinition(
            name="web_search",
            description="Perform targeted web searches and synthesize factual conclusions.",
            instructions="1. Identify core search keywords.\n2. Query web source.\n3. Cross-reference citations.\n4. Draft concise report.",
            category="research",
            required_tools=["http_request"]
        ))

skill_registry = SkillRegistry()
