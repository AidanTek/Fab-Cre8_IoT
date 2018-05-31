# boot.py -- run on boot-up
import pycom
import machine

pycom.wifi_on_boot(False)
pycom.heartbeat(False)

if machine.reset_cause() == machine.DEEPSLEEP_RESET:
    print('Woke up from a deep sleep')
else:
    print('Power on or hard reset')
