GOD AI OS — MOTHER AGENT

Autonomous Agent Operating System / Agent Factory

Master Build Prompt for Google Antigravity

You are the Principal AI Systems Architect, Senior Full-Stack Engineer, AI Agent Engineer, MCP Engineer, DevOps Engineer, Security Engineer, QA Engineer, Product Designer, and Technical Project Manager responsible for building a production-grade application called:

GOD AI OS — Mother Agent

Your mission is to design, implement, test, document, secure, and continuously improve a complete AI Agent Operating System.

Do not build a simple chatbot.

Build an extensible Agent Runtime + Agent Factory + MCP/Tool/Skill/Memory/Plugin Management Platform where a Mother Agent can create, configure, execute, monitor, evaluate, pause, resume, repair, clone, archive, and destroy specialized AI agents.

---

1. CORE PRODUCT VISION

The system must work conceptually like this:

USER
↓
GOD AI OS
↓
MOTHER AGENT
↓
UNDERSTAND REQUEST
↓
PLAN
↓
TASK DECOMPOSITION
↓
SELECT MODEL
↓
SELECT AGENT
↓
SELECT SKILLS
↓
SELECT MEMORY
↓
SELECT MCP SERVERS
↓
SELECT TOOLS
↓
CHECK PERMISSIONS
↓
CREATE / REUSE WORKER AGENTS
↓
EXECUTE
↓
OBSERVE
↓
EVALUATE
↓
RETRY / REPAIR / REASSIGN
↓
HUMAN APPROVAL IF REQUIRED
↓
FINAL RESULT
↓
STORE MEMORY / LEARNINGS
↓
AUDIT LOG

The Mother Agent must be the central orchestrator.

---

2. MOST IMPORTANT DESIGN PRINCIPLE

Do NOT hard-code the Mother Agent to one AI provider.

The architecture must support multiple interchangeable LLM/agent engines.

Examples:

- OpenAI
- Anthropic
- Google Gemini
- Open-source models
- Local Ollama models
- LM Studio
- vLLM
- OpenAI-compatible APIs
- Future model providers

Create a provider abstraction:

LLMProvider
AgentProvider
EmbeddingProvider
SpeechProvider
VisionProvider

The application must be able to switch models without rewriting the core system.

---

3. REQUIRED ARCHITECTURE

Build the system as modular layers:

Layer 1 — User Interface

Modern responsive web application.

Preferred stack:

- Next.js
- TypeScript
- Tailwind CSS
- shadcn/ui
- React
- TanStack Query
- Zustand where appropriate

The UI must work on:

- Desktop
- Tablet
- Mobile

---

Layer 2 — API / Application Backend

Preferred:

- Python
- FastAPI
- Pydantic
- SQLAlchemy
- PostgreSQL

Use REST APIs and WebSocket/SSE for realtime events.

Design APIs so that another frontend can consume them later.

---

Layer 3 — Mother Agent Runtime

Create a dedicated Mother Agent runtime.

Responsibilities:

- Intent detection
- Task planning
- Task decomposition
- Agent selection
- Agent creation
- Agent routing
- Tool selection
- MCP selection
- Skill selection
- Memory retrieval
- Context construction
- Permission checking
- Execution
- Monitoring
- Evaluation
- Retry
- Recovery
- Human approval
- Result synthesis
- Memory writing
- Audit logging

Mother Agent must never blindly execute dangerous operations.

---

4. AGENT FACTORY

Create an Agent Factory.

The Mother Agent must be able to create an agent dynamically from a specification.

Agent definition must support:

- Agent ID
- Name
- Description
- Role
- Goal
- System instructions
- Personality
- Model
- Model parameters
- Skills
- Tools
- MCP servers
- Memory
- Knowledge sources
- Permissions
- Security policy
- Budget
- Token limit
- Time limit
- Retry policy
- Human approval policy
- Input schema
- Output schema
- Evaluation criteria
- Lifecycle state
- Version
- Owner
- Tags
- Metadata

Agent lifecycle:

DRAFT
↓
VALIDATING
↓
READY
↓
RUNNING
↓
PAUSED
↓
WAITING_APPROVAL
↓
FAILED
↓
RECOVERING
↓
COMPLETED
↓
ARCHIVED
↓
DESTROYED

---

5. BUILT-IN AGENTS

Create initial built-in agent templates.

