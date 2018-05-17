# This is the network setup for the seedlingMonitor.py script.
#
# by Aidan Taylor, Fab-Cre8. 2018

from network import WLAN
from umqtt.simple import MQTTClient
import uos
from utime import sleep

# Key strings:
# Network
SSID = '' # Network Name
User = ''
Password = '' # Network password
deviceID = "" # Give the device a name
certPath = ''

#ThingSpeak
tsChan = b"" # ThingSpeak Channel
tsWAPI = b"" # ThingSpeak Write API Key
tsMQTTAPI = b"" # ThingSpeak User API Key
tsUrl = b"mqtt.thingspeak.com" # MQTT broker
tsUserId = b"" # ThingSpeak User ID
tsUserAPI = b""

# create a random MQTT clientID
randomNum = int.from_bytes(uos.urandom(3), 'little')
myMqttClient = bytes("client_"+str(randomNum), 'utf-8')

client = MQTTClient(client_id=myMqttClient,
                    server=tsUrl,
                    user=tsUserId,
                    password=tsMQTTAPI,
                    port=1883)

# WiFi init:
station = WLAN(mode=WLAN.STA)

def WiFiConnect():
    # Connect
    station.connect(ssid=SSID, auth=(WLAN.WPA2_ENT, User, Password), identity=deviceID, certfile=certPath)

    # Wait for connection
    print("connecting...")
    while not station.isconnected():
        print("...")
        sleep(5)
        print("Connected!\n")

WiFiConnect()

def ThingSpeakUpload(n):
    client.connect()
    credentials = bytes("channels/{:s}/publish/{:s}".format(tsChan, tsWAPI), 'utf-8')
    payload = bytes("field1={}\n".format(n), 'utf-8')
    client.publish(credentials, payload)
