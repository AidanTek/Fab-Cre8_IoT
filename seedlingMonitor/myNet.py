# This is the network setup for the seedlingMonitor.py
# script.
#
# by Aidan Taylor, Fab-Cre8 2018

import network
from umqtt.simple import MQTTClient
import uos
import time

# Key strings:
# Network
SSID = "###" # Network Name
Password = "###" # Network password
#ThingSpeak
tsChan = b"###" # ThingSpeak Channel
tsWAPI = b"###" # ThingSpeak Write API Key
tsMQTTAPI = b"###" # ThingSpeak User API Key
tsUrl = b"mqtt.thingspeak.com" # MQTT broker?
tsUserId = b"###" # ThingSpeak User ID
tsMQTTAPI = b"###" # ThingSpeak MQTT API Key

#
# create a random MQTT clientID
# I don't know why you need to do this...
randomNum = int.from_bytes(uos.urandom(3), 'little')
myMqttClient = bytes("client_"+str(randomNum), 'utf-8')

client = MQTTClient(client_id=myMqttClient,
                    server=tsUrl,
                    user=tsUserId,
                    password=tsMQTTAPI,
                    port=8883,
                    ssl=True)

# WiFi init:
station = network.WLAN(network.STA_IF)
station.active(True)
station.connect(SSID, Password)

# Wait for connection
print("connecting...")
while not station.isconnected():
    print("...")
    time.sleep(5)
print("Connected!\n")

def ThingSpeakUpload(l,t,h):
    client.connect()
    credentials = bytes("channels/{:s}/publish/{:s}".format(tsChan, tsWAPI), 'utf-8')
    payload = bytes("field1={}&field2={}&field3={}\n".format(l,t,h), 'utf-8')
    client.publish(credentials, payload)