At minimum:

1. Coding Agent
2. Research Agent
3. Browser Agent
4. Computer Use Agent
5. Voice Agent
6. Communication Agent
7. Email Agent
8. Marketing Agent
9. SEO Agent
10. Sales Agent
11. Customer Support Agent
12. CRM Agent
13. ERP Agent
14. Finance Agent
15. Data Analyst Agent
16. DevOps Agent
17. Security Agent
18. QA/Test Agent
19. Document Agent
20. File Management Agent
21. Social Media Agent
22. Scheduler Agent
23. Monitoring Agent
24. Knowledge/RAG Agent
25. Project Manager Agent

Every built-in agent must be implemented as a reusable template, not duplicated code.

---

6. MCP MANAGEMENT SYSTEM

Create a complete MCP management subsystem.

The system must support:

- MCP server registry
- MCP server installation
- MCP server configuration
- MCP server discovery
- MCP server enable/disable
- MCP server authentication
- MCP server health checks
- MCP server versioning
- MCP server permissions
- MCP server tool discovery
- MCP resources
- MCP prompts where supported
- MCP connection testing
- MCP logs
- MCP usage statistics

Support MCP transports where applicable:

- stdio
- SSE
- Streamable HTTP

Create an MCP Gateway/Registry abstraction.

Example:

MCP Registry
├── GitHub
├── Filesystem
├── Browser
├── PostgreSQL
├── Google
├── Microsoft
├── Slack
├── ClickUp
├── Notion
├── Telegram
├── WhatsApp
├── Email
├── ERPNext
├── n8n
├── ViciDial
├── Asterisk
└── Custom MCP

Do not assume every external service has an official MCP server.

Allow custom MCP registration.

---

7. TOOL REGISTRY

Create a universal Tool Registry.

Every tool must have:

- Tool ID
- Name
- Description
- Version
- Input schema
- Output schema
- Authentication
- Permission requirements
- Risk level
- Execution timeout
- Retry policy
- Rate limit
- Cost
- Provider
- Tags
- Enabled state
- Audit policy

Tool categories:

- Web
- Search
- Browser
- Computer
- Files
- Database
- API
- Email
- Messaging
- CRM
- ERP
- Finance
- Social
- Code
- Git
- DevOps
- Cloud
- Monitoring
- Security
- Voice
- Image
- Video
- Document
- Data
- Automation
- IoT

Create Tool Discovery and Tool Selection.

The Mother Agent must select tools dynamically according to the task.

---

8. SKILL SYSTEM

Create a reusable Skill Registry.

A Skill is NOT the same thing as a Tool.

Example:

Tool:
"send_email"

Skill:
"Professional Email Communication"

Skill structure:

- Skill ID
- Name
- Description
- Instructions
- Preconditions
- Required tools
- Required MCP
- Required knowledge
- Input schema
- Output schema
- Examples
- Evaluation criteria
- Version
- Author
- Tags

Create:

Skill Builder
Skill Editor
Skill Import
Skill Export
Skill Versioning
Skill Testing
Skill Activation

Support Markdown-based skills.

Recommended structure:

skills/
coding/
research/
email/
marketing/
sales/
devops/
security/
business/
communication/

---

9. PLUGIN SYSTEM

Create a Plugin Architecture.

A plugin may contain:

- UI
- backend service
- tools
- MCP connections
- skills
- workflows
- database models
- configuration
- permissions

Plugin manifest:

plugin.json

Example conceptual structure:

plugin/
plugin.json
README.md
backend/
frontend/
tools/
skills/
workflows/
migrations/
tests/

Support:

- Install
- Uninstall
- Enable
- Disable
- Update
- Version
- Dependency management
- Permission management
- Configuration

Never allow a plugin to execute arbitrary privileged operations without explicit permissions.

---

10. MEMORY SYSTEM

Create a multi-layer memory architecture.

Memory types

1. Working Memory
2. Short-Term Memory
3. Episodic Memory
4. Semantic Memory
5. Procedural Memory
6. User Memory
7. Agent Memory
8. Organization Memory
9. Project Memory
10. Task Memory
11. Tool Memory
12. Skill Memory
13. System Memory

Use PostgreSQL as the primary transactional database.

Add vector storage using a pluggable abstraction.

Possible backends:

- pgvector
- Qdrant
- Weaviate
- Milvus
- Chroma

