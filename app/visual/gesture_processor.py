import cv2
import mediapipe as mp
from app.system.mac_actions import MacActions
import pyautogui

class GestureProcessor:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            max_num_hands=1,
            min_detection_confidence=0.7,
            min_tracking_confidence=0.7,
        )
        self.mp_draw = mp.solutions.drawing_utils
        self.mac_actions = MacActions()
        self.state = "neutral"  # Estado inicial
        self.last_z = None  # Última posição z do dedo indicador para detectar cliques

    def process_frame(self, frame):
        # Converte o frame para RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.hands.process(rgb_frame)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Desenhar os pontos no frame
                self.mp_draw.draw_landmarks(frame, hand_landmarks, self.mp_hands.HAND_CONNECTIONS)

                # Atualizar estado com base no gesto detectado
                self.update_state(hand_landmarks, frame)

        return frame

    def update_state(self, hand_landmarks, frame):
        """
        Atualiza o estado com base nos gestos detectados.
        """
        if self.is_pointing(hand_landmarks):
            self.state = "pointing"
            self.move_mouse(hand_landmarks, frame)
            self.detect_click(hand_landmarks)
        elif self.is_two_fingers_up(hand_landmarks):
            if self.state == "neutral":
                print("Estado: Dois dedos levantados")
                self.state = "two_fingers_up"
        elif self.state == "two_fingers_up" and self.are_two_fingers_down(hand_landmarks):
            print("Gesto detectado: Minimizar janela")
            self.mac_actions.minimize_window()
            self.state = "neutral"
        else:
            self.state = "neutral"

    def is_two_fingers_up(self, hand_landmarks):
        """
        Verifica se apenas o indicador e o médio estão levantados.
        """
        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]

        index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        ring_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP]
        pinky_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP]

        return (
            index_tip.y < index_mcp.y and  # Indicador levantado
            middle_tip.y < middle_mcp.y and  # Médio levantado
            ring_tip.y > ring_mcp.y and  # Anular abaixado
            pinky_tip.y > pinky_mcp.y # Mínimo abaixado
        )

    def are_two_fingers_down(self, hand_landmarks):
        """
        Verifica se os dois dedos levantados (indicador e médio) abaixaram.
        """
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

        return (
            index_tip.y > index_mcp.y and  # Indicador abaixado
            middle_tip.y > middle_mcp.y  # Médio abaixado
        )

    def is_pointing(self, hand_landmarks):
        """
        Verifica se o dedo indicador está levantado, com maior tolerância para inclinações.
        """
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]

        index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]
        middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]
        ring_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP]
        pinky_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP]

        # Adicionar tolerância ao eixo Y (levemente abaixado ainda é considerado levantado)
        tolerance_y = 0.05  # Ajuste conforme necessário

        # Verificar se o indicador está levantado em relação à base (com tolerância)
        is_index_up = index_tip.y < index_mcp.y + tolerance_y

        # Verificar se o indicador está mais elevado que os outros dedos
        is_above_others = (
                index_tip.y < middle_tip.y and  # Acima do médio
                index_tip.y < ring_tip.y and  # Acima do anular
                index_tip.y < pinky_tip.y  # Acima do mínimo
        )

        # Verificar se o indicador está inclinado para a frente (posição z)
        is_pointing_forward = index_tip.z < index_mcp.z + 0.1  # Pequena margem para "frente"

        return is_index_up and is_above_others and is_pointing_forward

    def detect_click(self, hand_landmarks):
        """
        Detecta um clique baseado na movimentação do eixo z do dedo indicador.
        """
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

        if self.last_z is not None:
            # Detectar movimento para trás (afastar) e para frente (aproximar)
            if self.last_z - index_tip.z > 0.02:  # Valor ajustável para sensibilidade
                print("Clique detectado!")
                pyautogui.click()

        # Atualizar o último valor de z
        self.last_z = index_tip.z

    def move_mouse(self, hand_landmarks, frame):
        """
        Move o cursor do mouse com base na posição do dedo indicador.
        """
        # Obter a posição do dedo indicador (coordenadas normalizadas)
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

        # Resolução da tela
        screen_width, screen_height = pyautogui.size()

        # Coordenadas do dedo escaladas para a tela
        x = int((1 - index_tip.x) * screen_width)  # Inverter X para corresponder à direção correta
        y = int(index_tip.y * screen_height)  # Y sem inversão adicional

        # Mover o mouse
        pyautogui.moveTo(x, y)

    def run(self):
        cap = cv2.VideoCapture(1)
        try:
            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                frame = self.process_frame(frame)

                cv2.imshow("Detecção de Gestos", frame)

                if cv2.waitKey(1) & 0xFF == ord('q'):
                    break
        finally:
            cap.release()
            cv2.destroyAllWindows()


if __name__ == "__main__":
    processor = GestureProcessor()
    processor.run()