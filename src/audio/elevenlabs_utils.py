from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os

from src.ui.menu_bar import client

load_dotenv(dotenv_path="../../.env")
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_ACESS_KEY"))

def speak(message: str, debug=False) -> None:

    audio = client.text_to_speech.convert(
        text=message,
        voice_id="JBFqnCBsd6RMkjVDRZzb",  # Substitua pelo ID da voz desejada
        model_id="eleven_multilingual_v2",  # Modelo multilíngue
        output_format="mp3_44100_128",  # Formato de saída
    )

    play(audio)  # Reproduz o áudio
    if debug: print("[DEBUG] Fala concluída")


if __name__ == "__main__":
    speak("Olá, mundo!")