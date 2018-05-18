# Pycom LoPy4 Deepsleep Test

This script is for the PyCom LoPy4 and is designed to provide an example for deepsleep for any purpose, I am using it to test current consumption in this state.

**n.b.** while this script will work on most other hardware running MicroPython, it is not always the recommended method to send a device into deepsleep - please refer to the hardware documentation for further info.

The script will blink the onboard LED for just under 10 seconds, then it will send the device to sleep for 10 seconds.

**todo:**

* Try activating / deactivating LoRa Antenna between active/sleep state
