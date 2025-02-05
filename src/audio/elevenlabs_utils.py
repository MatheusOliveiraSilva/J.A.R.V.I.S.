from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play
import os

class ElevenLabsUtils:
    def __init__(self, dotenv_path: str = "../../.env"):

        load_dotenv(dotenv_path=dotenv_path)

        self.client = ElevenLabs(api_key=os.getenv("ELEVENLABS_ACESS_KEY"))
        pass

    def play_message(self, message: str, debug=False) -> None:

        audio = self.client.text_to_speech.convert(
            text=message,
            voice_id="JBFqnCBsd6RMkjVDRZzb",  # Substitua pelo ID da voz desejada
            model_id="eleven_multilingual_v2",  # Modelo multilíngue
            output_format="mp3_44100_128",  # Formato de saída
        )

        play(audio)  # Reproduz o áudio
        if debug: print("[DEBUG] Fala concluída")

if __name__ == "__main__":
    elevenlabs_utils = ElevenLabsUtils()
    elevenlabs_utils.play_message("Olá, mundo!")