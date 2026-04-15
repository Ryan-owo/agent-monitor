<div align="center">

<h1>🪼 Agent Monitor</h1>

<p>
  <strong>Lightweight real-time dashboard for <a href="https://openclaw.ai">OpenClaw</a> multi-agent setups</strong><br>
  <strong>轻量级实时仪表盘，专为 OpenClaw 多 Agent 工作流打造</strong>
</p>

<p>
  <a href="#english">English</a> · <a href="#中文">中文</a>
</p>

<p>
  <img src="https://img.shields.io/badge/python-3.8%2B-blue?style=flat-square&logo=python&logoColor=white" alt="Python 3.8+">
  <img src="https://img.shields.io/badge/dependencies-zero-brightgreen?style=flat-square" alt="Zero dependencies">
  <img src="https://img.shields.io/badge/license-MIT-orange?style=flat-square" alt="MIT License">
  <img src="https://img.shields.io/github/v/release/Ryan-owo/agent-monitor?style=flat-square&color=purple" alt="Latest Release">
</p>

<br>

<img src="https://raw.githubusercontent.com/Ryan-owo/agent-monitor/main/docs/screenshot-light.png" alt="Agent Monitor — Light Mode" width="100%">
<br><br>
<img src="https://raw.githubusercontent.com/Ryan-owo/agent-monitor/main/docs/screenshot-dark.png" alt="Agent Monitor — Dark Mode" width="100%">

</div>

---

<a name="english"></a>

## English

### Features

- 🟢 **Live status** — Running / Idle / Offline per agent, auto-refreshes every 5 s
- 📊 **Token & cost tracking** — Input / Output tokens and estimated USD cost, aggregated across all sessions
- 🤖 **Subagent visibility** — See active child agents spawned by each agent
- 📋 **Current task** — Latest task extracted from session data; click a card to expand the full task and subagent list
- 📈 **Context bar** — Visual context-window usage per agent; turns orange at 70 % and red at 90 %
- 🔔 **Tab badge** — Browser tab shows `[N] Agent Monitor` while agents are running
- 🌙 **Dark mode** — Follows system preference, manually toggleable, persisted in localStorage
- 🌐 **i18n** — Chinese / English / Japanese, persisted in localStorage
- 🎨 **Neumorphic UI** — Soft tactile design with smooth animations
- ⚡ **Zero dependencies** — Pure Python 3.8+ stdlib + React 18 via CDN

### Quickstart

```bash
# 1. Clone
git clone https://github.com/Ryan-owo/agent-monitor.git
cd agent-monitor

# 2. Run (auto-detects your OpenClaw agents directory)
python3 server.py

# 3. Open in browser
open http://localhost:7788
```

> **That's it.** No `pip install`, no Node.js, no config files required.

### Requirements

| | Version |
|---|---|
| Python | 3.8+ |
| OpenClaw | any |
| Browser | Chrome / Firefox / Safari / Edge (modern) |

### Configuration

**Auto-detection** — the server searches for your OpenClaw agents directory in this order:

1. `OPENCLAW_AGENTS_DIR` environment variable
2. `~/.openclaw/agents`
3. `~/.openclaw-project0/agents`
4. `~/.openclaw-default/agents`
5. Any `~/.openclaw*/agents` glob match

**CLI flags**

```
python3 server.py [options]

  -p, --port PORT    Port to listen on       (default: 7788)
      --host HOST    Bind address            (default: 127.0.0.1)
                                             Use 0.0.0.0 for LAN access
  -d, --dir  PATH    OpenClaw agents dir     (auto-detected if omitted)
```

**Environment variable**

```bash
OPENCLAW_AGENTS_DIR=~/.my-openclaw/agents python3 server.py
```

### Project Structure

```
agent-monitor/
├── server.py     # HTTP server + data layer  (stdlib only, ~200 lines)
├── index.html    # React 18 dashboard        (single file, CDN deps)
├── docs/
│   ├── screenshot-light.png
│   └── screenshot-dark.png
├── .gitignore
└── README.md
```

---

<a name="中文"></a>

## 中文

### 功能特性

- 🟢 **实时状态** — 每个 Agent 的执行中 / 空闲 / 离线状态，每 5 秒自动刷新
- 📊 **Token 与费用追踪** — 输入/输出 Token 用量与估算美元费用，跨所有 Session 聚合
- 🤖 **子 Agent 可见性** — 查看每个 Agent 当前活跃的子 Agent 列表
- 📋 **当前任务** — 从 Session 数据中提取最新任务标签；点击卡片可展开完整任务文本与子 Agent 列表
- 📈 **上下文进度条** — 直观显示每个 Agent 的上下文窗口用量；70 % 变橙色，90 % 变红色
- 🔔 **Tab 角标** — 有 Agent 运行时浏览器标签显示 `[N] Agent Monitor`
- 🌙 **深色模式** — 跟随系统偏好，可手动切换，设置持久化
- 🌐 **多语言** — 中文 / 英文 / 日文，设置持久化到 localStorage
- 🎨 **软 UI 设计** — Neumorphism 触觉风格，流畅动效
- ⚡ **零依赖** — 纯 Python 3.8+ 标准库 + React 18（CDN）

### 快速开始

```bash
# 1. 克隆仓库
git clone https://github.com/Ryan-owo/agent-monitor.git
cd agent-monitor

# 2. 启动服务（自动检测 OpenClaw agents 目录）
python3 server.py

# 3. 打开浏览器
open http://localhost:7788
```

> **就这三步。** 无需 `pip install`，无需 Node.js，无需任何配置文件。

### 环境要求

| | 版本 |
|---|---|
| Python | 3.8+ |
| OpenClaw | 任意版本 |
| 浏览器 | Chrome / Firefox / Safari / Edge（现代版本）|

### 配置说明

**自动检测** — 服务器按以下优先级查找 OpenClaw agents 目录：

1. 环境变量 `OPENCLAW_AGENTS_DIR`
2. `~/.openclaw/agents`
3. `~/.openclaw-project0/agents`
4. `~/.openclaw-default/agents`
5. 任意 `~/.openclaw*/agents` 通配符匹配

**命令行参数**

```
python3 server.py [选项]

  -p, --port 端口     监听端口（默认：7788）
      --host 地址     绑定地址（默认：127.0.0.1；局域网访问用 0.0.0.0）
  -d, --dir  路径     OpenClaw agents 目录（不填则自动检测）
```

**环境变量方式**

```bash
OPENCLAW_AGENTS_DIR=~/.my-openclaw/agents python3 server.py
```

### 项目结构

```
agent-monitor/
├── server.py     # HTTP 服务器 + 数据层（仅标准库，约 200 行）
├── index.html    # React 18 仪表盘（单文件，CDN 依赖）
├── docs/
│   ├── screenshot-light.png
│   └── screenshot-dark.png
├── .gitignore
└── README.md
```

---

<div align="center">
  <sub>Made with 🪼 for the OpenClaw community · MIT License</sub>
</div>
