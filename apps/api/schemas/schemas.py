from pydantic import BaseModel, Field, ConfigDict
from typing import List, Optional, Dict, Any
from datetime import datetime

# Agent Schemas
class AgentBase(BaseModel):
    name: str
    description: Optional[str] = None
    role: str
    goal: str
    system_instructions: str
    personality: Optional[str] = None
    model_id: Optional[str] = None
    model_provider: str = "openai"
    model_parameters: Dict[str, Any] = Field(default_factory=dict)
    category: str = "general"
    is_template: bool = False
    skills: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    mcp_servers: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)
    token_limit: int = 100000
    budget_usd: float = 10.0
    time_limit_sec: int = 300

class AgentCreate(AgentBase):
    pass

class AgentTemplateCreate(BaseModel):
    name: str
    category: str
    role: str
    goal: str
    system_instructions: str
    skills: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    permissions: List[str] = Field(default_factory=list)

class AgentTemplateUpdate(BaseModel):
    category: Optional[str] = None
    role: Optional[str] = None
    goal: Optional[str] = None
    system_instructions: Optional[str] = None
    skills: Optional[List[str]] = None
    tools: Optional[List[str]] = None
    permissions: Optional[List[str]] = None

class AgentUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    role: Optional[str] = None
    goal: Optional[str] = None
    system_instructions: Optional[str] = None
    personality: Optional[str] = None
    model_provider: Optional[str] = None
    model_id: Optional[str] = None
    skills: Optional[List[str]] = None
    tools: Optional[List[str]] = None
    mcp_servers: Optional[List[str]] = None
    lifecycle_state: Optional[str] = None

class AgentResponse(AgentBase):
    id: str
    lifecycle_state: str
    version: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Agent Run Schemas
class AgentRunCreate(BaseModel):
    agent_id: str
    input_prompt: str
    task_id: Optional[str] = None

class AgentRunResponse(BaseModel):
    id: str
    agent_id: str
    task_id: Optional[str] = None
    status: str
    input_prompt: str
    output_result: Optional[str] = None
    error_message: Optional[str] = None
    tokens_used: int
    cost_usd: float
    duration_sec: float
    trace_data: Dict[str, Any]
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# Task Schemas
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    assigned_agent_id: Optional[str] = None
    priority: int = 1
    payload: Dict[str, Any] = Field(default_factory=dict)

class TaskResponse(BaseModel):
    id: str
    title: str
    description: Optional[str] = None
    assigned_agent_id: Optional[str] = None
    status: str
    priority: int
    payload: Dict[str, Any]
    result: Dict[str, Any]
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)

# Tool Schemas
class ToolCreate(BaseModel):
    name: str
    description: str
    category: str = "general"
    risk_level: str = "LOW"
    input_schema: Dict[str, Any] = Field(default_factory=dict)
    output_schema: Dict[str, Any] = Field(default_factory=dict)
    provider: str = "builtin"

class ToolResponse(ToolCreate):
    id: str
    version: str
    enabled: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# MCP Server Schemas
class MCPServerCreate(BaseModel):
    name: str
    description: Optional[str] = None
    transport: str = "stdio"
    command: Optional[str] = None
    args: List[str] = Field(default_factory=list)
    url: Optional[str] = None
    env_vars: Dict[str, str] = Field(default_factory=dict)

class MCPServerUpdate(BaseModel):
    transport: Optional[str] = None
    command: Optional[str] = None
    args: Optional[List[str]] = None
    url: Optional[str] = None
    enabled: Optional[bool] = None

class MCPServerResponse(MCPServerCreate):
    id: str
    enabled: bool
    status: str
    tools_discovered: List[Dict[str, Any]]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Skill Schemas
class SkillCreate(BaseModel):
    name: str
    description: str
    instructions: str
    category: str = "general"
    required_tools: List[str] = Field(default_factory=list)

class SkillResponse(SkillCreate):
    id: str
    version: str
    enabled: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

# Mother Agent Chat Request
class MotherAgentChatRequest(BaseModel):
    user_prompt: str
    agent_id: Optional[str] = None
    context_memory: bool = True

# Plugin Schemas
class PluginCreate(BaseModel):
    plugin_id: str
    name: str
    version: str = "1.0.0"
    description: str
    author: str = "User"
    category: str = "custom"
    permissions: List[str] = Field(default_factory=list)
    tools: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    mcp_servers: List[str] = Field(default_factory=list)

class PluginUpdate(BaseModel):
    name: Optional[str] = None
    version: Optional[str] = None
    description: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    permissions: Optional[List[str]] = None
    tools: Optional[List[str]] = None
    skills: Optional[List[str]] = None
    mcp_servers: Optional[List[str]] = None
    enabled: Optional[bool] = None
