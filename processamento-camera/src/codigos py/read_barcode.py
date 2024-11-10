import cv2
from pyzbar.pyzbar import decode
import datetime
from camera import open_cam  

# Função para processar e interpretar o código de barras e salvar no arquivo
def process_barcode(frame, output_file):
    barcodes = decode(frame)
    
    for barcode in barcodes:
        # Decodifica os dados do código de barras
        barcode_data = barcode.data.decode('utf-8')
        print(f"Código de barras detectado: {barcode_data}")

        # Salva o dado detectado no arquivo de texto com data e hora
        with open(output_file, 'a') as f:
            f.write(f"{datetime.datetime.now()}: Código de barras detectado: {barcode_data}\n")

        # Desenha o contorno ao redor do código de barras
        points = barcode.polygon
        if len(points) == 4:
            pts = np.array(points, dtype=np.int32)
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)
        
        # Exibe o dado do código de barras na imagem
        cv2.putText(frame, barcode_data, (points[0].x, points[0].y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    return frame

# Função principal para capturar o vídeo da câmera e ler códigos de barras
def process_camera():
    # Abre a câmera usando a função open_cam do arquivo camera.py
    camera = open_cam()
    output_file = 'detected_barcodes.txt'

    # Cria ou limpa o arquivo de saída
    with open(output_file, 'w') as f:
        f.write("Histórico de Códigos de Barras Detectados:\n")

    while True:
        ret, frame = camera.read()
        if not ret:
            break

        # Processa o frame da câmera para decodificar códigos de barras
        frame = process_barcode(frame, output_file)

        # Mostra o frame com o código de barras detectado, se houver
        cv2.imshow("Leitura de Códigos de Barras", frame)

        # Pressione 'e' para sair
        if cv2.waitKey(1) & 0xFF == ord('e'):
            break

    camera.release()
    cv2.destroyAllWindows()

# Executa o programa
process_camera()
