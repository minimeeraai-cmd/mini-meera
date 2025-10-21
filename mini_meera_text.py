import os
import sounddevice as sd
import vosk
import queue
import json
import pyttsx3

def speak(text):
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)
    engine.setProperty('volume', 1.0)
    print(f"💬 Meera: {text}")
    engine.say(text)
    engine.runAndWait()

def callback(indata, frames, time, status):
    q.put(bytes(indata))

def listen_and_convert(model_path="model"):
    if not os.path.exists(model_path):
        print("❌ Vosk model not found. Please download and extract it.")
        return None

    model = vosk.Model(model_path)
    rec = vosk.KaldiRecognizer(model, 16000)
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("🎤 Speak now...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    print(f"🗣️ You said: {text}")
                    return text
