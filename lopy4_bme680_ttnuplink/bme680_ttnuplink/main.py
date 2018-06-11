# lopy4_bme680_ttnuplink/bme680_ttnuplink/main.py

from machine import Pin
import radio
import sensor
import time

# Configure IO Pins:
configPin = Pin('P21', Pin.IN, Pin.PULL_UP) # Pull low to exit to REPL
LoRaPin = Pin('P22', Pin.IN, Pin.PULL_UP) # Pull low to enable LoRa

# initial read from IO pins (Reverse the logic for better readability later):
config = not configPin()
lora_on = not LoRaPin()

if config:
    radio.config()

if lora_on:
    radio.connect()
    radio.make_socket()

if not config and lora_on:
    while True:
        btemp, bpres, bhumi, bgas = sensor.get_data()

        radio.send_packet(btemp, bpres, bhumi, bgas)

        time.sleep(30)
