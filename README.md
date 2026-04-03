# 🎙️ Voice AI Support Assistant — E-commerce Returns

A **production-style Voice AI pipeline** for e-commerce customer support. It listens to your voice, understands your intent, retrieves relevant data, generates a natural language response using an LLM, and speaks the answer back to you.

---

## 🚀 Project Agenda

This project implements a complete end-to-end **Voice AI system** for handling common e-commerce support queries:

- "Where is my order ORD124?"
- "Can I return my headphones?"
- "What is the refund policy?"

It follows **real-world AI system architecture** with each layer independently swappable.

---

## 🧠 Pipeline Architecture

```
🎤 Microphone Input
     │
     ▼
🔊 Audio Recording       →  sounddevice (16kHz WAV)
     │
     ▼
📝 ASR                   →  Groq Whisper Large v3 (Speech → Text)
     │
     ▼
🎯 Intent Detection      →  Keyword/regex classifier
     │                       order_tracking | return_policy | refund_policy | unknown
     ▼
📦 Data Retrieval        →  orders.json / policies.json
     │                       Fetch structured context for the detected intent
     ▼
🤖 LLM                   →  Groq LLaMA 3.1 8B Instant (Context → Response)
     │
     ▼
🔈 TTS                   →  pyttsx3 (Text → Speech → response.wav)
```

---

## 🏗️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Audio Recording | `sounddevice` + `scipy` | Capture mic input as 16kHz WAV |
| ASR (Speech → Text) | Groq `whisper-large-v3` | Cloud-based transcription |
| Intent Detection | Custom Python regex | Classify user query type |
| Data Retrieval | JSON files | Fetch order/policy context |
| LLM | Groq `llama-3.1-8b-instant` | Generate natural language responses |
| TTS (Text → Speech) | `pyttsx3` | Offline speech synthesis |
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
├── .env                       # API keys (never committed)
├── .env.example               # Template for environment setup
├── .gitignore
├── requirements.txt
├── README.md
│
└── app/
    ├── asr/
    │   ├── recorder.py        # Mic recording via sounddevice
    │   ├── groq_service.py    # Groq Whisper ASR (primary)
    │   └── whisper_service.py # Local Whisper (offline fallback)
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
git clone https://github.com/charanYelimela334/Voice-AI-Support-Assistant-E-commerce-Returns-.git
cd Voice-AI-Support-Assistant-E-commerce-Returns-
```

### Step 2: Create and Activate Virtual Environment

```bash
# Create
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

Or manually:

```bash
pip install sounddevice scipy numpy groq python-dotenv pyttsx3
```

### Step 4: Get Your Groq API Key

