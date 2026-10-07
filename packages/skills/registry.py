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
        author: str = "AgenticSkills.io",
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
        self._register_agentic_skills()

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

    def update_skill(self, skill_id: str, updated_fields: Dict[str, Any]) -> Optional[SkillDefinition]:
        skill = self.get_skill(skill_id)
        if not skill:
            return None
        for key, val in updated_fields.items():
            if hasattr(skill, key):
                setattr(skill, key, val)
        return skill

    def delete_skill(self, skill_id: str) -> bool:
        sid = skill_id.lower()
        if sid in self._skills:
            del self._skills[sid]
            return True
        return False

    def _register_agentic_skills(self):
        # 1. GitHub Code Reviewer
        self.register_skill(SkillDefinition(
            skill_id="github_pr_reviewer",
            name="GitHub Automated PR & Diff Reviewer",
            description="Autonomous pull request review, diff analysis, security audit, and actionable PR comments.",
            instructions="1. Fetch PR git diff.\n2. Audit code modifications against project style guidelines.\n3. Verify test coverage for added lines.\n4. Submit inline review feedback.",
            category="coding",
            required_tools=["mcp_github_get_repo", "file_read"],
            author="AgenticSkills.io"
        ))

        # 2. Database Architect & Query Optimizer
        self.register_skill(SkillDefinition(
            skill_id="pg_db_architect",
            name="PostgreSQL Database Architect & Index Optimizer",
            description="Generate Alembic/SQL schema migrations, inspect locks, analyze EXPLAIN execution plans, and tune indexes.",
            instructions="1. Inspect table schemas and query latencies.\n2. Analyze query execution plans for full table scans.\n3. Formulate partial or composite index recommendations.\n4. Draft migration script.",
            category="database",
            required_tools=["mcp_pg_query", "mcp_pg_inspect_schema"],
            author="AgenticSkills.io"
        ))

        # 3. Docker & Container Orchestrator
        self.register_skill(SkillDefinition(
            skill_id="docker_orchestrator",
            name="Docker Container & Compose Orchestrator",
            description="Inspect container health, validate Dockerfile builds, analyze log streams, and scan container images.",
            instructions="1. Inspect docker-compose.yml configuration.\n2. Verify service healthcheck rules and volume mounts.\n3. Scan container base images for security vulnerabilities.\n4. Fix startup failures.",
            category="devops",
            required_tools=["shell_exec", "file_read"],
            author="AgenticSkills.io"
        ))

        # 4. OpenAPI & REST Integration Generator
        self.register_skill(SkillDefinition(
            skill_id="openapi_generator",
            name="OpenAPI v3 Spec & REST API Generator",
            description="Generate clean OpenAPI v3 schema definitions, FastAPI routers, Pydantic schemas, and Swagger docs.",
            instructions="1. Parse target domain entities and relationships.\n2. Write Pydantic v2 schemas with field descriptions.\n3. Build async FastAPI route handlers.\n4. Verify OpenAPI schema compliance.",
            category="coding",
            required_tools=["file_write", "file_read"],
            author="AgenticSkills.io"
        ))

        # 5. OWASP Top 10 Security Auditor
        self.register_skill(SkillDefinition(
            skill_id="owasp_security_auditor",
            name="OWASP Top 10 Application Security Auditor",
            description="Audit web applications for SQL injection, XSS, CSRF, insecure deserialization, and prompt injection.",
            instructions="1. Perform static code analysis (SAST) on endpoint handlers.\n2. Verify input validation and parametrization.\n3. Inspect CORS origins and secret management.\n4. Generate vulnerability report.",
            category="security",
            required_tools=["file_read", "security_scanner"],
            author="AgenticSkills.io"
        ))

        # 6. Data Science & ML Pipeline Operator
        self.register_skill(SkillDefinition(
            skill_id="ml_pipeline_operator",
            name="Data Science & ML Pipeline Operator",
            description="Perform exploratory data analysis (EDA), data cleaning, statistical profiling, and model training.",
            instructions="1. Inspect input CSV/Parquet dataset schema.\n2. Compute descriptive statistics and missing value distributions.\n3. Preprocess feature vectors.\n4. Train baseline classifier/regressor.",
            category="data",
            required_tools=["python_eval", "file_read"],
            author="AgenticSkills.io"
        ))

        # 7. DevOps Incident Responder
        self.register_skill(SkillDefinition(
            skill_id="devops_incident_responder",
            name="DevOps Real-Time Incident Responder",
            description="Diagnose system log anomalies, correlate telemetry spikes, conduct root cause analysis (RCA), and draft incident reports.",
            instructions="1. Fetch recent server log output.\n2. Isolate exception stack traces and timestamp spikes.\n3. Identify offending service commit or config change.\n4. Draft Root Cause Analysis (RCA).",
            category="devops",
            required_tools=["sys_metrics", "shell_exec"],
            author="AgenticSkills.io"
        ))

        # 8. Web Performance & Technical SEO
        self.register_skill(SkillDefinition(
            skill_id="web_performance_seo",
            name="Core Web Vitals & Technical SEO Optimizer",
            description="Audit LCP, INP, CLS performance metrics, optimize image assets, structure semantic HTML, and generate sitemaps.",
            instructions="1. Audit page rendering performance and DOM depth.\n2. Verify semantic heading hierarchy (h1, h2, h3).\n3. Inspect meta title tags and OpenGraph cards.\n4. Provide optimization diffs.",
            category="marketing",
            required_tools=["http_request", "page_parser"],
            author="AgenticSkills.io"
        ))

        # 9. Enterprise CRM Lead Automation
        self.register_skill(SkillDefinition(
            skill_id="crm_lead_automation",
            name="Enterprise Lead Qualification & CRM Automation",
            description="Qualify inbound sales leads, compute intent scores, enrich contact data, and sync records into CRM.",
            instructions="1. Extract contact details from inbound submission.\n2. Compute lead qualification score based on company size and budget.\n3. Sync contact record into CRM database.\n4. Schedule follow-up email.",
            category="sales",
            required_tools=["crm_write", "send_email"],
            author="AgenticSkills.io"
        ))

        # 10. Multi-Layer Memory Graph Navigation
        self.register_skill(SkillDefinition(
            skill_id="memory_graph_navigator",
            name="Multi-Layer Episodic & Semantic Memory Graph Navigator",
            description="Query long-term agent memory, retrieve semantic graph relationships, and build contextual recall.",
            instructions="1. Extract intent keywords from current turn.\n2. Query episodic memory graph.\n3. Rank retrieved facts by confidence and importance score.\n4. Inject context into prompt.",
            category="memory",
            required_tools=["vector_query", "knowledge_search"],
            author="AgenticSkills.io"
        ))

skill_registry = SkillRegistry()