Do not tightly couple the system to one vector database.

Memory operations:

STORE
RETRIEVE
SEARCH
RANK
SUMMARIZE
COMPRESS
UPDATE
EXPIRE
ARCHIVE
DELETE

Memory must have:

- source
- timestamp
- confidence
- importance
- scope
- owner
- access policy
- retention policy

---

11. KNOWLEDGE / RAG SYSTEM

Build a Knowledge Base subsystem.

Sources:

- PDF
- DOCX
- XLSX
- CSV
- TXT
- Markdown
- Web pages
- URLs
- APIs
- Database
- Git repositories
- Email
- Cloud storage

Pipeline:

INGEST
↓
PARSE
↓
CHUNK
↓
EMBED
↓
INDEX
↓
RETRIEVE
↓
RERANK
↓
CONTEXT
↓
LLM

Support metadata filtering and source citations.

---

12. WORKFLOW ENGINE

Create a visual workflow system.

Node types:

- Trigger
- Agent
- LLM
- Tool
- MCP
- Skill
- Memory
- Condition
- Router
- Loop
- Parallel
- Merge
- Human Approval
- Delay
- Schedule
- Webhook
- API
- Code
- Database
- Notification
- Evaluation

Workflow example:

Trigger
→ Research Agent
→ Fact Check
→ Human Approval
→ Content Agent
→ SEO Agent
→ Publish
→ Analytics
→ Report

The architecture must allow integration with n8n rather than trying to replace every n8n capability.

---

13. TASK QUEUE

Create a durable task execution system.

Support:

- Queue
- Priority
- Retry
- Dead-letter queue
- Scheduled task
- Delayed task
- Recurring task
- Dependencies
- Parent/child tasks
- Parallel tasks
- Cancellation
- Timeout
- Resume

Recommended architecture:

PostgreSQL
+
Redis
+
Worker processes

Keep the queue abstraction replaceable.

---

14. MULTI-AGENT SYSTEM

Mother Agent must support:

Sequential agents:

A → B → C

Parallel agents:

A
B
C
↓
Aggregator

Hierarchical agents:

Mother
↓
Manager
↓
Workers

Debate:

Agent A ↔ Agent B
↓
Evaluator

Reviewer:

Worker
↓
Reviewer
↓
Correction
↓
Worker

Create explicit agent handoff protocols.

---

15. MODEL ROUTER

Create a Model Router.

Mother Agent should decide:

Which model is appropriate?

Based on:

- task complexity
- cost
- latency
- context size
- modality
- tool support
- coding capability
- reasoning capability
- privacy
- local/cloud preference

Example:

Simple task
→ cheap/local model

Coding
→ coding model

Research
→ research-capable model

Complex reasoning
→ premium reasoning model

Private data
→ local model

Voice
→ speech model

---

16. PERMISSION AND SECURITY SYSTEM

Implement RBAC and policy-based access control.

Entities:

- User
- Organization
- Workspace
- Agent
- Tool
- MCP
- Plugin
- Skill
- Workflow
- Secret
- Resource

Permission examples:

tool.email.send
tool.email.read
tool.github.write
tool.database.read
tool.database.write
tool.shell.execute
tool.browser.login
tool.payment.execute

Risk levels:

LOW
MEDIUM
HIGH
CRITICAL

High-risk operations require explicit approval.

Examples:

- Delete database
- Send mass email
- Financial transaction
- Production deployment
- Delete cloud resources
- Modify security settings
- Execute privileged shell commands

---

17. SECRET MANAGEMENT

Never store API keys in plain text.

Create a Secrets abstraction.

Support:

- Environment variables
- Encrypted database secrets
- External secret managers later

Secrets must never appear in:

- logs
- prompts
- frontend
- error messages
- audit logs

---

18. HUMAN-IN-THE-LOOP

Create an approval system.

Agent may request:

APPROVAL_REQUIRED

Example:

Agent:
"I am ready to deploy to production."

Mother Agent:
"Production deployment requires approval."

User:
APPROVE

Then execution continues.

Support:

- Approve
- Reject
- Modify
- Pause
- Resume

---

19. OBSERVABILITY

Every agent execution must produce a trace.

Trace:

Execution
├── Agent
├── Model
├── Prompt
├── Tool calls
├── MCP calls
├── Memory retrieval
├── Tokens
├── Cost
├── Duration
├── Errors
├── Approvals
└── Result

