#include <iostream>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <opencv2/dnn.hpp>
#include <zbar.h>

using namespace std;
using namespace cv;
using namespace zbar;
using namespace cv::dnn;

// Caminho para os arquivos do modelo
const string prototxt = "deploy.prototxt";
const string model = "mobilenet_iter_73000.caffemodel";

// Definir classes
const vector<string> CLASSES = {
    "background", "aeroplane", "bicycle", "bird", "boat",
    "bottle", "bus", "car", "cat", "chair", "cow", "diningtable",
    "dog", "horse", "motorbike", "person", "pottedplant",
    "sheep", "sofa", "train", "tvmonitor"
};

// Função para processar QR Code
void processa_qr_code(Mat &frame, const string &arquivo_saida) {
    ImageScanner scanner;
    scanner.set_config(ZBAR_QRCODE, ZBAR_CFG_ENABLE, 1);

    // Converte a imagem para escala de cinza
    Mat gray;
    cvtColor(frame, gray, COLOR_BGR2GRAY);

    // Converte a imagem para o formato do zbar
    Image image(frame.cols, frame.rows, "Y800", (uchar *)gray.data, frame.cols * frame.rows);

    // Escaneia a imagem
    scanner.scan(image);

    // Abre o arquivo para adicionar os dados detectados
    ofstream arquivo(arquivo_saida, ios::app);

    // Itera sobre os símbolos detectados (se houver)
    for (Image::SymbolIterator symbol = image.symbol_begin(); symbol != image.symbol_end(); ++symbol) {
        string qr_data = symbol->get_data();
        cout << "QR Code detectado: " << qr_data << endl;

        // Salva o dado detectado no arquivo de texto
        arquivo << "QR Code Data: " << qr_data << "\n";

        // Desenha o contorno ao redor do código QR
        vector<Point> pts;
        for (int i = 0; i < symbol->get_location_size(); i++) {
            pts.push_back(Point(symbol->get_location_x(i), symbol->get_location_y(i)));
        }
        polylines(frame, pts, true, Scalar(0, 255, 0), 2);

        // Exibe o dado do QR Code na imagem
        putText(frame, qr_data, Point(pts[0].x, pts[0].y - 10), FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 255, 0), 2);
    }

    // Fecha o arquivo
    arquivo.close();
}

// Função principal para capturar o vídeo da câmera e processar objetos e QR Codes
void processar_camera_e_gravar(const string &arquivo_saida) {
    VideoCapture cap(0);  // Usa a webcam como fonte de vídeo
    if (!cap.isOpened()) {
        cout << "Erro ao abrir a webcam" << endl;
        return;
    }

    // Carrega a rede neural MobileNet SSD
    Net net = readNetFromCaffe(prototxt, model);

    // Cria ou limpa o arquivo de saída
    ofstream arquivo(arquivo_saida, ios::out);
    arquivo << "Detecções:\n";
    arquivo.close();

    while (true) {
        Mat frame;
        cap >> frame;  // Captura o frame da câmera
        if (frame.empty()) break;

        int altura = frame.rows;
        int largura = frame.cols;

        // Processa o frame com a rede neural MobileNet SSD
        Mat blob = blobFromImage(frame, 0.007843, Size(300, 300), 127.5);
        net.setInput(blob);
        Mat deteccao = net.forward();

        // Percorre as detecções
        for (int i = 0; i < deteccao.size[2]; ++i) {
            float probabilidade = deteccao.at<float>(0, 0, i, 2);
            if (probabilidade > 0.2) {
                int idx = static_cast<int>(deteccao.at<float>(0, 0, i, 1));
                float box[4] = {
                    deteccao.at<float>(0, 0, i, 3) * largura,
                    deteccao.at<float>(0, 0, i, 4) * altura,
                    deteccao.at<float>(0, 0, i, 5) * largura,
                    deteccao.at<float>(0, 0, i, 6) * altura
                };

                int iniciaX = static_cast<int>(box[0]);
                int iniciaY = static_cast<int>(box[1]);
                int finalizaX = static_cast<int>(box[2]);
                int finalizaY = static_cast<int>(box[3]);

                string label = CLASSES[idx] + ": " + to_string(probabilidade);
                rectangle(frame, Point(iniciaX, iniciaY), Point(finalizaX, finalizaY), Scalar(0, 255, 0), 2);
                putText(frame, label, Point(iniciaX, iniciaY - 10), FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 255, 0), 2);

                // Salva no arquivo
                ofstream arquivo(arquivo_saida, ios::app);
                arquivo << "Detectado: " << label << " em [" << iniciaX << ", " << iniciaY << ", " << finalizaX << ", " << finalizaY << "]\n";
                arquivo.close();
            }
        }

        // Processa QR Codes
        processa_qr_code(frame, arquivo_saida);

        // Mostra o frame processado
        imshow("Detecção de Objetos e Código QR", frame);

        // Pressione 's' para sair
        if (waitKey(1) == 's') break;
    }

    cap.release();
    destroyAllWindows();
}

int main() {
    // Arquivo de saída para as detecções e códigos QR
    string arquivo_de_saida = "detecoes_e_codigos_qr.txt";
    processar_camera_e_gravar(arquivo_de_saida);

    return 0;
}
