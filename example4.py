#!/usr/bin/python3
import time
import sys
import logging
import pprint
logging.basicConfig(level=logging.DEBUG)

def syscb(src, *args):
    pprint.pprint(src)
    for arg in args:
        #print('')
        pprint.pprint(arg)

from pyhomematic import HMConnection

#pyhomematic = HMConnection(remote="ccu3-webui", remoteport=2001, systemcallback=syscb)
pyhomematic = HMConnection(
                               systemcallback=syscb,
                               remotes={
                                   "wired":{
                                   "ip":"ccu3-webui",
                                   "port": 2000,
                                   "resolvenames": "json",
                                   "username":"PmaticAdmin", 
                                   "password": "EPIC-SECRET-PW"},
                                   "Funk":{
                                   "ip":"ccu3-webui",
                                   "port": 2001,
                                   "resolvenames": "json",
                                   "username":"PmaticAdmin", 
                                   "password": "EPIC-SECRET-PW"},
                                   "HmIP":{
                                   "ip":"ccu3-webui",
                                   "username":"PmaticAdmin", 
                                   "password": "EPIC-SECRET-PW",
                                   "resolvenames": "json",
                                   "port": 2010},
                                   "CUxD":{
                                   "ip":"ccu3-webui",
                                   "resolvenames": "json",
                                   "username":"PmaticAdmin", 
                                   "password": "EPIC-SECRET-PW",
                                   "port": 8701},
                                   "groups":{
                                   "ip":"ccu3-webui",
                                   "resolvenames": "json",
                                   "username":"PmaticAdmin", 
                                   "password": "EPIC-SECRET-PW",
                                   "path": "/groups",
                                   "port": 9292}
                                   }
                                   )


from xml.dom import minidom

# parse an xml file by name
# mydoc = minidom.parse('tclrega-script.xml')

# items = mydoc.getElementsByTagName('item')  

from xmlrpc.client import ServerProxy
p = ServerProxy("http://ccu3-webui:2010")
t = p.getDeviceDescription("001658A99FD1E2:1")
print (t)
t = p.getParamsetDescription("001658A99FD1E2:1", "MASTER")
print (t)
t = p.getParamsetDescription("001718A9A77FBC:4", "VALUES")
print (t)
t = p.getParamset("001718A9A77FBC:4", "MASTER")
print (t)
t = p.getParamsetId("001718A9A77FBC:4", "MASTER")
print (t)




print('DEVICES: ' + str(pyhomematic.devices))

pyhomematic.stop()

sys.exit(0)
