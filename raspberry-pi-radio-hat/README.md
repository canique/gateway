# Canique Radio Hat for Raspberry Pi
![Radio Hat in Action](https://www.canique.com/img/1080px/radio_hat_cockpit_accuracy.jpg)

[Video showing accuracy of Canique Temperature Monitoring System](https://www.youtube.com/watch?v=cbi-35kW44U) - Video shows Raspberry Pi 4 + Radio Hat + 3 Canique Climat sensors and live updates on an iPad

## Quick-Installation

This How-To will explain how to turn your Raspberry Pi into a Canique 868MHz Gateway using a Canique Radio Hat for Raspberry Pi. Your Raspberry PI will then be able to communicate with Canique Temperature/Humidity sensors (with up to 20 years battery life time) via an encrypted 868 MHz channel.

There is also an [extended installation procedure](install_radiohat_software.md) available with more details.


Pre-Requisites:  
- a Raspberry Pi (tested on Raspberry Pi 3 and Raspberry Pi 4)
- a 32-bit Debian Bullseye based OS with systemd (tested with Raspberry Pi OS Lite 32-bit)
- a [Canique Radio Hat for Raspberry Pi](https://www.canique.com/radio-hat) with antenna and u.FL cable
- at least 1 [Canique Climat](https://www.canique.com/climat) (temperature/humidity sensor) to talk to  


1) Run install.sh on your Raspberry PI to automatically install InfluxDB, a bugfixed Canique version of Mosquitto, Nginx webserver, PHP 7.4, the Canique Local Cockpit (a webpage that gives you access to your sensor data without internet connection), and Canique software to communicate with the hat  
```
mkdir /tmp/cnq-gateway && cd /tmp/cnq-gateway && \
wget -q https://raw.githubusercontent.com/canique/gateway/main/raspberry-pi-radio-hat/install.sh
chmod u+x install.sh && ./install.sh
```  

2) Wait for the install script to finish, then shut down your Raspberry Pi:  
`sudo shutdown -h now`  

3) Wait for the LEDs on your Raspberry Pi to stop blinking, then disconnect Power from your Raspberry Pi  

4) - Insert CR2032 battery into Canique Radio Hat's battery holder (unless already done)
   - Attach the antenna cable to the Canique Radio Hat (unless already done)
   - Connect the Canique Radio Hat to your Raspberry Pi
   - Connect the antenna to the cable

5) Reconnect Power to your Raspberry Pi  
   After booting up, the Radio Hat should already be working. You can display the last 100 log lines with the command:  
   `journalctl -n100 -u canique-radio-bridge`  
   In case the radio bridge is not running, run:
   `sudo systemctl restart canique-radio-bridge`  

6) Setup connection between your mosquitto broker and Canique Cloud (optional)  
Enter in a terminal on your Raspberry Pi, replacing MQTT_USER and MQTT_PASSWORD with your own user and password that you got with the hat  
`sudo canique-setup-mosquitto-bridge MQTT_USER MQTT_PASSWORD`  
(You can skip this step if you do not want to use the Canique Cloud. Then your data will stay local.)

7) Setup sensor radio password for every Canique Climat that you have  
If you have a Radio Hat with HW version < 0.8.x, then run  
`sudo runuser -u cnq canique-setup-sensor-encryption`  
For HW versions 0.8.x or greater, your Radio Hat comes with an onboard EEPROM. The passwords are usually already setup at the factory, and you can skip this step. If you later add new sensors, though, then run   
`sudo -u cnq canique-sensor-keytool set`  
You will be asked for the sensor UID and the sensor radio password. Repeat this step for every sensor you want to connect.

8) For Radio Hat HW versions < 0.8.x, restart the Canique Radio Bridge so that all sensor passwords are updated  
`sudo systemctl restart canique-radio-bridge`  

