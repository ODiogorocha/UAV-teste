import cv2

def open_cam():
    # Abre a câmera padrão (índice 0)
    camera = cv2.VideoCapture(0)

    # Verifica se a câmera foi aberta corretamente
    if not camera.isOpened():
        print("Erro ao acessar a câmera")
        exit()

    return camera
