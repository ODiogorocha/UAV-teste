# Sistema de Controle de Movimento de Drone e Leitura de Códigos de Barras e QR Code

Este repositório contém um conjunto de módulos Python projetados para controle de movimento de drones e detecção de códigos de barras e QR codes utilizando feeds de câmeras. O sistema utiliza tecnologias como OpenCV, MediaPipe, Pyzbar e código personalizado para atingir seus objetivos. Os principais componentes deste repositório incluem módulos para controlar o drone, ler códigos de barras e QR codes, e interagir com a câmera.

## Funcionalidades

- **Movimento do Drone**: Controle programático dos movimentos do drone (frente, trás, esquerda, direita, subir, descer, etc.).
- **Interface de Câmera**: Captura de vídeo em tempo real usando uma webcam ou câmera conectada para processamento posterior.
- **Leitor de Códigos de Barras**: Detecção e decodificação de códigos de barras em tempo real, com registro dos códigos detectados e seus carimbos de data e hora.
- **Leitor de QR Codes**: Detecção e decodificação de QR codes, exibindo as informações relevantes.
- **Feedback em Tempo Real**: Exibição da taxa de FPS e feedback ao vivo tanto da leitura de códigos de barras e QR codes quanto do movimento do drone na tela.

## Requisitos

Para executar este projeto, você precisa das seguintes dependências:

- Python 3.x
- OpenCV (`opencv-python`)
- Pyzbar (`pyzbar`)
- MediaPipe (`mediapipe`)
- SDK do Drone (para controle do drone, como o `dronekit`)

Você pode instalar os pacotes necessários usando o `pip`:

```bash
pip install opencv-python mediapipe pyzbar dronekit
```

## Estrutura do Projeto

O projeto está organizado em módulos para maior clareza e facilidade de uso:

```bash
seu_projeto/
│
├── seu_pacote_nome/
│   ├── __init__.py       # Arquivo de inicialização do pacote
│   ├── camera.py         # Módulo de controle da câmera
│   ├── drone_movement.py # Módulo de controle do movimento do drone
│   ├── read_barcode.py   # Módulo de leitura de códigos de barras
│   └── read_qrcode.py    # Módulo de leitura de QR codes
│
├── main.py               # Script principal que executa o sistema
└── README.md             # Documentação do projeto
```

### Descrição dos Módulos:

- **camera.py**: Contém funcionalidades para interface com a câmera, captura de frames de vídeo e passagem desses frames para outros módulos para processamento.
- **drone_movement.py**: Controla o movimento do drone baseado em entradas (por exemplo, para frente, para trás, para a esquerda, para a direita).
- **read_barcode.py**: Utiliza `pyzbar` para ler e decodificar códigos de barras a partir do feed da câmera. Os dados dos códigos de barras detectados são registrados em um arquivo de texto com carimbos de data e hora.
- **read_qrcode.py**: Semelhante à leitura de códigos de barras, mas foca na decodificação de QR codes a partir do feed da câmera.

## Como Usar

1. **Executar o Sistema**: Para rodar o sistema, execute o arquivo `main.py`. Isso iniciará a câmera e começará o processamento tanto de códigos de barras quanto de QR codes, além de controlar o drone.

   ```bash
   python main.py
   ```

2. **Controle do Drone**: O movimento do drone pode ser controlado programaticamente dentro do módulo `drone_movement.py`. A lógica principal para controlar o drone deve ser invocada dentro do arquivo `main.py`.

3. **Leitura de Códigos de Barras e QR Codes**: Tanto o processamento de códigos de barras quanto o de QR codes são feitos utilizando a entrada da câmera, e os resultados são exibidos e registrados em tempo real. Os dados dos códigos de barras serão salvos em um arquivo chamado `detected_barcodes.txt`.

4. **Sair**: Para sair do sistema, pressione a tecla `q` na janela da câmera.

## Exemplo de Fluxo de Trabalho

- O sistema inicializa a câmera e começa a processar os frames.
- Códigos de barras e QR codes encontrados no feed da câmera serão decodificados e os resultados serão exibidos na tela.
- Os dados dos códigos de barras detectados serão registrados em um arquivo de texto com carimbos de data e hora.
- Simultaneamente, os movimentos do drone podem ser controlados conforme necessário.

## Contribuindo

Aceitamos contribuições para melhorar este projeto! Aqui estão algumas formas de contribuir:

- Corrigir bugs ou melhorar a legibilidade do código.
- Adicionar novas funcionalidades ou estender as existentes.
- Melhorar a documentação e exemplos.

### Passos para contribuir:
1. Faça um fork do repositório.
2. Crie uma nova branch para sua funcionalidade ou correção.
3. Envie um pull request com uma explicação clara das suas mudanças.


## Agradecimentos

- **OpenCV**: Para operações de visão computacional, como leitura de frames de vídeo.
- **MediaPipe**: Para detecção de mãos e poses no módulo de controle do drone.
- **Pyzbar**: Para leitura de códigos de barras e QR codes.
- **DroneKit**: Para controle do movimento do drone.

Para mais informações sobre qualquer um dos módulos ou bibliotecas usadas, consulte a documentação oficial:
- [Documentação OpenCV](https://docs.opencv.org/)
- [Documentação MediaPipe](https://google.github.io/mediapipe/)
- [Documentação Pyzbar](https://pyzbar.readthedocs.io/)
- [Documentação DroneKit](http://python.dronekit.io/)

---

Para quaisquer dúvidas ou problemas, fique à vontade para abrir um issue no repositório.
```

---

### Explicação das Seções do `README.md`:

1. **Visão Geral do Projeto**: Descreve as funcionalidades principais e objetivos do projeto.
2. **Requisitos**: Lista as dependências necessárias e como instalá-las.
3. **Estrutura do Projeto**: Fornece uma explicação clara da estrutura do repositório para ajudar os usuários a entenderem o layout do código.
4. **Como Usar**: Instruções sobre como rodar o sistema, controlar o drone e processar códigos de barras e QR codes.
5. **Contribuindo**: Oferece diretrizes para quem deseja contribuir com o projeto.
6. **Licença**: Esclarece as permissões de uso e contribuições sob a Licença MIT.
7. **Agradecimentos**: Cita as bibliotecas e ferramentas usadas no projeto e fornece links para as documentações oficiais.

Este `README.md` fornece uma visão geral clara e profissional do repositório, além de guiar os usuários na instalação, uso e contribuição para o projeto.