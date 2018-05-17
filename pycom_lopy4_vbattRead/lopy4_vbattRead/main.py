import machine
from machine import Pin, ADC
import pycom
from utime import sleep

pycom.heartbeat(False)

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('Woke from a deep sleep')
else:
    print('Power on or hard reset')

adc = ADC()

# Config pin:
configPin = Pin('P21', Pin.IN, Pin.PULL_UP)

# vbatt pin:
vbatt = adc.channel(attn=1, pin='P16')

def battConversion():
    adcVoltage = vbatt()
    voltage = adcVoltage*3*1.334/4095

    return voltage

# Check for config mode:
configPin()

if configPin():
    while True:
        print('Battery = {}V'.format(battConversion()))

        # Do something
        pycom.rgbled(0x0000FF)
        sleep(0.1)
        pycom.rgbled(0x000000)
        sleep(0.2)
        pycom.rgbled(0x0000FF)
        sleep(0.1)
        pycom.rgbled(0x000000)
        sleep(2)

            # Go to sleep for 10 seconds

    # machine.deepsleep(600000)

print('Config Mode')
