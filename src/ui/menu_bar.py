import os
import sys
import numpy as np
import sounddevice as sd
import pvporcupine
import speech_recognition as sr
from Cocoa import NSApplication, NSStatusBar, NSMenu, NSMenuItem, NSVariableStatusItemLength
from PyObjCTools import AppHelper
from dotenv import load_dotenv

load_dotenv(dotenv_path="../../.env")

class FlupsAssistant:
    def __init__(self):
        self.app = NSApplication.sharedApplication()
        self.status_bar = NSStatusBar.systemStatusBar()
        self.status_item = self.status_bar.statusItemWithLength_(NSVariableStatusItemLength)

        # Ícone e título do menu bar
        self.status_item.setTitle_("🔵 Flups")
        self.status_item.setHighlightMode_(True)

        # Criando o menu dropdown
        self.menu = NSMenu.alloc().init()

        # Adicionando um item de feedback
        self.feedback_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Aguardando comando...", None, "")
        self.menu.addItem_(self.feedback_item)

        # Adicionando um botão de teste
        self.test_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Testar", "testCommand:", "t")
        self.test_item.setTarget_(self)
        self.menu.addItem_(self.test_item)

        # Adicionando a opção de sair
        self.quit_item = NSMenuItem.alloc().initWithTitle_action_keyEquivalent_("Sair", "quitApp:", "q")
        self.quit_item.setTarget_(self)
        self.menu.addItem_(self.quit_item)

        self.status_item.setMenu_(self.menu)

        # Inicializar Porcupine
        self.porcupine = pvporcupine.create(access_key=os.getenv("PV_ACCESS_KEY"), keywords=["jarvis"])
        self.recognizer = sr.Recognizer()  # Inicializar o reconhecedor de fala
        self.start_listening()

    def testCommand_(self, sender):
        print("Comando Testado!")  # Log no terminal
        self.feedback_item.setTitle_("Comando recebido! 🚀")

    def quitApp_(self, sender):
        print("Saindo do assistente...")
        sys.exit()

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(status, file=sys.stderr)
        pcm = np.frombuffer(indata, dtype=np.int16)
        result = self.porcupine.process(pcm)
        if result >= 0:
            print("Hotword detectada: Flups!")
            self.feedback_item.setTitle_("🔊 Flups detectado! Aguardando comando...")
            self.listen_for_command()  # Iniciar a escuta para comandos de voz

    def listen_for_command(self):
        """Captura áudio e converte para texto."""
        with sr.Microphone() as source:
            print("Escutando...")
            self.feedback_item.setTitle_("Escutando... 🎤")
            audio = self.recognizer.listen(source)  # Captura o áudio

            try:
                # Usa o Google Web Speech API para reconhecer o áudio
                text = self.recognizer.recognize_google(audio, language="pt-BR")
                print(f"Você disse: {text}")
                self.feedback_item.setTitle_(f"Comando: {text}")
                self.process_command(text)  # Processa o comando reconhecido
            except sr.UnknownValueError:
                print("Não entendi o comando.")
                self.feedback_item.setTitle_("Não entendi o comando. Tente novamente.")
            except sr.RequestError as e:
                print(f"Erro ao acessar o serviço de reconhecimento de fala: {e}")
                self.feedback_item.setTitle_("Erro no serviço de reconhecimento de fala.")

    def process_command(self, command):
        """Processa o comando de voz reconhecido."""
        if "hora" in command.lower():
            import datetime
            now = datetime.datetime.now()
            self.feedback_item.setTitle_(f"Hora atual: {now.strftime('%H:%M')}")
        elif "sair" in command.lower():
            self.quitApp_(None)
        else:
            self.feedback_item.setTitle_("Comando não reconhecido.")

    def start_listening(self):
        self.stream = sd.InputStream(callback=self.audio_callback, samplerate=16000, blocksize=512, dtype=np.int16,
                                     channels=1, device=3) # se não tiver o celular vai quebrar.
        self.stream.start()

if __name__ == "__main__":
    import sounddevice as sd

    print(sd.query_devices())
    assistant = FlupsAssistant()
    AppHelper.runEventLoop()
