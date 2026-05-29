# ◈ NEXUS AI — Futuristic Virtual Assistant

A Python-based AI desktop assistant with a neon-glass UI, animated avatar,
voice interaction, and dual AI backends (TinyLlama local + OpenRouter cloud).

---

## ✨ Features

| Feature | Details |
|---|---|
| 🤖 Dual AI backends | TinyLlama via Ollama (free, local) + OpenRouter (GPT-3.5/4) |
| 🎙 Voice I/O | Speech recognition + pyttsx3 TTS synthesis |
| 🎨 Animated avatar | Blinking eyes, talking mouth, mood-reactive colours |
| 💬 Continuous chat | Memory-based multi-turn context (last 10 turns) |
| 🌊 Wave animations | Live header wave + voice visualizer bars |
| 😄 Dynamic moods | 8 mood states with icons & colour shifts |
| ⌨️ Typing indicator | Animated dots while NEXUS thinks |
| ⚡ Latency display | Shows response time per message |
| 🌙 Dark neon theme | Fully dark, neon-cyan/green palette, Courier font |

---

## 🚀 Quick Start

### 1 — Install Python dependencies

```bash
pip install -r requirements.txt
```

> **pyaudio** can be tricky on some platforms:
> - **Windows**: `pip install pyaudio` usually works
> - **macOS**: `brew install portaudio && pip install pyaudio`
> - **Linux**: `sudo apt install portaudio19-dev && pip install pyaudio`

### 2 — Set up environment variables

A `.env` file has been created in the project root.
Open `.env` and update the API key if needed.

```bash
# .env file (KEEP THIS SECURE - DO NOT COMMIT)
OPENROUTER_API_KEY=sk-or-your-key-here
OPENROUTER_URL=https://openrouter.ai/api/v1/chat/completions
OPENROUTER_MODEL=openai/gpt-3.5-turbo
OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=tinyllama
```

If you prefer not to use `.env`, you can still set `OPENROUTER_API_KEY` as a normal environment variable.

### 3 — (Optional) Set up TinyLlama for local AI

1. Install [Ollama](https://ollama.ai)
2. Pull the model: `ollama pull tinyllama`
3. Ollama starts automatically on `localhost:11434`

### 4 — Run NEXUS

```bash
python assistant.py
```

---

## 🎛 Backend Priority

NEXUS tries backends in this order:

```
OpenRouter (if API key set)  →  TinyLlama via Ollama  →  Built-in fallback
```

The badge in the top-right of the window shows which backend is active.

---

## 🎙 Voice Usage

1. Click the **🎙** microphone button to start listening
2. Speak your message — NEXUS captures ~12 seconds
3. Your speech is transcribed by Google (free, no key needed)
4. Enable **Voice I/O** checkbox to have NEXUS also speak replies aloud

---

## 🖥 UI Layout

```
┌─────────────────────────────────────────────────────────┐
│  ◈ NEXUS  · AI ASSISTANT              ⚡ OpenRouter  ~~~│  ← header + wave
├────────────┬────────────────────────────────────────────┤
│  [Avatar]  │                                            │
│  😄 HAPPY  │   Chat bubbles with timestamps             │
│            │   User bubbles right-aligned               │
│ [VIZ BARS] │   NEXUS bubbles left-aligned               │
│            │                                            │
│ MEMORY: 3  │                                            │
│ 🎙 Voice   │                                            │
├────────────┴────────────────────────────────────────────┤
│  🎙  [ Type your message... ]          [⟳] [SEND ▶]   │  ← input row
├─────────────────────────────────────────────────────────┤
│  ◈ NEXUS ONLINE — Ready                        ⚡ 0.82s │  ← status bar
└─────────────────────────────────────────────────────────┘
```

---

## 🛠 Customisation

Edit `assistant.py` to change:
- `OPENROUTER_MODEL` — swap to `openai/gpt-4o`, `anthropic/claude-3-haiku`, etc.
- `OLLAMA_MODEL` — swap to `mistral`, `phi3`, `llama3`, etc.
- `SYSTEM_PROMPT` — change NEXUS's personality
- `NexusUI.C` dict — retheme all colours instantly

---

## 📦 Dependency Summary

| Package | Purpose | Required? |
|---|---|---|
| `requests` | HTTP to OpenRouter / Ollama | ✅ Yes |
| `pyttsx3` | Text-to-speech output | Optional |
| `SpeechRecognition` | Mic → text | Optional |
| `pyaudio` | Microphone hardware driver | Optional |
| `tkinter` | GUI (ships with Python) | ✅ Yes |

All optional packages degrade gracefully — the app runs fine without them.
