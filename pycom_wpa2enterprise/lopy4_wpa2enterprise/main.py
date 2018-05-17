import machine
import ubinascii
from network import WLAN
from time import sleep
import socket
# import urllib.urequest

# Network
SSID = 'eduroam' # Network Name
User = 'fablab@cardiffmet.ac.uk'
Password = 'Fa6La6!' # Network password
deviceID = 'LoPy4Test'
certPath = '/flash/pfencehaca.cer'

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

def http_get(url):
    _, _, host, path = url.split('/', 3)
    addr = socket.getaddrinfo(host, 80)[0][-1]
    s = socket.socket()
    s.connect(addr)
    s.send(bytes('GET /%s HTTP/1.0\r\nHost: %s\r\n\r\n' % (path, host), 'utf8'))
    while True:
        data = s.recv(100)
        if data:
            print(str(data, 'utf8'), end='')
        else:
            break
    s.close()

def socketTest():
    addr_info = socket.getaddrinfo("towel.blinkenlights.nl", 23)
    addr = addr_info[0][-1]
    s = socket.socket()
    s.connect(addr)

    data = s.recv(500)
    print(str(data, 'utf8'), end='')

while True:
    print('ip address, netmask, gateway, DNS:')
    print(station.ifconfig()) # reveal the devices ip address
    print('')
    print('Device MAC = ', ubinascii.hexlify(machine.unique_id(),':').decode())
    print('')

    #try:
    #    socketTest()

    http_get('http://micropython.org/ks/test.html')
    #contents = urllib.urequest.urlopen("http://google.com")
    #contents.close()
    sleep(10)
