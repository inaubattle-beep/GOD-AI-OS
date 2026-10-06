# GOD AI OS — Mother Agent Operating System

Production-grade Autonomous AI Agent Operating System, Agent Factory, and MCP/Tool/Skill/Memory Runtime Platform.

## 🚀 Key Features

- **Mother Agent Runtime:** Central orchestrator handling intent understanding, task decomposition, agent routing, tool selection, observation, evaluation, and recovery.
- **Model Provider Independence:** Interchangeable drivers for OpenAI, Google Gemini, Anthropic Claude, Ollama, and local OpenAI-compatible endpoints.
- **Agent Factory:** Dynamic agent creation from specifications and 25+ built-in templates (Coding, Research, Browser, DevOps, Security, QA, Sales, Finance, etc.).
- **Universal Tool Registry:** Fine-grained risk levels, execution sandboxing, input/output schemas, and system capabilities.
- **MCP Subsystem:** Model Context Protocol gateway supporting `stdio`, `SSE`, and `Streamable HTTP` transports.
- **Multi-Layer Memory:** Working, short-term, episodic, semantic, agent, and system memory with pluggable vector storage (`pgvector` baseline).
- **Security & RBAC:** Policy engine, encrypted secret management (AES-256), prompt injection defense, and human-in-the-loop approval triggers.
- **AI Command Center & Agent IDE UI:** Next.js / Tailwind CSS / Glassmorphism visual operating dashboard.

---

## 🏗️ Architecture Overview

```
                               ┌─────────────────────────────────────────┐
                               │       User Interface (Next.js App)      │
                               └────────────────────┬────────────────────┘
                                                    │
                               ┌────────────────────▼────────────────────┐
                               │    FastAPI Application Gateway & API    │
                               └────────────────────┬────────────────────┘
                                                    │
                 ┌──────────────────────────────────┼──────────────────────────────────┐
                 │                                  │                                  │
    ┌────────────▼────────────┐        ┌────────────▼────────────┐        ┌────────────▼────────────┐
    │      Mother Agent       │        │      Agent Factory      │        │     Workflow Engine     │
    │   Planner & Execution   │        │ 25+ Built-in Templates  │        │   DAG Node Executor     │
    └────────────┬────────────┘        └────────────┬────────────┘        └────────────┬────────────┘
                 │                                  │                                  │
                 └──────────────────────────────────┼──────────────────────────────────┘
                                                    │
    ┌───────────────────────────────────────────────┼───────────────────────────────────────────────┐
    │                                               │                                               │
┌───▼──────────────┐                      ┌─────────▼────────┐                            ┌──────────▼───────────┐
│ Model Providers  │                      │ Universal Tools  │                            │ Multi-Layer Memory   │
│ OpenAI / Gemini  │                      │ & MCP Gateway    │                            │ PG / Vector Stores   │
│ Anthropic/Ollama │                      │ stdio/SSE/HTTP   │                            │ Document RAG         │
└──────────────────┘                      └──────────────────┘                            └──────────────────────┘
```

---

## ⚙️ Quick Start

### 1. Environment Setup
Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

### 2. Run Backend API
```bash
python -m venv .venv
.venv\Scripts\activate # On Windows
pip install -r requirements.txt
python -m uvicorn apps.api.main:app --reload --port 8000
```

### 3. Run Web Dashboard
```bash
cd apps/web
npm install
npm run dev
```
Open [http://localhost:3000](http://localhost:3000) to access the AI Command Center.

### 4. Run Automated Test Suite
```bash
$env:PYTHONPATH="."
.venv\Scripts\pytest
```

---

## 🐳 Docker Deployment
```bash
docker-compose up --build -d
```
Services spun up: `api` (8000), `web` (3000), `postgres` (5432 with pgvector), `redis` (6379).
