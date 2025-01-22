import speech_recognition as sr
import time


class VoiceProcessor:
    def __init__(self, wake_word="jarvis", active_timeout=10):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.wake_word = wake_word.lower()  # Wake word em minúsculas para comparação
        self.active = False  # Estado inicial
        self.active_until = None  # Tempo limite para o estado ativo
        self.active_timeout = active_timeout  # Tempo máximo ativo em segundos

        # Ajustes de configuração para escuta
        self.recognizer.pause_threshold = 2.0  # Esperar até 2 segundos de silêncio
        self.recognizer.dynamic_energy_threshold = True  # Ajuste dinâmico para ruídos
        self.recognizer.energy_threshold = 300  # Limite de energia para ruídos baixos

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
                        self.execute_command(command)  # Executa o comando imediatamente após detectar o wake word
                        self.active_until = time.time() + self.active_timeout
                else:
                    # Processar comandos no estado ativo
                    self.execute_command(command)

                    # Atualizar o timeout
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
        if "desligar" in command:
            print("Comando: Desligar assistente.")
            self.active = False
        elif "aberta" in command or "e-mail" in command:
            print("Comando: Abrindo e-mail.")
            self.open_email()
        else:
            print(f"Comando não reconhecido: {command}")

    def open_email(self):
        """
        Função simulada para abrir o e-mail.
        Aqui, você pode chamar uma função para abrir seu cliente de e-mail.
        """
        print("E-mail aberto!")  # Simulando a ação de abrir o e-mail
        # Por exemplo, você poderia usar algo como:
        # subprocess.run(["open", "-a", "Mail"])  # Para abrir o aplicativo de e-mail no macOS


if __name__ == "__main__":
    processor = VoiceProcessor(wake_word="jarvis", active_timeout=10)
    processor.listen()
