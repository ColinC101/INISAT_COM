from network import WLAN
import time
import config


import state

class WifiObject:

    def __init__(self):
        #Getting WLAN object
        self.wlan = WLAN()


    ########################### HANDLING ###########################

    def convertTxPower(dBmValue):
        #"Possible values are between 8 and 78, where 8 corresponds to 2dBm
        #and 78 to 20dBm. All values in between increase the maximum
        #output power in 0.25dBm increments." (Pycom doc)
        return int(dBmValue * 4);


    def initWifi(self):
        """
        Initiate the WiFi communication.
        """
        print("Initializing WiFi Access Point ...")
        self.wlan.init(mode=config.wifiMode, ssid=config.wifiSsid, auth=config.wifiAuth)
                #max_tx_pwr=convertTxPower(wifiMaxTxPower))
                #protocol=
        print("WLAN initialized.")
        self.wlan.ifconfig(id=1)#Config in AP mode, with DHCP auto-negociation
        time.sleep(1)
        print("WiFi ready.")


    def disableWifi(self):
        """
        Disable the WiFi communication.
        """
        self.wlan.deinit()
        print("WiFi disabled.")

    def macDecoder(macAddr):
        """
        Decode the MAC address returned by WiFi module,
        as encoding is not standard.

            Returns:
                decodedAddr (str): The decoded MAC address
        """
        decodedAddr = ""
        for i in macAddr:
            decodedAddr = decodedAddr + '{:02X}'.format(i) + ":"
        return decodedAddr[:17]


    def getConnectedDevices(self):
        """
        Display information about all devices connected to the board in WiFi.

            Returns:
                deviceList (list): A list of MAC/IP addresses of connected devices
        """
        deviceList = self.wlan.ap_tcpip_sta_list()
        print("Connected devices :")
        for i in (deviceList):
            try:
                print("MAC: " + self.macDecoder(i.MAC)  + "|IP : " + i.IP)
            except:
                print("MAC: ??.??.??.??.??.?? |IP: " + i.IP)
        return deviceList
        #i.mac.decode('utf-16')
        #b'\xf4B\x8f\x96\xb1\x91'
        #    f4 42 8f 96 b1 91
        #b'\xd0W{\x8c(\x0O)}
        #    d0:57:7b:8c:28:00
        #b'\xc8!Xk\xfeE
        #    c8 21 58 6b fe 45
