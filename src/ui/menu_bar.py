import os
import sys
import threading
import numpy as np
import sounddevice as sd
import pvporcupine
import speech_recognition as sr
from src.audio import elevenlabs_utils
from src.agent.jarvis import graph as JARVIS_AGENT
from langchain_core.messages import HumanMessage
from Cocoa import NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSVariableStatusItemLength
from PyObjCTools import AppHelper
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../.env")

class FlupsAssistant:
    def __init__(self):
        self.app = NSApplication.sharedApplication()
        self.status_bar = NSStatusBar.systemStatusBar()
        self.status_item = self.status_bar.statusItemWithLength_(NSVariableStatusItemLength)

        # Configurações de UI
        self.menu = NSMenu.alloc().init()
        self.feedback_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("🔵 Pronto", None, "")
        self.menu.addItem_(self.feedback_item)
        self.status_item.setMenu_(self.menu)
        self.status_item.setTitle_("Jarvis")

        # Configurações de áudio
        self.mic_device_index = 4  # Índice fixo para MacBook Pro Microphone
        self.mic_name = sr.Microphone.list_microphone_names()[self.mic_device_index]
        print(f"[DEBUG] Microfone selecionado: {self.mic_name} (índice {self.mic_device_index})")

        self.porcupine = pvporcupine.create(
            access_key=os.getenv("PV_ACCESS_KEY"),
            keywords=["jarvis"]
        )
        self.recognizer = sr.Recognizer()
        self.is_processing = False

        # Inicia stream de áudio
        self.start_audio_stream()

    def start_audio_stream(self):
        self.stream = sd.InputStream(
            callback=self.audio_callback,
            samplerate=16000,
            blocksize=512,
            dtype=np.int16,
            channels=1,
            device=self.mic_device_index
        )
        self.stream.start()
        print("[DEBUG] Stream de áudio iniciado")

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"[DEBUG] Erro no áudio: {status}", file=sys.stderr)

        if not self.is_processing:
            pcm = np.frombuffer(indata, dtype=np.int16)
            if self.porcupine.process(pcm) >= 0:
                print("[DEBUG] Hotword 'jarvis' detectada!")
                self.trigger_listen_mode()

    def trigger_listen_mode(self):
        if not self.is_processing:
            self.is_processing = True
            print("[DEBUG] Iniciando modo de escuta...")
            AppHelper.callAfter(self.feedback_item.setTitle_, "🎤 Escutando...")
            self.status_item.setTitle_("🎤 Escutando...")
            threading.Thread(target=self.listen_and_process, daemon=True).start()

    def listen_and_process(self):
        try:
            with sr.Microphone(device_index=self.mic_device_index) as source:
                print("[DEBUG] Ajustando para ruído ambiente...")
                self.recognizer.adjust_for_ambient_noise(source)
                print("[DEBUG] Gravando áudio...")

                # Configurações de tempo de escuta
                audio = self.recognizer.listen(
                    source,
                    timeout=5,  # Tempo máximo para começar a falar
                    phrase_time_limit=10  # Tempo máximo de fala após começar
                )

                print("[DEBUG] Áudio capturado, convertendo para texto...")
                text = self.recognizer.recognize_google(audio, language="pt-BR")
                print(f"[DEBUG] Texto reconhecido: '{text}'")
                self.process_command(text)
        except sr.WaitTimeoutError:
            print("[DEBUG] Timeout: Nenhum comando detectado")
        except Exception as e:
            print(f"[DEBUG] Erro na captura: {str(e)}")
        finally:
            AppHelper.callAfter(self.reset_to_ready)

    def process_command(self, command):
        print(f"[DEBUG] Processando comando: {command}")
        AppHelper.callAfter(self.feedback_item.setTitle_, "⚙️ Processando...")
        self.status_item.setTitle_("⚙️ Processando...")
        response = f"Comando recebido: {command}"

        JARVIS_AGENT.invoke(
            {"messages": [
                HumanMessage(content=command)
            ]},
            {"configurable": {"thread_id": '1'}}
        )

        # Resetar o estado após o processamento
        AppHelper.callAfter(self.reset_to_ready)

    def reset_to_ready(self):
        self.is_processing = False
        print("[DEBUG] Resetando para estado pronto")
        AppHelper.callAfter(self.feedback_item.setTitle_, "Jarvis")
        self.status_item.setTitle_("Jarvis")

        self.start_audio_stream()

if __name__ == "__main__":
    assistant = FlupsAssistant()
    AppHelper.runEventLoop()