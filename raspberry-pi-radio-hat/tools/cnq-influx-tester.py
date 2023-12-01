#!/bin/python3

import time
import http.client, socket

'''
This test script will write test sensor data with ID 1 to the influx database "canique", every 2 seconds
It will output how long every HTTP request took and show if errors occured
Press CTRL-C to abort script
'''


def postInfluxMsg(msg):
    print('Sending msg to InfluxDB: ', msg)

    httpStartTime = time.perf_counter_ns()
    httpConn = http.client.HTTPConnection("localhost", 8086, timeout=5)
    httpConn.connect()

    httpStartTime2 = time.perf_counter_ns()

    try:
        httpConn.request("POST", "/write?db=canique&precision=ms", msg)
        response = httpConn.getresponse()
        if response.status != 204:
            print("InfluxDB rejected msg. HTTP Status", response.status, "msg", response.read().decode('utf-8'), flush=True)
        else:
            httpEndTime = time.perf_counter_ns()
            print("Transmission: OK. Request took {} ms.".format((httpEndTime-httpStartTime) // 1_000_000), flush=True)
            print("Connection took {} ms.".format((httpStartTime2-httpStartTime) // 1_000_000), flush=True)
    except socket.timeout as st:
        print("HTTP Timeout", st, flush=True)
    except http.client.HTTPException as e:
        print("HTTP Request error", e, flush=True)





while True:
    sensorId=1
    temperature=15.50
    humidity=62.74
    timestamp=time.time_ns() // 1_000_000

    msg = 'air,sensor=' + str(sensorId) + ' temperature=' + str(temperature) + ',humidity=' + str(humidity) + ' ' + str(timestamp)

    postInfluxMsg(msg)

    time.sleep(2) #wait 2 seconds
