# LoPy4 LiPo Battery Monitor

This script is for the PyCom LoPy4 and Expansion Board. The expansion board can recharge and power a project from a LiPo battery. The board also has a voltage divider that connects the battery V+ to P16 on a mounted LoPy4 - this can be read with the onboard ADC to get an idea of the battery level, a small equation is required to work this out.

I haven't tested this robustly, but on the board I am working with, I get a reading that is accurate to about 0.1V which is good enough for general purpose. 

You can put the device into 'config' mode which can be a little easier for reprogramming by placing a jumper wire between **'P21'** and **GND**

This script is working towards a battery monitoring system for a solar charging setup. 

I recommend [Atom](https://atom.io/) and the PyMakr plugin to work with this code. Make sure your LoPy4 has the [latest firmware](https://docs.pycom.io/chapter/gettingstarted/installation/firmwaretool.html)