1. Go to [https://console.groq.com](https://console.groq.com)
2. Sign up / Log in
3. Navigate to **API Keys** → **Create API Key**
4. Copy your key

### Step 5: Configure Environment

```bash
cp .env.example .env
```

Open `.env` and add your key:

```env
GROQ_API_KEY=your_groq_api_key_here
```

> ⚠️ `.env` is in `.gitignore` — it will never be committed.

### Step 6: Run the Assistant

**With microphone (5-second recording):**

```bash
python main.py
```

**Without microphone (text input — works everywhere):**

```bash
python main.py --text "Where is my order ORD124?"
```

---

## 💬 Example Queries & Outputs

### Query 1: Order Tracking — Delivered

```bash
python main.py --text "Where is my order ORD123?"
```

```
💬 Using text input: Where is my order ORD123?
🤖 Response: Your order ORD123 for Wireless Headphones was delivered on 2026-03-20.
🔈 Audio saved as: response.wav
```

### Query 2: Order Tracking — In Transit

```bash
python main.py --text "Where is my order ORD124?"
```

```
💬 Using text input: Where is my order ORD124?
🤖 Response: Your order ORD124 for Running Shoes is currently in transit
             and is expected to arrive by 2026-03-30.
🔈 Audio saved as: response.wav
```

### Query 3: Return Policy

```bash
python main.py --text "I want to return a product."
```

```
💬 Using text input: I want to return a product.
🤖 Response: You're eligible to return the product within 7 days.
             The item must be unused and in its original packaging.
🔈 Audio saved as: response.wav
```

### Query 4: Refund Policy

```bash
python main.py --text "What is the refund policy?"
```

```
💬 Using text input: What is the refund policy?
🤖 Response: Refunds are processed to your original payment method
             within 5 business days.
🔈 Audio saved as: response.wav
```

### Query 5: Out of Scope

```bash
python main.py --text "Tell me a joke."
```

```
💬 Using text input: Tell me a joke.
🤖 Response: I can only assist with orders, returns, and refunds.
             I don't have information on that topic.
🔈 Audio saved as: response.wav
```

---

## 🧩 Key Code Snippets

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

### Intent Detection + Retrieval (`app/core/assistant.py`)

```python
def detect_intent(self, text):
    text = text.lower()
    if "order"  in text: return "order_tracking"
    elif "return" in text: return "return_policy"
    elif "refund" in text: return "refund_policy"
    else:                  return "unknown"

def extract_order_id(self, text):
    # Match ORD-prefixed IDs: ORD123
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

### LLM Response (`app/core/llm_service.py`)

```python
response = self.client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[{"role": "user", "content": prompt}]
)
```

---

## 📋 Assumptions

- **Single-session, no authentication**: All orders are accessible to any caller. In production, this would require user_id verification before exposing order data.

- **Fixed 5-second audio capture**: The recorder captures exactly 5 seconds of audio — sufficient for short support queries. Longer queries may get cut off; VAD (voice activity detection) would solve this in production.

- **Order IDs are explicitly spoken**: The user must say the order ID clearly (e.g. "ORD123"). Fuzzy matching on paraphrased descriptions ("my shoe order") is not implemented.

- **Single user context**: The `user_id` field in `orders.json` is not used for filtering in the demo. Any query can retrieve any order — this simplifies the demo scope.

- **Static dataset**: `orders.json` and `policies.json` are treated as the single source of truth. No external database or live order system is queried.

- **English only**: The ASR model is configured for English. Multi-language support is out of scope for this version.

---

## 🔀 Design Decisions & Tradeoffs

### Groq over OpenAI for both ASR and LLM
**Decision**: Use Groq's Whisper Large v3 (ASR) and LLaMA 3.1 8B Instant (LLM) instead of OpenAI Whisper + GPT-4.
**Why**: Groq's LPU inference is ~10x faster than standard GPU endpoints — critical for voice UX where latency above 2–3 seconds feels broken.
**Tradeoff**: LLaMA 3.1 8B has lower reasoning quality than GPT-4 on complex queries. Acceptable for 3 well-defined intents; would matter more with open-ended queries.

### Rule-based intent detection over embedding similarity
**Decision**: Use regex/keyword matching for intent classification.
**Why**: Zero API cost, ~0ms latency, deterministic behavior — sufficient for exactly 3 well-defined intents.
**Tradeoff**: Brittle to paraphrasing. "Track my package" or "shipment status" will NOT match `order_tracking`. A `sentence-transformers` model would handle this but adds ~100MB dependency and ~200ms latency.

### pyttsx3 over cloud TTS
**Decision**: Use pyttsx3 for offline text-to-speech.
**Why**: No API cost, no network latency for synthesis, works in any environment including CI/CD and servers without audio devices.
**Tradeoff**: Robotic voice quality vs. ElevenLabs or Groq's TTS API. For a production assistant, cloud TTS would be mandatory.

### Modular `app/` architecture
**Decision**: Separate ASR, core logic, and TTS into distinct modules.
**Why**: Each layer is independently swappable. Switching from pyttsx3 to cloud TTS requires changing only `tts_service.py`. Switching ASR requires changing only `groq_service.py`.
**Tradeoff**: More files than a single-file script — worth it for maintainability.

### CLI interface with `--text` flag
**Decision**: Implement as a command-line tool with an optional text bypass.
**Why**: Fastest to build, easiest to demo, and the `--text` flag ensures evaluators can test the pipeline on any machine — even without a microphone.
**Tradeoff**: Not user-facing ready. A FastAPI wrapper would enable production deployment with ~30 minutes of extra work.

---

## 🔮 If I Had More Time

1. **Semantic intent detection**: Replace regex with `sentence-transformers` embeddings so paraphrased queries ("track my package", "shipment ETA") still hit the correct intent.

2. **Multi-turn conversation**: Maintain a conversation history list so follow-up questions work naturally ("What about my other order?" after asking about ORD123).

3. **Groq TTS**: Replace pyttsx3 with Groq's TTS API for natural, human-quality voice responses.

4. **Streaming LLM output**: Stream tokens from the LLM to TTS progressively to reduce time-to-first-audio from ~2s to under 500ms.

5. **User authentication**: Add `user_id` filtering so each caller only sees their own orders — essential before any real deployment.

6. **Wake word detection**: Integrate Porcupine or Picovoice so the assistant activates only on "Hey Assistant" rather than recording on a fixed timer.

7. **FastAPI wrapper**: Expose the pipeline as a `POST /query` endpoint accepting audio file uploads and returning JSON + audio — enabling production deployment.

---

## 📦 Requirements

```
sounddevice
scipy
numpy
groq
python-dotenv
pyttsx3
```

Generate `requirements.txt`:

```bash
pip freeze > requirements.txt
```

---

## 🛡️ Security Notes

- Store your `GROQ_API_KEY` only in `.env` — never hardcode it in source files
- `.env` is listed in `.gitignore` and will never be committed
- Rotate your API key immediately if accidentally exposed in git history

---

## 📄 License

MIT License — free to use, modify, and distribute.
