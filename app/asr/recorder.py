import sounddevice as sd
from scipy.io.wavfile import write
import numpy as np

class AudioRecorder:
    def __init__(self, sample_rate=16000):
        self.sample_rate = sample_rate

    def record(self, duration=60, filename="input.wav"):
        print("🎤 Recording... Speak now")

        audio = sd.rec(
            int(duration * self.sample_rate),
            samplerate=16000,
            channels=1,
            dtype='float32'
        )

        sd.wait()  # wait until recording is finished

        write(filename, self.sample_rate, audio)

        print(f"✅ Saved recording as {filename}")
        return filename