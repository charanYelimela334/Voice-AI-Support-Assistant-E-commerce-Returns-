# 🎙️ Voice AI Assistant

A **production-style Voice AI pipeline** that listens to your voice, understands your intent, retrieves relevant data, generates a natural language response using an LLM, and speaks the answer back to you.

---

## 🚀 Project Agenda

This project demonstrates a complete end-to-end **Voice AI system** for an e-commerce support use-case. It is designed to:

- Accept voice input from the microphone
- Convert speech to text using Groq's **Whisper Large v3** ASR model
- Detect the user's **intent** (order tracking, returns, refunds)
- Retrieve relevant **structured data** (orders, policies)
- Generate a natural, conversational **LLM response** using Groq's **LLaMA 3.1**
- Speak the response back using **Text-to-Speech (TTS)**

This is not a toy demo — it follows **real-world AI system architecture** used in production voice assistants.

---

## 🧠 Pipeline Architecture

```
🎤 Microphone
     │
     ▼
🔊 Audio Recording (sounddevice)
     │
     ▼
📝 ASR — Groq Whisper Large v3
     │  (Speech → Text)
     ▼
🎯 Intent Detection (rule-based)
     │  order_tracking | return_policy | refund_policy | unknown
     ▼
📦 Data Retrieval (orders.json / policies.json)
     │  Fetch relevant context
     ▼
🤖 LLM — Groq LLaMA 3.1 8B Instant
     │  (Context + Query → Natural Language Response)
     ▼
🔈 TTS — pyttsx3
     │  (Text → Speech → response.mp3)
     ▼
🖥️ Console Output + Audio File
```

---

## 🏗️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Audio Recording | `sounddevice` + `scipy` | Capture mic input as WAV |
| ASR (Speech-to-Text) | `Groq` — `whisper-large-v3` | Cloud-based transcription |
| Intent Detection | Custom Python regex | Classify user query type |
| Data Retrieval | JSON files | Fetch order/policy context |
| LLM | `Groq` — `llama-3.1-8b-instant` | Generate natural responses |
| TTS (Text-to-Speech) | `pyttsx3` | Offline speech synthesis |
| Env Management | `python-dotenv` | Secure API key handling |

---

## 📁 Project Structure

```
voice-ai-assistant/
│
├── main.py                    # Entry point — full pipeline
│
├── orders.json                # Sample order data
├── policies.json              # Return & refund policies
│
├── .env                       # API keys (not committed)
├── requirements.txt           # Python dependencies
│
└── app/
    ├── asr/
    │   ├── recorder.py        # Mic recording (sounddevice)
    │   ├── groq_service.py    # Groq Whisper ASR
    │   └── whisper_service.py # Local Whisper (alternative)
    │
    ├── core/
    │   ├── assistant.py       # Intent detection + data retrieval
    │   └── llm_service.py     # Groq LLM response generation
    │
    └── tts/
        └── tts_service.py     # pyttsx3 Text-to-Speech
```

---

## ⚙️ Setup — Step by Step

### Step 1: Clone the Repository

```bash
git clone https://github.com/your-username/voice-ai-assistant.git
cd voice-ai-assistant
```

### Step 2: Create and Activate a Virtual Environment

```bash
# Create venv
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install sounddevice scipy numpy groq python-dotenv pyttsx3
```

> **Note:** If you want to use the local Whisper fallback instead of Groq ASR:
> ```bash
> pip install openai-whisper
> ```

### Step 4: Get Your Groq API Key

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Navigate to **API Keys** → **Create API Key**
4. Copy your key

### Step 5: Create the `.env` File

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> ⚠️ Never commit this file. Add `.env` to your `.gitignore`.

### Step 6: Review the Data Files

**`orders.json`** — contains customer order records:

```json
[
  {
    "order_id": "ORD123",
    "user_id": "U1",
    "status": "delivered",
    "item": "Wireless Headphones",
    "delivery_date": "2026-03-20",
    "return_window_days": 7
  },
  {
    "order_id": "887",
    "user_id": "U1",
    "status": "in_transit",
    "item": "Running Shoes",
    "expected_delivery": "2026-03-30"
  }
]
```

**`policies.json`** — contains store return/refund policies:

```json
{
  "returns": {
    "allowed": true,
    "window_days": 7,
    "conditions": ["Item must be unused", "Original packaging required"]
  },
  "refunds": {
    "method": "original payment method",
    "processing_time_days": 5
  }
}
```

### Step 7: Run the Assistant

```bash
python main.py
```

---

## 💬 Example Queries & Outputs

### 🔍 Query 1: Order Tracking

**Say:** `"Where is my order ORD123?"`

