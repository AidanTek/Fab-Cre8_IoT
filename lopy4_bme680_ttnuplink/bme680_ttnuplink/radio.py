# lopy4_bme680_ttnuplink/bme680_ttnuplink/radio.py

import time
from network import LoRa
import binascii
import pycom
import socket

#Set AppEUI and AppKey - use your values from the device settings --> https://console.thethingsnetwork.org/
dev_eui = binascii.unhexlify('')
app_eui = binascii.unhexlify('')
app_key = binascii.unhexlify('')

# In 'config mode' print the LoRa DevEUI before exit:
def config():
    print('Config Mode')

    lora = LoRa()
    print("DevEUI: %s" % (binascii.hexlify(lora.mac()).decode('ascii')))

# Otherwise, we probably want to activate LoRa:
def connect():
    global _lora

    pycom.rgbled(0x7f0000) #red

    _lora = LoRa(mode=LoRa.LORAWAN, region = LoRa.EU868)

    # Remove all the non-default channels
    for i in range(3, 16):
        _lora.remove_channel(i)
    print('Removed default channels')
    time.sleep(1)

    # Set EU ISM 868 channel plan for TTN Europe
    _lora.add_channel(0, frequency=868100000, dr_min=0, dr_max=5)
    _lora.add_channel(1, frequency=868300000, dr_min=0, dr_max=5)
    _lora.add_channel(2, frequency=868500000, dr_min=0, dr_max=5)
    _lora.add_channel(3, frequency=867100000, dr_min=0, dr_max=5)
    _lora.add_channel(4, frequency=867300000, dr_min=0, dr_max=5)
    _lora.add_channel(5, frequency=867500000, dr_min=0, dr_max=5)
    _lora.add_channel(6, frequency=867700000, dr_min=0, dr_max=5)
    _lora.add_channel(7, frequency=867900000, dr_min=0, dr_max=5)

    print('EU channels set')
    time.sleep(1)

    #Join TTN Network via OTAA
    _lora.join(activation=LoRa.OTAA, auth=(dev_eui, app_eui, app_key), timeout=0, dr=0)

    # wait until the module has joined the network
    print('Trying to join TTN Network...')
    while not _lora.has_joined():
        pycom.rgbled(0x7f7f00) #yellow
        time.sleep(5)
        print('...')
        pass

    print('Network joined')
    pycom.rgbled(0x009999) #teal

def make_socket():
    # create a LoRa socket
    global _s

    _s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

    # set the LoRaWAN data rate
    _s.setsockopt(socket.SOL_LORA, socket.SO_DR, 1)

    # Socket will only ever send, so use blocking:
    _s.setblocking(True)

def send_packet(a,b,c,d):
    if _lora.has_joined():
        print('Sending some bytes:', a, b, c, d)

        packet = '{}{}{}{}'.format(a,b,c,d)

        _s.send(packet)

        time.sleep(1)

        print('Packet sent')

    else:
        print('Connection lost')
