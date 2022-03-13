from network import WLAN
import time
import config


import state

class WifiObject:

    def __init__(self):
        """
        Constructor for the object.
        """
        #Getting WLAN object
        self.wlan = WLAN()


    def initWifi(self):
        """
        Initiates the WiFi communication.
        Parameters (mode, ssid, auth) can be modified in config.py file
        """
        print(state.lang["wifi_init"])
        self.wlan.init(mode=config.wifiMode, ssid=config.wifiSsid, auth=config.wifiAuth, antenna=config.wifiAntenna)
        print(state.lang["wlan_init"])
        # Config in AP mode, with DHCP auto-negociation
        self.wlan.ifconfig(id=1,config=(config.localIP,config.localMask,config.localIP,config.localDNS))
        time.sleep(1)
        print(state.lang["wifi_ready"])


    def disableWifi(self):
        """
        Disables the WiFi communication.
        """
        self.wlan.deinit()
        print(state.lang["wifi_desinit"])


    def convertTxPower(dBmValue):
        """
        "Possible values are between 8 and 78, where 8 corresponds to 2dBm
        and 78 to 20dBm. All values in between increase the maximum
        output power in 0.25dBm increments." (Pycom doc)
        """
        return int(dBmValue * 4);


    def macDecoder(macAddr):
        """
        Decodes the MAC address returned by WiFi module, as encoding is not standard.

            Returns:
                decodedAddr (str): The decoded MAC address
        """
        decodedAddr = ""
        for i in macAddr:
            decodedAddr = decodedAddr + '{:02X}'.format(i) + ":"
        return decodedAddr[:17]


    def getConnectedDevices(self):
        """
        Displays information about all devices connected to the board in WiFi.

            Returns:
                deviceList (list): A list of MAC/IP addresses of connected devices
        """
        deviceList = self.wlan.ap_tcpip_sta_list()
        print(state.lang["con_devices"])
        for i in (deviceList):
            try:
                print("MAC: " + self.macDecoder(i.MAC) + "|IP : " + i.IP)
            except:
                print("MAC: ??.??.??.??.??.?? |IP: " + i.IP)
        return deviceList

    def getMode(self):
        """
        Return a string reprensting the current WiFi mode
        """
        crMode = self.wlan.mode()
        if crMode == WLAN.STA:
            return "WIFI_MODE_STA"
        elif crMode == WLAN.AP:
            return "WIFI_MODE_AP"
        elif crMode == WLAN.STA_AP:
            return "WIFI_MODE_AP_STA"
        else:
            return "UNKNOWN"
