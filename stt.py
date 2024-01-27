import json, pyaudio
from params import session
import vosk
import os

model = vosk.Model(os.path.join(os.path.dirname(__file__), session.VOSK_MODEL))
rec = vosk.KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


class SpeechToText:
    MICROPHONE = False

    def listen(self):
        while self.MICROPHONE:
            data = stream.read(4000, exception_on_overflow=False)
            if rec.AcceptWaveform(data) and len(data) > 0:
                anwser = json.loads(rec.Result())
                if anwser['text']:
                    yield anwser['text']

    def status(self, status):
        self.MICROPHONE = status


stt = SpeechToText()
