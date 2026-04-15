#!/usr/bin/env python3
"""
Agent Monitor — One-file dashboard for OpenClaw multi-agent setups.

Usage:
    python3 server.py                        # auto-detect OpenClaw agents dir
    python3 server.py --port 8080            # custom port
    python3 server.py --dir ~/.openclaw/agents  # explicit agents dir
    python3 server.py --host 0.0.0.0         # expose to LAN

Then open http://localhost:7788 in your browser.
No dependencies beyond Python 3.8+ stdlib.
"""

import json
import os
import sys
import time
import argparse
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime, timezone
from pathlib import Path

# --------------------------------------------------------------------------- #
#  Config                                                                       #
# --------------------------------------------------------------------------- #

DEFAULT_PORT = 7788
DEFAULT_HOST = "127.0.0.1"
CORS_ORIGIN  = "*"

# Ordered list of candidate agent directories (first match wins)
AGENTS_DIR_CANDIDATES = [
    "~/.openclaw/agents",
    "~/.openclaw-project0/agents",
    "~/.openclaw-default/agents",
]

# Script directory — used to locate index.html
SCRIPT_DIR = Path(__file__).parent.resolve()


def find_agents_dir() -> str:
    """
    Resolve the OpenClaw agents directory in priority order:
    1. OPENCLAW_AGENTS_DIR environment variable
    2. Known candidate paths
    3. Glob scan of ~/.openclaw*/agents
    4. Fallback: ~/.openclaw/agents (may not exist yet)
    """
    # 1. Env override
    env = os.environ.get("OPENCLAW_AGENTS_DIR", "").strip()
    if env:
        p = os.path.expanduser(env)
        if os.path.isdir(p):
            return p

    # 2. Candidate paths
    for candidate in AGENTS_DIR_CANDIDATES:
        p = os.path.expanduser(candidate)
        if os.path.isdir(p):
            return p

    # 3. Glob scan
    matches = sorted(Path.home().glob(".openclaw*/agents"))
    if matches:
        return str(matches[0])

    # 4. Fallback
    return os.path.expanduser("~/.openclaw/agents")


# --------------------------------------------------------------------------- #
#  Data Layer                                                                   #
# --------------------------------------------------------------------------- #

