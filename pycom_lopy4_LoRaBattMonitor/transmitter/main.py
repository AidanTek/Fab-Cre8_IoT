from machine import Pin, ADC
from network import LoRa
import socket
from utime import sleep

# Use a pin for a 'config' mode
configPin = Pin('P21', Pin.IN, Pin.PULL_UP)

# Create an ADC object
adc = ADC()

# vbatt pin:
vbatt = adc.channel(attn=1, pin='P16')

def battConversion():
    adcVoltage = vbatt()
    voltage = adcVoltage*3*1.334/4095

    return voltage

# Initialise LoRa in LoRa mode
# For Europe, use LoRa.EU868

lora = LoRa(mode=LoRa.LORA, region=LoRa.EU868)

# Create a raw LoRa socket
s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)

# Check the Config pin:
configMode = configPin()

if configMode:
    print('Reading Battery')
    pycom.rgbled(0x0000FF)
    message = 'Battery Status: {}'.format(battConversion())
    print(message)
    sleep(2)

    print('Sending battery status estimate...')
    pycom.rgbled(0xFF0000)
    sleep(2)
    s.setblocking(True)
    # Send some data
    s.send(message)

    print('Message Sent!')
    pycom.rgbled(0x00FF00)
    sleep(2)

    print('Going to sleep')
    machine.deepsleep(300000)

# Otherwise, we are in 'config' so exit to REPL
print('Config Mode')
