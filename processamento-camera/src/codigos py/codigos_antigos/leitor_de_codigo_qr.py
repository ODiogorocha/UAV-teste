import cv2
import numpy as np
from pyzbar.pyzbar import decode

# Caminhos dos arquivos do modelo
caminho_prototxt = 'processamento-camera/src/arq/deploy.prototxt'
caminho_modelo = 'processamento-camera/src/arq/mobilenet_iter_73000.caffemodel'

# Carrega a rede neural MobileNet SSD
rede_neural = cv2.dnn.readNetFromCaffe(caminho_prototxt, caminho_modelo)

# Definição das classes de objetos detectáveis
CLASSES = [
    "fundo", "aviao", "bicicleta", "passaro", "barco",
    "garrafa", "onibus", "carro", "gato", "cadeira", "vaca", "mesa_de_jantar",
    "cachorro", "cavalo", "moto", "pessoa", "vaso_de_planta",
    "ovelha", "sofa", "trem", "monitor_de_tv"
]

def processar_qr_code(frame, arquivo_saida):
    """Detecta e processa QR Codes no quadro atual."""
    objetos_qr = decode(frame)
    for objeto in objetos_qr:
        pontos = objeto.polygon
        if len(pontos) == 4:
            pontos_array = np.array(pontos, dtype=np.int32)
            cv2.polylines(frame, [pontos_array], True, (0, 255, 0), 2)
            dados_qr = objeto.data.decode('utf-8')
            cv2.putText(frame, dados_qr, (pontos_array[0][0], pontos_array[0][1] - 10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            arquivo_saida.write(f"QR Code Detectado: {dados_qr}\n")

def processar_camera(arquivo_saida):
    captura_camera = cv2.VideoCapture(1)  

    if not captura_camera.isOpened():
        print("Erro ao abrir a câmera.")
        return

    with open(arquivo_saida, 'w') as arquivo:
        arquivo.write("Detecções:\n")

        while True:
            sucesso, quadro = captura_camera.read()
            if not sucesso:
                print("Erro ao capturar o quadro.")
                break

            altura_quadro, largura_quadro = quadro.shape[:2]

            # Pré-processamento do quadro para a rede neural
            blob = cv2.dnn.blobFromImage(
                cv2.resize(quadro, (300, 300)), 0.007843, (300, 300), 127.5
            )
            rede_neural.setInput(blob)
            deteccoes = rede_neural.forward()

            for i in range(deteccoes.shape[2]):
                confianca = deteccoes[0, 0, i, 2]
                if confianca > 0.2:
                    caixa = deteccoes[0, 0, i, 3:7] * np.array(
                        [largura_quadro, altura_quadro, largura_quadro, altura_quadro]
                    )
                    (inicio_x, inicio_y, fim_x, fim_y) = caixa.astype("int")
                    indice_classe = int(deteccoes[0, 0, i, 1])
                    rotulo = f"{CLASSES[indice_classe]}: {confianca:.2f}"
                    cv2.rectangle(quadro, (inicio_x, inicio_y), (fim_x, fim_y), (0, 255, 0), 2)
                    cv2.putText(quadro, rotulo, (inicio_x, inicio_y - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                    arquivo.write(
                        f"Objeto: {rotulo}, Posição: [{inicio_x}, {inicio_y}, {fim_x}, {fim_y}]\n"
                    )

            processar_qr_code(quadro, arquivo)

            # Exibe o quadro processado
            cv2.imshow("Detecção de Objetos e QR Codes", quadro)

            # Pressione 'q' para sair do loop
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    captura_camera.release()
    cv2.destroyAllWindows()

# Caminho do arquivo de saída
caminho_arquivo_saida = 'detecoes_e_codigos_qr.txt'
processar_camera(caminho_arquivo_saida)
