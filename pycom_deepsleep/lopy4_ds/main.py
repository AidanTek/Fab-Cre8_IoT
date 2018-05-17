import machine
from machine import Pin
import pycom
from utime import sleep

# Config pin:
configPin = Pin('P21', Pin.IN, Pin.PULL_UP)

pycom.heartbeat(False)

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('Woke from a deep sleep')
else:
    print('Power on or hard reset')

# Check for config mode:
configPin()

if configPin():
    # Do something

    for i in range(0, 10):
        pycom.rgbled(0x0000FF)
        sleep(0.2)
        pycom.rgbled(0x000000)
        sleep(0.2)
        pycom.rgbled(0xFF0000)
        sleep(0.2)
        pycom.rgbled(0x000000)
        sleep(0.2)

        # Go to sleep for 10 seconds

    machine.deepsleep(10000)

print('Config Mode')
