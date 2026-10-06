'use client';

import React, { useState, useEffect } from 'react';
import { 
  Bot, Cpu, Terminal, Shield, Wrench, Network, Activity, 
  Layers, PlusCircle, CheckCircle2, AlertCircle, Play, Settings, RefreshCw, Zap
} from 'lucide-react';

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<'command' | 'agents' | 'templates' | 'tools' | 'mcp'>('command');
  const [promptInput, setPromptInput] = useState('');
  const [chatLogs, setChatLogs] = useState<Array<{ sender: string; text: string; trace?: any }>>([
    {
      sender: 'MOTHER AGENT',
      text: 'Greetings. I am GOD AI OS Mother Agent. Ready to orchestrate specialized worker agents, tools, MCP servers, and multi-step workflows. Enter a command or ask me to create an agent.'
    }
  ]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [templates, setTemplates] = useState<any[]>([]);
  const [activeAgents, setActiveAgents] = useState<any[]>([]);
  const [tools, setTools] = useState<any[]>([]);
  const [mcpServers, setMcpServers] = useState<any[]>([]);
  const [systemHealth, setSystemHealth] = useState<any>(null);

  // Fetch initial telemetry
  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [tRes, aRes, toolRes, mcpRes, healthRes] = await Promise.all([
        fetch('http://localhost:8000/api/v1/agents/templates').then(r => r.json()).catch(() => []),
        fetch('http://localhost:8000/api/v1/agents').then(r => r.json()).catch(() => []),
        fetch('http://localhost:8000/api/v1/tools').then(r => r.json()).catch(() => []),
        fetch('http://localhost:8000/api/v1/mcp/servers').then(r => r.json()).catch(() => []),
        fetch('http://localhost:8000/health').then(r => r.json()).catch(() => null)
      ]);
      setTemplates(tRes || []);
      setActiveAgents(aRes || []);
      setTools(toolRes || []);
      setMcpServers(mcpRes || []);
      setSystemHealth(healthRes);
    } catch (e) {
      console.error('Error connecting to backend API', e);
    }
  };

  const handleMotherSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!promptInput.trim() || isProcessing) return;

    const userText = promptInput;
    setPromptInput('');
    setChatLogs(prev => [...prev, { sender: 'USER', text: userText }]);
    setIsProcessing(true);

    try {
      const res = await fetch('http://localhost:8000/api/v1/mother/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_prompt: userText })
      });
      const data = await res.json();

      if (data.status === 'AGENT_CREATED') {
        setChatLogs(prev => [...prev, { 
          sender: 'MOTHER AGENT', 
          text: `✅ ${data.message}` 
        }]);
        fetchData();
      } else {
        setChatLogs(prev => [...prev, { 
          sender: 'MOTHER AGENT', 
          text: data.result || 'Task execution completed.', 
          trace: data.trace 
        }]);
      }
    } catch (err: any) {
      setChatLogs(prev => [...prev, { 
        sender: 'SYSTEM', 
        text: `Error connecting to Mother Agent Runtime: ${err.message}` 
      }]);
    } finally {
      setIsProcessing(false);
    }
  };

  const instantiateTemplate = async (name: string) => {
    try {
      const res = await fetch(`http://localhost:8000/api/v1/agents/templates/${encodeURIComponent(name)}/instantiate`, {
        method: 'POST'
      });
      if (res.ok) {
        alert(`Successfully instantiated template: ${name}`);
        fetchData();
      }
    } catch (err) {
      alert(`Failed to instantiate template ${name}`);
    }
  };

  return (
    <div className="flex h-screen bg-[#090c15] text-slate-100 font-sans">
      {/* Sidebar Navigation */}
      <aside className="w-64 glass-panel border-r border-slate-800 flex flex-col justify-between p-4 z-20">
        <div>
          <div className="flex items-[#6366f1] items-center gap-3 mb-8 px-2">
            <div className="p-2 rounded-xl bg-indigo-600/20 text-indigo-400 border border-indigo-500/30">
              <Cpu className="w-6 h-6 animate-pulse" />
            </div>
            <div>
              <h1 className="font-bold text-lg tracking-wider text-white">GOD AI OS</h1>
              <p className="text-xs text-indigo-400 font-medium">Mother Agent v1.0</p>
            </div>
          </div>

          <nav className="space-y-1">
            <button
              onClick={() => setActiveTab('command')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'command' ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 glow-primary' : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <Terminal className="w-4 h-4" />
              AI Command Center
            </button>
            <button
              onClick={() => setActiveTab('agents')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'agents' ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 glow-primary' : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <Bot className="w-4 h-4" />
              Active Agents ({activeAgents.length})
            </button>
            <button
              onClick={() => setActiveTab('templates')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'templates' ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 glow-primary' : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <Layers className="w-4 h-4" />
              Agent Templates ({templates.length})
            </button>
            <button
              onClick={() => setActiveTab('tools')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'tools' ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 glow-primary' : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <Wrench className="w-4 h-4" />
              Universal Tools ({tools.length})
            </button>
            <button
              onClick={() => setActiveTab('mcp')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'mcp' ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 glow-primary' : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <Network className="w-4 h-4" />
              MCP Servers ({mcpServers.length})
            </button>
          </nav>
        </div>

        {/* System Health Card */}
        <div className="p-3 rounded-xl bg-slate-900/60 border border-slate-800">
          <div className="flex items-center justify-between text-xs mb-2">
            <span className="text-slate-400 flex items-center gap-1.5">
              <Activity className="w-3.5 h-3.5 text-emerald-400" /> System Status
            </span>
            <span className="text-emerald-400 font-semibold">ONLINE</span>
          </div>
          <div className="text-[11px] text-slate-500 space-y-0.5">
            <p>Provider: Multi-LLM Active</p>
            <p>Database: SQLite Async / PG</p>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col overflow-hidden bg-[#090c15]">
        {/* Top Navbar */}
        <header className="h-16 border-b border-slate-800/80 px-6 flex items-center justify-between glass-panel">
          <div className="flex items-center gap-4">
            <h2 className="text-lg font-semibold text-slate-100 capitalize">
              {activeTab === 'command' && 'AI Command Center & Mother Agent'}
              {activeTab === 'agents' && 'Active Agent Directory'}
              {activeTab === 'templates' && 'Built-in Agent Templates (25+)'}
              {activeTab === 'tools' && 'Universal Tool Registry'}
              {activeTab === 'mcp' && 'MCP Subsystem & Servers'}
            </h2>
          </div>
          <div className="flex items-center gap-3">
            <button 
              onClick={fetchData} 
              className="p-2 rounded-lg bg-slate-800/60 hover:bg-slate-700/60 text-slate-300 transition-colors"
              title="Refresh Data"
            >
              <RefreshCw className="w-4 h-4" />
            </button>
          </div>
        </header>

        {/* Content Body */}
        <div className="flex-1 p-6 overflow-y-auto">
          {activeTab === 'command' && (
            <div className="max-w-5xl mx-auto flex flex-col h-full space-y-4">
              {/* Chat Output Area */}
              <div className="flex-1 glass-panel rounded-2xl p-4 overflow-y-auto space-y-4 border border-slate-800">
                {chatLogs.map((log, index) => (
                  <div 
                    key={index}
                    className={`flex flex-col ${log.sender === 'USER' ? 'items-end' : 'items-start'}`}
                  >
                    <div className="flex items-center gap-2 mb-1 text-xs text-slate-400">
                      <span className="font-semibold text-indigo-400">{log.sender}</span>
                    </div>
                    <div className={`p-4 rounded-xl max-w-3xl text-sm leading-relaxed ${
                      log.sender === 'USER' 
                        ? 'bg-indigo-600 text-white rounded-br-none' 
                        : 'bg-slate-800/80 border border-slate-700 text-slate-200 rounded-bl-none'
                    }`}>
                      <p className="whitespace-pre-wrap">{log.text}</p>
                      {log.trace && (
                        <div className="mt-3 pt-3 border-t border-slate-700/60 text-xs font-mono text-slate-400 space-y-1">
                          <p>⏱️ Duration: {log.trace.duration_sec}s | Tokens: {log.trace.tokens_used}</p>
                          <details className="cursor-pointer mt-1">
                            <summary className="text-indigo-400 hover:underline">View Execution Trace Steps ({log.trace.steps?.length})</summary>
                            <pre className="mt-2 p-2 bg-slate-900 rounded text-[11px] overflow-x-auto text-slate-300">
                              {JSON.stringify(log.trace.steps, null, 2)}
                            </pre>
                          </details>
                        </div>
                      )}
                    </div>
                  </div>
                ))}

                {isProcessing && (
                  <div className="flex items-center gap-3 p-4 text-indigo-400 text-sm">
                    <Zap className="w-4 h-4 animate-spin" />
                    Mother Agent is planning and executing task loop...
                  </div>
                )}
              </div>

              {/* Chat Input Form */}
              <form onSubmit={handleMotherSubmit} className="flex gap-3">
                <input
                  type="text"
                  value={promptInput}
                  onChange={(e) => setPromptInput(e.target.value)}
                  placeholder="Ask Mother Agent to execute a task or create an agent (e.g. 'Create a DevOps agent that monitors server health')..."
                  className="flex-1 bg-slate-900/90 border border-slate-700/80 rounded-xl px-4 py-3 text-sm focus:outline-none focus:border-indigo-500 text-slate-100"
                />
                <button
                  type="submit"
                  disabled={isProcessing}
                  className="px-6 py-3 bg-indigo-600 hover:bg-indigo-500 font-medium rounded-xl text-sm transition-all shadow-lg glow-primary flex items-center gap-2"
                >
                  <Play className="w-4 h-4" /> Send Command
                </button>
              </form>
            </div>
          )}

          {activeTab === 'agents' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {activeAgents.map((agent) => (
                <div key={agent.id} className="glass-card p-5 rounded-2xl flex flex-col justify-between">
                  <div>
                    <div className="flex justify-between items-start mb-3">
                      <div>
                        <h3 className="font-semibold text-lg text-white">{agent.name}</h3>
                        <p className="text-xs text-indigo-400 font-medium">{agent.role}</p>
                      </div>
                      <span className="px-2.5 py-1 rounded-full text-[10px] font-bold bg-emerald-500/20 text-emerald-400 border border-emerald-500/30">
                        {agent.lifecycle_state}
                      </span>
                    </div>
                    <p className="text-xs text-slate-300 line-clamp-3 mb-4">{agent.goal}</p>
                  </div>

                  <div className="pt-3 border-t border-slate-800 text-xs text-slate-400 flex justify-between items-center">
                    <span>Provider: {agent.model_provider}</span>
                    <span className="text-slate-500">v{agent.version}</span>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'templates' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {templates.map((tpl, i) => (
                <div key={i} className="glass-card p-5 rounded-2xl flex flex-col justify-between">
                  <div>
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-semibold text-base text-white">{tpl.name}</h3>
                      <span className="px-2 py-0.5 rounded text-[10px] bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 capitalize">
                        {tpl.category}
                      </span>
                    </div>
                    <p className="text-xs text-indigo-400 font-medium mb-2">{tpl.role}</p>
                    <p className="text-xs text-slate-300 line-clamp-3 mb-4">{tpl.goal}</p>
                  </div>

                  <button
                    onClick={() => instantiateTemplate(tpl.name)}
                    className="w-full py-2 bg-indigo-600/30 hover:bg-indigo-600 text-indigo-200 border border-indigo-500/40 rounded-xl text-xs font-medium transition-all flex items-center justify-center gap-1.5"
                  >
                    <PlusCircle className="w-3.5 h-3.5" /> Instantiate Agent
                  </button>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'tools' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {tools.map((tool, i) => (
                <div key={i} className="glass-card p-5 rounded-2xl">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-semibold text-base text-white">{tool.name}</h3>
                    <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                      tool.risk_level === 'HIGH' ? 'bg-rose-500/20 text-rose-400 border border-rose-500/30' : 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30'
                    }`}>
                      Risk: {tool.risk_level}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 mb-3">{tool.description}</p>
                  <div className="text-[11px] font-mono text-slate-400 bg-slate-900/80 p-2.5 rounded-lg border border-slate-800">
                    Input Params: {JSON.stringify(tool.input_schema)}
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'mcp' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {mcpServers.map((server, i) => (
                <div key={i} className="glass-card p-5 rounded-2xl">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-semibold text-base text-white">{server.name}</h3>
                    <span className="px-2 py-0.5 rounded text-[10px] bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 uppercase">
                      {server.transport}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mb-3">Command: <code className="text-indigo-300">{server.command} {server.args?.join(' ')}</code></p>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
