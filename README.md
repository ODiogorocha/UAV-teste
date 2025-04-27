# UAV Simulador

Simulador de UAVs (Veículos Aéreos Não Tripulados) desenvolvido em C++.

## Estrutura de Pastas

```plaintext
UAV-teste/
│
├── src/             # Códigos-fonte (.cpp)
│   ├── main.cpp
│   ├── uav.cpp
│   └── controlador.cpp
│
├── include/         # Cabeçalhos (.h)
│   ├── uav.h
│   └── controlador.h
│
├── bin/             # Executáveis ficam aqui
│
├── Makefile         # Arquivo de automação de build
│
└── README.md        # Instruções e documentação do projeto
```

## Como Compilar e Executar

### 1. Abra o terminal na raiz do projeto

```bash
cd UAV-teste
```

### 2. Compile com `make`

```bash
make
```

O compilador (`g++`) vai gerar o executável no diretório `bin/`.

### 3. Execute o simulador

```bash
./bin/uav_simulator
```

### 4. Para limpar os arquivos compilados

```bash
make clean
```

Isso remove todos os arquivos `.o` e o executável para deixar o projeto limpo.

## Makefile Explicado

```makefile
# Nome do executável
TARGET = bin/uav_simulator

# Compilador
CC = g++

# Flags de compilação
CFLAGS = -Wall -g -Iinclude

# Arquivos fonte e objetos
SOURCES = $(wildcard src/*.cpp)
OBJECTS = $(SOURCES:src/%.cpp=src/%.o)

# Compilação padrão
all: $(TARGET)

$(TARGET): $(OBJECTS)
	$(CC) $(CFLAGS) -o $@ $(OBJECTS)

src/%.o: src/%.cpp include/%.h
	$(CC) $(CFLAGS) -c $< -o $@

# Limpar build
clean:
	rm -f src/*.o $(TARGET)
```

- `-Iinclude`: Informa ao compilador onde estão os cabeçalhos `.h`.
- `-Wall`: Ativa todos os avisos durante a compilação.
- `-g`: Gera informações de debug para uso com ferramentas como o gdb.

## Requisitos

- g++ (Compilador C++)
- make (Automação de build)

Instalação no Ubuntu:

```bash
sudo apt update
sudo apt install g++ make
```

## Observações Importantes

- Sempre coloque novos arquivos `.cpp` dentro da pasta `src/`.
- Sempre coloque novos arquivos `.h` dentro da pasta `include/`.
- O Makefile já está preparado para compilar automaticamente qualquer novo código que for adicionado.

## Extras (opcional)

- Utilizar o VS Code com a extensão C/C++ para autocomplete e debug.
- Rodar o executável com `gdb` para depuração:

```bash
gdb ./bin/uav_simulator
```
- Criar testes automatizados usando frameworks como GoogleTest.

---

