#!/usr/bin/env python3

from zeroconf import ServiceBrowser, Zeroconf, IPVersion
import time

class MyListener:

    def remove_service(self, zeroconf, type, name):
        print("Service %s removed" % (name,))

    def add_service(self, zeroconf, type, name):
        info = zeroconf.get_service_info(type, name)
        #print("Service %s added, service info: %s" % (name, info))

        addresses = info.parsed_addresses(IPVersion.V4Only)
        addr = None
        if len(addresses) > 0:
            addr = addresses[0]

        print("Service {} @ {}:{} ".format(info.name, addr, info.port))


zeroconf = Zeroconf(ip_version=IPVersion.V4Only)
listener = MyListener()

browser = ServiceBrowser(zeroconf, "_mqtt._tcp.local.", listener)
try:
    time.sleep(1)
finally:
    zeroconf.close()
