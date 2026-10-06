from sqlalchemy import Column, String, Integer, Float, Boolean, Text, JSON, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
import uuid
import enum

from apps.api.database import Base

def generate_uuid():
    return str(uuid.uuid4())

def utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)

class AgentLifecycle(str, enum.Enum):
    DRAFT = "DRAFT"
    VALIDATING = "VALIDATING"
    READY = "READY"
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    WAITING_APPROVAL = "WAITING_APPROVAL"
    FAILED = "FAILED"
    RECOVERING = "RECOVERING"
    COMPLETED = "COMPLETED"
    ARCHIVED = "ARCHIVED"
    DESTROYED = "DESTROYED"

class RiskLevel(str, enum.Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class User(Base):
    __tablename__ = "users"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    email = Column(String, unique=True, nullable=False, index=True)
    full_name = Column(String, nullable=False)
    role = Column(String, default="admin")
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)

class Organization(Base):
    __tablename__ = "organizations"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    slug = Column(String, unique=True, nullable=False)
    created_at = Column(DateTime, default=utc_now)

class Workspace(Base):
    __tablename__ = "workspaces"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    org_id = Column(String, ForeignKey("organizations.id"), nullable=True)
    created_at = Column(DateTime, default=utc_now)

class ModelProvider(Base):
    __tablename__ = "providers"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False) # e.g. OpenAI, Gemini, Anthropic, Ollama
    provider_type = Column(String, nullable=False) # openai, gemini, anthropic, ollama
    base_url = Column(String, nullable=True)
    is_enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)

class AIModel(Base):
    __tablename__ = "models"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False) # e.g. gpt-4o, gemini-2.0-flash, claude-3-5-sonnet, llama3
    model_id = Column(String, nullable=False)
    provider_id = Column(String, ForeignKey("providers.id"), nullable=False)
    context_window = Column(Integer, default=128000)
    supports_tools = Column(Boolean, default=True)
    supports_vision = Column(Boolean, default=False)
    cost_per_1k_input = Column(Float, default=0.0)
    cost_per_1k_output = Column(Float, default=0.0)
    created_at = Column(DateTime, default=utc_now)

class Agent(Base):
    __tablename__ = "agents"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    role = Column(String, nullable=False)
    goal = Column(Text, nullable=False)
    system_instructions = Column(Text, nullable=False)
    personality = Column(String, nullable=True)
    
    model_id = Column(String, nullable=True)
    model_provider = Column(String, default="openai")
    model_parameters = Column(JSON, default=dict)
    
    lifecycle_state = Column(String, default=AgentLifecycle.READY.value)
    version = Column(String, default="1.0.0")
    is_template = Column(Boolean, default=False)
    category = Column(String, default="general")
    
    skills = Column(JSON, default=list) # List of Skill IDs
    tools = Column(JSON, default=list)  # List of Tool IDs
    mcp_servers = Column(JSON, default=list) # List of MCP Server IDs
    permissions = Column(JSON, default=list)
    
    token_limit = Column(Integer, default=100000)
    budget_usd = Column(Float, default=10.0)
    time_limit_sec = Column(Integer, default=300)
    
    created_at = Column(DateTime, default=utc_now)
    updated_at = Column(DateTime, default=utc_now, onupdate=utc_now)

class AgentRun(Base):
    __tablename__ = "agent_runs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    task_id = Column(String, nullable=True)
    status = Column(String, default="RUNNING") # RUNNING, COMPLETED, FAILED, WAITING_APPROVAL
    input_prompt = Column(Text, nullable=False)
    output_result = Column(Text, nullable=True)
    error_message = Column(Text, nullable=True)
    
    tokens_used = Column(Integer, default=0)
    cost_usd = Column(Float, default=0.0)
    duration_sec = Column(Float, default=0.0)
    
    trace_data = Column(JSON, default=dict)
    created_at = Column(DateTime, default=utc_now)
    completed_at = Column(DateTime, nullable=True)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    assigned_agent_id = Column(String, ForeignKey("agents.id"), nullable=True)
    status = Column(String, default="PENDING") # PENDING, IN_PROGRESS, COMPLETED, FAILED, CANCELLED
    priority = Column(Integer, default=1) # 1 low, 5 high
    payload = Column(JSON, default=dict)
    result = Column(JSON, default=dict)
    
    parent_task_id = Column(String, ForeignKey("tasks.id"), nullable=True)
    created_at = Column(DateTime, default=utc_now)
    completed_at = Column(DateTime, nullable=True)