Build dashboards:

- Agent runs
- Success rate
- Failure rate
- Token usage
- Estimated cost
- Tool usage
- MCP usage
- Latency
- Memory usage
- Errors

---

20. EVALUATION SYSTEM

Do not assume an agent's output is correct.

Create:

Evaluator Agent

Evaluation criteria:

- correctness
- completeness
- relevance
- safety
- format
- factual consistency
- task completion

Support:

Worker
↓
Evaluator
↓
Score
↓
Pass / Retry / Escalate

Store evaluations for future improvement.

---

21. SELF-IMPROVEMENT

Create a controlled learning mechanism.

Mother Agent can identify:

- repeated failures
- missing skills
- missing tools
- missing MCP
- bad prompts
- workflow bottlenecks
- recurring user corrections

Then propose:

"New Skill required"

"New Tool required"

"New MCP required"

"Prompt improvement required"

But NEVER silently modify critical system policies.

Require approval for system-level changes.

---

22. AGENT TEMPLATE SYSTEM

Create templates:

Coding Agent
Research Agent
Sales Agent
Marketing Agent
Voice Agent
DevOps Agent
Security Agent
Finance Agent
Customer Support Agent
ERP Agent

Each template should define:

Goal
Instructions
Model policy
Tools
MCP
Skills
Memory
Permissions
Evaluation
Output format

Allow users to clone and customize templates.

---

23. AGENT MARKETPLACE / REGISTRY

Create an internal marketplace architecture.

Agent package:

agent.json
skills/
tools/
workflows/
README.md
tests/

Allow:

Import
Export
Clone
Version
Publish
Install
Update

Do not require a public marketplace in version 1.

Build the architecture so one can be added later.

---

24. USER INTERFACE

Create these major pages:

Dashboard

Agents

Agent Builder

Agent Templates

Agent Runs

Tasks

Workflows

MCP Servers

Tools

Skills

Plugins

Memory

Knowledge

Models

Providers

Secrets

Approvals

Schedules

Logs

Evaluations

Settings

System Health

Audit Logs

---

25. AGENT BUILDER UI

Build a visual Agent Builder.

Sections:

Identity
Goal
Instructions
Model
Tools
MCP
Skills
Memory
Knowledge
Permissions
Triggers
Workflow
Evaluation
Output
Security

Provide:

Create Agent

Test Agent

Run Agent

Save

Publish

Clone

Export

Import

---

26. CHAT INTERFACE

Create a primary Mother Agent chat.

User should be able to say:

"Create a marketing agent."

Mother Agent should respond:

"I will create a marketing agent with SEO, content, social media and analytics capabilities."

Then internally:

Create Agent
→ Attach Skills
→ Select Tools
→ Attach MCP
→ Configure Memory
→ Configure Permissions
→ Test
→ Return Agent

The user must not have to manually configure everything.

---

27. NATURAL LANGUAGE SYSTEM ADMINISTRATION

The Mother Agent should understand commands such as:

"Create a coding agent."

"Give it GitHub access."

"Add PostgreSQL."

"Connect this agent to my ERP."

"Create a daily sales report."

"Create an agent that monitors server health."

"Create a Bengali voice agent for ViciDial."

"Give this agent read-only access."

"Run the workflow every morning."

"Stop this agent."

"Show me what this agent did today."

---

28. BUSINESS INTEGRATION ARCHITECTURE

Prepare connectors/adapters for:

- ERPNext
- Odoo
- WooCommerce
- Shopify
- ViciDial
- Asterisk
- Grandstream
- Gmail
- Google Workspace
- Microsoft 365
- Outlook
- WhatsApp
- Telegram
- Slack
- ClickUp
- GitHub
- GitLab
- LinkedIn
- Facebook/Meta
- Instagram
- n8n

Do not implement every integration completely in version 1.

Create a clean adapter interface so connectors can be added incrementally.

---

29. LOCAL / SELF-HOSTED FIRST

The system must be deployable on:

- Local machine
- Linux server
- Docker
- Docker Compose
- VPS
- Private cloud

Avoid unnecessary vendor lock-in.

Support:

Cloud LLM
+
Local LLM

Example:

Ollama
vLLM
OpenAI-compatible endpoint

---

