# 🪼 Agent Monitor

A lightweight, zero-dependency dashboard for monitoring [OpenClaw](https://openclaw.ai) multi-agent setups in real time.

![screenshot placeholder](docs/screenshot.png)

---

## Features

- **Live status** — Running / Idle / Offline for every agent
- **Token & cost tracking** — Aggregated across all sessions
- **Active subagents** — See spawned child agents at a glance
- **Current task** — Latest task label per agent
- **Dark mode + multi-language** — ZH / EN / JA, persisted in localStorage
- **Neumorphic UI** — Soft, tactile design with a 🪼 that bounces when you click it
- **Zero dependencies** — Pure Python 3.8+ stdlib + React 18 via CDN

---

## Quickstart

```bash
# 1. Clone
git clone https://github.com/YOUR_USERNAME/agent-monitor.git
cd agent-monitor

# 2. Run (auto-detects your OpenClaw agents directory)
python3 server.py

# 3. Open in browser
open http://localhost:7788
```

That's it. No `pip install`, no Node.js, no config files.

---

## Requirements

| Requirement | Version |
|-------------|---------|
| Python      | 3.8+    |
| OpenClaw    | any     |
| Browser     | Modern (Chrome / Firefox / Safari / Edge) |

---

## Configuration

### Auto-detection

The server searches for your OpenClaw agents directory in this order:

1. `OPENCLAW_AGENTS_DIR` environment variable
2. `~/.openclaw/agents`
3. `~/.openclaw-project0/agents`
4. `~/.openclaw-default/agents`
5. Any `~/.openclaw*/agents` glob match

### CLI flags

```
python3 server.py [options]

  -p, --port PORT     Port to listen on (default: 7788)
      --host HOST     Bind address (default: 127.0.0.1; use 0.0.0.0 for LAN access)
  -d, --dir  PATH     Explicit path to OpenClaw agents directory
```

### Environment variable

```bash
OPENCLAW_AGENTS_DIR=~/.my-openclaw/agents python3 server.py
```

---

## Project Structure

```
agent-monitor/
├── server.py     # Python HTTP server + data layer (stdlib only)
└── index.html    # React 18 dashboard (single file, CDN deps)
```

---

## Roadmap

- [x] Phase 1 — Live status dashboard
- [x] Phase 1 — Dark mode & i18n (ZH/EN/JA)
- [ ] Phase 2 — Pause / Stop agent sessions
- [ ] Phase 2 — Live log drawer (transcript JSONL)
- [ ] Phase 3 — macOS menu bar app (Tauri)

---

## Contributing

PRs welcome. Keep it zero-dependency on the server side.

---

## License

MIT
