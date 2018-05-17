import machine
from machine import Pin, ADC
import pycom
from utime import sleep
import myNet

pycom.heartbeat(False)

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('Woke up from a deep sleep')
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

    # Wait for established connection:
    if not myNet.station.isconnected():
        myNet.WiFiConnect()

    print('Battery = {}V'.format(battConversion()))

    # Upload to ThingSpeak:
    # Blink for aesthetic touch ;)
    pycom.rgbled(0x0000FF)
    sleep(0.1)
    pycom.rgbled(0x000000)
    sleep(0.2)
    pycom.rgbled(0x0000FF)
    sleep(0.1)
    pycom.rgbled(0x000000)
    sleep(2)

    print('Attempting to publish data...')

    myNet.ThingSpeakUpload(battConversion())
    sleep(5)

    print('done!')

    myNet.client.disconnect()

    # Go to sleep for 10 minutes

    machine.deepsleep(600000)

# Otherwise we are in 'Config' and exit to REPL
print('Config Mode')
