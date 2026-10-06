'use client';

import React, { useState, useEffect } from 'react';
import { 
  Bot, Cpu, Terminal, Shield, Wrench, Network, Activity, 
  Layers, PlusCircle, CheckCircle2, AlertCircle, Play, Settings, RefreshCw, Zap, Sliders, Package, BookOpen, MessageSquare, Send
} from 'lucide-react';

export default function DashboardPage() {
  const [activeTab, setActiveTab] = useState<'command' | 'agents' | 'templates' | 'tools' | 'mcp' | 'models' | 'plugins' | 'skills' | 'communications'>('command');
  const [promptInput, setPromptInput] = useState('');
  const [chatLogs, setChatLogs] = useState<Array<{ sender: string; text: string; trace?: any }>>([
    {
      sender: 'MOTHER AGENT',
      text: 'Greetings. I am GOD AI OS Mother Agent. Ready to orchestrate specialized worker agents, tools, MCP servers, plugins, communications channels, and multi-step workflows. Enter a command or ask me to create an agent.'
    }
  ]);
  const [isProcessing, setIsProcessing] = useState(false);
  const [templates, setTemplates] = useState<any[]>([]);
  const [activeAgents, setActiveAgents] = useState<any[]>([]);
  const [tools, setTools] = useState<any[]>([]);
  const [mcpServers, setMcpServers] = useState<any[]>([]);
  const [availableModels, setAvailableModels] = useState<any[]>([]);
  const [modelProviders, setModelProviders] = useState<any[]>([]);
  const [plugins, setPlugins] = useState<any[]>([]);
  const [skills, setSkills] = useState<any[]>([]);
  const [commChannels, setCommChannels] = useState<any[]>([]);
  const [commLogs, setCommLogs] = useState<any[]>([]);
  const [systemHealth, setSystemHealth] = useState<any>(null);

  // Communications Dispatch Form State
  const [dispatchChannel, setDispatchChannel] = useState('telegram-bot');
  const [dispatchRecipient, setDispatchRecipient] = useState('@ops_team');
  const [dispatchMessage, setDispatchMessage] = useState('System alert: All agent runtimes online');

  // Router test states
  const [routerPrompt, setRouterPrompt] = useState('Write an efficient sorting algorithm');
  const [routerTaskType, setRouterTaskType] = useState('coding');
  const [routerPrivacy, setRouterPrivacy] = useState(false);
  const [routerResult, setRouterResult] = useState<any>(null);

  useEffect(() => {
    fetchData();
  }, []);

  const safeArray = (val: any) => (Array.isArray(val) ? val : []);

  const fetchData = async () => {
    try {
      const [tRes, aRes, toolRes, mcpRes, modelsRes, provRes, plugRes, skillRes, commChanRes, commLogRes, healthRes] = await Promise.all([
        fetch('http://localhost:8000/api/v1/agents/templates').then(r => r.json()).catch(() => []),
        fetch('http://localhost:8000/api/v1/agents').then(r => r.json()).catch(() => []),
        fetch('http://localhost:8000/api/v1/tools').then(r => r.json()).catch(() => []),
        fetch('http://localhost:8000/api/v1/mcp/servers').then(r => r.json()).catch(() => []),
        fetch('http://localhost:8000/api/v1/models').then(r => r.json()).catch(() => []),
        fetch('http://localhost:8000/api/v1/models/providers').then(r => r.json()).catch(() => []),
        fetch('http://localhost:8000/api/v1/plugins').then(r => r.json()).catch(() => []),
        fetch('http://localhost:8000/api/v1/skills').then(r => r.json()).catch(() => []),
        fetch('http://localhost:8000/api/v1/communications/channels').then(r => r.json()).catch(() => []),
        fetch('http://localhost:8000/api/v1/communications/logs').then(r => r.json()).catch(() => []),
        fetch('http://localhost:8000/health').then(r => r.json()).catch(() => null)
      ]);
      setTemplates(safeArray(tRes));
      setActiveAgents(safeArray(aRes));
      setTools(safeArray(toolRes));
      setMcpServers(safeArray(mcpRes));
      setAvailableModels(safeArray(modelsRes));
      setModelProviders(safeArray(provRes));
      setPlugins(safeArray(plugRes));
      setSkills(safeArray(skillRes));
      setCommChannels(safeArray(commChanRes));
      setCommLogs(safeArray(commLogRes));
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

  const handleDispatchCommunication = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/v1/communications/dispatch', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          channel_id: dispatchChannel,
          recipient: dispatchRecipient,
          message_text: dispatchMessage
        })
      });
      if (res.ok) {
        alert('Message successfully dispatched across channel!');
        fetchData();
      }
    } catch (err) {
      alert('Failed to dispatch communication message.');
    }
  };

  const handleTestRouter = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const res = await fetch('http://localhost:8000/api/v1/models/route', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          prompt: routerPrompt,
          task_type: routerTaskType,
          require_privacy: routerPrivacy
        })
      });
      const data = await res.json();
      setRouterResult(data);
    } catch (err) {
      alert('Failed to execute Model Gateway router');
    }
  };

  const togglePlugin = async (plugin_id: string, current_state: boolean) => {
    try {
      const res = await fetch(`http://localhost:8000/api/v1/plugins/${plugin_id}/toggle`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ enabled: !current_state })
      });
      if (res.ok) {
        fetchData();
      }
    } catch (err) {
      alert('Failed to toggle plugin status');
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
              onClick={() => setActiveTab('communications')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'communications' ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 glow-primary' : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <MessageSquare className="w-4 h-4" />
              Communications Hub ({safeArray(commChannels).length})
            </button>
            <button
              onClick={() => setActiveTab('models')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'models' ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 glow-primary' : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <Sliders className="w-4 h-4" />
              Model Gateway ({safeArray(availableModels).length})
            </button>
            <button
              onClick={() => setActiveTab('plugins')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'plugins' ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 glow-primary' : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <Package className="w-4 h-4" />
              Plugins ({safeArray(plugins).length})
            </button>
            <button
              onClick={() => setActiveTab('skills')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'skills' ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 glow-primary' : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <BookOpen className="w-4 h-4" />
              Skills Library ({safeArray(skills).length})
            </button>
            <button
              onClick={() => setActiveTab('agents')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'agents' ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 glow-primary' : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <Bot className="w-4 h-4" />
              Active Agents ({safeArray(activeAgents).length})
            </button>
            <button
              onClick={() => setActiveTab('templates')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'templates' ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 glow-primary' : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <Layers className="w-4 h-4" />
              Agent Templates ({safeArray(templates).length})
            </button>
            <button
              onClick={() => setActiveTab('tools')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'tools' ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 glow-primary' : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <Wrench className="w-4 h-4" />
              Universal Tools ({safeArray(tools).length})
            </button>
            <button
              onClick={() => setActiveTab('mcp')}
              className={`w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm font-medium transition-all ${
                activeTab === 'mcp' ? 'bg-indigo-600/20 text-indigo-300 border border-indigo-500/40 glow-primary' : 'text-slate-400 hover:bg-slate-800/50 hover:text-slate-200'
              }`}
            >
              <Network className="w-4 h-4" />
              MCP Servers ({safeArray(mcpServers).length})
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
            <p>Channels: Omnichannel ({safeArray(commChannels).length})</p>
            <p>Plugins: Active ({safeArray(plugins).length})</p>
          </div>
        </div>
      </aside>

      {/* Main Content Area */}
      <main className="flex-1 flex flex-col overflow-hidden bg-[#090c15]">
        <header className="h-16 border-b border-slate-800/80 px-6 flex items-center justify-between glass-panel">
          <div className="flex items-center gap-4">
            <h2 className="text-lg font-semibold text-slate-100 capitalize">
              {activeTab === 'command' && 'AI Command Center & Mother Agent'}
              {activeTab === 'communications' && 'Omnichannel Communications Hub (Email, Telegram, WhatsApp, Slack, ViciDial)'}
              {activeTab === 'models' && 'Multi-Model Gateway & Intelligent Router'}
              {activeTab === 'plugins' && 'Plugin Ecosystem & Manager'}
              {activeTab === 'skills' && 'Reusable Skills Library'}
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
              <div className="flex-1 glass-panel rounded-2xl p-4 overflow-y-auto space-y-4 border border-slate-800">
                {safeArray(chatLogs).map((log, index) => (
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
                            <summary className="text-indigo-400 hover:underline">View Execution Trace Steps ({safeArray(log.trace.steps).length})</summary>
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

              <form onSubmit={handleMotherSubmit} className="flex gap-3">
                <input
                  type="text"
                  value={promptInput}
                  onChange={(e) => setPromptInput(e.target.value)}
                  placeholder="Ask Mother Agent to execute a task or create an agent..."
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

          {activeTab === 'communications' && (
            <div className="max-w-6xl mx-auto space-y-6">
              <div>
                <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Active Omnichannel Gateway Interfaces</h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                  {safeArray(commChannels).map((c, i) => (
                    <div key={i} className="glass-card p-4 rounded-xl">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-bold text-white text-sm">{c.name}</h4>
                        <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-400 font-bold border border-emerald-500/30">
                          {c.status}
                        </span>
                      </div>
                      <p className="text-xs text-indigo-400 font-mono">Channel ID: {c.channel_id}</p>
                      <p className="text-[11px] text-slate-400 capitalize mt-1">Type: {c.channel_type}</p>
                    </div>
                  ))}
                </div>
              </div>

              <div className="glass-panel p-6 rounded-2xl border border-slate-800">
                <h3 className="font-bold text-lg text-white mb-4 flex items-center gap-2">
                  <Send className="w-5 h-5 text-indigo-400" /> Dispatch Communication Message / Alert
                </h3>

                <form onSubmit={handleDispatchCommunication} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                      <label className="text-xs text-slate-400 mb-1 block">Target Communication Channel</label>
                      <select 
                        value={dispatchChannel}
                        onChange={(e) => setDispatchChannel(e.target.value)}
                        className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-100 focus:outline-none"
                      >
                        {safeArray(commChannels).map((c, idx) => (
                          <option key={idx} value={c.channel_id}>{c.name} ({c.channel_type})</option>
                        ))}
                      </select>
                    </div>

                    <div>
                      <label className="text-xs text-slate-400 mb-1 block">Recipient (Email / Phone / Telegram Handle / Slack Channel)</label>
                      <input 
                        type="text"
                        value={dispatchRecipient}
                        onChange={(e) => setDispatchRecipient(e.target.value)}
                        className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-100 focus:outline-none"
                      />
                    </div>
                  </div>

                  <div>
                    <label className="text-xs text-slate-400 mb-1 block">Message Content / Text Prompt</label>
                    <textarea 
                      rows={3}
                      value={dispatchMessage}
                      onChange={(e) => setDispatchMessage(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-xs text-slate-100 focus:outline-none"
                    />
                  </div>

                  <button
                    type="submit"
                    className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold rounded-xl text-white transition-all shadow glow-primary flex items-center gap-1.5"
                  >
                    <Send className="w-3.5 h-3.5" /> Dispatch Communication
                  </button>
                </form>
              </div>

              <div>
                <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Recent Communication Dispatch Logs</h3>
                <div className="glass-panel rounded-xl overflow-hidden border border-slate-800">
                  <table className="w-full text-left text-xs text-slate-300">
                    <thead className="bg-slate-900/80 text-slate-400 uppercase font-mono text-[10px]">
                      <tr>
                        <th className="p-3">Dispatch ID</th>
                        <th className="p-3">Channel</th>
                        <th className="p-3">Recipient</th>
                        <th className="p-3">Message Snippet</th>
                        <th className="p-3">Status</th>
                      </tr>
                    </thead>
                    <tbody className="divide-y divide-slate-800/60">
                      {safeArray(commLogs).length === 0 ? (
                        <tr>
                          <td colSpan={5} className="p-4 text-center text-slate-500 font-mono">No communication dispatches recorded yet. Use form above to test.</td>
                        </tr>
                      ) : (
                        safeArray(commLogs).map((log, i) => (
                          <tr key={i} className="hover:bg-slate-800/40">
                            <td className="p-3 font-mono text-indigo-400">{log.dispatch_id}</td>
                            <td className="p-3 uppercase text-[11px] font-semibold">{log.channel_type}</td>
                            <td className="p-3 font-mono">{log.recipient}</td>
                            <td className="p-3">{log.message_snippet}</td>
                            <td className="p-3">
                              <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-400 font-bold border border-emerald-500/30">
                                {log.status}
                              </span>
                            </td>
                          </tr>
                        ))
                      )}
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          )}

          {activeTab === 'plugins' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {safeArray(plugins).map((p, i) => (
                <div key={i} className="glass-card p-5 rounded-2xl flex flex-col justify-between">
                  <div>
                    <div className="flex justify-between items-start mb-2">
                      <div>
                        <h3 className="font-bold text-white text-base">{p.name}</h3>
                        <p className="text-xs text-indigo-400">by {p.author} • v{p.version}</p>
                      </div>
                      <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                        p.enabled ? 'bg-emerald-500/20 text-emerald-400 border border-emerald-500/30' : 'bg-slate-700 text-slate-400'
                      }`}>
                        {p.enabled ? 'ENABLED' : 'DISABLED'}
                      </span>
                    </div>
                    <p className="text-xs text-slate-300 mb-4">{p.description}</p>
                    
                    <div className="space-y-1 text-xs text-slate-400 font-mono mb-4">
                      <p>Category: {p.category}</p>
                      <p>Tools Attached: {safeArray(p.tools).join(', ')}</p>
                      <p>MCP Servers: {safeArray(p.mcp_servers).join(', ')}</p>
                    </div>
                  </div>

                  <button
                    onClick={() => togglePlugin(p.plugin_id, p.enabled)}
                    className={`w-full py-2 rounded-xl text-xs font-semibold transition-all ${
                      p.enabled ? 'bg-rose-600/20 text-rose-300 hover:bg-rose-600/30 border border-rose-500/30' : 'bg-indigo-600 hover:bg-indigo-500 text-white'
                    }`}
                  >
                    {p.enabled ? 'Disable Plugin' : 'Enable Plugin'}
                  </button>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'skills' && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {safeArray(skills).map((s, i) => (
                <div key={i} className="glass-card p-5 rounded-2xl">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-bold text-white text-base">{s.name}</h3>
                    <span className="px-2 py-0.5 rounded text-[10px] bg-indigo-500/20 text-indigo-300 border border-indigo-500/30 uppercase">
                      {s.category}
                    </span>
                  </div>
                  <p className="text-xs text-slate-300 mb-3">{s.description}</p>
                  <div className="text-[11px] font-mono text-slate-400 bg-slate-900/80 p-3 rounded-xl border border-slate-800 space-y-1">
                    <p className="text-indigo-400 font-semibold">Skill Instructions Snippet:</p>
                    <p className="whitespace-pre-wrap">{s.instructions_snippet}</p>
                  </div>
                </div>
              ))}
            </div>
          )}

          {activeTab === 'models' && (
            <div className="max-w-6xl mx-auto space-y-6">
              <div>
                <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Active LLM Providers</h3>
                <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
                  {safeArray(modelProviders).map((p, i) => (
                    <div key={i} className="glass-card p-4 rounded-xl flex items-center justify-between">
                      <div>
                        <h4 className="font-semibold text-white text-sm">{p.name}</h4>
                        <span className="text-[10px] text-slate-400 uppercase">{p.type} Provider</span>
                      </div>
                      <span className="px-2 py-0.5 rounded text-[10px] bg-emerald-500/20 text-emerald-400 font-bold border border-emerald-500/30">
                        {p.status}
                      </span>
                    </div>
                  ))}
                </div>
              </div>

              <div>
                <h3 className="text-sm font-semibold text-slate-400 uppercase tracking-wider mb-3">Registered Models & Capabilities</h3>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                  {safeArray(availableModels).map((m, i) => (
                    <div key={i} className="glass-card p-5 rounded-2xl">
                      <div className="flex justify-between items-start mb-2">
                        <h4 className="font-bold text-white text-base">{m.name}</h4>
                        <span className={`px-2 py-0.5 rounded text-[10px] font-bold ${
                          m.is_local ? 'bg-cyan-500/20 text-cyan-400 border border-cyan-500/30' : 'bg-purple-500/20 text-purple-400 border border-purple-500/30'
                        }`}>
                          {m.is_local ? 'LOCAL' : 'CLOUD'}
                        </span>
                      </div>
                      <p className="text-xs text-indigo-400 font-mono mb-3">Model ID: {m.model_id}</p>
                      
                      <div className="space-y-1.5 text-xs text-slate-300">
                        <div className="flex justify-between">
                          <span className="text-slate-400">Context Window:</span>
                          <span className="font-mono">{m.context_window?.toLocaleString()} tokens</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Coding Score:</span>
                          <span className="font-mono text-emerald-400">{(m.coding_score * 100).toFixed(0)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Reasoning Score:</span>
                          <span className="font-mono text-indigo-400">{(m.reasoning_score * 100).toFixed(0)}%</span>
                        </div>
                        <div className="flex justify-between">
                          <span className="text-slate-400">Cost / 1k tokens:</span>
                          <span className="font-mono text-cyan-300">${m.cost_per_1k_input}</span>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>

              <div className="glass-panel p-6 rounded-2xl border border-slate-800">
                <h3 className="font-bold text-lg text-white mb-4 flex items-center gap-2">
                  <Sliders className="w-5 h-5 text-indigo-400" /> Test Intelligent Model Router
                </h3>

                <form onSubmit={handleTestRouter} className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    <div>
                      <label className="text-xs text-slate-400 mb-1 block">Task Intent</label>
                      <select 
                        value={routerTaskType}
                        onChange={(e) => setRouterTaskType(e.target.value)}
                        className="w-full bg-slate-900 border border-slate-700 rounded-xl px-3 py-2 text-xs text-slate-100 focus:outline-none"
                      >
                        <option value="coding">Coding & Software Engineering</option>
                        <option value="reasoning">Complex Logical Reasoning</option>
                        <option value="fast">Fast / Cheap Execution</option>
                        <option value="general">General Purpose</option>
                      </select>
                    </div>

                    <div className="flex items-center pt-5">
                      <label className="flex items-center gap-2 text-xs text-slate-300 cursor-pointer">
                        <input 
                          type="checkbox"
                          checked={routerPrivacy}
                          onChange={(e) => setRouterPrivacy(e.target.checked)}
                          className="rounded bg-slate-900 border-slate-700 text-indigo-600 focus:ring-0"
                        />
                        Strict Local Privacy (Route to Ollama)
                      </label>
                    </div>
                  </div>

                  <div>
                    <label className="text-xs text-slate-400 mb-1 block">Test Prompt</label>
                    <input 
                      type="text"
                      value={routerPrompt}
                      onChange={(e) => setRouterPrompt(e.target.value)}
                      className="w-full bg-slate-900 border border-slate-700 rounded-xl px-4 py-2.5 text-xs text-slate-100 focus:outline-none"
                    />
                  </div>

                  <button
                    type="submit"
                    className="px-5 py-2.5 bg-indigo-600 hover:bg-indigo-500 text-xs font-semibold rounded-xl text-white transition-all shadow glow-primary"
                  >
                    Route Prompt & Execute
                  </button>
                </form>

                {routerResult && (
                  <div className="mt-4 p-4 rounded-xl bg-slate-900/90 border border-slate-800 space-y-2 font-mono text-xs">
                    <p className="text-indigo-400 font-bold">🎯 Routed Target Model: {routerResult.routed_model} ({routerResult.provider})</p>
                    <p className="text-slate-300">Is Local Execution: {routerResult.is_local ? 'YES' : 'NO'}</p>
                    <p className="text-slate-300">Estimated Cost: ${routerResult.estimated_cost_usd}</p>
                    <div className="pt-2 border-t border-slate-800 text-slate-200">
                      Response: {routerResult.content}
                    </div>
                  </div>
                )}
              </div>
            </div>
          )}

          {activeTab === 'agents' && (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
              {safeArray(activeAgents).map((agent) => (
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
              {safeArray(templates).map((tpl, i) => (
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
              {safeArray(tools).map((tool, i) => (
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
              {safeArray(mcpServers).map((server, i) => (
                <div key={i} className="glass-card p-5 rounded-2xl">
                  <div className="flex justify-between items-start mb-2">
                    <h3 className="font-semibold text-base text-white">{server.name}</h3>
                    <span className="px-2 py-0.5 rounded text-[10px] bg-cyan-500/20 text-cyan-300 border border-cyan-500/30 uppercase">
                      {server.transport}
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 mb-3">Command / URL: <code className="text-indigo-300">{server.command ? `${server.command} ${safeArray(server.args).join(' ')}` : server.url}</code></p>
                </div>
              ))}
            </div>
          )}
        </div>
      </main>
    </div>
  );
}
