# LoPy4_files/main.py

import time
from network import LoRa
import binascii
import pycom
from machine import Pin
import socket

# Configure IO Pins:
configPin = Pin('P21', Pin.IN, Pin.PULL_UP) # Pull low to exit to REPL
LoRaPin = Pin('P22', Pin.IN, Pin.PULL_UP) # Pull low to enable LoRa

#Set AppEUI and AppKey - use your values from the device settings --> https://console.thethingsnetwork.org/
dev_eui = binascii.unhexlify('***')
app_eui = binascii.unhexlify('***')
app_key = binascii.unhexlify('***')

# initial read from IO pins:
config = configPin()
radio = LoRaPin()

# In 'config mode' exit to the REPL, and print the LoRa DevEUI:
if not config:
    print('Config Mode')

    lora = LoRa()
    print("DevEUI: %s" % (binascii.hexlify(lora.mac()).decode('ascii')))

# Otherwise, we probably want to activate LoRa:
if not radio:
    pycom.rgbled(0x7f0000) #red

    lora = LoRa(mode=LoRa.LORAWAN, region = LoRa.EU868)

    # Remove all the non-default channels
    for i in range(3, 16):
        lora.remove_channel(i)
    print('Removed default channels')
    time.sleep(1)

    # Set EU ISM 868 channel plan for TTN Europe
    lora.add_channel(0, frequency=868100000, dr_min=0, dr_max=5)
    lora.add_channel(1, frequency=868300000, dr_min=0, dr_max=5)
    lora.add_channel(2, frequency=868500000, dr_min=0, dr_max=5)
    lora.add_channel(3, frequency=867100000, dr_min=0, dr_max=5)
    lora.add_channel(4, frequency=867300000, dr_min=0, dr_max=5)
    lora.add_channel(5, frequency=867500000, dr_min=0, dr_max=5)
    lora.add_channel(6, frequency=867700000, dr_min=0, dr_max=5)
    lora.add_channel(7, frequency=867900000, dr_min=0, dr_max=5)

    print('EU channels set')
    time.sleep(1)

    #Join TTN Network via OTAA
    lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=0)

    # wait until the module has joined the network
    print('Trying to join TTN Network...')
    while not lora.has_joined():
        pycom.rgbled(0x7f7f00) #yellow
        time.sleep(5)
        print('...')
        pass

    print('Network joined')
    pycom.rgbled(0x009999) #teal


    # Now let's send some data...
    # create a LoRa socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # set the LoRaWAN data rate
    s.setsockopt(socket.SOL_LORA, socket.SO_DR, 1)

    while lora.has_joined():
        print('Sending some bits:', bytes([0x01, 0x02, 0x03]))
        # make the socket blocking
        s.setblocking(True)
        s.send(bytes([0x01, 0x02, 0x03]))

        time.sleep(0.5)

        print('Listening for bits:')
        s.setblocking(False)
        data = s.recv(64)
        print(data)

        time.sleep(30)

    print('Connection lost')
