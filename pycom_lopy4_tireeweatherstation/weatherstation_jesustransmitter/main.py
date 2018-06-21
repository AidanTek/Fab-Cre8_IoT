import bme680
from bme680.i2c import I2CAdapter
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

# Setup I2C and BME680: P9/G16=SDA, P10/G17=SCL
i2c_dev = I2CAdapter(1, pins=('P9','P10'), baudrate=100000)
sensor = bme680.BME680(i2c_device=i2c_dev)

# LDR setup
adc = ADC()
ldr = adc.channel(pin='P13')

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

config = configPin()
radio = radioPin()

# LoRa setup:
lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)

# Raw socket setup:
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

if config and not radio:
    while True:
        if sensor.get_sensor_data():
            lgtlv = ((ldr()/4095)*100) # Perform LDR Conversion:

            output = "{}%, {} C, {} hPa, {} RH, {} RES".format(
                lgtlv,
                sensor.data.temperature,
                sensor.data.pressure,
                sensor.data.humidity,
                sensor.data.gas_resistance)

            print(output)

            light = binascii.hexlify(struct.pack('f',lgtlv))
            temp = binascii.hexlify(struct.pack('f',sensor.data.temperature))
            pres = binascii.hexlify(struct.pack('f',sensor.data.pressure))
            humi = binascii.hexlify(struct.pack('f',sensor.data.humidity))
            gas = binascii.hexlify(struct.pack('f',sensor.data.gas_resistance))

            packet = ('{} {} {} {} {}'.format(lgtlv,
            sensor.data.temperature,
            sensor.data.pressure,
            sensor.data.humidity,
            sensor.data.gas_resistance))

            s.send(packet)
            pycom.rgbled(0x0000FF)
            utime.sleep(0.2)
            pycom.rgbled(0x000000)
            utime.sleep(0.2)
            pycom.rgbled(0x0000FF)
            utime.sleep(0.2)
            pycom.rgbled(0x000000)
            utime.sleep(0.6)

            utime.sleep(10)
