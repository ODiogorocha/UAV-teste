import cv2
import mediapipe as mp
import time

# Função para contar os dedos levantados
def contar_dedos(landmarks):
    dedos = 0

    # Condições para detectar se os dedos estão levantados (dedos individuais)
    if landmarks[4].y < landmarks[3].y:  # Polegar
        dedos += 1
    if landmarks[8].y < landmarks[6].y:  # Indicador
        dedos += 1
    if landmarks[12].y < landmarks[10].y:  # Médio
        dedos += 1
    if landmarks[16].y < landmarks[14].y:  # Anelar
        dedos += 1
    if landmarks[20].y < landmarks[18].y:  # Mínimo
        dedos += 1

    return dedos

# Função principal para processar a imagem da câmera
def processar_camera():
    # Testa os índices 0, 1, 2... para encontrar uma câmera disponível
    camera = None
    for i in range(3):  # Testa até 3 câmeras
        camera = cv2.VideoCapture(i)
        if camera.isOpened():
            print(f"Câmera encontrada no índice {i}")
            break
        else:
            print(f"Não foi possível abrir a câmera no índice {i}")

    if not camera or not camera.isOpened():
        print("Erro ao acessar a câmera.")
        return

    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands()
    mp_drawing = mp.solutions.drawing_utils

    tic = 0
    tac = 0

    while True:
        sucesso, imagem = camera.read()
        if not sucesso:
            print("Erro ao ler a imagem da câmera")
            break

        imagem_rgb = cv2.cvtColor(imagem, cv2.COLOR_BGR2RGB)
        resultados = hands.process(imagem_rgb)

        if resultados.multi_hand_landmarks:
            for hand_landmarks in resultados.multi_hand_landmarks:
                mp_drawing.draw_landmarks(imagem, hand_landmarks, mp_hands.HAND_CONNECTIONS)

                # Contar dedos levantados
                dedos = contar_dedos(hand_landmarks.landmark)
                cv2.putText(imagem, f'Dedos: {dedos}', (10, 130), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # FPS
        tac = time.time()
        fps = 1 / (tac - tic)
        tic = tac
        cv2.putText(imagem, f'FPS: {int(fps)}', (10, 70), cv2.FONT_HERSHEY_PLAIN, 3, (0, 255, 0), 3)

        # Mostrar a imagem
        cv2.imshow("Câmera", imagem)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

# Chama a função principal
processar_camera()
