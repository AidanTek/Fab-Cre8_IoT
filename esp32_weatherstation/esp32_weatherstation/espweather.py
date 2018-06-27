from machine import Pin, I2C, deepsleep
import utime
from bme280 import BME280
from apds9960.const import *
from apds9960 import uAPDS9960 as APDS9960
import myNet

i2c = I2C(scl=Pin(0), sda=Pin(4))
bme = BME280(i2c=i2c)
apds = APDS9960(i2c)

led = Pin(22, Pin.OUT)
configPin = Pin(2, Pin.IN, Pin.PULL_UP)

apds.enableLightSensor()
utime.sleep(2) # allow sensor to init
def get_sensors():
    temperature, pressure, humidity = bme.read_compensated_data()
    light = apds.readAmbientLight()
    temperature = temperature / 100
    pressure = pressure / 256
    humidity = humidity / 1024
    return temperature, pressure, humidity, light

configMode = not configPin.value()

while not configMode:
    configMode = not configPin.value()

    if not myNet.station.isconnected():
        myNet.WiFiConnect()

    temp, pres, humi, light = get_sensors()
    print('Temperature = {} C || Pressure = {} Pa || humidity = {} % || light = {}lux'.format(
    temp, pres, humi, light))
    utime.sleep(10)

    myNet.ThingSpeakUpload(temp, pres, humi, light)

    utime.sleep(5)

    myNet.client.disconnect()
    myNet.station.disconnect()

    # Blink the LED to indicate a new reading:
    led.value(0)
    utime.sleep(0.2)
    led.value(1)
    utime.sleep(0.2)
    led.value(0)
    utime.sleep(0.2)
    led.value(1)
    utime.sleep(0.2)

    # deepsleep for 60 seconds
    deepsleep(60000)

    if configMode:
        myNet.debugs()
