# This is the network setup for the seedlingMonitor.py
# script.
#
# by Aidan Taylor, Fab-Cre8. 2018

import network
from umqtt.simple import MQTTClient
import uos
import utime

# Key strings:
# Network
SSID = "" # Network Name
Password = "" # Network password
#ThingSpeak
tsChan = b"" # ThingSpeak Channel
tsWAPI = b"" # ThingSpeak Write API Key
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
                    port=1883)

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

    print('ip address, netmask, gateway, DNS:')
    print(station.ifconfig()) # reveal the devices ip address

WiFiConnect()

def ThingSpeakUpload(l,t,h,p):
    client.connect()
    credentials = bytes("channels/{:s}/publish/{:s}".format(tsChan, tsWAPI), 'utf-8')
    payload = bytes("field1={}&field2={}&field3={}&field4={}\n".format(l,t,h,p), 'utf-8')
    client.publish(credentials, payload)

def debugs():
    print('ip address, netmask, gateway, DNS:')
    print(station.ifconfig()) # reveal the devices ip address
    print('')
    print('Device MAC = ', ubinascii.hexlify(machine.unique_id(),':').decode())
    print('')
    print('wifi interface MAC = ', ubinascii.hexlify(station.config('mac'),':').decode())
    print('')
