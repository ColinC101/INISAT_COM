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



print("Begin Main")

#Getting WLAN object
wlan = WLAN() 

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
    wlan.init(mode=config.wifiMode, ssid=config.wifiSsid, auth=config.wifiAuth)
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
#######################        WEB       #######################
################################################################


def tcpClientThread(tcpClientSocket, threadNumber):
    """
    TCP request handler.

        Parameters:
            tcpClientSocket (socket): The socket of the web client
            threadNumber (int): The thread number

        Returns:
            sentBytes (int): The number of bytes sent in HTTP response
    """

    #Isolate request arguments as strings
    request = str(tcpClientSocket.recv(config.tcpBufferSize))
    splitRequest = request.split(" ")

    #Default response header
    http_header = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:close \r\n\r\n"

    #List of possible response file types
    mimeTypeList = [(".html", b"text/html"),
                    (".css", b"text/css"),
                    (".jpg", b"image/jpeg"),
                    (".js", b"application/javascript"),
                    (".txt", b"text/plain"),
                    (".woff", b"font/woff"),
                    (".woff2", b"font/woff2")]

    if len(splitRequest) <= 1: #If request is empty
        http_body = b"Invalid request, ignoring .."
    else:
        #Get the requested ressource
        requestContent = "index.html" if splitRequest[1]=="/" else splitRequest[1][1:]

        #Check if the request is a command or an asynchronous event
        isCommand = general.commandHandler(requestContent)
        isEvent = general.eventHandler(requestContent, tcpClientSocket)

        if isCommand[0] == 1: #If command
            http_body = isCommand[1]  #Return the answer of the command
        elif isEvent[0] == 1: #If event
            return 0 #Return nothing (the event handler is in charge of responding)
        else: #If file

            #Get the file type
            mimeType = b"application/octet-string"
            for i in mimeTypeList:
                if i[0] in requestContent:
                    mimeType = i[1]
            #Read the file content in binary mode
            try:
                with open("web/" + requestContent, 'rb') as infile:
                    http_header = b"HTTP/1.1 200 OK\r\nContent-Type: " + mimeType + b"\r\nContent-Lenght: " + str(uos.stat("web/" + requestContent)[6]) + b"\r\nConnection:close \r\n\r\n"
                    http_body = infile.read()
                    infile.close()
            except OSError:
                http_body = b"Requested file : not found .."

    #Send the HTTP response and close the connection
    sentBytes = tcpClientSocket.send(http_header + http_body)
    tcpClientSocket.close()

    #Clear string for memory saving (experimental)
    http_header = ""
    http_body = ""

    return sentBytes

def initWeb():
    """
    Initiate TCP connection for Web server communication.
    """
    tcpServersocket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM) #Create the socket
    tcpServersocket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1) #Initialize the socket
    tcpServersocket.bind((config.localIp, config.tcpPort)) #Bind the socket
    tcpServersocket.listen(config.maxTcpConnection) #Start listening for in coming connections

    while True:

        (tcpClientsocket, tcpAddress) = tcpServersocket.accept()
        tcpClientThread(tcpClientsocket, utime.ticks_ms()) #Start a new thread to handler the new connection

    tcpServersocket.close() #Close the server-side socket

################################################################
#######################     EXECUTION    #######################
################################################################
state.init()

print(config.wifiSsid)

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

general.startUDPServer("192.168.4.1")

while True:
    utime.sleep(5)
    print("Attempt to read UDP...")
    general.udpServ.readPacket()
# Start WebServer
initWeb()



print("End Main")
