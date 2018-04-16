### PyCom Media Network Setup

This code is an example to demonstrate how to set up a PyCom board for connectivity on the Universities "media" network

The devices MAC address must be reported to IT in order to connect. If you are using one of the FabCre8 PyCom boards, the chances are that this step has already been set up.

Upload the sketch to the PyCom board, the sketch will do nothing initially, but the MAC address will be reported in the REPL - use this to register the device, then update myNet.py with the correct SSID and PASSWORD details to connect to the network.

*n.b. it looks like the PyCom boards support WPA-2 Enterprise authentication, so it should be possible to connect to eduroam - the method will be different in this case so please wait for an update if this is important for your project*  
