# Canique Radio Hat for Raspberry Pi


## Installation

This How-To will explain how to turn your Raspberry Pi into a Canique 868MHz Gateway using a Canique Radio Hat for Raspberry Pi. Your Raspberry PI will then be able to communicate with Canique Temperature/Humidity sensors (with up to 20 years battery life time) via an encrypted 868 MHz channel.


Pre-Requisites:  
You need a Raspberry Pi (tested on Raspberry Pi 3 and Raspberry Pi 4)  
You need a Debian Bullseye based OS on your Raspberry Pi  
You need a Canique Radio Hat (available soon in Canique Shop) with antenna and u.FL cable  
You need at least 1 [Canique Climat](https://www.canique.com/climat) (temperature/humidity sensor) to talk to  


1) Run install.sh on your Raspberry PI to automatically install InfluxDB, a bugfixed Canique version of Mosquitto, Nginx webserver, PHP 7.4, the Canique Local Cockpit (a webpage that gives you access to your sensor data without internet connection), and Canique software to communicate with the hat  
Open a terminal on your Raspberry Pi  
`mkdir /tmp/cnq-gateway && cd /tmp/cnq-gateway && wget -q https://raw.githubusercontent.com/canique/gateway/main/raspberry-pi-radio-hat/install.sh`  
`chmod u+x install.sh && ./install.sh`  

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



## Technical Details

Canique specific configuration files can be found in /etc/cnq-xxxxxxx  

The following packages from Canique are installed:

canique-radio-bridge  
This package is necessary for the Raspberry Pi to communicate with the Canique Hat. UART settings will be automatically adjusted during installation.

canique-mqtt-tools  
This package will install a bridge that forwards mosquitto data to influxdb so that you can see charts in your Canique Local Cockpit.  
It will furthermore replace the InfluxDB configuration, install some scripts, create an InfluxDB database and create some mosquitto passwords.  

canique-web-conf  
This will change some PHP and Nginx configuration files  

canique-local-cockpit  
This will install the Canique Local Cockpit in /var/www
