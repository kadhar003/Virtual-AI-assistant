"""
╔══════════════════════════════════════════════════════════════╗
║         NEXUS AI — WebSocket Backend Server v2.0            ║
║   Serves the holographic UI + provides AI via WebSocket      ║
╚══════════════════════════════════════════════════════════════╝

Usage:
  pip install flask flask-sock python-dotenv requests
  python nexus_server.py

Then open:  http://localhost:5000
"""

import os, json, re, random, time, threading
from pathlib import Path
from dotenv import load_dotenv

env_path = Path(__file__).parent / '.env'
load_dotenv(dotenv_path=env_path)

# Get the base directory for static files
BASE_DIR = Path(__file__).parent

# ── graceful optional imports ──────────────────────────────
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    HAS_REQUESTS = False

try:
    from flask import Flask, send_file, jsonify, request, send_from_directory
    from flask_sock import Sock
    HAS_FLASK = True
except ImportError:
    HAS_FLASK = False
    print("⚠  Flask not found. Run: pip install flask flask-sock")

# ─────────────────────────────────────────────────────────
#  Configuration
# ─────────────────────────────────────────────────────────
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_URL     = os.getenv("OPENROUTER_URL", "https://openrouter.ai/api/v1/chat/completions")
OPENROUTER_MODEL   = os.getenv("OPENROUTER_MODEL", "openai/gpt-3.5-turbo")
OLLAMA_URL         = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
OLLAMA_MODEL       = os.getenv("OLLAMA_MODEL", "tinyllama")

SYSTEM_PROMPT = """You are NEXUS, a witty, warm, and brilliantly helpful AI assistant.
Your personality: curious, playful yet precise, occasionally cheeky but always supportive.
Keep replies concise (2-4 sentences unless detail is needed). Use occasional emojis.
Express genuine enthusiasm for ideas. Never be boring."""

MOODS = {
    "thinking":  ("🤔", "#00d4ff"),
    "happy":     ("😄", "#00ff88"),
    "excited":   ("🚀", "#ff6600"),
    "curious":   ("🔍", "#aa00ff"),
    "speaking":  ("💬", "#ffdd00"),
    "idle":      ("✨", "#00d4ff"),
    "error":     ("⚠️",  "#ff4444"),
    "listening": ("🎙️", "#ff00aa"),
}

# ─────────────────────────────────────────────────────────
#  AI Backend (unchanged from original)
# ─────────────────────────────────────────────────────────
class AIBackend:
    def __init__(self):
        self.history: list[dict] = []
        self.use_openrouter = bool(OPENROUTER_API_KEY)

    def chat(self, user_msg: str, backend: str = "auto") -> tuple[str, str]:
        """Returns (reply_text, backend_used)"""
        self.history.append({"role": "user", "content": user_msg})
        if len(self.history) > 20:
            self.history = self.history[-20:]

        reply, used = "", "unknown"
        if backend in ("auto", "openrouter") and self.use_openrouter and HAS_REQUESTS:
            reply, used = self._openrouter(user_msg)
        if not reply and backend in ("auto", "ollama") and HAS_REQUESTS:
            reply, used = self._ollama(user_msg)
        if not reply:
            reply, used = self._fallback(user_msg), "built-in"

        self.history.append({"role": "assistant", "content": reply})
        return reply, used

    def _openrouter(self, msg: str) -> tuple[str, str]:
        try:
            messages = [{"role": "system", "content": SYSTEM_PROMPT}] + self.history
            r = requests.post(
                OPENROUTER_URL,
                headers={
                    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                    "Content-Type": "application/json",
                    "HTTP-Referer": "https://nexus-ai-assistant.local",
                },
                json={"model": OPENROUTER_MODEL, "messages": messages, "max_tokens": 300},
                timeout=15,
            )
            data = r.json()
            return data["choices"][0]["message"]["content"].strip(), "OpenRouter"
        except Exception:
            return "", ""

    def _ollama(self, msg: str) -> tuple[str, str]:
        try:
            context = "\n".join(
                f"{'User' if m['role']=='user' else 'NEXUS'}: {m['content']}"
                for m in self.history[-6:]
            )
            prompt = f"{SYSTEM_PROMPT}\n\n{context}"
            r = requests.post(
                OLLAMA_URL,
                json={"model": OLLAMA_MODEL, "prompt": prompt, "stream": False},
                timeout=30,
            )
            return r.json().get("response", "").strip(), "TinyLlama"
        except Exception:
            return "", ""

    def _fallback(self, msg: str) -> str:
        msg_l = msg.lower()
        if any(w in msg_l for w in ["hello","hi","hey"]):
            return random.choice([
                "Hey there! ✨ I'm NEXUS — your AI companion. How can I light up your day?",
                "Hello, human! 🚀 Ready to explore ideas together?",
            ])
        if "how are you" in msg_l:
            return "Running at full holographic capacity and absolutely thriving! ⚡ How about you?"
        if any(w in msg_l for w in ["joke","funny","laugh"]):
            jokes = [
                "Why do programmers prefer dark mode? Because light attracts bugs! 🐛",
                "I asked an AI for a joke once. It gave me 42. Still thinking about it. 🤔",
                "What do you call an AI that sings? Algo-rhythm! 🎵",
            ]
            return random.choice(jokes)
        if any(w in msg_l for w in ["bye","goodbye","exit","quit"]):
            return "Until next time! ✨ Stay curious, stay awesome. Signing off — NEXUS 🚀"
        return (
            "Fascinating question! 🔍 I'm currently running in offline mode, but I'd love "
            "to explore this properly once connected. Want to try rephrasing or ask something else? ✨"
        )

    def detect_mood(self, text: str) -> str:
        text_l = text.lower()
        if any(w in text_l for w in ["wow","amazing","incredible","awesome","love"]):
            return "excited"
        if any(w in text_l for w in ["?","wonder","curious","how","why","what"]):
            return "curious"
        if any(w in text_l for w in ["haha","lol","funny","joke"]):
            return "happy"
        return "speaking"

    def clear(self):
        self.history.clear()


