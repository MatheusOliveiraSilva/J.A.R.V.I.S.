import sounddevice as sd
import numpy as np

def callback(indata, frames, time, status):
    volume_norm = np.linalg.norm(indata) * 10
    print(f"Nível de Áudio: {volume_norm}")

with sd.InputStream(callback=callback, channels=1, samplerate=16000):
    print("Fale algo no microfone...")
    sd.sleep(5000)  # Aguarde 5 segundos
