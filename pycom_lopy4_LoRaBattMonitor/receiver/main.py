from machine import Pin
from network import LoRa
import socket
from utime import sleep

# Use a pin for a 'config' mode
configPin = Pin('P21', Pin.IN, Pin.PULL_UP)

# Initialise LoRa in LoRa mode
# For Europe, use LoRa.EU868

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)

# Create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Check the Config pin:
configMode = configPin()

if configMode:
    print("Basic LoRa Receiver")
    s.setblocking(False)

    while True:
        pycom.rgbled(0xFF0000)
        sleep(1)

        # Receive data
        data = s.recv(64)
        if not data == b'':
            pycom.rgbled(0x00FF00)
            print(data)
            sleep(2)

# Otherwise, we are in 'config' so exit to REPL
print('Config Mode')