def load_sessions_for_agent(agent_name: str, agents_dir: str) -> dict:
    agent_dir = os.path.join(agents_dir, agent_name)
    sessions_file = os.path.join(agent_dir, "sessions", "sessions.json")
    if not os.path.exists(sessions_file):
        return {}
    try:
        with open(sessions_file, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def compute_status(session: dict) -> str:
    """Derive agent status from session fields."""
    status = session.get("status", "")
    if status == "running":
        return "running"
    if status in ("idle", "done", "completed"):
        return "idle"
    # Infer from recency of updatedAt
    updated_ms = session.get("updatedAt", 0)
    age = time.time() - (updated_ms / 1000)
    if age < 30:
        return "running"
    if age < 300:
        return "idle"
    return "offline"


def extract_last_task(sessions: dict) -> str:
    """Extract the most-recent meaningful task label."""
    labeled = [(k, v) for k, v in sessions.items() if v.get("label")]
    if labeled:
        labeled.sort(key=lambda x: x[1].get("updatedAt", 0), reverse=True)
        return labeled[0][1].get("label", "")
    return ""


def get_main_session(sessions: dict):
    """Return the primary (non-subagent) session, or the most recent."""
    for key, session in sessions.items():
        if "subagent" not in key:
            return session
    if sessions:
        return sorted(sessions.values(), key=lambda s: s.get("updatedAt", 0), reverse=True)[0]
    return None


def build_agent_data(agent_name: str, agents_dir: str) -> dict:
    all_sessions = load_sessions_for_agent(agent_name, agents_dir)

    if not all_sessions:
        return {
            "id":          agent_name,
            "name":        agent_name.capitalize(),
            "status":      "offline",
            "currentTask": None,
            "lastSeen":    None,
            "sessions":    {"total": 0, "subagents": 0, "activeSubagents": []},
            "usage":       {"inputTokens": 0, "outputTokens": 0,
                            "totalTokens": 0, "estimatedCostUsd": 0},
            "model":       None,
        }

    main_session      = get_main_session(all_sessions)
    all_sessions_list = list(all_sessions.values())

    status = compute_status(main_session) if main_session else "offline"

    total_input  = sum(s.get("inputTokens",       0) for s in all_sessions_list)
    total_output = sum(s.get("outputTokens",      0) for s in all_sessions_list)
    total_tokens = sum(s.get("totalTokens",       0) for s in all_sessions_list)
    total_cost   = sum(s.get("estimatedCostUsd",  0) for s in all_sessions_list)

    last_ms = max((s.get("updatedAt", 0) for s in all_sessions_list), default=0)
    last_seen = (
        datetime.fromtimestamp(last_ms / 1000, tz=timezone.utc).isoformat()
        if last_ms else None
    )

    subagent_count = sum(1 for k in all_sessions if "subagent" in k)

    current_task = extract_last_task(all_sessions)
    if not current_task and main_session:
        current_task = main_session.get("lastTask") or None

    model = None
    if main_session:
        model = main_session.get("model") or main_session.get("modelOverride")

    active_subagents = [
        {
            "sessionId": s.get("sessionId", ""),
            "label":     s.get("label", k.split(":")[-1][:30]),
            "model":     s.get("model", ""),
            "startedAt": s.get("startedAt"),
            "updatedAt": s.get("updatedAt"),
        }
        for k, s in all_sessions.items()
        if "subagent" in k and s.get("status") == "running"
    ]

    return {
        "id":          agent_name,
        "name":        agent_name.capitalize(),
        "status":      status,
        "currentTask": current_task or None,
        "lastSeen":    last_seen,
        "sessions": {
            "total":          len(all_sessions_list),
            "subagents":      subagent_count,
            "activeSubagents": active_subagents,
        },
        "usage": {
            "inputTokens":      total_input,
            "outputTokens":     total_output,
            "totalTokens":      total_tokens,
            "estimatedCostUsd": round(total_cost, 6),
        },
        "model": model,
    }


def get_all_agents(agents_dir: str) -> list:
    if not os.path.isdir(agents_dir):
        return []
    names = sorted(
        d for d in os.listdir(agents_dir)
        if os.path.isdir(os.path.join(agents_dir, d))
    )
    return [build_agent_data(name, agents_dir) for name in names]


# --------------------------------------------------------------------------- #
#  HTTP Handler                                                                 #
# --------------------------------------------------------------------------- #

class Handler(BaseHTTPRequestHandler):
    agents_dir: str = ""   # set at startup

    def log_message(self, format, *args):
        pass  # suppress default access log

    def send_cors(self):
        self.send_header("Access-Control-Allow-Origin",  CORS_ORIGIN)
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_cors()
        self.end_headers()

    def do_GET(self):
        # ── API: agent list ─────────────────────────────────────────────────
        if self.path == "/api/agents":
            agents  = get_all_agents(self.agents_dir)
            payload = {
                "agents":     agents,
                "serverTime": datetime.now(tz=timezone.utc).isoformat(),
                "agentsDir":  self.agents_dir,
            }
            body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type",   "application/json; charset=utf-8")
            self.send_header("Content-Length", len(body))
            self.send_cors()
            self.end_headers()
            self.wfile.write(body)
            return

        # ── Health check ────────────────────────────────────────────────────
        if self.path == "/health":
            self.send_response(200)
            self.send_cors()
            self.end_headers()
            self.wfile.write(b"ok")
            return

        # ── Serve index.html (root or any unknown path) ─────────────────────
        index = SCRIPT_DIR / "index.html"
        if not index.exists():
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"index.html not found")
            return

        body = index.read_bytes()
        self.send_response(200)
        self.send_header("Content-Type",   "text/html; charset=utf-8")
        self.send_header("Content-Length", len(body))
        self.end_headers()
        self.wfile.write(body)


# --------------------------------------------------------------------------- #
#  Entry Point                                                                  #
# --------------------------------------------------------------------------- #

def parse_args():
    p = argparse.ArgumentParser(
        description="Agent Monitor — OpenClaw multi-agent dashboard"
    )
    p.add_argument("--port", "-p", type=int,  default=DEFAULT_PORT,
                   help=f"Port to listen on (default: {DEFAULT_PORT})")
    p.add_argument("--host",       type=str,  default=DEFAULT_HOST,
                   help=f"Host to bind (default: {DEFAULT_HOST}; use 0.0.0.0 for LAN)")
    p.add_argument("--dir",  "-d", type=str,  default=None,
                   help="Path to OpenClaw agents directory (auto-detected if omitted)")
    return p.parse_args()


def main():
    args = parse_args()

    agents_dir = os.path.expanduser(args.dir) if args.dir else find_agents_dir()
    Handler.agents_dir = agents_dir

    server = HTTPServer((args.host, args.port), Handler)
    url    = f"http://localhost:{args.port}"

    print(f"")
    print(f"  🪼  Agent Monitor")
    print(f"  ─────────────────────────────────────────")
    print(f"  Dashboard  →  {url}")
    print(f"  API        →  {url}/api/agents")
    print(f"  Agents dir →  {agents_dir}")
    if not os.path.isdir(agents_dir):
        print(f"")
        print(f"  ⚠️  Agents dir not found — check --dir or OPENCLAW_AGENTS_DIR")
    print(f"  ─────────────────────────────────────────")
    print(f"  Press Ctrl+C to stop")
    print(f"")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  [Agent Monitor] Stopped.")


if __name__ == "__main__":
    main()
