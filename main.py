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
#######################        UDP       #######################
################################################################

"""
def udpSend():
    udpIp = "192.168.4.2"
    udpPort = 55057
    udpMsg = b"Coucou"
    sock = socket.socket(socket.AF_INET, # Interne
                         socket.SOCK_DGRAM) # UDP
    sock.sendto(udpMsg, (udpIp, udpPort))
    #print("Sent \"" + udpMsg + "\" to " + udpIp)

def udpReceive():
    print("Ready to receive ...")
    udpIp = "192.168.4.1"
    udpPort = 5005
    sock = socket.socket(socket.AF_INET,
                         socket.SOCK_DGRAM)
    sock.bind((udpIp, udpPort))
    while True:
        data, addr = sock.recvfrom(1024) #Buffer size
        print("Received UDP mdg : %s" % data)
"""


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
general.startUDPServer("192.168.4.1")
x=0
while True:
    utime.sleep(1)
    x+=1
    print("#"+str(x)+"Attempt to read UDP...")
    general.udpServ.readPacket()
# Start WebServer
initWeb()



print("End Main")
