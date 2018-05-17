import machine
import pycom
from utime import sleep

pycom.heartbeat(False)

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('Woke from a deep sleep')
else:
    print('Power on or hard reset')

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