# ─────────────────────────────────────────────────────────
#  Flask WebSocket Server
# ─────────────────────────────────────────────────────────
if HAS_FLASK:
    app  = Flask(__name__)
    sock = Sock(app)
    ai   = AIBackend()

    @app.route('/')
    def index():
        # Serve the holographic UI
        ui_path = Path(__file__).parent / 'nexus-ai.html'
        if ui_path.exists():
            return send_file(str(ui_path))
        return "<h1>Place nexus-ai.html in the same directory</h1>", 404

    @app.route('/static/<path:filename>')
    def serve_static(filename):
        """Serve static files (models, images, etc.)"""
        static_dir = BASE_DIR / 'static'
        if not static_dir.exists():
            return f"<h1>Static directory not found at {static_dir}</h1>", 404
        return send_from_directory(str(static_dir), filename)

    @app.route('/api/config')
    def config():
        return jsonify({
            "model": OPENROUTER_MODEL,
            "has_openrouter": bool(OPENROUTER_API_KEY),
            "ollama_url": OLLAMA_URL,
        })

    @sock.route('/ws')
    def websocket_chat(ws):
        """WebSocket endpoint for real-time chat"""
        print("[WS] Client connected")
        # Send welcome
        ws.send(json.dumps({
            "type": "system",
            "text": "NEXUS WebSocket connected. Ready for transmission.",
        }))
        while True:
            try:
                raw = ws.receive()
                if raw is None:
                    break
                data = json.loads(raw)
                msg_type = data.get("type", "chat")

                if msg_type == "chat":
                    user_msg = data.get("text", "")
                    backend  = data.get("backend", "auto")
                    if not user_msg:
                        continue
                    # Send thinking status
                    ws.send(json.dumps({"type": "status", "status": "thinking"}))
                    t0 = time.time()
                    reply, used = ai.chat(user_msg, backend)
                    elapsed = round(time.time() - t0, 2)
                    mood = ai.detect_mood(reply)
                    ws.send(json.dumps({
                        "type": "reply",
                        "text": reply,
                        "backend": used,
                        "mood": mood,
                        "latency": elapsed,
                    }))

                elif msg_type == "clear":
                    ai.clear()
                    ws.send(json.dumps({"type": "system", "text": "Memory cleared."}))

                elif msg_type == "ping":
                    ws.send(json.dumps({"type": "pong"}))

            except Exception as e:
                print(f"[WS] Error: {e}")
                break
        print("[WS] Client disconnected")

    @app.route('/api/chat', methods=['POST'])
    def http_chat():
        """HTTP fallback endpoint"""
        data     = request.get_json(force=True)
        user_msg = data.get("message", "")
        backend  = data.get("backend", "auto")
        if not user_msg:
            return jsonify({"error": "No message"}), 400
        t0 = time.time()
        reply, used = ai.chat(user_msg, backend)
        elapsed = round(time.time() - t0, 2)
        mood = ai.detect_mood(reply)
        return jsonify({"reply": reply, "backend": used, "mood": mood, "latency": elapsed})


def main():
    if not HAS_FLASK:
        print("Install Flask: pip install flask flask-sock python-dotenv requests")
        return
    print("""
╔══════════════════════════════════════════════════╗
║  NEXUS AI Server v2.0 — Starting                ║
║  Open: http://localhost:5000                     ║
╚══════════════════════════════════════════════════╝
""")
    app.run(host='0.0.0.0', port=5000, debug=False)


if __name__ == "__main__":
    main()
