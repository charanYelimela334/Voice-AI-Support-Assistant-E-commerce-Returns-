import pyttsx3

class TTSService:
    def __init__(self):
        self.engine = pyttsx3.init()

    def speak(self, text, filename="response.wav"):
        self.engine.save_to_file(text, filename)
        self.engine.runAndWait()
        return filename
