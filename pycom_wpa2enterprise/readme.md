# PyCom WPA2-Enterprise Connection

This script is designed to demonstrate how to connect to a WPA2-Enterprise type WiFi network. **This is a work in progress**, I am not convinced the certificate is working correctly and I'm not sure of the implications this has - it definitely means that your device is not secure as a 'malicious network' could trick your device into connecting to it instead of the genuine secure network. Use at your own risk for the time being.

I am able to perform http get requests and pings, but for some reason I am unable to use message protocols like MQTT still - stay tuned for an update on this.

I recommend using [Atom](https://atom.io/) and the PyMakr plugin to upload this code to a PyCom device. Any PyCom device with a WiFi connection should run this example, and it is possible that it will work on other MicroPython ready devices as well. Remember to update your device to the [latest firmware](https://docs.pycom.io/chapter/gettingstarted/installation/firmwaretool.html).