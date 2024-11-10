#include <iostream>
#include <fstream>
#include <opencv2/opencv.hpp>
#include <zbar.h>
#include <ctime>

using namespace std;
using namespace cv;
using namespace zbar;

// Função para obter a data e hora atuais
string obter_data_hora() {
    time_t now = time(0);
    tm *ltm = localtime(&now);
    char buffer[30];
    strftime(buffer, sizeof(buffer), "%Y-%m-%d %H:%M:%S", ltm);
    return string(buffer);
}

// Função para processar e interpretar o código de barras e salvar no arquivo
Mat processa_codigo_de_barras(const Mat &frame, const string &arquivo_saida) {
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
        string codigo_data = symbol->get_data();
        cout << "Código de Barras detectado: " << codigo_data << endl;

        // Salva o dado detectado no arquivo de texto com data e hora
        arquivo << obter_data_hora() << ": Código de Barras detectado: " << codigo_data << "\n";

        // Desenha o contorno ao redor do código de barras
        vector<Point> pts;
        for (int i = 0; i < symbol->get_location_size(); i++) {
            pts.push_back(Point(symbol->get_location_x(i), symbol->get_location_y(i)));
        }
        polylines(frame, pts, true, Scalar(0, 255, 0), 2);

        // Exibe o dado do código de barras na imagem
        putText(frame, codigo_data, Point(pts[0].x, pts[0].y - 10), FONT_HERSHEY_SIMPLEX, 0.5, Scalar(0, 255, 0), 2);
    }

    // Fecha o arquivo
    arquivo.close();

    return frame;
}

// Função principal para capturar o vídeo da câmera e ler códigos de barras
void processar_camera() {
    VideoCapture cap(0); // Usa a webcam como fonte de vídeo
    string arquivo_saida = "codigos_detectados.txt";

    if (!cap.isOpened()) {
        cout << "Erro ao acessar a câmera." << endl;
        return;
    }

    // Cria ou limpa o arquivo de saída
    ofstream arquivo(arquivo_saida, ios::out);
    arquivo << "Histórico de Códigos de Barras Detectados:\n";
    arquivo.close();

    while (true) {
        Mat frame;
        cap >> frame; // Captura o frame da câmera
        if (frame.empty()) break;

        // Processa o frame da câmera para decodificar códigos de barras
        frame = processa_codigo_de_barras(frame, arquivo_saida);

        // Mostra o frame com o código de barras detectado, se houver
        imshow("Leitura de Código de Barras", frame);

        // Pressione 'q' para sair
        if (waitKey(1) == 'q') break;
    }

    // Libera a câmera
    cap.release();
    destroyAllWindows();
}

int main() {
    processar_camera();
    return 0;
}
