# Canique Radio Hat for Raspberry Pi

This How-To will explain how to turn your Raspberry Pi into a Canique 868MHz Gateway using a Canique Radio Hat for Raspberry Pi. Your Raspberry PI will then be able to communicate with Canique Temperature/Humidity sensors (with up to 20 years battery life time) via an encrypted 868 MHz channel.


Pre-Requisites:  
You need a Raspberry Pi (tested on Raspberry PI 3)  
You need a Debian Bullseye based OS on your Raspberry Pi  
You need a Canique Radio Hat (available soon in Canique Shop) with antenna and u.FL cable  
You need at least 1 Canique Climat (temperature/humidity sensor) to talk to  


1) Run install.sh on your Raspberry PI to automatically install InfluxDB, a bugfixed Canique version of Mosquitto, Nginx webserver, PHP 7.4, the Canique Local Cockpit (a webpage that gives you access to your sensor data without internet connection), and Canique software to communicate with the hat  
Open a terminal on your Raspberry PI  
`cd /tmp && git clone https://github.com/canique/gateway`  
`chmod u+x gateway/raspberry-pi-radio-hat/install.sh && gateway/raspberry-pi-radio-hat/install.sh`  

2) Shut down your Raspberry PI:  
`sudo shutdown -h now`  

3) Disconnect Power from your Raspberry Pi  

4) Attach the antenna cable to the Canique Radio Hat  
   Attach the Canique Radio Hat to your Raspberry Pi  
   Connect the antenna to the cable  

5) Reconnect Power to your Raspberry Pi  

6) Setup connection between your mosquitto broker and Canique Cloud  
Enter in a terminal on your Raspberry Pi, replacing MQTT_USER and MQTT_PASSWORD with your own user and password that you got with the hat  
`canique-setup-mosquitto-bridge MQTT_USER MQTT_PASSWD`  

6) Setup sensor radio password for every Canique Climat that you have  
`runuser -u cnq canique-setup-sensor-encryption`  
You will be asked for the sensor UID and the sensor radio password. Repeat this step for every sensor you want to connect.

7) Restart the Canique Radio Bridge so that all sensor passwords are updated  
`sudo systemctl restart canique-radio-bridge`  

8) Insert battery into Canique Climat  


That's it.  
You can now see your sensor data on https://cockpit.canique.com and in your local network visiting the IP address of your Raspberry Pi in a webbrowser.
