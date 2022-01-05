#!/usr/bin/env python3

import asyncio
import os, sys, signal
import datetime
import json

from gmqtt import Client as MQTTClient
import gmqtt
import re

#
# pip3 install gmqtt uvloop
#

import uvloop
asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())


STOP = asyncio.Event()
keepRunning = True

def on_connect(client, flags, rc, properties):
    print('Connected. Session present:', flags, 'Props:', properties)

    if flags == 0: #session NOT present, when subscribing we'll receive retained msgs
        print('Subscribing...')
        client.subscribe([gmqtt.Subscription('sensors/+/+/reading', qos=1),
        gmqtt.Subscription('sensors/+/+/battery', qos=1)])



async def on_message(client, topic, payload, qos, properties):
    m = re.fullmatch('sensors/([a-z]+)/([0-9]+)/(reading|battery)', topic) #e.g. sensors/air/5/reading

    if m != None:
        if m.group(1) == 'air' and m.group(3) == 'reading':
            sensorData = json.loads(payload)

            if 'aH' not in sensorData or 'rssi' not in sensorData:
                return

            temperature = sensorData['tmp']
            relHum = sensorData['hdt']

            absHum = sensorData['aH']
            rssi = sensorData['rssi']

            timestamp = sensorData['ts']
            sensorId = sensorData['sid']

            #timestamp is unix time in ms
            nowTime = datetime.datetime.fromtimestamp(int(timestamp / 1000))

            print("{} - Air Sensor {}: Rel. Humidity = {}%, Absolute Humidity = {}, Temperature = {}°C, Signal Strength: {} dBm".format(nowTime, sensorId, relHum, absHum, temperature, rssi))
        elif m.group(3) == 'battery':
            sensorData = json.loads(payload)

            timestamp = sensorData['ts']
            sensorId = sensorData['sid']
            milliVolts = sensorData['mV']

            #timestamp is unix time in ms
            nowTime = datetime.datetime.fromtimestamp(int(timestamp / 1000))

            print("{} - Battery Status Sensor {}: {} V".format(nowTime, sensorId, milliVolts/1000))





def on_disconnect(client, packet, exc=None):
    print('Disconnected', flush=True)

def on_subscribe(client, mid, qos, properties):
    print('SUBSCRIBED')

def ask_exit(*args):
    global keepRunning
    keepRunning = False
    STOP.set()

async def main(broker_host, token):
    client = MQTTClient("mqtt-print-data-test-client", clean_session=True)

    client.on_connect = on_connect
    client.on_message = on_message
    client.on_disconnect = on_disconnect
    client.on_subscribe = on_subscribe

    #client.set_auth_credentials(token, None)

    while keepRunning:
        waitTime = 60 # reconnect interval after a manual disconnect
        try:
            await client.connect(broker_host, 1883, keepalive=60)

            await STOP.wait()
            STOP.clear()

            await client.disconnect()
        except Exception as e: #ConnectionRefusedError (MQTT)
            waitTime = 5
            print("Exception while connecting to MQTT", e)


        #wait before connecting again
        if keepRunning:
            try:
                await asyncio.wait_for(STOP.wait(), waitTime)
                STOP.clear()
            except asyncio.TimeoutError:
                pass

    print("Exiting", flush=True)



if __name__ == '__main__':
    loop = asyncio.get_event_loop()

    if len(sys.argv) != 2:
        print("Please specify host IP as argument")
        exit(1)

    host = sys.argv[1]
    token = ''

    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    loop.run_until_complete(main(host, token))
