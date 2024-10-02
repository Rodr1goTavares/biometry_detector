import cv2
import mediapipe as mp  # Renomeado para facilitar o uso

class HandCapture:
    def __init__(self):
        self._capture = None
        self._mp_hands = mp.solutions.hands  # Solução correta para acessar 'hands'
        self._hands = self._mp_hands.Hands(
            static_image_mode=False,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self._mp_drawing = mp.solutions.drawing_utils  # Solução correta para desenhar os landmarks

    def startCapture(self):
        self._capture = cv2.VideoCapture(0)
        while self._capture.isOpened():
            ret, frame = self._capture.read()
            if not ret:
                break
            # Convert to RGB
            image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            
            processedFrame = self._hands.process(image)
            
            # Return to BGR
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

            # Se mãos forem detectadas
            if processedFrame.multi_hand_landmarks:
                for hand_landmarks in processedFrame.multi_hand_landmarks:
                    # Desenhar os landmarks
                    self._mp_drawing.draw_landmarks(image, hand_landmarks, self._mp_hands.HAND_CONNECTIONS)

                    # Contar os dedos levantados
                    fingers = self._calcFingersPosition(hand_landmarks)
                    cv2.putText(image, f'Dedos levantados: {fingers}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                    print("Dedos levantados: " + str(fingers))

            # Exibir o frame com a detecção
            cv2.imshow('Hand Tracking', image)

            # Sair do loop se a tecla 'q' for pressionada
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Liberar recursos
        self._capture.release()
        cv2.destroyAllWindows()

    def _calcFingersPosition(self, hand_landmarks):
        # Índices dos dedos
        thumb_tip = hand_landmarks.landmark[self._mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self._mp_hands.HandLandmark.INDEX_FINGER_TIP]
        middle_tip = hand_landmarks.landmark[self._mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        ring_tip = hand_landmarks.landmark[self._mp_hands.HandLandmark.RING_FINGER_TIP]
        pinky_tip = hand_landmarks.landmark[self._mp_hands.HandLandmark.PINKY_TIP]
    
        # Definindo um critério simples de se o dedo está levantado:
        wrist = hand_landmarks.landmark[self._mp_hands.HandLandmark.WRIST]
    
        fingers_up = 0
        if index_tip.y < wrist.y:
            fingers_up += 1
        if middle_tip.y < wrist.y:
            fingers_up += 1
        if ring_tip.y < wrist.y:
            fingers_up += 1
        if pinky_tip.y < wrist.y:
            fingers_up += 1
        if thumb_tip.x > wrist.x:
            fingers_up += 1

        return fingers_up