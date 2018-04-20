# Seedling Monitor v2

This is a MicroPython project for the ESP32
Any ESP32 dev board is suitable, I am currently using the Lolin32 Pro

The project is a simple environmental monitoring system to report on the immediate ambient conditions in close proximity to your seedlings.

The main update for v2 is the DHT11 sensor has been replaced with the more accurate BME280 sensor which also reports on ambient pressure.

I have also been working on power optimisation for battery use. I think I have pushed the limits of what can be achieved with the Lolin32 as power is wasted by both the on-board regulator and USB Serial chip. At the moment the project can run for approximately 96 hours before the 1000mAh battery runs too low and needs recharging. The best way to change things from here would be to use a different system all together.

The ESP32 is used as a MQTT client to send data to the Thingspeak MQTT Broker service.

myNet.py needs to be modified with your network settings. All files excluding this one should be copied to the ESP32 board.

My ThingSpeak channel is here: https://thingspeak.com/channels/456189

Please visit http://micropython.org/ for more information on setting up the ESP32 and please visit https://fabcre8.wordpress.com for more information on our projects

**Aidan Taylor, Fab-Cre8 2018.**