```
🎤 Recording... Speak now
✅ Saved recording as input.wav
📝 Transcribed: Where is my order ORD123?
🤖 Response: Your order ORD123 for Wireless Headphones was delivered on 2026-03-20.
🔈 Audio saved as: response.mp3
```

---

### 🔍 Query 2: In-Transit Order (Numeric ID)

**Say:** `"Where is my order 887?"`

```
📝 Transcribed: Where is my order 887?
🤖 Response: Your order 887 for Running Shoes is currently in transit and is expected to arrive by 2026-03-30.
🔈 Audio saved as: response.mp3
```

---

### 🔍 Query 3: Return Policy

**Say:** `"I want to return a product."`

```
📝 Transcribed: I want to return a product.
🤖 Response: You're eligible to return the product. The return window is active for 7 days.
             To initiate the return, please ensure the item is unused and in its original packaging.
🔈 Audio saved as: response.mp3
```

---

### 🔍 Query 4: Refund Policy

**Say:** `"What is the refund policy?"`

```
📝 Transcribed: What is the refund policy?
🤖 Response: Refunds are processed to your original payment method within 5 business days.
🔈 Audio saved as: response.mp3
```

---

### 🔍 Query 5: Unknown / Out-of-Scope

**Say:** `"Tell me a joke."`

```
📝 Transcribed: Tell me a joke.
🤖 Response: I can only help with orders, returns, and refunds. I don't have information on that topic.
🔈 Audio saved as: response.mp3
```

---

## 🧩 Key Code Snippets

### Audio Recording (`app/asr/recorder.py`)

```python
import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

class AudioRecorder:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def record(self, duration=5, filename="input.wav"):
        print("🎤 Recording... Speak now")
        audio = sd.rec(int(duration * self.sample_rate),
                       samplerate=self.sample_rate, channels=1, dtype=np.int16)
        sd.wait()
        write(filename, self.sample_rate, audio)
        print(f"✅ Saved recording as {filename}")
        return filename
```

### Groq ASR (`app/asr/groq_service.py`)

```python
from groq import Groq
import os

class GroqASRService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def transcribe(self, audio_path):
        with open(audio_path, "rb") as audio_file:
            transcription = self.client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3"
            )
        return transcription.text
```

### Intent + Retrieval (`app/core/assistant.py`)

```python
def detect_intent(self, text):
    text = text.lower()
    if "order" in text:   return "order_tracking"
    elif "return" in text: return "return_policy"
    elif "refund" in text: return "refund_policy"
    else:                  return "unknown"

def extract_order_id(self, text):
    # Match ORD-prefixed IDs e.g. ORD123
    match = re.search(r'ORD\d+', text, re.IGNORECASE)
    if match:
        return match.group(0).upper()
    # Match plain numeric IDs against actual order data
    numbers = re.findall(r'\d+', text)
    all_order_ids = [o["order_id"] for o in self.orders]
    for num in numbers:
        if num in all_order_ids: return num
        if f"ORD{num}" in all_order_ids: return f"ORD{num}"
    return None
```

### LLM Response Generation (`app/core/llm_service.py`)

```python
from groq import Groq

class LLMService:
    def __init__(self):
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    def generate_response(self, user_query, context_data):
        prompt = f"""
You are an e-commerce support assistant.
User query: {user_query}
Available data: {context_data}
Rules:
- Answer ONLY using the data provided
- Be concise and clear
- If data is missing, say you don't know
"""
        response = self.client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[{"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
```

### Text-to-Speech (`app/tts/tts_service.py`)

```python
import pyttsx3

class TTSService:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text, filename="response.mp3"):
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()
        return filename
```

---

## 🔑 Requirements

```
sounddevice
scipy
numpy
groq
python-dotenv
pyttsx3
openai-whisper   # optional, for local fallback
```

Generate a `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

## 🌱 Future Improvements

- [ ] **Continuous loop** — keep listening instead of one-shot recording
- [ ] **Multi-turn conversation** — maintain chat history for context
- [ ] **User authentication** — support multiple user IDs
- [ ] **Real database** — replace JSON files with PostgreSQL/SQLite
- [ ] **Groq TTS** — replace pyttsx3 with a higher-quality cloud TTS
- [ ] **Wake word detection** — activate only on "Hey Assistant"
- [ ] **Streaming responses** — stream LLM output in real time

---

## 🛡️ Security Notes

- Store your `GROQ_API_KEY` only in `.env` — never hardcode it
- Add `.env` to `.gitignore` before pushing to GitHub
- Rotate your API key immediately if accidentally exposed

---

## 📄 License

MIT License — free to use, modify, and distribute.
