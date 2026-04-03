from dotenv import load_dotenv
load_dotenv()

from app.asr.recorder import AudioRecorder
from app.asr.groq_service import GroqASRService
from app.core.assistant import VoiceAssistant
from app.tts.tts_service import TTSService

def main():
    recorder = AudioRecorder()
    asr = GroqASRService()
    assistant = VoiceAssistant()
    tts = TTSService()

    # 🎤 Step 1: Record
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