# 🎙️ AI Voice Assistant

A conversational AI voice assistant built with **FastAPI**, featuring real-time speech-to-text, intelligent responses powered by **Google's Gemini AI**, and natural text-to-speech conversion using **Murf AI**.

---

## ✨ Features

- **🎤 Real-time Voice Recording** – Click-to-talk interface with visual feedback  
- **🧠 Intelligent Conversations** – Powered by Google Gemini AI with conversation history  
- **🗣️ Natural Speech Output** – High-quality voice synthesis using Murf AI  
- **💬 Session Management** – Maintains conversation context across interactions  
- **🎨 Modern UI** – Clean, responsive interface with recording animations  
- **🔄 Auto-play Responses** – Seamless audio playback without manual controls  

---

## 🏗️ Architecture

```plaintext
┌────────────────────────-─┐
│        Frontend          │
│  (HTML, JS, Bootstrap)   │
│ ─ Voice UI               │
│ ─ Recording              │
│ ─ Auto-play Responses    │
└───────────▲──────────────┘
            │
            ▼
┌───────────────────────-──┐
│         Backend          │
│        (FastAPI)         │
│ ─ Session Management     │
│ ─ Audio Processing       │
│ ─ API Routes             │
└───────────▲──────────────┘
            │
            ▼
┌─────────────────────-────┐
│        External APIs     │
│ ─ AssemblyAI  (STT)      │
│ ─ Gemini AI   (NLP)      │
│ ─ Murf AI     (TTS)      │
└────────────────────────-─┘
```

---

## 🛠️ Technologies Used

**Backend**
- FastAPI
- Python 3.8+
- AssemblyAI
- Google Gemini AI
- Murf AI
- Jinja2

**Frontend**
- HTML5
- Bootstrap 5
- JavaScript
- Web Audio API

**Additional Tools**
- python-dotenv
- Requests
- Uvicorn

---

## 📋 Prerequisites

- Python 3.8+
- Browser with microphone access
- API keys for:
  - AssemblyAI  
  - Gemini AI  
  - Murf AI  

---

## 🚀 Installation & Setup

1. **Clone the repo**
```bash
git clone https://github.com/mdzaid7817/ai-voice-assistant.git
cd ai-voice-assistant
```

2. **Create a virtual environment**
```bash
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install fastapi uvicorn assemblyai google-generativeai python-dotenv requests jinja2 python-multipart
```

4. **Set environment variables** in `.env`
```
ASSEMBLYAI_API_KEY=your_assemblyai_api_key
GEMINI_API_KEY=your_google_gemini_api_key
MURF_API_KEY=your_murf_api_key
```

5. **Create static and template folders**
```bash
mkdir static templates
```

---

## 🔑 Environment Variables

| Variable             | Description                      | Required |
| -------------------- | -------------------------------- | -------- |
| `ASSEMBLYAI_API_KEY` | API key for speech-to-text       | ✅        |
| `GEMINI_API_KEY`     | API key for conversation AI      | ✅        |
| `MURF_API_KEY`       | API key for text-to-speech       | ✅        |

---

## 🏃 Running the App

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
