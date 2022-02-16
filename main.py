#COMMON
import pycom
import time
import utime
import uos
#WIFI
from network import WLAN
#UDP
import socket
#WEB
import usocket
import _thread
import general
import micropython
# CONFIG
import config
import state

################################################################
#######################     EXECUTION    #######################
################################################################
state.init()

print(config.wifiSsid)

# Init IOs
general.initSystemHardware()

# Init WiFi
general.initWiFi()

# Init LoRa
general.initLoRa()

general.startTCPServer()
general.startUDPServer(config.localIP)
x=0
while True:
    utime.sleep(1)
    x+=1
    print("#"+str(x)+"Attempt to read UDP...")
    general.udpServ.readPacket()
# Start WebServer
initWeb()



print("End Main")
