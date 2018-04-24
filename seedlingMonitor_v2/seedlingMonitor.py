# v1.4 Seedling Monitor for MicroPython on the ESP32
#
# Hardware involves a Lolin32 Pro with a ORP12 LDR and a BME280 sensor
# Data is sent to the ThingSpeak MQTT broker, please see myNet.py
#
# The ESP32 is put into deepsleep for 15 minutes after every upload
# - this should go a long way to conserving battery life!
#
# Because it can be hard to catch the ESP32 before it goes into deepsleep, a
# jumper wire on GPIO2 to ground kills the script, so you can reprogram.
#
# Script by Aidan Taylor, Fab-Cre8. 2018
# BME280 and umqtt libraries are used. See the BME280.py file for license, umqtt
# is part of the micropython libraries provided under the MIT license.

from machine import Pin, ADC, I2C, deepsleep
from bme280 import BME280
import time

print("Seedling Environment Monitor by Aidan Taylor")
print("v1.5 2018. Fab-Cre8\n")

import myNet

# Hardware object setup:
led = Pin(5, Pin.OUT) # on board LED on pin 5 (active LOW)
ks = Pin(2, Pin.IN, Pin.PULL_UP) # killswitch pin, tie to gnd to stop loop
# ldr BIAS resistor is set as 56k - should test for range to calibrate
ldr = ADC(Pin(35))
BMEEn = Pin(16, Pin.OUT) # EXPERIMENTAL power the BME280 from a GPIO pin
ldrEn = Pin(17, Pin.OUT) # EXPERIMENTAL Bias the from a GPIO pin
i2c = I2C(scl=Pin(0), sda=Pin(4))
sensor = BME280(i2c=i2c)

print("setup complete, starting loop...\n\n\n")

configMode = ks.value()

# note internal LED will stay on when in configMode

while configMode:
    configMode = ks.value()

    if not myNet.station.isconnected():
        myNet.WiFiConnect()

    # EXPERIMENTAL activate the BME & ldr
    BMEEn.value(1)
    ldrEn.value(1)

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

    # Read BME280
    temperature, pressure, humidity = sensor.read_compensated_data()
    temperature = temperature / 100
    pressure = pressure / 256
    humidity = humidity / 1024


    # Print the values:
    print("Light Level = {}%".format(LgtLv))
    print('Temperature = {} C || Pressure = {} Pa || humidity = {} %'.format(temperature, pressure, humidity))

    myNet.ThingSpeakUpload(LgtLv, temperature, pressure, humidity)

    time.sleep(5) # A little time is needed to allow for the upload

    myNet.client.disconnect()

    # Try disconnecting WiFi to save on power - EXPERIMENTAL
    myNet.station.disconnect()

    # EXPERIMENTAL deactivate the BME280 and ldr bias
    BMEEn.value(0)
    ldrEn.value(0)

    # deepsleep for 15 minutes (900000)
    deepsleep(900000)
