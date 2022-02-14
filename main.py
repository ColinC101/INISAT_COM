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

tcpBufferSize = 4096 #Reception buffer for TCP requests

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
    print("Initializing WiFi Access Point ...")
    wlan.init(mode=wifiMode, ssid=wifiSsid, auth=wifiAuth, channel=wifiChannel, antenna=wifiAntenna, bandwidth=wifiBandwidth, max_tx_pwr=78)
              #max_tx_pwr=convertTxPower(wifiMaxTxPower))
              #protocol=
    print("WLAN initialized")
    wlan.ifconfig(id=1)#, config='dhcp') #Config in AP mode, with DHCP auto-negociation
    time.sleep(1)
    print("Success")


def disableWifi():
    wlan.deinit()

def getConnectedDevices():
    print("Connected devices :")
    deviceList = wlan.ap_tcpip_sta_list()
    for i in (deviceList):
        print("MAC: " + "000"  + "|IP : " + i.IP)
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


################################################################
#######################        WEB       #######################
################################################################


def tcpClientThread(tcpClientsocket, n):
    """
    TCP request handler
    """
    request = str(tcpClientsocket.recv(tcpBufferSize))
    splitRequest = request.split(" ")

    http_header = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:close \r\n\r\n"
    mimeTypeList = [(".html", b"text/html"),
                    (".css", b"text/css"),
                    (".jpg", b"image/jpeg"),
                    (".js", b"application/javascript"),
                    (".txt", b"text/plain"),
                    (".woff", b"font/woff"),
                    (".woff2", b"font/woff2")]

    if len(splitRequest) <= 1:
        http_body = b"Invalid request, ignoring .."
    else:
        requestContent = "index.html" if splitRequest[1]=="/" else splitRequest[1][1:]

        isCommand = general.commandHandler(requestContent)
        isEvent = general.eventHandler(requestContent, tcpClientsocket)
        if isCommand[0] == 1:
            http_body = isCommand[1]
        elif isEvent[0] == 1:
            return
        else:
            mimeType = b"application/octet-string"
            for i in mimeTypeList:
                if i[0] in requestContent:
                    mimeType = i[1]
            try:
                with open("web/" + requestContent, 'rb') as infile:
                    http_header = b"HTTP/1.1 200 OK\r\nContent-Type: " + mimeType + b"\r\nContent-Lenght: " + str(uos.stat("web/" + requestContent)[6]) + b"\r\nConnection:close \r\n\r\n"
                    http_body = infile.read()
                    infile.close()
            except OSError:
                http_body = b"Requested file : not found .."
    tcpClientsocket.send(http_header + http_body)
    http_header = ""
    http_body = ""
    tcpClientsocket.close()

def initWeb():
    """
    Initiate TCP connection for Web server communication
    """
    tcpServersocket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    tcpServersocket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
    tcpServersocket.bind((localIp, tcpPort))
    tcpServersocket.listen(maxTcpConnection)

    while True:
        (tcpClientsocket, tcpAddress) = tcpServersocket.accept()
        tcpClientThread(tcpClientsocket, utime.ticks_ms())

    tcpServersocket.close()

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
