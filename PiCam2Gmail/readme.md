## Readme

This is a Python script for a Raspberry Pi - tested on a Pi Zero W

The Raspberry Pi PiCam Camera peripheral is used in this example. Pressing a
button connected to BCM26 triggers a sequence where a photo is taken by the
camera and this is saved as a jpeg named as the current date and time. The jpeg
is then sent as an e-mail to a recipient, or number of recipients.

You need to make the following directory in the home folder:

```
cd ~/Documents/

mkdir myCamPics
```

Or alternatively change the filepath in the script.

**n.b.** this requires the sender to have a gmail account and the account must be
set up to "allow less secure apps" which is disabled by default.

*By Aidan Taylor and Serena Pearce.*

**Fab-Cre8 2018.**
