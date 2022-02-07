from network import WLAN
import pycom
import time

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
        print("MAC: " + i.mac.decode('utf-16') + "|IP : " + i.IP)
    return deviceList
    #b'\xf4B\x8f\x96\xb1\x91'
    #    f4 42 8f 96 b1 91
    #b'\xd0W{\x8c(\x0O)}
    #    70:4d:7b:c2:f1:f4
    #    d0:57:7b:8c:28:00

print(wifiSsid)

initWifi()
time.sleep(10)
getConnectedDevices()
