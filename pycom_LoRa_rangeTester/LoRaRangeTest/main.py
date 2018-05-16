from network import LoRa
import socket
from machine import Pin, rng
import pycom
import utime

pycom.heartbeat(False)

# Initialise Pins:
RxPin = Pin('P23', Pin.IN, Pin.PULL_UP)
TxPin = Pin('P22', Pin.IN, Pin.PULL_UP)
configPin = Pin('P21', Pin.IN, Pin.PULL_UP)

# Initialise LoRa in LoRa mode
# For Europe, use LoRa.EU868

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)

# Create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

message = "live"

# Exit to REPL if configPin is pulled low
configMode = configPin()

if configMode:
    print("Main Loop")

    # Check pins for mode
    TxMode = TxPin()
    RxMode = RxPin()

    print(TxMode, RxMode)

    # Tx Mode
    if not TxMode:
        print("Transmit Mode")
        pycom.rgbled(0x0000FF)
        utime.sleep(2)
        s.setblocking(True)
        while True:
            # Send some data
            s.send(message)
            pycom.rgbled(0x0000FF)
            utime.sleep(0.2)
            pycom.rgbled(0x000000)
            utime.sleep(0.2)
            pycom.rgbled(0x0000FF)
            utime.sleep(0.2)
            pycom.rgbled(0x000000)
            utime.sleep(0.6)

    # Rx Mode
    if not RxMode:
        print("Receive Mode")
        timer = 0
        timerTest = 0
        pycom.rgbled(0xFF0000)
        utime.sleep(0.2)
        pycom.rgbled(0x000000)
        utime.sleep(0.2)
        pycom.rgbled(0xFF0000)
        utime.sleep(0.2)
        pycom.rgbled(0x000000)
        utime.sleep(0.2)

        s.setblocking(False)

        while True:
            timer = utime.ticks_ms()
            if (timer - timerTest > 5000):
                pycom.rgbled(0x000000)
            else:
                pycom.rgbled(0x00FF00)
                utime.sleep(0.2)
                pycom.rgbled(0x000000)
                utime.sleep(0.2)
                pycom.rgbled(0x00FF00)
                utime.sleep(0.2)
                pycom.rgbled(0x000000)
                utime.sleep(0.2)

            # Receive data
            data = s.recv(64)
            print(data)

            # Test for signal
            if data == b'live':
                timerTest = utime.ticks_ms()

            utime.sleep(1)

# Otherwise Exit
print("Config Mode")