30. DOCKER ARCHITECTURE

Create Docker Compose for development.

Expected services:

frontend
backend
worker
postgres
redis
vector-db
mcp-gateway

Optional:

observability
reverse-proxy

Make every service configurable.

---

31. PROJECT STRUCTURE

Create a clean monorepo.

Suggested:

god-ai-os/
│
├── apps/
│   ├── web/
│   ├── api/
│   └── worker/
│
├── packages/
│   ├── agent-core/
│   ├── agent-runtime/
│   ├── agent-factory/
│   ├── mcp/
│   ├── tools/
│   ├── skills/
│   ├── memory/
│   ├── knowledge/
│   ├── workflow/
│   ├── models/
│   ├── security/
│   ├── evaluation/
│   └── shared/
│
├── agents/
│   ├── coding/
│   ├── research/
│   ├── voice/
│   └── ...
│
├── skills/
├── plugins/
├── mcp/
├── workflows/
├── docs/
├── tests/
├── scripts/
├── docker/
└── infrastructure/

You may improve this structure if a better architecture is justified.

---

32. DATABASE DESIGN

Create migrations for at least:

users
organizations
workspaces
agents
agent_versions
agent_runs
tasks
task_dependencies
models
providers
tools
tool_permissions
mcp_servers
mcp_tools
skills
skill_versions
plugins
plugin_versions
workflows
workflow_runs
memory_items
knowledge_sources
knowledge_documents
secrets
approvals
evaluations
audit_logs
schedules
events

Use proper indexes and foreign keys.

---

33. API DESIGN

Create versioned APIs:

/api/v1/agents
/api/v1/tasks
/api/v1/workflows
/api/v1/mcp
/api/v1/tools
/api/v1/skills
/api/v1/plugins
/api/v1/memory
/api/v1/knowledge
/api/v1/models
/api/v1/providers
/api/v1/approvals
/api/v1/evaluations
/api/v1/audit

Provide OpenAPI documentation.

---

34. EVENT BUS

Create an internal event architecture.

Events:

agent.created
agent.started
agent.paused
agent.completed
agent.failed

task.created
task.started
task.completed
task.failed

tool.called
tool.completed
tool.failed

mcp.connected
mcp.disconnected

approval.requested
approval.granted
approval.rejected

memory.created
memory.updated

Use an abstraction so Redis Streams/RabbitMQ/Kafka can be introduced later.

---

35. SCHEDULER

Support:

One-time
Hourly
Daily
Weekly
Monthly
Cron
Event-triggered
Webhook-triggered

Examples:

"Run server monitoring every 5 minutes."

"Send sales report every morning."

"Check website SEO every Sunday."

---

36. TESTING

Create:

Unit tests
Integration tests
API tests
Agent tests
Tool tests
MCP tests
Workflow tests
Security tests
Permission tests
Memory tests
Evaluation tests
End-to-end tests

Create test fixtures.

Every major feature must have automated tests.

---

37. SECURITY REQUIREMENTS

Implement:

- Authentication
- Authorization
- RBAC
- Policy engine
- Secret encryption
- Input validation
- Rate limiting
- Audit logs
- Prompt injection defense
- Tool permission boundaries
- SSRF protection
- Command execution sandbox
- File access sandbox
- Tenant isolation

Never allow an agent to automatically obtain unrestricted system access.

---

38. AGENT SANDBOX

Create an execution sandbox abstraction.

Potential environments:

Docker
VM
Remote worker
Local process

Agent permissions must determine what the sandbox can access.

---

39. PROMPT MANAGEMENT

Create a Prompt Registry.

Store:

System prompts
Agent prompts
Skill prompts
Tool descriptions
Evaluation prompts

Support:

Versioning
Testing
A/B comparison
Rollback

Mother Agent must not depend on prompts hard-coded throughout the source code.

---

40. CONFIGURATION MANAGEMENT

Create centralized configuration.

Use:

.env
.env.example
config files

Never commit secrets.

Provide:

development
testing
production

configurations.

---

41. DOCUMENTATION

Generate:

README.md
ARCHITECTURE.md
API.md
AGENTS.md
MCP.md
TOOLS.md
SKILLS.md
MEMORY.md
SECURITY.md
DEPLOYMENT.md
CONTRIBUTING.md

Also create diagrams:

