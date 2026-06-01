#!/usr/bin/env python3
"""
ops-server.py — local Flask server that exposes the Venture Community Workspace ops agent for the team dashboard.

Backend selection (auto-detected):
    1. If ANTHROPIC_API_KEY is set -> uses Anthropic API
    2. Else if Ollama is reachable at localhost:11434 -> uses local LLM (free)
    3. Else returns 503 with setup instructions

Run:
    pip install flask flask-cors anthropic requests
    # Local/free path, no API key:
    brew install ollama && ollama pull llama3.1:8b && ollama serve &
    python3 ops-server.py
    # Optional cloud path: set ANTHROPIC_API_KEY before running for direct Claude API chat.

Endpoints:
    GET  /health    -> { ok, backend, model, ... }
    POST /chat      -> { "message": "..." } -> { "reply": "...", "history_len": N }
    POST /upload    -> { "title": "...", "content": "..." } -> appended to context
    GET  /history   -> last 20 messages
    POST /reset     -> wipe history (uploads kept)
    GET  /context   -> what's currently loaded
"""

import os
import json
import datetime
from pathlib import Path

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS

DASH_ROOT = Path(__file__).resolve().parents[1]
OPS_MD    = DASH_ROOT / "agent-config" / "workspace-framework-ops.md"
HISTORY   = DASH_ROOT / "scripts" / "ops-history.json"
UPLOADS   = DASH_ROOT / "scripts" / "ops-uploads.json"

ANTHROPIC_MODEL = "claude-sonnet-4-6"
OLLAMA_URL     = "http://localhost:11434"
OLLAMA_MODEL   = os.environ.get("OLLAMA_MODEL", "llama3.1:8b")

DEFAULT_SYSTEM_PROMPT = """You are the Venture Community Workspace ops agent for the team dashboard.

You run the full event-ops pipeline (pull snapshot, gmail-reader, telegram-reader, classifier, approval gate, sheet writer, refresh snapshot), trigger venue-workstream runs, build approval digests in Telegram, watch Gmail replies, and compose the weekly Monday digest.

Hard rules:
- Never send any email. Drafts only; humans send.
- Never write to the Events Master Sheet without explicit Telegram approval.
- Never update Relay CRM (read-only adapter, propose-only writes).
- Never rebuild the newsletter v11 Apps Script (route around it).
- Use Haiku for extraction and relay. Sonnet only for judgment. Never default to Opus.

Voice: operator-to-operator, no em dashes, no buzzwords, no hedging. Confident, specific.
"""

def detect_backend():
    if os.environ.get("ANTHROPIC_API_KEY"):
        try:
            from anthropic import Anthropic
            return "anthropic", Anthropic(), ANTHROPIC_MODEL
        except Exception:
            pass
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=1)
        if r.ok:
            return "ollama", None, OLLAMA_MODEL
    except Exception:
        pass
    return "none", None, None

BACKEND, ANTHROPIC_CLIENT, MODEL = detect_backend()

app = Flask(__name__)
CORS(app)

def load_ops_prompt() -> str:
    if not OPS_MD.exists():
        return DEFAULT_SYSTEM_PROMPT
    raw = OPS_MD.read_text()
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            return parts[2].strip()
    return raw.strip()

SYSTEM_PROMPT = load_ops_prompt()

def load_json(path: Path, default):
    if path.exists():
        try:
            return json.loads(path.read_text())
        except Exception:
            return default
    return default

def save_json(path: Path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2))

history = load_json(HISTORY, [])
uploads = load_json(UPLOADS, [])

def build_system_text() -> str:
    base = SYSTEM_PROMPT
    if uploads:
        upload_text = "\n\n".join(
            f"<upload title=\"{u['title']}\" at=\"{u['added_at']}\">\n{u['content']}\n</upload>"
            for u in uploads
        )
        base += f"\n\n<team_uploads>\n{upload_text}\n</team_uploads>"
    return base

def chat_anthropic(user_msg: str):
    system_blocks = [{"type": "text", "text": SYSTEM_PROMPT, "cache_control": {"type": "ephemeral"}}]
    if uploads:
        upload_text = "\n\n".join(
            f"<upload title=\"{u['title']}\" at=\"{u['added_at']}\">\n{u['content']}\n</upload>"
            for u in uploads
        )
        system_blocks.append({"type": "text", "text": f"<team_uploads>\n{upload_text}\n</team_uploads>", "cache_control": {"type": "ephemeral"}})
    messages = [{"role": m["role"], "content": m["content"]} for m in history[-20:]]
    messages.append({"role": "user", "content": user_msg})
    resp = ANTHROPIC_CLIENT.messages.create(
        model=MODEL, max_tokens=4096,
        system=system_blocks, messages=messages,
    )
    reply = "".join(b.text for b in resp.content if hasattr(b, "text"))
    return reply, {
        "input":  resp.usage.input_tokens,
        "output": resp.usage.output_tokens,
        "cache_read":   getattr(resp.usage, "cache_read_input_tokens", 0),
        "cache_create": getattr(resp.usage, "cache_creation_input_tokens", 0),
    }

