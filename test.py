# More details can be found in TechToTinker.blogspot.com 
# George Bantique | tech.to.tinker@gmail.com

from mfrc522 import MFRC522
from i2c_lcd import I2cLcd
from machine import Pin
from machine import SoftI2C
from machine import SPI

DEFAULT_I2C_ADDR = 0x27
i2c = SoftI2C(scl=Pin(22, Pin.OUT, Pin.PULL_UP),
              sda=Pin(21, Pin.OUT, Pin.PULL_UP),
              freq=400000) 
lcd = I2cLcd(i2c, DEFAULT_I2C_ADDR, 2, 16)

red = Pin(14, Pin.OUT)
grn = Pin(13, Pin.OUT)

spi = SPI(2, baudrate=2500000, polarity=0, phase=0)
# Using Hardware SPI pins:
#     sck=18   # yellow
#     mosi=23  # orange
#     miso=19  # blue
#     rst=4    # white
#     cs=5     # green, DS
# *************************
# To use SoftSPI,
# from machine import SOftSPI
# spi = SoftSPI(baudrate=100000, polarity=0, phase=0, sck=sck, mosi=mosi, miso=miso)
spi.init()
rdr = MFRC522(spi=spi, gpioRst=4, gpioCs=5)

rfid_name = ["Teacher1",
             "Teacher2",
             "Student1",
             "Student2",
             "Student3"]
rfid_uid = ["0x0bb3052e",
            "0xe7458e7a",
            "0x2907b498",
            "0x29eec498",
            "0x59e1f097"]

def get_username(uid):
    index = 0
    try:
        index = rfid_uid.index(uid)
        return rfid_name[index]
    except:
        index = -1
        print("RFID is not recognized")
        return 0

print("Place card")

lcd.clear()
lcd.move_to(0, 0)
lcd.putstr("Scan RFID")

while True:
    (stat, tag_type) = rdr.request(rdr.REQIDL)
    if stat == rdr.OK:
        (stat, raw_uid) = rdr.anticoll()
        if stat == rdr.OK:
            lcd.clear()
            lcd.move_to(0, 0)
            lcd.putstr("RFID: ")
            
            card_id = "0x%02x%02x%02x%02x" %(raw_uid[0], raw_uid[1], raw_uid[2], raw_uid[3])
            print("UID:", card_id)
            lcd.putstr(card_id)

            username = get_username(card_id)
            lcd.move_to(0, 1)
            if username != 0:
                grn.value(True)
                red.value(False)
                lcd.putstr("Welcome {}".format(username))
            else:
                grn.value(False)
                red.value(True)
                lcd.putstr(" Access Denied! ")
