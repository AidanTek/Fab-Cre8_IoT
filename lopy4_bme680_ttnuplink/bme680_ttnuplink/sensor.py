import bme680
from bme680.i2c import I2CAdapter
import time
import struct
import binascii

# Setup I2C and BME680: P9/G16=SDA, P10/G17=SCL
i2c_dev = I2CAdapter(1, pins=('P9','P10'), baudrate=100000)
sensor = bme680.BME680(i2c_device=i2c_dev)

# These oversampling settings can be tweaked to
# change the balance between accuracy and noise in
# the data.
sensor.set_humidity_oversample(bme680.OS_2X)
sensor.set_pressure_oversample(bme680.OS_4X)
sensor.set_temperature_oversample(bme680.OS_8X)
sensor.set_filter(bme680.FILTER_SIZE_3)

def get_data():
    if sensor.get_sensor_data():

        output = "{} C, {} hPa, {} RH, {} RES,".format(
            sensor.data.temperature,
            sensor.data.pressure,
            sensor.data.humidity,
            sensor.data.gas_resistance)

        print(output)

        temp = binascii.hexlify(struct.pack('f',sensor.data.temperature))
        pres = binascii.hexlify(struct.pack('f',sensor.data.pressure))
        humi = binascii.hexlify(struct.pack('f',sensor.data.humidity))
        gas = binascii.hexlify(struct.pack('f',sensor.data.gas_resistance))

        return(temp, pres, humi, gas)
