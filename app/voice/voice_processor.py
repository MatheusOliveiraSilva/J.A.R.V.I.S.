import speech_recognition as sr
import time
from langchain_core.messages import HumanMessage
from langgraph.checkpoint.memory import MemorySaver
from app.agent.jarvis import graph

# Configuração do agente
config = {"configurable": {"thread_id": '1'}}

# Classe de Processamento de Voz
class VoiceProcessor:
    def __init__(self, wake_word="jarvis", active_timeout=10):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.wake_word = wake_word.lower()
        self.active = False
        self.active_until = None
        self.active_timeout = active_timeout

        # Configurações de áudio
        self.recognizer.pause_threshold = 2.0
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.energy_threshold = 300

    def listen(self):
        """
        Escuta o áudio continuamente e ativa/desativa conforme a wake word.
        """
        print("Aguardando wake word...")
        while True:
            try:
                with self.microphone as source:
                    # Ajustar para o ruído ambiente por 2 segundos
                    self.recognizer.adjust_for_ambient_noise(source, duration=2)
                    print("Pronto para ouvir...")

                    # Escutar o áudio com um limite de timeout maior
                    audio = self.recognizer.listen(source, timeout=10)

                # Reconhecer o que foi dito
                command = self.recognizer.recognize_google(audio, language="pt-BR").lower()
                print(f"Você disse: {command}")

                # Verificar wake word
                if not self.active:
                    if self.wake_word in command:
                        print("Wake word detectada! Assistente ativado.")
                        self.active = True
                        self.execute_command(command)
                        self.active_until = time.time() + self.active_timeout
                else:
                    # Processar comandos no estado ativo
                    self.execute_command(command)
                    self.active_until = time.time() + self.active_timeout

            except sr.UnknownValueError:
                print("Não entendi. Por favor, repita.")
            except sr.RequestError as e:
                print(f"Erro no serviço de reconhecimento de voz: {e}")
            except sr.WaitTimeoutError:
                print("Tempo de escuta esgotado, tentando novamente.")

            # Verificar se o timeout expirou no estado ativo
            if self.active and time.time() > self.active_until:
                print("Tempo de inatividade expirado. Retornando ao estado inativo.")
                self.active = False

    def execute_command(self, command):
        """
        Executa comandos quando o assistente está ativo.
        """
        # Integração com o LangGraph
        messages = [HumanMessage(content=command)]
        result = graph.invoke({"messages": messages}, config)

        # Processar e exibir a resposta do agente
        for message in result["messages"]:
            print(f"Agente: {message.content}")
            print("--" * 50)

# Inicializar e executar o processamento contínuo
if __name__ == "__main__":
    processor = VoiceProcessor(wake_word="jarvis", active_timeout=10)
    processor.listen()
