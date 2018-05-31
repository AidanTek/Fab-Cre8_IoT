# LoPy4 Battery Monitor over LoRa

This script combines some of the other examples on this repository, but the hardware has some other notable features as well. The idea is to have a remote setup that can transmit some useful data over a LoRa network. Two LoPy4 boards are involved, a transmitter and a receiver.

### The Transmitter:

The transmitting LoPy4 is powered by a battery and periodically goes into an active state to transmit data, but is otherwise in deepsleep. I have this board connected to a Sparkfun "Solar Buddy" and two solar panels - the aim being to monitor solar charging over a period.

### The Receiver:

At the moment, the receiver is on all the time and listening on a socket. I am just monitoring the data in realtime using a Raspberry Pi - next step is to actually get this data onto a real network.
