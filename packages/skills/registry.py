from typing import Dict, Any, List, Optional
import os
import re

class SkillDefinition:
    def __init__(
        self,
        skill_id: str,
        name: str,
        description: str,
        instructions: str,
        category: str = "general",
        required_tools: Optional[List[str]] = None,
        author: str = "System",
        version: str = "1.0.0"
    ):
        self.skill_id = skill_id
        self.name = name
        self.description = description
        self.instructions = instructions
        self.category = category
        self.required_tools = required_tools or []
        self.author = author
        self.version = version
        self.enabled = True

class SkillRegistry:
    def __init__(self):
        self._skills: Dict[str, SkillDefinition] = {}
        self._register_default_skills()

    def register_skill(self, skill: SkillDefinition):
        self._skills[skill.skill_id.lower()] = skill

    def list_skills(self) -> List[Dict[str, Any]]:
        return [
            {
                "skill_id": s.skill_id,
                "name": s.name,
                "description": s.description,
                "category": s.category,
                "required_tools": s.required_tools,
                "author": s.author,
                "version": s.version,
                "enabled": s.enabled,
                "instructions_snippet": s.instructions[:150] + "..."
            }
            for s in self._skills.values()
        ]

    def get_skill(self, skill_id: str) -> Optional[SkillDefinition]:
        return self._skills.get(skill_id.lower())

    def _register_default_skills(self):
        self.register_skill(SkillDefinition(
            skill_id="code_refactoring",
            name="Professional Code Refactoring & Linting",
            description="Refactor existing source code to improve modularity, static type safety, and maintainability.",
            instructions="1. Inspect target source module.\n2. Preserve existing public API signatures.\n3. Add type annotations and async handlers.\n4. Execute unit test suite.",
            category="coding",
            required_tools=["file_read", "file_write", "shell_exec"],
            author="Software Engineering Lead"
        ))
        self.register_skill(SkillDefinition(
            skill_id="web_search",
            name="Deep Web Research & Citation Analysis",
            description="Perform targeted web searches, extract content, fact-check citations, and generate reports.",
            instructions="1. Formulate search query keywords.\n2. Fetch target pages.\n3. Verify cross-source accuracy.\n4. Structure summary report with links.",
            category="research",
            required_tools=["http_request", "file_write"],
            author="Research Ops"
        ))
        self.register_skill(SkillDefinition(
            skill_id="financial_auditing",
            name="Quantitative Financial Balance Sheet Audit",
            description="Parse balance sheets, calculate operating margins, verify tax compliance, and flag cost anomalies.",
            instructions="1. Extract revenue and operating expense line items.\n2. Compute EBITDA, ROI, and margin variance.\n3. Compare with historical quarterly benchmarks.\n4. Flag discrepancies.",
            category="finance",
            required_tools=["file_read", "calculator"],
            author="Financial Analytics"
        ))
        self.register_skill(SkillDefinition(
            skill_id="vulnerability_scanning",
            name="AppSec Vulnerability & Dependency Scan",
            description="Scan source code repositories for CVE dependencies, exposed secrets, and security risks.",
            instructions="1. Inspect package lockfiles.\n2. Match dependency versions against CVE advisory database.\n3. Scan source for hardcoded API keys.\n4. Report severity matrix.",
            category="security",
            required_tools=["file_read", "security_scanner"],
            author="Security Team"
        ))
        self.register_skill(SkillDefinition(
            skill_id="voice_synthesis",
            name="Multilingual Voice Dialog & IVR Management",
            description="Synthesize natural low-latency text-to-speech dialog in English, Bengali, and Spanish.",
            instructions="1. Process incoming transcript.\n2. Select appropriate TTS voice timbre and emotion model.\n3. Generate audio buffer stream.\n4. Dispatch to ViciDial IVR line.",
            category="communication",
            required_tools=["audio_stream", "tts_generate"],
            author="Speech AI Specialist"
        ))
        self.register_skill(SkillDefinition(
            skill_id="database_optimization",
            name="SQL Query Performance & Index Tuning",
            description="Analyze slow query logs, evaluate EXPLAIN execution plans, and generate composite index recommendations.",
            instructions="1. Inspect database query execution plan.\n2. Identify full table scans.\n3. Formulate minimal index recommendations.\n4. Benchmark query latency improvements.",
            category="database",
            required_tools=["db_query", "python_eval"],
            author="Database Operations"
        ))
        self.register_skill(SkillDefinition(
            skill_id="technical_copywriting",
            name="Developer Marketing & Content Copywriting",
            description="Draft engaging technical blog posts, release notes, documentation, and product announcements.",
            instructions="1. Identify target developer audience persona.\n2. Highlight key technical architecture differentiators.\n3. Format with clean GFM markdown.\n4. Optimize title meta tags.",
            category="marketing",
            required_tools=["file_write"],
            author="Growth Engineering"
        ))

skill_registry = SkillRegistry()
