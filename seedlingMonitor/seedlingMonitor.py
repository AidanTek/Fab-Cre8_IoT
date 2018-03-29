# v1.3 Seedling Monitor for MicroPython on the ESP32
#
# Hardware involves a Lolin32 Lite with a ORP12 LDR and a DHT11 sensor
# Data is sent to the ThingSpeak MQTT broker, please see myNet.py
#
# The ESP32 is put into deepsleep for 15 minutes after every upload
# - this should go a long way to conserving battery life!
#
# Because it can be hard to catch the ESP32 before it goes into deepsleep, a
# jumper wire on GPIO2 to ground kills the script, so you can reprogram.
#
# Script by Aidan Taylor, Fab-Cre8. 2018

from machine import Pin, ADC, deepsleep
from dht import DHT11
import time

print("Seedling Environment Monitor by Aidan Taylor")
print("v1.3 2018. Fab-Cre8\n")

import myNet

# Hardware object setup:
led = Pin(22, Pin.OUT) # on board LED on pin 22
ks = Pin(2, Pin.IN, Pin.PULL_UP) # killswitch pin, tie to gnd to stop loop
# Todo - try different resistor value for LDR, between 47k and 75k, maybe trim?
ldr = ADC(Pin(35))
dSens = DHT11(Pin(17))

print("setup complete, starting loop...\n\n\n")

configMode = ks.value()

# note internal LED will stay on when in configMode

while configMode:
    configMode = ks.value()

    if not myNet.station.isconnected():
        myNet.WiFiConnect()

    # Blink the LED to indicate a new reading:
    led.value(0)
    time.sleep(0.2)
    led.value(1)
    time.sleep(0.2)
    led.value(0)
    time.sleep(0.2)
    led.value(1)
    time.sleep(0.2)

    # Perform LDR Conversion:
    LgtLv = ((4095 - ldr.read())/4095)*100

    # Read DHT11
    dSens.measure()

    # Print the values:
    print("Light Level = {}%".format(LgtLv))
    print("Temperature = {}C".format(dSens.temperature()))
    print("Humidity = {}%\n".format(dSens.humidity()))

    myNet.ThingSpeakUpload(LgtLv, dSens.temperature(), dSens.humidity())

    time.sleep(5) # A little time is needed to allow for the upload

    myNet.client.disconnect()

    # Try disconnecting WiFi to save on power - EXPERIMENTAL
    myNet.station.disconnect()

    # deepsleep for 15 minutes
    deepsleep(900000)
