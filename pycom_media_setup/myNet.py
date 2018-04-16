# myNet network config file for pycom

import machine
import ubinascii
from network import WLAN
wlan = WLAN(mode=WLAN.STA)

# Show the MAC address:
print(ubinascii.hexlify(machine.unique_id(),':').decode())
# or...
#print(ubinascii.hexlify(wlan.mac(),':').decode())

SSID = ''
PASSWORD = ''

nets = wlan.scan()
for net in nets:
    if net.ssid == SSID:
        print('Network found!')
        wlan.connect(net.ssid, auth=(net.sec, PASSWORD), timeout=5000)
        while not wlan.isconnected():
            machine.idle() # save power while waiting
        print('WLAN connection succeeded!')
        break
