# PyCom LoRa Range Tester

This project is a basic example to use with the [PyCom LoPy4](https://docs.pycom.io/chapter/gettingstarted/connection/lopy4.html) board. It will probably work with the LoPy as well but you may need to reconfigure pins. The project utilises the LoRa functionality of the LoPy4 to create a "Raw" LoRa Network. This network does not connect to the internet, but allows two devices to communicate with each other. Some testing has shown that even with the stock antenna the signal range is surprisingly good - I haven't found the limit yet!

This is a very simple project to construct, but please pay attention to the following:

It is recommended that you update the PyCom LoPy4 firmware before doing anything else. Follow the instructions here: [PyCom Firmware Update](https://docs.pycom.io/chapter/gettingstarted/installation/firmwaretool.html)

**Warning** - The PyCom documentation states that a LoRa antenna must be connected if LoRa is active - failure to do so can damage the board. Connect an antenna before you flash the microcontroller.

---

### Project notes:

**Parts:**

* 2 x PyCom LoPy4
* 2 x PyCom Expansion Boards
* 2 x PyCom Antenna
* 2 x Lithium Battery with JST connector - I am using a 1000mAh battery
* Micro USB data lead to flash
* 2 x Case (optional)

**Notes:**
 
* You need a pair of LoPy4 boards, one to act as the transmitter and one to act as a receiver.
* Both boards have the same code (from this repository) flashed to them
* Place a jumper wire between 'P' and GND to put a board into Transmiter mode
* Place a jumper wire between 'P' and GND to put a board into Receiver mode
* See the [pin reference](https://docs.pycom.io/chapter/datasheets/development/lopy4.html) here to find the pins mentioned above, it's a bit confusing but they are directly next to the GND and 3V3 pins - be careful not to tie 3V3 and GND together! 
* If you don't place a jumper wire, the program will exit immediately to a REPL state, which makes it easier to reflash code to the PyCom board in my experience
* I am using Atom with the PyMakr plugin to flash the LoPy4. 

**Testing**

* Having run some tests, I have found that with LoRa active the project runs at 110mAh consistently - I haven't removed any of the jumpers from the PyCom expansion board, I think this might save on some power if the USB serial port or battery charging circuitry is disconnected. I will test deep sleep and wake soon.
* As mentioned, I have yet to find the range of these antennas, I tried outdoors already but all I can say is it is **BIG**!

