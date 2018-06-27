from machine import Pin
import utime
import myNet

led = Pin(5, Pin.OUT)
configPin = Pin(2, Pin.IN, Pin.PULL_UP)

configMode = not configPin.value()

while not configMode:
    configMode = not configPin.value()

    if not myNet.station.isconnected():
        myNet.WiFiConnect()

    myNet.ThingSpeakDownload()

    led.value(0)
    utime.sleep(0.2)
    led.value(1)
    utime.sleep(0.2)
    led.value(0)
    utime.sleep(0.2)
    led.value(1)

    utime.sleep(10)

if configMode:
    myNet.debugs()
