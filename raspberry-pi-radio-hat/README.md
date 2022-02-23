# Canique Radio Hat for Raspberry Pi


## Installation

This How-To will explain how to turn your Raspberry Pi into a Canique 868MHz Gateway using a Canique Radio Hat for Raspberry Pi. Your Raspberry PI will then be able to communicate with Canique Temperature/Humidity sensors (with up to 20 years battery life time) via an encrypted 868 MHz channel.


Pre-Requisites:  
- a Raspberry Pi (tested on Raspberry Pi 3 and Raspberry Pi 4)
- a Debian Bullseye based OS on your Raspberry Pi (with systemd)
- a Canique Radio Hat (available soon in Canique Shop) with antenna and u.FL cable
- at least 1 [Canique Climat](https://www.canique.com/climat) (temperature/humidity sensor) to talk to  


1) Run install.sh on your Raspberry PI to automatically install InfluxDB, a bugfixed Canique version of Mosquitto, Nginx webserver, PHP 7.4, the Canique Local Cockpit (a webpage that gives you access to your sensor data without internet connection), and Canique software to communicate with the hat  
```
mkdir /tmp/cnq-gateway && cd /tmp/cnq-gateway && \
wget -q https://raw.githubusercontent.com/canique/gateway/main/raspberry-pi-radio-hat/install.sh
chmod u+x install.sh && ./install.sh
```  

2) Shut down your Raspberry Pi:  
`sudo shutdown -h now`  

3) Disconnect Power from your Raspberry Pi  

4) Attach the antenna cable to the Canique Radio Hat  
   Attach the Canique Radio Hat to your Raspberry Pi  
   Connect the antenna to the cable  

5) Reconnect Power to your Raspberry Pi  

6) Setup connection between your mosquitto broker and Canique Cloud  
Enter in a terminal on your Raspberry Pi, replacing MQTT_USER and MQTT_PASSWORD with your own user and password that you got with the hat  
`canique-setup-mosquitto-bridge MQTT_USER MQTT_PASSWORD`  

6) Setup sensor radio password for every Canique Climat that you have  
`runuser -u cnq canique-setup-sensor-encryption`  
You will be asked for the sensor UID and the sensor radio password. Repeat this step for every sensor you want to connect.

7) Restart the Canique Radio Bridge so that all sensor passwords are updated  
`sudo systemctl restart canique-radio-bridge`  

8) Insert battery into Canique Climat  


That's it.  
You can now see your sensor data on https://cockpit.canique.com and in your local network visiting the IP address of your Raspberry Pi in a webbrowser.



## Radio Reception Quality / Noise Indicator

The Raspberry Pi can emit noise (which also covers the 868MHz band) while doing SD card writes, or while  heavily using the WiFi chip or LAN (e.g. while downloading a file). To keep the received noise level to a minimum so that the antenna of the Canique Gateway Hat does not see much interference, you should keep heavy SD card writes or network transactions to a minimum.   
You can see the noise level visually by looking at the amber RX LED of the Canique Gateway Hat. Ideally it should blink once in a while (whenever it thinks it is receiving a message). If the RX LED is on all the time, though, this means that the received noise is above the RX threshold (set to -98 dBm by default).
Please note that noise can also stem from a TV in the close proximity or some other electronic device.


## Raspberry Pi4 Power Optimization and Tuning

If you want to reduce the power consumption of your Raspberry Pi 4...  

To disable WiFi/Bluetooth:  
Add this to /boot/config.txt, then reboot:  
```
[all]
dtoverlay=disable-wifi
dtoverlay=disable-bt
```

To make your SD card more resilient against errors (for a tradeoff for slower writes), run  
`sudo tune2fs -o journal_data /dev/mmcblk0p2`  
This command assumes that your root parition is on /dev/mmcblk0p2 - adjust it to your needs.


## Technical Details

Canique specific configuration files can be found in /etc/cnq-xxxxxxx  

The following packages from Canique are installed:

canique-radio-bridge  
This package is necessary for the Raspberry Pi to communicate with the Canique Hat. UART settings of your Raspberry Pi's operating system will be automatically adjusted during installation.

canique-mqtt-tools  
This package will install a bridge that forwards mosquitto data to influxdb so that you can see charts in your Canique Local Cockpit.  
It will furthermore replace the InfluxDB configuration, install some scripts, create an InfluxDB database and create some mosquitto passwords.  

canique-web-conf  
This will change some PHP and Nginx configuration files  

canique-local-cockpit  
This will install the Canique Local Cockpit in /var/www
