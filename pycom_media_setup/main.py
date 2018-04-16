import pycom
pycom.heartbeat(False)

import myNet

pycom.rgbled(0x000055)
print("Ready")