def chat_ollama(user_msg: str):
    system_text = build_system_text()
    messages = [{"role": "system", "content": system_text}]
    for m in history[-20:]:
        messages.append({"role": m["role"], "content": m["content"]})
    messages.append({"role": "user", "content": user_msg})
    r = requests.post(
        f"{OLLAMA_URL}/api/chat",
        json={"model": MODEL, "messages": messages, "stream": False, "options": {"temperature": 0.7}},
        timeout=300,
    )
    r.raise_for_status()
    data = r.json()
    reply = data.get("message", {}).get("content", "")
    return reply, {
        "input":  data.get("prompt_eval_count", 0),
        "output": data.get("eval_count", 0),
        "backend": "ollama",
    }

@app.route("/health")
def health():
    return jsonify({
        "ok": BACKEND != "none",
        "backend": BACKEND,
        "model": MODEL,
        "system_prompt_chars": len(SYSTEM_PROMPT),
        "history_len": len(history),
        "uploads": len(uploads),
        "setup_hint": (
            None if BACKEND != "none"
            else "Set ANTHROPIC_API_KEY OR run `brew install ollama && ollama pull llama3.1:8b && ollama serve &`"
        ),
    })

@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(force=True)
    user_msg = (data.get("message") or "").strip()
    if not user_msg:
        return jsonify({"error": "empty message"}), 400
    if BACKEND == "none":
        return jsonify({"error": "no backend available. Set ANTHROPIC_API_KEY or start Ollama (ollama serve)."}), 503

    try:
        if BACKEND == "anthropic":
            reply, tokens = chat_anthropic(user_msg)
        else:
            reply, tokens = chat_ollama(user_msg)
    except Exception as e:
        return jsonify({"error": str(e), "backend": BACKEND}), 500

    now = datetime.datetime.utcnow().isoformat() + "Z"
    history.append({"role": "user",      "content": user_msg, "at": now})
    history.append({"role": "assistant", "content": reply,    "at": now})
    save_json(HISTORY, history)

    return jsonify({"reply": reply, "history_len": len(history), "backend": BACKEND, "model": MODEL, "tokens": tokens})

@app.route("/upload", methods=["POST"])
def upload():
    data = request.get_json(force=True)
    title   = data.get("title", "untitled").strip()
    content = data.get("content", "").strip()
    if not content:
        return jsonify({"error": "empty content"}), 400
    uploads.append({
        "title":    title,
        "content":  content,
        "added_at": datetime.datetime.utcnow().isoformat() + "Z",
    })
    save_json(UPLOADS, uploads)
    return jsonify({"ok": True, "uploads": len(uploads)})

@app.route("/uploads", methods=["GET"])
def list_uploads():
    return jsonify([{"title": u["title"], "added_at": u["added_at"], "chars": len(u["content"])} for u in uploads])

@app.route("/uploads/<int:idx>", methods=["DELETE"])
def delete_upload(idx):
    if 0 <= idx < len(uploads):
        uploads.pop(idx)
        save_json(UPLOADS, uploads)
        return jsonify({"ok": True})
    return jsonify({"error": "out of range"}), 404

@app.route("/history")
def get_history():
    return jsonify(history[-20:])

@app.route("/reset", methods=["POST"])
def reset():
    global history
    history = []
    save_json(HISTORY, history)
    return jsonify({"ok": True})

@app.route("/context")
def context_view():
    return jsonify({
        "system_prompt_path": str(OPS_MD),
        "system_prompt_preview": SYSTEM_PROMPT[:500] + ("..." if len(SYSTEM_PROMPT) > 500 else ""),
        "uploads": [{"title": u["title"], "added_at": u["added_at"]} for u in uploads],
        "history_count": len(history),
        "model": MODEL,
    })

if __name__ == "__main__":
    print(f"[ops-server] system prompt: {len(SYSTEM_PROMPT)} chars (ops prompt exists: {OPS_MD.exists()})")
    print(f"[ops-server] history: {len(history)} msgs / uploads: {len(uploads)}")
    print(f"[ops-server] backend: {BACKEND} / model: {MODEL or '(none)'}")
    if BACKEND == "none":
        print(f"[ops-server] NO BACKEND - set ANTHROPIC_API_KEY or run `ollama serve`")
    print(f"[ops-server] running at http://localhost:5059")
    app.run(host="127.0.0.1", port=5059, debug=False)