class ToolEntity(Base):
    __tablename__ = "tools"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    version = Column(String, default="1.0.0")
    category = Column(String, default="general")
    risk_level = Column(String, default=RiskLevel.LOW.value)
    input_schema = Column(JSON, default=dict)
    output_schema = Column(JSON, default=dict)
    enabled = Column(Boolean, default=True)
    provider = Column(String, default="builtin")
    created_at = Column(DateTime, default=utc_now)

class MCPServerEntity(Base):
    __tablename__ = "mcp_servers"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=True)
    transport = Column(String, default="stdio") # stdio, sse, http
    command = Column(String, nullable=True)     # e.g., npx -y @modelcontextprotocol/server-filesystem
    args = Column(JSON, default=list)
    url = Column(String, nullable=True)
    env_vars = Column(JSON, default=dict)
    enabled = Column(Boolean, default=True)
    status = Column(String, default="DISCONNECTED") # CONNECTED, DISCONNECTED, ERROR
    tools_discovered = Column(JSON, default=list)
    created_at = Column(DateTime, default=utc_now)

class SkillEntity(Base):
    __tablename__ = "skills"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, nullable=False)
    description = Column(Text, nullable=False)
    instructions = Column(Text, nullable=False)
    category = Column(String, default="general")
    required_tools = Column(JSON, default=list)
    version = Column(String, default="1.0.0")
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)

class PluginEntity(Base):
    __tablename__ = "plugins"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, unique=True, nullable=False)
    version = Column(String, default="1.0.0")
    description = Column(Text, nullable=True)
    enabled = Column(Boolean, default=True)
    manifest = Column(JSON, default=dict)
    created_at = Column(DateTime, default=utc_now)

class WorkflowEntity(Base):
    __tablename__ = "workflows"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    definition = Column(JSON, default=dict) # DAG definition (nodes & edges)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, default=utc_now)

class MemoryItem(Base):
    __tablename__ = "memory_items"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    memory_type = Column(String, nullable=False) # working, short_term, episodic, semantic, user, agent
    agent_id = Column(String, nullable=True, index=True)
    content = Column(Text, nullable=False)
    importance = Column(Float, default=1.0)
    confidence = Column(Float, default=1.0)
    scope = Column(String, default="global")
    metadata_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=utc_now)

class KnowledgeSource(Base):
    __tablename__ = "knowledge_sources"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    title = Column(String, nullable=False)
    source_type = Column(String, nullable=False) # pdf, docx, txt, url, git
    location = Column(Text, nullable=False)
    chunk_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=utc_now)

class ApprovalRequest(Base):
    __tablename__ = "approvals"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    action_type = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    payload = Column(JSON, default=dict)
    status = Column(String, default="PENDING") # PENDING, APPROVED, REJECTED
    requested_at = Column(DateTime, default=utc_now)
    resolved_at = Column(DateTime, nullable=True)

class EvaluationRecord(Base):
    __tablename__ = "evaluations"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    agent_run_id = Column(String, ForeignKey("agent_runs.id"), nullable=False)
    score = Column(Float, nullable=False) # 0.0 - 1.0
    passed = Column(Boolean, default=True)
    feedback = Column(Text, nullable=True)
    criteria_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=utc_now)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(String, primary_key=True, default=generate_uuid)
    event_type = Column(String, nullable=False, index=True)
    actor = Column(String, default="system")
    target_id = Column(String, nullable=True)
    details = Column(JSON, default=dict)
    created_at = Column(DateTime, default=utc_now)
