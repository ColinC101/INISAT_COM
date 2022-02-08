#COMMON
import pycom
import time
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

def client_thread(clientsocket, n):
    request = str(clientsocket.recv(4096))
    if len(request) == 0:
        clientsocket.close()
        return
    #else:
        #print("Received: {}".format(request))


    splitRequest = request.split(" ")
    if len(splitRequest) <= 1:
        fileName = "1"
    else:
        fileName = "/index.html" if splitRequest[1]=="/" else splitRequest[1]


    mimeTypeList = [(".html", b"text/html"),
                    (".css", b"text/css"),
                    (".jpg", b"image/jpeg"),
                    (".js", b"application/javascript"),
                    (".txt", b"text/plain"),
                    (".woff", b"font/woff"),
                    (".woff2", b"font/woff2")]

    mimeType = b"application/octet-string"
    for i in mimeTypeList:
        if i[0] in fileName:
            mimeType = i[1]

    try:
        with open("web" + fileName, 'rb') as infile: #(fileName if fileName[0]=='/' else ("/"+fileName))
            print(fileName)
            http = b"HTTP/1.1 200 OK\r\nContent-Type: " + mimeType + b"\r\nContent-Lenght: " + str(uos.stat("web" + fileName)[6]) + b"\r\nConnection:close \r\n\r\n"
            response_body = infile.read()
            infile.close()
    except OSError:
        http = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:close \r\n\r\n"
        response_body = b"No index file found..."

    clientsocket.send(http + response_body)

    clientsocket.close()
    time.sleep_ms(500)

def initWeb():
    """PORT = 8080
    Handler = http.server.SimpleHTTPRequestHandler

    with socketserver.TCPServer(("", PORT), Handler) as httpd:
        print("serving at port", PORT)
        httpd.serve_forever()
    """

    serversocket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM)
    serversocket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1)
    serversocket.bind(("192.168.4.1", 8080))
    serversocket.listen(1)

    while True:
        (clientsocket, address) = serversocket.accept()
        _thread.start_new_thread(client_thread, (clientsocket, 1))
    serversocket.close()
################################################################
#######################     EXECUTION    #######################
################################################################

print(wifiSsid)

#initWifi()
#time.sleep(10)
#getConnectedDevices()
#udpReceive();
initWifi()
initWeb()
