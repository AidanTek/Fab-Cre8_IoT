from machine import Pin, ADC
import utime
import struct
import binascii
from network import LoRa
import socket
import pycom

# Config pin:
configPin = Pin('P21', Pin.IN, Pin.PULL_UP)
radioPin = Pin('P22', Pin.IN, Pin.PULL_UP)

config = configPin()
radio = radioPin()

# LoRa setup:
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)

# Raw socket setup:
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

if config and not radio:
    s.setblocking(False)

    while True:
        # Listen on socket
        light = 0. # Light %
        temp = 0. # Temperature C
        humi = 0. # Humidity
        pres = 0. # Pressure
        gas = 0. # Gas

        data = s.recv(64)
        if data != b'':
            pycom.rgbled(0x00FF00)
            utime.sleep(0.2)
            pycom.rgbled(0x000000)
            utime.sleep(0.2)
            pycom.rgbled(0x00FF00)
            utime.sleep(0.2)
            pycom.rgbled(0x000000)
            utime.sleep(0.2)

            vals = data.split()

            light = str(vals[0], 'utf-8')
            temp = str(vals[1], 'utf-8')
            humi = str(vals[2], 'utf-8')
            pres = str(vals[3], 'utf-8')
            gas = str(vals[4], 'utf-8')

            print('Light = {}%, Temperature = {}C, Pressure = {}hPa, Humidity = {}RH, Gas = {}RES'.format(light, temp, humi, pres, gas))

        utime.sleep(1)
