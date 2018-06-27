# This is the network setup for the seedlingMonitor.py
# script.
#
# by Aidan Taylor, Fab-Cre8. 2018

import network
from umqtt.simple import MQTTClient
import uos
import utime
import ubinascii
import machine

# Key strings:
# Network
SSID = "" # Network Name
Password = "" # Network password
#ThingSpeak
tsChan = b"" # ThingSpeak Channel
tsRAPI = b"" # ThingSpeak Write API Key
tsMQTTAPI = b"" # ThingSpeak User API Key
tsUrl = b"mqtt.thingspeak.com" # MQTT broker
tsUserId = b"" # ThingSpeak User ID
tsUserAPI = b""

# create a random MQTT clientID
# (I don't know why you need to do this...)
randomNum = int.from_bytes(uos.urandom(3), 'little')
myMqttClient = bytes("client_"+str(randomNum), 'utf-8')

client = MQTTClient(client_id=myMqttClient,
                    server=tsUrl,
                    user=tsUserId,
                    password=tsMQTTAPI,
                    ssl=False)

# WiFi init:
station = network.WLAN(network.STA_IF)
station.active(True)

def WiFiConnect():
    # Connect
    station.connect(SSID, Password)

    # Wait for connection
    print("connecting...")
    while not station.isconnected():
        print("...")
        utime.sleep(5)
        print("Connected!\n")

WiFiConnect()

def cb(topic, msg):
    if 'field1' in topic:
        temp = str(msg, 'utf-8')
        print('Temperature = {} C'.format(temp))
    if 'field2' in topic:
        pres = str(msg, 'utf-8')
        print('Pressure = {} Pa'.format(pres))
    if 'field3' in topic:
        humi = str(msg, 'utf-8')
        print('Humidity = {} RH'.format(humi))
    if 'field4' in topic:
        light = str(msg, 'utf-8')
        print('Light = {}'.format(light))

    #freeheap = float(str(msg,'utf-8'))
    #print("free heap size = {} bytes".format(freeheap))

def ThingSpeakDownload():
    client.set_callback(cb)
    client.connect()

    utime.sleep(2)

    subscribefield1 = bytes("channels/{:s}/subscribe/fields/field1/{:s}".format(tsChan, tsRAPI), 'utf-8')
    client.subscribe(subscribefield1)
    subscribefield2 = bytes("channels/{:s}/subscribe/fields/field2/{:s}".format(tsChan, tsRAPI), 'utf-8')
    client.subscribe(subscribefield2)
    subscribefield3 = bytes("channels/{:s}/subscribe/fields/field3/{:s}".format(tsChan, tsRAPI), 'utf-8')
    client.subscribe(subscribefield3)
    subscribefield4 = bytes("channels/{:s}/subscribe/fields/field4/{:s}".format(tsChan, tsRAPI), 'utf-8')
    client.subscribe(subscribefield4)

    while True:
        client.wait_msg()
        utime.sleep(1)

    client.disconnect()

def debugs():
    print('ip address, netmask, gateway, DNS:')
    print(station.ifconfig()) # reveal the devices ip address
    print('')
    print('Device MAC = ', ubinascii.hexlify(machine.unique_id(),':').decode())
    print('')
    print('wifi interface MAC = ', ubinascii.hexlify(station.config('mac'),':').decode())
    print('')
