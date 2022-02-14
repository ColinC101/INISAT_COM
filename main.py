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
#import http.server
#import socketserver
import general

import micropython

#import utime
#tics_ms()

print("Begin Main")

################################################################
#######################  GLOBAL CONFIG   #######################
################################################################

localIp = "192.168.4.1"
tcpPort = 8080


################################################################
#######################       WIFI       #######################
################################################################

#   https://docs.pycom.io/firmwareapi/pycom/network/wlan/#app

############################ CONFIG ############################

wlan = WLAN() #Getting WLAN object

wifiMode = WLAN.AP #Wifi mode (AP, STA or STA_AP)
wifiSsid = 'INISAT' #SSID of Wifi AP
wifiAuth=(WLAN.WPA2, "123456789") #Authentification key for Wifi AP
wifiChannel = 1 #Channel for Wifi connection
wifiAntenna = WLAN.INT_ANT #Select between integrated and external antenna (WLAN.EXT_ANT)
wifiBandwidth = WLAN.HT40 #Bandwith to use for Wifi, 20MHz or 40MHz
wifiMaxTxPower = 19.5 #WiFi power in dBm

#wifiProtocol =
maxTcpConnection = 5

########################### HANDLING ###########################

def convertTxPower(dBmValue):
    #"Possible values are between 8 and 78, where 8 corresponds to 2dBm
    #and 78 to 20dBm. All values in between increase the maximum
    #output power in 0.25dBm increments." (Pycom doc)
    return int(dBmValue * 4);


def initWifi():
    """
    Initiate the WiFi communication.
    """
    print("Initializing WiFi Access Point ...")
    wlan.init(mode=wifiMode, ssid=wifiSsid, auth=wifiAuth, channel=wifiChannel, antenna=wifiAntenna, bandwidth=wifiBandwidth, max_tx_pwr=78)
              #max_tx_pwr=convertTxPower(wifiMaxTxPower))
              #protocol=
    print("WLAN initialized.")
    wlan.ifconfig(id=1)#Config in AP mode, with DHCP auto-negociation
    time.sleep(1)
    print("WiFi ready.")


def disableWifi():
    """
    Disable the WiFi communication.
    """
    wlan.deinit()
    print("WiFi disabled.")

def macDecoder(macAddr):
    """
    Decode the MAC address returned by WiFi module,
    as encoding is not standard.

        Returns:
            decodedAddr (str): The decoded MAC address
    """
    pos = 0
    decodedAddr = ""
    while pos < len(macAddr):
        if macAddr[pos] == "\\":
            pos += 1
        elif macAddr[pos] == "x":
            decodedAddr = decodedAddr + macAddr[pos+1:pos+3] + ":"
            pos += 3
        else:
            decodedAddr = decodedAddr + "??:"
            pos += 1
    return decodedAddr


def getConnectedDevices():
    """
    Display information about all devices connected to the board in WiFi.

        Returns:
            deviceList (list): A list of MAC/IP addresses of connected devices
    """
    deviceList = wlan.ap_tcpip_sta_list()
    print("Connected devices :")
    for i in (deviceList):
        print("MAC: " + macDecoder(i.MAC)  + "|IP : " + i.IP)
    return deviceList
    #i.mac.decode('utf-16')
    #b'\xf4B\x8f\x96\xb1\x91'
    #    f4 42 8f 96 b1 91
    #b'\xd0W{\x8c(\x0O)}
    #    d0:57:7b:8c:28:00
    #b'\xc8!Xk\xfeE
    #    c8 21 58 6b fe 45

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

print(wifiSsid)

#initWifi()
#time.sleep(10)
#getConnectedDevices()
#udpReceive();

# Init IOs
general.setupGPIO()

# Init WiFi
initWifi()

# Init LoRa
general.initLoRa()

# Start WebServer
initWeb()

print("End Main")