9) Insert battery into Canique Climat or follow [Canique Climat setup steps](https://www.canique.com/climat-first-steps) skipping the first sections and proceeding with *Setting up Canique Climat*   


That's it.  
You can now see your sensor data on https://cockpit.canique.com (if you also followed step 6) and in your local network visiting the IP address of your Raspberry Pi in a webbrowser.



## Troubleshooting RF issues

If message loss occurs, this guide will help you:
1) Make sure the amber LED on the radio hat is not fully turned on. It should not blink more often than once a second. If it is blinking permanently,
   - You can try changing the direction of the u.FL antenna cable, gently turn it to the left or to the right while taking care to not pull it off its socket. This may sometimes help.
   - Make sure you are using a high quality power supply. The radio hat is tested with the original Raspberry Pi Power Supply. If you use a bad quality one, the output voltage may contain high ripple voltage which will lead to an increased radio noise floor and which in turn will lead to message loss.
   - if you are already using a good power supply and playing with the u.FL cable direction did not help, you can increase the threshold above which the radio will accept messages. The goal is to increase this threshold above the RF noise floor. By default it is set to -98 dBm. You can open the settings in an editor by running `sudo nano /etc/cnq-radio-bridge` and then add/change the section
   ```
   [RADIO]
   rssi-threshold=-92
   ```
   Then run `sudo systemctl restart canique-radio-bridge` for the changes to take effect - in this case the threshold is increased to -92 dBm so that noise is blocked better but at the same time the wireless range is slightly reduced. You should keep that level between -85 and -98 dBm. If you go beyond -85dBm even valid messages might not be recognized. If you go beyond -98 dBm you may risk message loss.

2) In case you only observe message loss on one sensor, make sure that the antenna of the sensor and the antenna of the radio hat are parallel to each other. If the sensor is in an enclosure, the antenna is placed lengthwise inside.


## Radio Reception Quality / Noise Indicator

The Raspberry Pi can emit noise (which also covers the 868MHz band) while doing SD card writes, or while  heavily using the WiFi chip or LAN (e.g. while downloading a file). To keep the received noise level to a minimum so that the antenna of the Canique Gateway Hat does not see much interference, you should keep heavy SD card writes or network transactions to a minimum.   
You can see the noise level visually by looking at the amber RX LED of the Canique Gateway Hat. If the RX LED is on all the time, this means that the received noise is above the RX threshold (set to -98 dBm by default) all the time and message loss will occur.
Please note that noise can also stem from a TV in the close proximity or some other electronic device.


## Canique Radio Bridge Log Format

You can see the last 100 lines of log data about how messages from the Canique Radio Hat are received, by running   
`journalctl -n100 -u canique-radio-bridge` or   
`journalctl -n100 -f -u canique-radio-bridge` to see new data as it arrives.   

Sometimes you may see a message like
```
TX 5 -> RX 1: Decrypt Failed. [12, 1, 5, 64, 110, 131, 71, 123, 189, 169, 125, 13, 111]
```
This is to be read as: A sender with network ID 5, sent a message to a receiver with network ID 1 (gateway) which is the radio hat. The message could not be decrypted successfully. In square brackets you see the original bytes that were received.   
The possible reasons as to why a message could not be decrypted are:
1) The radio hat has just been (re)started and the sensor must send a long message first with all the necessary data for decryption to work
2) There was a transmission error of the message while it was sent over the air, e.g. due to bad reception quality.
3) The password for that sender has not been setup with the radio hat

Once in while you may see a message like
```
[GW Log] RX Rdy: 579926, Sync Addr: 13292, Sync Addr Tout 566634, Fifo Level Tout 0, Payload Rdy Tout 0
```
The radio hat gathers statistics about certain events.   
First an easy explanation:   

RX Ready = how often the RX LED turned on   
Sync Address = number of messages from a Canique device   
Sync Address Timeout = number of false positives (radio thinking it's a message but it is noise)   
Fifo Level Timeout = number of cut off messages   
Payload Ready Timeout = number of incomplete messages that were too long to be counted as cut off but too short to be complete


The technical explanation:   

Rx Rdy (RX Ready): number of times that the radio has seen a signal which is above the receive RSSI threshold (-98 dBm by default). This is basically the number of times that the RX LED has turned on.   

Sync Addr (Synchronization Address): number of times that a certain byte sequence has been received after the RX Ready event. This byte sequence is telling the Radio Hat that this is most probably a Canique message.   

Sync Addr Tout (Synchronization Address Timeout): number of times that the radio timed out waiting for the synchronization address. This timeout will happen on a false Rx Ready, e.g. if the RX Ready event was triggered by EMI or some other noise in the frequency spectrum rather than by a genuine message.   
So basically: Number of RX Ready = Number of Sync Addr + Number of Sync Addr Timeout   

Fifo Level Tout (Fifo Level Timeout): After receiving the Synchronization Address, the radio waits for a certain number of bytes to be received. These are written into a first-in-first-out (Fifo) queue. If these bytes are not received within a certain timeout, then this counter will increment.   

Payload Rdy Tout (Payload Ready Timeout): After enough bytes have been written to the Fifo, the complete message must be received within a certain time. If the radio fails to receive the complete message within a certain time, this counter will increment.


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
This command assumes that your root partition is on /dev/mmcblk0p2 - adjust it to your needs.


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


## Developer Information

[Adjusting the local cockpit to your needs](local_cockpit.md)
