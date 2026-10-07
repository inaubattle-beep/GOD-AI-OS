from typing import Dict, Any, List, Optional
from apps.api.schemas.schemas import AgentCreate

BUILTIN_AGENT_TEMPLATES: List[Dict[str, Any]] = [
    {
        "name": "Coding Agent",
        "category": "engineering",
        "role": "Senior Full-Stack AI Engineer",
        "goal": "Write, debug, refactor, and review clean production-grade code adhering to best practices.",
        "system_instructions": "You are a master Software Engineer. Inspect architecture, adhere to static typing, write robust unit tests, and never swallow exceptions.",
        "skills": ["code_refactoring", "unit_testing", "architecture_design"],
        "tools": ["shell_exec", "file_read", "file_write", "git_status"],
        "permissions": ["file.read", "file.write", "shell.execute"]
    },
    {
        "name": "Research Agent",
        "category": "research",
        "role": "Principal Research Analyst",
        "goal": "Gather, synthesize, fact-check, and summarize complex domain knowledge and literature.",
        "system_instructions": "Conduct deep objective research, extract key metrics, compare sources, and summarize clear actionable reports.",
        "skills": ["web_search", "fact_checking", "document_summarization"],
        "tools": ["http_request", "file_read"],
        "permissions": ["web.search", "file.read"]
    },
    {
        "name": "Browser Agent",
        "category": "automation",
        "role": "Autonomous Web Navigator",
        "goal": "Interact with web applications, extract structured data, perform form submissions, and automate web workflows.",
        "system_instructions": "Navigate websites safely, extract target DOM elements, respect dynamic rendering, and avoid unintended actions.",
        "skills": ["browser_automation", "web_scraping"],
        "tools": ["browser_click", "browser_type", "browser_scrape"],
        "permissions": ["browser.navigate", "browser.interact"]
    },
    {
        "name": "Computer Use Agent",
        "category": "automation",
        "role": "OS Desktop Automation Specialist",
        "goal": "Perform desktop level interactions, screenshot inspection, dynamic GUI control, and app orchestration.",
        "system_instructions": "Execute precise OS-level commands and GUI interactions safely within sandboxed security boundaries.",
        "skills": ["desktop_gui_control", "keyboard_mouse_simulation"],
        "tools": ["screenshot", "mouse_click", "key_press"],
        "permissions": ["desktop.control"]
    },
    {
        "name": "Voice Agent",
        "category": "communication",
        "role": "Realtime Audio & Speech Specialist",
        "goal": "Handle bidirectional voice interactions, speech-to-text, text-to-speech, and IVR dialog systems.",
        "system_instructions": "Process natural low-latency voice communications in multiple target languages including English and Bengali.",
        "skills": ["voice_synthesis", "speech_recognition", "conversational_flow"],
        "tools": ["audio_stream", "tts_generate"],
        "permissions": ["audio.input", "audio.output"]
    },
    {
        "name": "Communication Agent",
        "category": "communication",
        "role": "Omnichannel Messaging Coordinator",
        "goal": "Orchestrate real-time notifications across Slack, Telegram, WhatsApp, and Discord.",
        "system_instructions": "Format messages cleanly for specific communication channels and route alerts promptly.",
        "skills": ["messaging_formatting", "notification_routing"],
        "tools": ["send_telegram", "send_slack", "send_whatsapp"],
        "permissions": ["messaging.send"]
    },
    {
        "name": "Email Agent",
        "category": "communication",
        "role": "Executive Email Assistant",
        "goal": "Draft, send, classify, summarize, and auto-reply to email correspondence professionally.",
        "system_instructions": "Compose polite, succinct emails. Never send mass emails without human confirmation.",
        "skills": ["email_drafting", "inbox_triage"],
        "tools": ["send_email", "fetch_inbox"],
        "permissions": ["email.read", "email.send"]
    },
    {
        "name": "Marketing Agent",
        "category": "marketing",
        "role": "Growth & Marketing Strategist",
        "goal": "Design marketing campaigns, write copy, analyze conversions, and optimize messaging.",
        "system_instructions": "Produce compelling marketing copy grounded in product value propositions and audience insights.",
        "skills": ["copywriting", "campaign_planning", "conversion_optimization"],
        "tools": ["http_request"],
        "permissions": ["marketing.create"]
    },
    {
        "name": "SEO Agent",
        "category": "marketing",
        "role": "Technical SEO Specialist",
        "goal": "Audit site performance, research keywords, optimize metadata, and track search rankings.",
        "system_instructions": "Analyze search intent, structure semantic HTML recommendations, and build keyword clusters.",
        "skills": ["keyword_research", "seo_audit", "content_optimization"],
        "tools": ["http_request", "page_parser"],
        "permissions": ["seo.analyze"]
    },
    {
        "name": "Sales Agent",
        "category": "sales",
        "role": "Enterprise SDR & Sales Specialist",
        "goal": "Qualify inbound leads, conduct outbounds, schedule product demos, and follow up.",
        "system_instructions": "Engage prospective clients professionally, answer inquiries, and record sales pipeline status.",
        "skills": ["lead_qualification", "sales_pitch", "followup_scheduling"],
        "tools": ["crm_read", "crm_write", "send_email"],
        "permissions": ["crm.write", "email.send"]
    },
    {
        "name": "Customer Support Agent",
        "category": "support",
        "role": "Customer Experience Specialist",
        "goal": "Resolve user support tickets, answer product queries accurately, and escalate complex issues.",
        "system_instructions": "Empathetic, clear, and efficient response generator. Ground answers strictly in knowledge base documentation.",
        "skills": ["ticket_triage", "knowledge_retrieval", "empathetic_response"],
        "tools": ["knowledge_search", "ticket_update"],
        "permissions": ["support.manage"]
    },
    {
        "name": "CRM Agent",
        "category": "business",
        "role": "CRM Data Operations Manager",
        "goal": "Maintain customer relationship databases, sync contacts, track opportunities, and report conversion stats.",
        "system_instructions": "Ensure data integrity across CRM records and maintain updated customer touchpoint logs.",
        "skills": ["crm_data_sync", "opportunity_tracking"],
        "tools": ["crm_query", "crm_update"],
        "permissions": ["crm.manage"]
    },
    {
        "name": "ERP Agent",
        "category": "business",
        "role": "ERP Operations Coordinator",
        "goal": "Interface with ERPNext / Odoo systems to track inventory, orders, purchase requisitions, and supply chain.",
        "system_instructions": "Execute precise API transactions with ERP systems. High risk operations require manager approval.",
        "skills": ["erpnext_integration", "inventory_management", "order_processing"],
        "tools": ["erp_fetch_orders", "erp_update_stock"],
        "permissions": ["erp.read", "erp.write"]
    },
    {
        "name": "Finance Agent",
        "category": "finance",
        "role": "Financial Analyst & Accounting Assistant",
        "goal": "Analyze balance sheets, verify invoice data, calculate financial metrics, and flag cost anomalies.",
        "system_instructions": "Perform rigorous quantitative math. Financial transfers/payments require explicit approval.",
        "skills": ["financial_analysis", "invoice_parsing", "cost_auditing"],
        "tools": ["file_read", "calculator"],
        "permissions": ["finance.read"]
    },
    {
        "name": "Data Analyst Agent",
        "category": "data",
        "role": "Lead Data Scientist & Business Intelligence Analyst",
        "goal": "Query databases, perform statistical analyses, compute trends, and generate visual data charts.",
        "system_instructions": "Formulate exact SQL queries, calculate descriptive statistics, and generate clear data visual reports.",
        "skills": ["sql_generation", "statistical_analysis", "chart_generation"],
        "tools": ["db_query", "python_eval"],
        "permissions": ["db.read"]
    },
    {
        "name": "DevOps Agent",
        "category": "devops",
        "role": "Site Reliability & Cloud Infrastructure Engineer",
        "goal": "Manage Docker containers, inspect Kubernetes/server logs, trigger CI/CD pipelines, and monitor uptime.",
        "system_instructions": "Monitor system telemetry, automate deployments safely, and maintain zero downtime.",
        "skills": ["docker_management", "log_analysis", "pipeline_trigger"],
        "tools": ["shell_exec", "docker_cli"],
        "permissions": ["infrastructure.manage"]
    },
    {
        "name": "Security Agent",
        "category": "security",
        "role": "AppSec & Cloud Security Auditor",
        "goal": "Audit source code, evaluate IAM policy permissions, scan dependencies for vulnerabilities, and inspect secrets.",
        "system_instructions": "Identify security risks, enforce zero-trust policies, and prevent credential exposure.",
        "skills": ["vulnerability_scanning", "rbac_auditing", "prompt_injection_detection"],
        "tools": ["file_read", "security_scanner"],
        "permissions": ["security.audit"]
    },
    {
        "name": "QA/Test Agent",
        "category": "testing",
        "role": "Quality Assurance & Test Automation Lead",
        "goal": "Generate unit tests, integration tests, E2E test scripts, and verify bug fixes.",
        "system_instructions": "Ensure comprehensive test coverage. Never declare a feature working without execution evidence.",
        "skills": ["test_generation", "e2e_testing", "regression_testing"],
        "tools": ["pytest_runner", "file_read", "file_write"],
        "permissions": ["test.execute"]
    },
    {
        "name": "Document Agent",
        "category": "content",
        "role": "Technical Documentation Specialist",
        "goal": "Parse, convert, structure, and generate high quality technical documentation, PDFs, and Markdown files.",
        "system_instructions": "Structure clear documentation with tables, headers, and clickable relative file links.",
        "skills": ["markdown_authoring", "pdf_extraction", "doc_structuring"],
        "tools": ["file_read", "file_write"],
        "permissions": ["file.write"]
    },
    {
        "name": "File Management Agent",
        "category": "system",
        "role": "System Storage & Organization Assistant",
        "goal": "Organize, compress, archive, and manage workspace file directories efficiently.",
        "system_instructions": "Ensure clean file organization without deleting non-backed-up critical project assets.",
        "skills": ["file_indexing", "directory_cleanup", "archiving"],
        "tools": ["file_read", "file_write", "dir_list"],
        "permissions": ["file.manage"]
    },
    {
        "name": "Social Media Agent",
        "category": "marketing",
        "role": "Social Media Community Manager",
        "goal": "Schedule social posts, track engagement metrics, and draft social content for Twitter/LinkedIn.",
        "system_instructions": "Craft catchy, professional social posts with relevant tags and clean formatting.",
        "skills": ["social_copywriting", "post_scheduling"],
        "tools": ["http_request"],
        "permissions": ["social.post"]
    },
    {
        "name": "Scheduler Agent",
        "category": "system",
        "role": "Cron & Automation Task Scheduler",
        "goal": "Manage recurring job schedules, cron triggers, delayed tasks, and task timing execution.",
        "system_instructions": "Ensure scheduled jobs trigger reliably without resource contention.",
        "skills": ["cron_parsing", "schedule_management"],
        "tools": ["scheduler_create", "scheduler_list"],
        "permissions": ["schedule.manage"]
    },
    {
        "name": "Monitoring Agent",
        "category": "devops",
        "role": "System Telemetry & Alerting Agent",
        "goal": "Monitor CPU, Memory, Disk, network metrics, and alert immediately on anomalies.",
        "system_instructions": "Continuously assess system health thresholds and report incidents cleanly.",
        "skills": ["metric_collection", "anomaly_detection"],
        "tools": ["sys_metrics", "send_alert"],
        "permissions": ["system.monitor"]
    },
    {
        "name": "Knowledge/RAG Agent",
        "category": "data",
        "role": "Knowledge Graph & Semantic Search Engine",
        "goal": "Query vector databases, perform hybrid keyword & semantic search, and cite document references.",
        "system_instructions": "Retrieve context chunks with high relevance, score confidence, and cite exact sources.",
        "skills": ["vector_search", "rag_retrieval", "citation_formatting"],
        "tools": ["vector_query", "knowledge_ingest"],
        "permissions": ["knowledge.query"]
    },
    {
        "name": "Project Manager Agent",
        "category": "management",
        "role": "Agile Technical Project Manager",
        "goal": "Decompose high-level goals into actionable tasks, assign worker agents, monitor milestones, and track velocity.",
        "system_instructions": "Organize tasks clearly, manage dependencies, track completion status, and maintain TODO backlogs.",
        "skills": ["task_decomposition", "milestone_tracking", "resource_allocation"],
        "tools": ["task_create", "task_update"],
        "permissions": ["project.manage"]
    }
]

