# v2 Seedling Monitor for MicroPython on the ESP32
# Hardware involves a Lolin32 Lite with a ORP12 LDR and a DHT11 sensor
# ThingSpeak or Adafruit.io to be implemented.
#
# Script by Aidan Taylor, Fab-Cre8 2018

from machine import Pin, ADC
from dht import DHT11
import time

print("Seedling Environment Monitor by Aidan Taylor")
print("v1.2 2018. Fab-Cre8\n")

import myNet

# Hardware object setup:
led = Pin(22, Pin.OUT) # on board LED on pin 22
ldr = ADC(Pin(35)) # LDR has a 75k pullup resistor which seems good
dSens = DHT11(Pin(17))

print("setup complete, starting loop...\n\n\n")

while True:
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

    # rest for 30 seconds - would be good to try low power?
    time.sleep(900)

myNet.client.disconnect()
