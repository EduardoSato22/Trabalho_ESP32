🔐 Descrição
Este projeto implementa uma fechadura eletrônica com ESP32 utilizando um leitor RFID MFRC522, permitindo controlar o acesso via tags RFID previamente cadastradas. O sistema valida as tags lidas e, se autorizadas, aciona um servo motor que simula a abertura da fechadura. Também inclui recursos como cadastro e remoção de tags, armazenamento em EEPROM, e feedback via buzzer e LED.

📦 Tecnologias e Componentes
ESP32 DevKit v1

Leitor RFID MFRC522

Tags RFID (13.56 MHz)

Servo motor SG90

Buzzer piezoelétrico

LEDs indicadores

EEPROM (armazenamento das tags autorizadas)

Arduino IDE com bibliotecas:

MFRC522

Servo

EEPROM

SPI

⚙️ Funcionalidades
📗 Leitura de tags RFID

🔐 Validação contra tags autorizadas

✅ Acionamento do servo motor para simular abertura

🧠 Armazenamento das tags em memória EEPROM

➕ Modo de cadastro de novas tags

➖ Modo de exclusão de tags

🔊 Sinalização via buzzer e LED

🔄 Reset de memória via botão (ou tag mestre)

📁 Estrutura de Diretórios
bash
Copiar
Editar
Trabalho_ESP32/
├── src/
│   └── main.ino            # Código principal do projeto
├── images/
│   ├── esquema_bb.png      # Esquema de ligação (Fritzing ou similar)
│   └── prototipo.jpg       # Foto real do circuito
├── docs/
│   └── funcionamento.md    # Detalhes do funcionamento interno
├── data/                   # EEPROM dump ou dados extras
├── README.md
└── LICENSE
🔌 Esquema de Ligação (MFRC522 com ESP32)
MFRC522	ESP32 (GPIO)
SDA	D21
SCK	D18
MOSI	D23
MISO	D19
RST	D22
3.3V	3.3V
GND	GND

Obs: pinos podem variar, confirme no código #define.

🧪 Como Usar
1. ⚙️ Instalação
Instale a Arduino IDE

Instale as bibliotecas via Gerenciador de Bibliotecas:

MFRC522

Servo

EEPROM (já incluída)

Configure a placa como ESP32 Dev Module

2. 🛠️ Upload e Teste
Conecte o ESP32 via USB

Altere o código para definir uma tag mestre

Envie para o ESP32

No monitor serial (baud: 115200), acompanhe as leituras

3. 🧾 Cadastro de Tags
Aproxime a tag mestre

Entre no modo de cadastro

Aproxime as novas tags

Use o botão físico ou comandos via Serial para salvar

📸 Imagens do Projeto

Protótipo com ESP32, leitor RFID, servo e LED.


Esquema de ligação no Fritzing.

🔐 Segurança
Tags armazenadas na EEPROM permanecem após reboot

Sistema só responde a tags autorizadas

Pode-se configurar um “modo manutenção” com botão físico

🧠 Melhorias Futuras
Interface web para cadastro/remoção de tags

Integração com banco de dados via Wi-Fi

Autenticação multifatorial (RFID + senha)

Log de acessos em tempo real

📄 Licença
Este projeto está licenciado sob a MIT License – veja o arquivo LICENSE para detalhes.
