import machine
import network
import utime
import urequests
import ujson
import ubinascii
from machine import SPI, Pin, I2C, PWM
from umqtt.simple import MQTTClient
from mfrc522 import MFRC522
from i2c_lcd import I2cLcd

# Conecta ao WiFi
print("Conectando ao WiFi", end="")
estacao = network.WLAN(network.STA_IF)
estacao.active(True)
estacao.connect('Eduardo', 'leticia01')
while not estacao.isconnected():
    print(".", end="")
    utime.sleep(0.1)
print(" Conectado!")

# Configuração do MQTT
MQTT_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Gera ID único
MQTT_BROKER = "broker.mqttdashboard.com"                 # Endereço do broker
MQTT_USER = ""                                           # Usuário (caso possua)
MQTT_PASSWORD = ""
MQTT_TOPIC = "rele/trava"                                # Tópico MQTT
mqtt_topic = MQTT_TOPIC

# Configuração do rele
rele_pin = machine.Pin(25, machine.Pin.OUT)

# Configuração do buzzer
buzzer_pin = machine.Pin(13, machine.Pin.OUT)
buzzer = PWM(buzzer_pin)

# Configuração dos LEDs
led_verde_pin = machine.Pin(26, machine.Pin.OUT)
led_vermelho_pin = machine.Pin(12, machine.Pin.OUT)

# Configuração do LCD
I2C_ADDR = 0x27
i2c = I2C(scl=Pin(22), sda=Pin(21), freq=400000)  # Conecta scl ao GPIO 22, sda ao GPIO 21
lcd = I2cLcd(i2c, I2C_ADDR, 2, 16)

# Função para emitir som no buzzer
def emitir_som(frequencia, duracao):
    buzzer.freq(frequencia)
    buzzer.duty(512)  # 50% duty cycle
    utime.sleep(duracao)
    buzzer.duty(0)

# Função para acionar o rele
def acionar_rele():
    rele_pin.value(1)
    led_verde_pin.value(1)
    led_vermelho_pin.value(0)
    lcd.clear()
    lcd.putstr("Ligado (Aberta)")
    emitir_som(1000, 0.2)  # Som de desbloqueio

# Função para desligar o rele
def desligar_rele():
    rele_pin.value(0)
    led_verde_pin.value(0)
    led_vermelho_pin.value(1)
    lcd.clear()
    lcd.putstr("Desligado (Fechada)")
    emitir_som(500, 0.2)  # Som de bloqueio

# Função que será chamada quando o ESP receber uma mensagem
def obter_mensagem(topico, mensagem):
    print("\n")
    print("Tópico recebido: %s" % (topico))
    print("Mensagem recebida: %s" % (mensagem))
    print("\n")

    if mensagem == b'ligar':
        print("Ligando rele")
        acionar_rele()
        client.publish(mqtt_topic, "ativado")

    elif mensagem == b'desligar':
        print("Desligando rele")
        desligar_rele()
        client.publish(mqtt_topic, "desativado")

    else:
        print("Mensagem não reconhecida")

# Configuração do RFID
spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)

rfid_name = ["Pai", "Mae", "Filho", "Filha"]
rfid_uid = ["0x0bb3052e", "0xe7458e7a", "0x2907b498", "0x29eec498"]

MASTER_CARD_UID = "0x0bb3052e"  # Substitua pelo UID do seu cartão mestre
cadastro_modo = False  # Modo de cadastro/desativação

def get_username(uid):
    try:
        index = rfid_uid.index(uid)
        return rfid_name[index]
    except ValueError:
        print("RFID não reconhecido")
        return None

def cadastrar_desativar_cartao(uid):
    global cadastro_modo
    if cadastro_modo:
        if uid in rfid_uid:
            index = rfid_uid.index(uid)
            print("Cartão removido: ", uid)
            lcd.clear()
            lcd.putstr("Cartao removido")
            rfid_uid.pop(index)
            rfid_name.pop(index)
        else:
            rfid_uid.append(uid)
            rfid_name.append("Usuario{}".format(len(rfid_uid)))
            print("Cartão cadastrado: ", uid)
            lcd.clear()
            lcd.putstr("Cartao cadastrado")
        cadastro_modo = False

# Função para verificar RFID
def verificar_rfid():
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            card_id = "0x%02x%02x%02x%02x" % (raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            print("UID:", card_id)
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("RFID: ")
            lcd.putstr(card_id)

            if card_id == MASTER_CARD_UID:
                global cadastro_modo
                cadastro_modo = True
                print("Cartão mestre reconhecido")
                lcd.clear()
                lcd.putstr("Cartao mestre")
                lcd.move_to(0, 1)
                lcd.putstr("reconhecido")
                utime.sleep(2)
                return

            if cadastro_modo:
                cadastrar_desativar_cartao(card_id)
                return

            username = get_username(card_id)
            lcd.move_to(0, 1)
            if username:
                led_verde_pin.value(1)
                led_vermelho_pin.value(0)
                lcd.putstr("Bem-vindo {}".format(username))
                acionar_rele()
                utime.sleep(5)  # Mantenha o relé acionado por 5 segundos
                desligar_rele()
            else:
                led_verde_pin.value(0)
                led_vermelho_pin.value(1)
                lcd.putstr("Acesso negado!")
                emitir_som(2000, 0.5)  # Som de acesso negado

# Conecta ao broker MQTT
print("Conectando ao servidor MQTT... ", end="")
client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, user=MQTT_USER, password=MQTT_PASSWORD)
client.set_callback(obter_mensagem)
client.connect()
client.subscribe(MQTT_TOPIC)
print(" Conectado!")

# Inicializa o estado do relé e LED
desligar_rele()

print("Aproxime o cartão")
lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("Aproxime o cartao")

while True:
    # Verifica se há novas mensagens MQTT
    client.check_msg()

    # Verifica se um cartão RFID autorizado é lido
    verificar_rfid()

    utime.sleep(0.1)
