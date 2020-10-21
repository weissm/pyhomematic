#!/usr/bin/python3
import time
import sys
import logging
from pyhomematic import HMConnection

logging.basicConfig(level=logging.INFO)

DEVICE1 = '001718A9A77FBC:1'  # e.g. KEQ7654321
DEVICE2 = '001718A9A77FBC'  # e.g. LEQ1234567
DEVICE3 = 'address_of_thermostat'

def systemcallback(src, *args):
    print("hier:", src)
    for arg in args:
        print(arg)
    return {}


#pyhomematic = HMConnection(local="192.168.178.35", localport=7080, remote="192.168.178.39", remoteport=2001, systemcallback=systemcallback) # Create server thread
#pyhomematic.start() # Start server thread, connect to homegear, initialize to receive events


#for room in ccu.rooms:
#    print("%-30s %d devices" % (room.name, len(room.devices)))


try:
    # Create a server that listens on 127.0.0.1:7080 and identifies itself as myserver.
    # Connect to Homegear at 127.0.0.1:2001
    # Automatically start everything. Without autostart, pyhomematic.start() can be called.
    # We add a systemcallback so we can see what else happens besides the regular events.
    pyhomematic = HMConnection(
                               interface_id="myserver",
#                               autostart=True,
                               local="raspberrypi",
                               localport=7080,
                               systemcallback=systemcallback,
                               remotes={
                                   "Funk":{
                                   "ip":"ccu3-webui",
                                   "username":"PmaticAdmin", 
                                   "password": "EPIC-SECRET-PW",
                                   "resolvenames": "json",
                                   "port": 2010}
				   }
                                   )
except Exception:
    sys.exit(1)

import sys
sys.path.append('/home/pi/shared/work/pmatic')
import pmatic

print ("--------------------------------------------------------------------------------------------------")
ccu = pmatic.CCU(address="http://ccu3-webui", credentials=("PmaticAdmin", "EPIC-SECRET-PW"))
test = ccu.api.interface_get_paramset(interface="HmIP-RF",
                                         address="001718A9A77FBC:1", paramsetKey="MASTER")
print(test)
test = ccu.api.interface_get_paramset(interface="CUxD",
                                         address="CUX2801001:1", paramsetKey="MASTER")
print("hier: ", test)
result = ccu.api.interface_init(interface="HmIP-RF",
            url="http://ccu3-webui:9124", interfaceId="HmIP-RF")
test = ccu.api.interface_get_paramset(interface="HmIP-RF",
                                         address="001718A9A77FBC:1", paramsetKey="MASTER")
print("from 9124", test)

test = pmatic.events.EventListener(ccu)
test._register_with_ccu(interface = "HmIP-RF", interfaceId = "HmIP-RF")
test = ccu.api.interface_get_paramset(interface="HmIP-RF",
                                         address="001718A9A77FBC:1", paramsetKey="MASTER")
print(test)

print ("--------------------------------------------------------------------------------------------------")
pyhomematic.start()


def eventcallback(address, interface_id, key, value):
    print("CALLBACK: %s, %s, %s, %s" % (address, interface_id, key, value))

sleepcounter = 0
while not pyhomematic.devices and sleepcounter < 20:
    print("Waiting for devices")
    sleepcounter += 1
    time.sleep(1)
print(pyhomematic.devices)



print("start devices")
test = ccu.api.interface_get_paramset(interface="HmIP-RF",
                                         address="001718A9A77FBC:1", paramsetKey="MASTER")


from xmlrpc.client import ServerProxy
p2 = ServerProxy("http://ccu3-webui:2010")
t = p2.getParamset("001718A9A77FBC:1", "MASTER")
print ("after init proxie1", t)


print("test:", test)
print(pyhomematic.getAllSystemVariables("Funk"))
print(pyhomematic.listBidcosInterfaces("Funk"))
print(pyhomematic.devices['Funk'])

# Get level of rollershutter from 0.0 to 1.0.
print(pyhomematic.devices_all["Funk"][DEVICE1])

# Set level of rollershutter to 50%.
pyhomematic.devices[DEVICE1].set_level(0.5)
time.sleep(10)

# Move rollershutter down.
pyhomematic.devices[DEVICE1].move_down()
time.sleep(10)

# Get level of rollershutter from 0.0 to 1.0 directly from channel.
print(pyhomematic.devices_all[DEVICE1 + ':1'].getValue("LEVEL"))

# Check if doorcontact is open by querying the device.
print(pyhomematic.devices[DEVICE2].is_open())

# Check if doorcontact is open or closed by querying the device-channel. True or False, depending on state.
print(pyhomematic.devices_all[DEVICE2 + ':1'].getValue("STATE"))

# Get Actual Temperature
print(pyhomematic.devices[DEVICE3].actual_temperature)

# Get Set Temperature
print(pyhomematic.devices[DEVICE3].set_temperature)

# Get Battery State
print(pyhomematic.devices[DEVICE3].battery_state)

# Set an eventcallback for the doorcontact that should be called when events occur.
pyhomematic.devices[DEVICE2].setEventCallback(eventcallback)
time.sleep(10)
# Now open / close doorcontact and watch the eventcallback being called.

# Stop the server thread so Python can exit properly.
pyhomematic.stop()

sys.exit(0)
