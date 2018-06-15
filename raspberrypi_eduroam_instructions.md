# Raspberry Pi WiFi Eduroam Connection

This guide should help you get connected to eduroam, this is working and secure at Cardiff Metropolitan University. If you work or study at another institution then please consult with your IT department first. You alone are responsible for any usage of the instructions in this document!

---

## Requirements:
* A Raspberry Pi with WiFi interface
* A micro SD card
* An ethernet cable
* A usb power supply (2.5A for Raspberry Pi 3)
* To make things easier bring a USB mouse, keyboard and HDMI screen

---

## Instructions:
* Flash the SD card with the latest version of Raspbian [Instructions here](https://www.raspberrypi.org/downloads/)
* Connect the keyboard, mouse, monitor and ethernet cable to the Raspberry Pi and boot it up for the first time
* **I strongly recommend you set up a strong password on the Pi you are working with now** you can do this with the Raspberry Pi config tool. Open terminal with **ctrl+alt+t** and enter the command ```sudo raspi-config``` - you can change your password here
* Now open the Raspberry Pi Chromium browser and navigate to [https://cat.eduroam.org](https://cat.eduroam.org)
* Once the page has loaded, click the lower box labelled "download your eduroam installer"
* A pop-up will appear with a list of institutions, select Cardiff Metropolitan University (if you are based at another institution, try to find your institution from the list, if it isn't there, please consult with your IT department). Accept the download.
* The download will appear in your Downloads folder. Open terminal with **ctrl+alt+t** and navigate to the folder with ```cd Downloads```
* You can check the file is there by typing ```ls```
* You won't have permissions to run the script, change permissions with the command ```chmod 755 eduroam-linux-... ``` (you can press **tab** to complete a long file name)
* Now run the script with the command ```./eduroam-linux-... ``` 
* Follow the instructions but note that *the script will fail!* however, an output file is generated that we can use to manually set up connection
* Back in terminal (**ctrl+alt+t**) navigate to the hidden folder ```cd ~/.cat_installer```
* type ```ls``` to reveal the contents of this folder. ca.pem is the eduroam certificate and this file is very important, the other file is the output from the installer script. Let's look at this file now with ```cat cat_installer.conf```
* I made a dummy file that looks like this:
```
network={
	ssid="eduroam"
	key_mgmt=WPA-EAP
	pairwise=CCMP
	group=CCMP TKIP
	eap=PEAP
	ca_cert="/home/pi/.cat_installer/ca.pem"
	identity="yourLogin"
	domain_suffix_match="ac.uk"
	phase2="auth=MSCHAPV2"
	password="yourPassword"
}
```
* Note that your login and password will be exposed in plain text in this document! We will fix that shortly.
* This file is pretty much what we need, but it is in the wrong place. Keeping this window open, start another terminal window with **ctrl+alt+t** and navigate to this folder: ```cd /etc/wpa-supplicant```
* There is a file in this folder called wpa-supplicant.conf, we can now edit it with the updated information, use nano or another text editor to do this: ```nano wpa-supplicant.conf```
* There should already be a ```network {}``` section of this file, you just need to copy the contents from the output of the cat_installer tool into this file. Mine looks a bit like this:
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=GB

network={
	stuff shared above!!
}
```
* Save the file with **ctrl-x** and **y** in nano, don't change the filename
* So far so good, now let's secure that password for peace of mind. In terminal, type the following command: ```echo -n yourPasswordHere | iconv -t utf16le | openssl md4```
* Make a note of the output and edit your wpa-supplicant.conf file again: ```nano /etc/wpa-supplicant/wpa-supplicant.conf```
* Replace the password field in ```network {}``` with:
```
password=hash:(the generated hash key)

mine looks like:
password=hash:4c7d63814...
```
* Finally, let's get rid of the generated output from cat_installer as this also contains your password in human readable form: ```rm ~/.cat_installer/cat_installer.conf```
* Now remove the ethernet lead and reboot your Pi with ```reboot```
* Once the desktop has started, you should see the WiFi symbol come to life in the top right hand corner of the screen, success!!

---

If you don't have success then go through the steps carefully checking files as you go. You can contact me on GitHub if you want some further support with this, time permitting I will do my best!
