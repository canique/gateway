# Installation - Step by Step

These are detailed install instructions for setting up a Raspberry Pi to be able to communicate with a Canique Radio Hat.


## Pre-Requisites
- a Raspberry Pi (tested on Raspberry Pi 3B and Raspberry Pi 4)
- a computer with an SD card writer
- a [Canique Radio Hat for Raspberry Pi](https://www.canique.com/radio-hat) with antenna and u.FL cable
- at least 1 [Canique Climat](https://www.canique.com/climat) (temperature/humidity sensor) to talk to  


## Settings used during test installation
- Raspberry Pi Imager/Timezone: Europe/Vienna
- Raspberry Pi Imager/Keyboard Layut: German
- Host System: Linux Mint
- SD Card: Sandisk Ultra 16GB A1
- Raspberry Pi Power Supply: original Raspberry Foundation power supply

## Steps
1) Download and install [Raspberry Pi Imager](https://www.raspberrypi.com/software/) on your computer

2) Insert an SD card into your computer

3) Run Raspberry Pi Imager: when choosing the OS, select "Raspberry Pi OS (other)" -> then "Raspberry Pi OS Lite (32-bit)"

4) Select your SD card as target

5) In the Raspberry Pi Imager settings (you can get there using the settings symbol) you can assign a hostname. Make sure you activate SSH, and that a password is used for authentication. Also make sure to choose a username and password.

6) Write the image to the SD card using Raspberry Pi Imager

7) When prompted to do so, remove the SD card from your computer, insert it into your Raspberry Pi, connect a network cable to your Raspberry Pi, then connect power to your Raspberry Pi

8) Find out the IP address of your Raspberry Pi (by visiting router administration site)

9) Run `ssh pi@x.x.x.x` on a linux computer in the same network (replace x.x.x.x by the IP address of your Raspberry Pi, and replace "pi" by the username you chose in step 5). When prompted for it, enter the password you chose in the settings in step 5.

10) Run install.sh on your Raspberry PI to automatically install InfluxDB, a bugfixed Canique version of Mosquitto, Nginx webserver, PHP 7.4, the Canique Local Cockpit (a webpage that gives you access to your sensor data without internet connection), and Canique software to communicate with the hat  
```
mkdir /tmp/cnq-gateway && cd /tmp/cnq-gateway && \
wget -q https://raw.githubusercontent.com/canique/gateway/main/raspberry-pi-radio-hat/install.sh
chmod u+x install.sh && ./install.sh
```  

11) Wait for the install script to finish, then shut down your Raspberry Pi:  
`sudo shutdown -h now`  

12) Wait for the LEDs on your Raspberry Pi to stop blinking (green LED must be off), then disconnect Power from your Raspberry Pi  

13) - Insert CR2032 battery into Canique Radio Hat's battery holder (unless already done)
   - Attach the antenna cable to the Canique Radio Hat (unless already done)
   - Connect the Canique Radio Hat to your Raspberry Pi
   - Connect the antenna to the cable

14) Reconnect Power to your Raspberry Pi  
   After booting up, the Radio Hat should already be working. It is actively listening for messages, when the log reads "Gateway Module initialized". You can display the last 100 log lines with the command:  
   `journalctl -n100 -u canique-radio-bridge`  
   In case the radio bridge is not running, run:
   `sudo systemctl restart canique-radio-bridge`  

6) Setup connection between your mosquitto broker and Canique Cloud (optional)  
Enter in a terminal on your Raspberry Pi, replacing MQTT_USER and MQTT_PASSWORD with your own user and password that you got with the hat  
`canique-setup-mosquitto-bridge MQTT_USER MQTT_PASSWORD`  
(You can skip this step if you do not want to use the Canique Cloud. Then your data will stay local.)

7) Setup sensor radio password for every Canique Climat that you have  
If you have a Radio Hat with HW version < 0.8.x, then run  
`sudo runuser -u cnq canique-setup-sensor-encryption`  
For HW versions 0.8.x or greater (this applies to every radio hat shipped in 2023 or later, you can see the HW version both in the log output and printed on the radio hat itself), your Radio Hat comes with an onboard EEPROM. The passwords are already setup at the factory when you order radio hat and sensor(s) together, and you can skip step 7 altogether. If you later order new sensors, though, and you wish to add them to your existing setup, then run   
`sudo -u cnq canique-sensor-keytool set`  
You will be asked for the sensor UID and the sensor radio password. Repeat this step for every sensor you want to connect.

8) For Radio Hat HW versions < 0.8.x (only applies to some radio hats shipped in 2022), restart the Canique Radio Bridge so that all sensor passwords are updated  
`sudo systemctl restart canique-radio-bridge`  

9) Insert battery into Canique Climat or follow [Canique Climat setup steps](https://www.canique.com/climat-first-steps) skipping the first sections and proceeding with *Setting up Canique Climat*   


That's it.  
You can now see your sensor data on https://cockpit.canique.com (if you also followed step 6) and in your local network visiting the IP address of your Raspberry Pi in a webbrowser.
