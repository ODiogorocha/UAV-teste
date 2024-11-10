import cv2
import numpy as np
from pyzbar.pyzbar import decode
from pyparrot.Minidrone import Mambo  
import datetime
from camera import open_cam  
from pyzbar.pyzbar import decode  

# Definição das classes de objetos detectáveis (para detecção de objetos)
CLASSES = [
    "background", "airplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "dining_table",
    "dog", "horse", "motorcycle", "person", "potted_plant",
    "sheep", "sofa", "train", "tv_monitor"
]

# Caminhos dos arquivos do modelo de rede neural
caminho_prototxt = 'UAV-teste/processamento-camera/src/arq/deploy.prototxt'
caminho_modelo = 'UAV-teste/processamento-camera/src/arq/mobilenet_iter_73000.caffemodel'
rede_neural = cv2.dnn.readNetFromCaffe(caminho_prototxt, caminho_modelo)

# Inicialização do drone
mamboAddr = "your_drone_address"
mambo = Mambo(mamboAddr, use_wifi=False)

# Conectar ao drone
print("Connecting to the drone...")
if not mambo.connect(num_retries=3):
    print("Failed to connect to the drone.")
    exit(1)

# Função para processar QR Codes e gerar comandos para o drone
def process_qr_code(frame):
    objetos_qr = decode(frame)
    for objeto in objetos_qr:
        dados_qr = objeto.data.decode('utf-8')
        print(f"QR Code command detected: {dados_qr}")
        
        # Movimentos do drone baseado no QR Code
        if dados_qr == "forward":
            print("Moving forward.")
            mambo.fly_direct(roll=0, pitch=30, yaw=0, vertical_movement=0, duration=1)
        elif dados_qr == "backward":
            print("Moving backward.")
            mambo.fly_direct(roll=0, pitch=-30, yaw=0, vertical_movement=0, duration=1)
        elif dados_qr == "left":
            print("Moving left.")
            mambo.fly_direct(roll=-30, pitch=0, yaw=0, vertical_movement=0, duration=1)
        elif dados_qr == "right":
            print("Moving right.")
            mambo.fly_direct(roll=30, pitch=0, yaw=0, vertical_movement=0, duration=1)
        elif dados_qr == "up":
            print("Moving up.")
            mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=30, duration=1)
        elif dados_qr == "down":
            print("Moving down.")
            mambo.fly_direct(roll=0, pitch=0, yaw=0, vertical_movement=-30, duration=1)
        elif dados_qr == "land":
            print("Landing the drone.")
            mambo.safe_land()
            return True  # Returns True to indicate the landing occurred
    return False  # Returns False if there was no landing command

# Função para processar e salvar os dados de códigos de barras
def process_barcode(frame, output_file):
    barcodes = decode(frame)
    
    for barcode in barcodes:
        barcode_data = barcode.data.decode('utf-8')
        print(f"Barcode detected: {barcode_data}")

        # Salva os dados no arquivo de texto
        with open(output_file, 'a') as f:
            f.write(f"{datetime.datetime.now()}: Barcode detected: {barcode_data}\n")

        # Desenha o contorno do código de barras
        points = barcode.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
        
        # Exibe o dado do código de barras na imagem
        cv2.putText(frame, barcode_data, (points[0].x, points[0].y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return frame

# Função para processar a câmera e controlar o drone
def process_camera_and_move_drone():
    camera = open_cam()  # Open the camera
    output_file = 'detected_barcodes.txt'

    # Cria ou limpa o arquivo de saída para códigos de barras
    with open(output_file, 'w') as f:
        f.write("History of Detected Barcodes:\n")

    mambo.safe_takeoff()  # The drone takes off

    while True:
        sucesso, frame = camera.read()
        if not sucesso:
            break

        # Process QR Codes to control drone movement
        if process_qr_code(frame):
            break

        # Process barcodes
        frame = process_barcode(frame, output_file)

        # Display the processed frame with QR Code and barcodes
        cv2.imshow("QR Code and Barcode Detection", frame)

        # Press 'e' to exit the loop
        if cv2.waitKey(1) & 0xFF == ord('e'):
            break

    camera.release()
    cv2.destroyAllWindows()

# Executa o programa
try:
    process_camera_and_move_drone()
finally:
    mambo.safe_land()  # Lands the drone safely
    mambo.disconnect()  # Disconnects from the drone
