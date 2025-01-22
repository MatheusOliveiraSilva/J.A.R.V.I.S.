import speech_recognition as sr

class VoiceProcessor:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def send_to_api(self, source, content, action):
        url = "http://localhost:5005/commands/"
        payload = {"source": source, "content": content, "action": action}
        try:
            response = requests.post(url, json=payload)
            print(f"API Response: {response.json()}")
        except Exception as e:
            print(f"Erro ao enviar para a API: {e}")

    def process_audio(self):
        print("Aguardando comando de voz...")
        try:
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source)
                print("Pronto para ouvir...")
                audio = self.recognizer.listen(source)

            # Converter áudio em texto
            text = self.recognizer.recognize_google(audio, language="pt-BR")
            print(f"Você disse: {text}")

            # Simulação de envio para o agente
            self.send_to_api("audio", text, "Comando de voz processado")
        except sr.UnknownValueError:
            print("Não entendi o que foi dito. Por favor, tente novamente.")
        except sr.RequestError as e:
            print(f"Erro no serviço de reconhecimento de voz: {e}")

    def send_to_agent(self, text):
        """
        Simula o envio do comando de texto para um agente.
        Aqui você pode adicionar lógica para interpretar e executar o comando.
        """
        print(f"Enviando ao agente: {text}")
        # No futuro, podemos integrar isso ao FastAPI ou outro agente.

    def run(self):
        while True:
            try:
                self.process_audio()
            except KeyboardInterrupt:
                print("\nEncerrando o processador de voz...")
                break

if __name__ == "__main__":
    processor = VoiceProcessor()
    processor.run()
