# Canique Gateway

Here you'll find tools related to the 868MHz Radio Gateway on https://www.canique.com/gateway


# Canique Gateway Discovery

You can discover all Canique Gateways in your local network (and find out their IP addresses) by doing the following:

Install zeroconf for python:  
`pip3 install zeroconf`

Run the Canique Gateway Discovery tool:  
`python3 ./cnq-gateway-discovery.py`


# Sample Script to output air sensor and battery data

`cnq-print-sensor-data.py` is a Python script that connects to a Canique Gateway and prints live air sensor and battery status updates. You can quit it by pressing CTRL-C.  

Install dependencies first: `pip3 install gmqtt uvloop`  

Let's say your Canique Gateway IP is 192.168.1.200  
Then run: `python3 ./cnq-print-sensor-data.py 192.168.1.200`