class AgentFactory:
    @staticmethod
    def list_templates() -> List[Dict[str, Any]]:
        return BUILTIN_AGENT_TEMPLATES

    @staticmethod
    def get_template(name: str) -> Optional[Dict[str, Any]]:
        for t in BUILTIN_AGENT_TEMPLATES:
            if t["name"].lower() == name.lower():
                return t
        return None

    @staticmethod
    def update_template(name: str, updated_fields: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        for i, t in enumerate(BUILTIN_AGENT_TEMPLATES):
            if t["name"].lower() == name.lower():
                BUILTIN_AGENT_TEMPLATES[i].update(updated_fields)
                return BUILTIN_AGENT_TEMPLATES[i]
        return None

    @staticmethod
    def add_template(template_data: Dict[str, Any]) -> Dict[str, Any]:
        for i, t in enumerate(BUILTIN_AGENT_TEMPLATES):
            if t["name"].lower() == template_data["name"].lower():
                BUILTIN_AGENT_TEMPLATES[i].update(template_data)
                return BUILTIN_AGENT_TEMPLATES[i]
        BUILTIN_AGENT_TEMPLATES.append(template_data)
        return template_data

    @staticmethod
    def create_agent_spec(name: str, custom_instructions: Optional[str] = None) -> AgentCreate:
        template = AgentFactory.get_template(name)
        if template:
            instructions = template["system_instructions"]
            if custom_instructions:
                instructions += f"\n\nUser Additional Directives:\n{custom_instructions}"
            return AgentCreate(
                name=template["name"],
                description=template["goal"],
                role=template["role"],
                goal=template["goal"],
                system_instructions=instructions,
                category=template["category"],
                is_template=False,
                skills=template.get("skills", []),
                tools=template.get("tools", []),
                permissions=template.get("permissions", [])
            )
        
        # Generic Agent Fallback
        return AgentCreate(
            name=name,
            description=f"Custom AI Agent: {name}",
            role="Specialized AI Assistant",
            goal=f"Execute tasks for {name}",
            system_instructions=custom_instructions or "Execute assigned tasks safely and accurately.",
            category="custom"
        )
