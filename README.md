# 🔐 Fechadura Eletrônica com ESP32 e RFID

Este projeto implementa uma **fechadura eletrônica com ESP32**, utilizando um **leitor RFID MFRC522** e um **servo motor** para simular o mecanismo de travamento. O sistema permite o cadastro, validação e exclusão de tags RFID autorizadas, armazenando as permissões diretamente na **EEPROM**, garantindo persistência mesmo após reinicializações.

---

## ⚙️ Funcionalidades

- 📗 Leitura de cartões RFID (13.56 MHz)
- ✅ Validação de acesso com base em tags autorizadas
- ➕ Cadastro de novas tags via tag mestre
- ➖ Remoção de tags da memória
- 🔐 Abertura da “fechadura” com servo motor SG90
- 💾 Armazenamento persistente em EEPROM
- 🔊 Feedback visual e sonoro (LEDs e buzzer)
- 🔁 Reset total com botão ou tag mestre

---

## 🧰 Componentes Utilizados

- ESP32 DevKit V1
- MFRC522 RFID Reader
- Tags RFID (cartão e chaveiro)
- Servo motor SG90
- Buzzer piezoelétrico
- LEDs (verde e vermelho)
- Push-button
- Jumpers e protoboard

---

## 🧠 Bibliotecas Necessárias

- `MFRC522`
- `SPI`
- `Servo`
- `EEPROM`

Todas disponíveis na **Arduino IDE**.

---

## 🔌 Esquema de Ligações

| Componente | ESP32 (GPIO) |
|------------|--------------|
| SDA (RFID) | 21           |
| SCK        | 18           |
| MOSI       | 23           |
| MISO       | 19           |
| RST        | 22           |
| Servo      | 27 (exemplo) |
| Buzzer     | 26 (exemplo) |
| LED Verde  | 32           |
| LED Verm.  | 33           |
| Botão      | 25           |

---

## 🚀 Como Executar

1. Instale a Arduino IDE e o pacote do ESP32.
2. Instale as bibliotecas mencionadas acima.
3. Conecte os componentes conforme o esquema.
4. Altere o código para definir uma **tag mestre** no início.
5. Compile e envie para o ESP32.
6. Acompanhe a leitura pelo **Monitor Serial** (baud: 115200).

---

## 🖼️ Imagens (adicione em `/images`)

- `images/prototipo.jpg` — Foto real do projeto montado.
- `images/esquema_bb.png` — Esquema eletrônico (Fritzing).

---

## 📈 Melhorias Futuras

- Interface web para gerenciamento remoto
- Registro de logs via Wi-Fi ou SD card
- Autenticação por múltiplos fatores (RFID + senha)
- Integração com app mobile via Bluetooth

---

## 📄 Licença

Este projeto está licenciado sob a **Licença MIT**. Consulte o arquivo [LICENSE](LICENSE) para mais detalhes.

---

## 🤝 Contribuição

Contribuições são bem-vindas! Sinta-se livre para abrir issues, pull requests ou sugerir melhorias.

---

## 👤 Autor

**Eduardo Sato**  
🔗 [LinkedIn](https://www.linkedin.com/in/eduardosato)  
📁 [Repositório no GitHub](https://github.com/EduardoSato22)

