# 🎙️ V2V Interview Agent (Voice-to-Voice AI)

An end-to-end **real-time Voice-to-Voice AI Interview Agent** that listens, thinks, and speaks back — all in real time.  
Built using **Deepgram (STT + TTS)**, **Groq LLM**, **FastAPI WebSockets**, and a **browser-based frontend**.

> 🎧 Speak → 🧠 AI Thinks → 🔊 AI Speaks  
No buttons. No delays. Just conversation.

---

## 🚀 Features

✅ Real-time **speech-to-text** using Deepgram Nova-2  
✅ Ultra-fast **LLM responses** via Groq (LLaMA 3)  
✅ Natural **AI voice output** (Deepgram Aura)  
✅ **WebSocket-based streaming** (low latency)  
✅ Works in **Terminal mode** and **Browser mode**  
✅ Clean modular architecture (STT · LLM · TTS)

---

## 🧠 System Architecture


Browser Mic 🎤
 → 
WebSocket (Raw PCM Audio)
 → 
Deepgram STT (Live)
 → 
Groq LLM (Interview Brain)
 → 
Deepgram TTS (Aura Voice)
 → 
WebSocket Audio Stream
 → 
Browser Speaker 🔊


---

## 🗂️ Project Structure


├── server.py # FastAPI WebSocket server (Browser mode)

├── main.py # Terminal-based V2V agent

├── index.html # Frontend UI (Mic + Audio playback)

│

├── src/

│ ├── brain/

│ │ └── llm_agent.py # LLM logic (Groq / OpenAI)

│ ├── transcription/

│ │ └── deepgram_stt.py # Live Speech-to-Text

│ └── audio/

│ └── tts_engine.py # Text-to-Speech (Deepgram Aura)

│

├── .env # API keys

└── README.md



---

## 🔑 Requirements

- Python **3.9+**
- A microphone 🎤
- Internet connection 🌐

### API Keys Needed
Create a `.env` file:

```env
DEEPGRAM_API_KEY=your_deepgram_key
GROQ_API_KEY=your_groq_key
# Optional:
OPENAI_API_KEY=your_openai_key


📦 Installation

git clone https://github.com/hiteshjha24/AI-Interview-Agent.git
cd AI-Interview-Agent
pip install -r requirements.txt



