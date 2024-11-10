import cv2
import mediapipe as mp

# Inicializa o mediapipe
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=False, min_detection_confidence=0.5, min_tracking_confidence=0.5)

# Função para desenhar uma caixa em volta da pessoa detectada
def desenhar_caixa_pessoa(imagem, landmarks):
    altura, largura, _ = imagem.shape

    # Obtém as coordenadas x e y dos pontos do corpo
    x_min = int(min(landmark.x for landmark in landmarks) * largura)
    x_max = int(max(landmark.x for landmark in landmarks) * largura)
    y_min = int(min(landmark.y for landmark in landmarks) * altura)
    y_max = int(max(landmark.y for landmark in landmarks) * altura)

    # Desenha a caixa em volta da pessoa detectada
    cv2.rectangle(imagem, (x_min, y_min), (x_max, y_max), (0, 255, 0), 2)  # Verde (BGR)

# Função para processar o vídeo da câmera
def processar_camera(camera):
    print("Entrou no processamento de humano")
    
    while True:
        ret, frame = camera.read()
        if not ret:
            print("Erro ao acessar o vídeo da câmera")
            break

        # Converte o frame para RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        resultados = pose.process(rgb_frame)

        if resultados.pose_landmarks:
            landmarks = resultados.pose_landmarks.landmark

            # Desenha a caixa em volta da pessoa
            frame_com_caixa = frame.copy()
            desenhar_caixa_pessoa(frame_com_caixa, landmarks)

            # Mostra o frame com a caixa
            cv2.imshow('Camera com Caixa em Volta da Pessoa', frame_com_caixa)

        if cv2.waitKey(1) & 0xFF == ord('q'):  # Encerra ao pressionar 'q'
            break
