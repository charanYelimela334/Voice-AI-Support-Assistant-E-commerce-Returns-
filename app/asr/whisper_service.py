import whisper
import os

os.environ["PATH"] += os.pathsep + r"D:\ffmpeg-2026-04-01-git-eedf8f0165-full_build\ffmpeg-2026-04-01-git-eedf8f0165-full_build\bin"


class WhisperService:
    def __init__(self):
        # You can change model size: tiny, base, small, medium
        self.model = whisper.load_model("medium")

    def transcribe(self, audio_path: str) -> str:
        result = self.model.transcribe(audio_path)
        return result["text"]