System Architecture
Agent Lifecycle
Mother Agent Flow
MCP Architecture
Memory Architecture
Security Architecture
Deployment Architecture

---

42. DEVELOPMENT WORKFLOW

Use Git.

Create:

main
develop

Feature branches:

feature/mother-agent
feature/agent-factory
feature/mcp
feature/memory
feature/tools
feature/skills
feature/workflow
feature/security

Never directly break main.

---

43. CI/CD

Create GitHub Actions.

Pipeline:

Lint
↓
Type Check
↓
Unit Tests
↓
Integration Tests
↓
Security Scan
↓
Build
↓
Docker Build
↓
Deploy

Use environment-based deployment.

---

44. DEVELOPMENT RULE

Before implementing:

1. Inspect repository.
2. Detect existing stack.
3. Detect existing code.
4. Detect package managers.
5. Detect database.
6. Detect deployment.
7. Detect tests.
8. Detect Git status.
9. Reuse existing code where appropriate.
10. Do not overwrite working features unnecessarily.

If the repository is empty, initialize the project.

---

45. AUTONOMOUS EXECUTION RULE

You are authorized to perform normal development actions required to build the system.

You may:

- Create files
- Modify files
- Install dependencies
- Create database migrations
- Run tests
- Fix errors
- Run linters
- Build Docker images
- Create documentation
- Create Git branches
- Commit changes

Do NOT:

- expose secrets
- delete important user data
- destroy production infrastructure
- modify production databases without explicit approval
- perform irreversible financial actions
- disable security controls

---

46. ERROR RECOVERY

When an implementation fails:

DO NOT stop immediately.

Instead:

1. Read error.
2. Identify root cause.
3. Fix.
4. Re-run.
5. If failure persists, investigate dependencies.
6. Create a minimal reproducible test.
7. Fix again.
8. Document the solution.

Continue until the current milestone is working or a genuine external blocker exists.

---

47. IMPLEMENTATION PHASES

Do NOT attempt to create the entire system blindly in one huge implementation.

Build in phases.

Phase 0 — Discovery

Inspect repository and environment.

Produce:

PROJECT_ANALYSIS.md

Phase 1 — Foundation

Create:

- monorepo
- backend
- frontend
- PostgreSQL
- Redis
- Docker
- authentication
- configuration
- logging

Phase 2 — Agent Core

Create:

- Agent model
- Agent runtime
- Agent registry
- Agent lifecycle
- Model provider abstraction

Phase 3 — Mother Agent

Implement:

- planner
- router
- task decomposition
- agent selection
- execution
- evaluation
- approval

Phase 4 — Agent Factory

Implement dynamic agent creation.

Phase 5 — Tools

Implement Tool Registry.

Phase 6 — MCP

Implement MCP Registry/Gateway.

Phase 7 — Skills

Implement Skill Registry.

Phase 8 — Memory

Implement multi-layer memory.

Phase 9 — Knowledge/RAG

Implement ingestion and retrieval.

Phase 10 — Workflow

Implement workflow engine.

Phase 11 — Multi-Agent

Implement agent teams, parallel execution and handoffs.

Phase 12 — Security

Implement sandbox, RBAC and policy engine.

Phase 13 — UI

Complete Agent Builder and management dashboard.

Phase 14 — Integrations

Start with:

GitHub
Google
Email
n8n
ERPNext
ViciDial/Asterisk

Phase 15 — Evaluation

Implement automated agent evaluation.

Phase 16 — Observability

Implement traces, metrics and dashboards.

Phase 17 — Production

Docker deployment
CI/CD
backup
monitoring
security hardening

---

48. FIRST MVP

Do not wait for every integration.

The first working MVP must allow:

USER
↓
Mother Agent
↓
Create Worker Agent
↓
Attach Model
↓
Attach Skill
↓
Attach Tool
↓
Attach MCP
↓
Attach Memory
↓
Execute
↓
Evaluate
↓
Store Result

MVP must be genuinely executable, not merely UI mockups.

---

49. DEFINITION OF DONE

A feature is NOT complete when the code exists.

It is complete only when:

- implementation exists
- database migration exists if required
- API exists
- UI exists if required
- validation exists
- tests exist
- error handling exists
- security is considered
- documentation exists
- feature works end-to-end

---

50. UI/UX DESIGN

Design the application as a professional AI operating system.

Visual concepts:

- Agent cards
- Agent hierarchy
- Workflow canvas
- Tool registry
- MCP registry
- Skill library
- Memory explorer
- Execution timeline
- Live agent status
- Task graph
- Approval center
- System health

Avoid a generic chatbot-only interface.

The primary experience should feel like:

AI Command Center
+
Agent IDE
+
Workflow Automation Platform
+
System Administration Console

---

51. MOTHER AGENT INTERNAL DECISION LOOP

Implement this conceptual loop:

OBSERVE
↓
UNDERSTAND
↓
PLAN
↓
SELECT
↓
ACT
↓
OBSERVE
↓
EVALUATE
↓
REFLECT
↓
REPLAN
↓
COMPLETE

Maximum retries must be configurable.

Prevent infinite loops.

---

52. AGENT CREATION EXAMPLE

User:

"Create an agent that monitors my Linux servers and alerts me on Telegram."

Mother Agent should determine:

Goal:
Server monitoring

Skills:
Infrastructure Monitoring
Incident Response

Tools:
SSH
System Metrics
Telegram

MCP:
Server management MCP if available

Memory:
Infrastructure Memory

Permission:
Read server metrics
Send Telegram messages

Schedule:
Every 5 minutes

Evaluation:
Alert accuracy

Then create and deploy the agent.

---

53. BUSINESS AUTOMATION EXAMPLE

User:

"Every morning at 9 AM, collect yesterday's sales from ERPNext, compare with previous week, create a report and send it to management."

Mother Agent should construct:

Scheduler
↓
ERP Agent
↓
Data Analysis Agent
↓
Report Agent
↓
Evaluator
↓
Email Agent

This must be represented as a workflow.

---

54. AGENT RESOURCE GRAPH

Create an internal graph:

Agent
├── Model
├── Skills
├── Tools
├── MCP
├── Memory
├── Knowledge
├── Permissions
├── Workflows
└── Secrets

The UI must be able to visualize these relationships.

---

55. FUTURE EXTENSIBILITY

Design for future support:

- Voice-first OS
- Mobile application
- Desktop application
- Browser extension
- IoT agents
- Robotics
- CCTV/vision agents
- Smart home
- financial agents
- autonomous DevOps
- autonomous business operations
- agent marketplace
- distributed agents
- multi-server agent execution
- edge agents

Do not implement these prematurely.

Create extension points.

---

56. IMPORTANT ENGINEERING PRINCIPLE

Do not build unnecessary complexity merely because this specification is large.

Use:

Simple implementation first.
Clear abstractions.
Strong interfaces.
Incremental development.

Prefer:

Working MVP
→ Test
→ Refactor
→ Extend

rather than:

Huge unfinished architecture.

---

57. FINAL EXECUTION INSTRUCTION

Start NOW.

First:

1. Inspect the repository.
2. Produce PROJECT_ANALYSIS.md.
3. Identify what already exists.
4. Propose the implementation roadmap based on the actual repository.
5. Start Phase 1.
6. Implement working code.
7. Run tests.
8. Fix errors.
9. Continue to the next phase automatically when the current phase is stable.
10. Maintain a DEVELOPMENT_STATUS.md file.
11. Maintain TODO.md.
12. Maintain ARCHITECTURE.md.
13. Never claim a feature is complete unless it has been tested.

At every milestone record:

- What was built
- Files changed
- Tests executed
- Test results
- Known limitations
- Next milestone

When you encounter an ambiguity, prefer the safest, most modular, least vendor-locked implementation.

When choosing technologies, prioritize:

1. Open source
2. Self-hosted
3. Local deployment
4. API-first
5. MCP compatibility
6. Model-provider independence
7. Security
8. Maintainability
9. Scalability
10. Low operational cost

The ultimate objective is:

BUILD A REAL GOD AI OS

where:

USER
↓
MOTHER AGENT
↓
AGENT FACTORY
↓
AGENTS
↓
SKILLS + TOOLS + MCP + MEMORY + KNOWLEDGE
↓
WORKFLOWS
↓
EXECUTION
↓
EVALUATION
↓
HUMAN APPROVAL WHEN REQUIRED
↓
RESULT
↓
MEMORY
↓
CONTINUOUS IMPROVEMENT

Do not build a demo.

Build the foundation of a production-grade, extensible, self-hostable AI Agent Operating System.