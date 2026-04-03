import os
import argparse
from dotenv import load_dotenv

load_dotenv()

if not os.getenv("GROQ_API_KEY"):
    raise EnvironmentError(
        "\n❌ GROQ_API_KEY not set.\n"
        "   Copy .env.example to .env and add your Groq API key.\n"
        "   Get a free key at: https://console.groq.com\n"
    )

from app.asr.recorder import AudioRecorder
from app.asr.groq_service import GroqASRService
from app.core.assistant import VoiceAssistant
from app.tts.tts_service import TTSService


def main():
    parser = argparse.ArgumentParser(description="Voice AI E-commerce Support Assistant")
    parser.add_argument(
        "--text",
        type=str,
        help="Skip microphone recording and use this text directly as input"
    )
    args = parser.parse_args()

    asr = GroqASRService()
    assistant = VoiceAssistant()
    tts = TTSService()

    # 🎤 Step 1: Get input (mic or text)
    if args.text:
        text = args.text
        print(f"\n💬 Using text input: {text}")
    else:
        recorder = AudioRecorder()
        audio_file = recorder.record(duration=5)

        # 🧠 Step 2: Speech → Text
        text = asr.transcribe(audio_file)
        print("\n📝 Transcribed:", text)

    # 🤖 Step 3: LLM Response
    response = assistant.handle_query(text)
    print("\n🤖 Response:", response)

    # 🔊 Step 4: Text → Speech
    audio_output = tts.speak(response)
    print(f"\n🔈 Audio saved as: {audio_output}")


if __name__ == "__main__":
    main()