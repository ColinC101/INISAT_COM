#WIFI
from network import WLAN
from network import LoRa

################################################################
#######################  HARDWARE CONFIG   #####################
################################################################

# Inertia wheel / magneto coupler X 
PIN_PWM_X = 'P8'
PIN_DIR_X = 'P9'


# Magneto coupler Y 
PIN_PWM_Y = 'P10'
PIN_DIR_Y = 'P11'

# LoRa status LED
PIN_LORA_LED = 'P19'

# WiFi status LED
PIN_WIFI_LED = 'P2'

# PyCam control
PIN_CAM_CONTROL = 'P20'

# UART OBC
PIN_UART_OBC_RX = 'P4'
PIN_UART_OBC_TX = 'P3'
UART_OBC_BAUD = 115200

################################################################
#######################  WEB SERVER CONFIG   ###################
################################################################

# Server Port
tcpPort = 8080

# Reception buffer for TCP requests
tcpBufferSize = 4096 

# Backlog of Web Server socket
maxFailedConnection = 5

################################################################
#######################  WIFI CONFIG     #######################
################################################################

#   https://docs.pycom.io/firmwareapi/pycom/network/wlan/#app

# IP of server
localIP = "192.168.4.1"

# Mask of the subnet
localMask = "255.255.255.0"

# Address of the DNS
localDNS = "8.8.8.8"

# Wifi mode (AP, STA or STA_AP)
wifiMode = WLAN.AP 

# SSID of Wifi AP
wifiSsid = 'INISAT' 

# Authentification key for Wifi AP
wifiAuth=(WLAN.WPA2, "123456789") 

# Channel for Wifi connection
wifiChannel = 1 

# Select between integrated and external antenna (WLAN.EXT_ANT)
wifiAntenna = WLAN.INT_ANT 

# Bandwith to use for WiFi, 20MHz or 40MHz
# wifiBandwidth = WLAN.HT40 

# WiFi power in dBm
wifiMaxTxPower = 19.5 

# Blink period for WiFi LED 
WIFI_LED_BLINK_CYCLE = 3000

################################################################
#####################  CAMERA CONFIG     #######################
################################################################
CAMERA_IP = "192.168.4.2"

################################################################
#######################  LoRa CONFIG     #######################
################################################################

loraMode = LoRa.LORA
loraRegion = LoRa.EU868  # Europe

# Parameters only for LoRa.LORA mode
#loraFrequency = 0  #TODO, est-ce qu'il y a une valeur par défaut ? Rien trouvé dans le code .ino
loraTxPower = 17  # 17dBm
loraBandwidth = LoRa.BW_125KHZ
loraSpreadingFactor = 7
loraPreamble = 8
loraCodingRate = LoRa.CODING_4_5
loraPowerMode = LoRa.ALWAYS_ON
loraTxIQ = False
loraRxIQ = False
loraPublicSync = True

# Parameters only for LoRa.LORAWAN mode
loraAdaptativeDataRate = 0
loraTxRetries = 0
loraDeviceClass = 0

# Blink period for LoRa LED
LORA_LED_BLINK_CYCLE = 3000

################################################################
#######################  UDP SERVER CONFIG   ###################
################################################################
UDP_PORT = 9991


################################################################
#######################  SYSTEM CONFIG   #######################
################################################################

# OBC interval for requests
OBC_INTERVAL = 1000

# 5min30, time window for connected user (with '/ouvPage' or '/user' request)
USER_SIGNALING_INTERVAL = 330000 

# LoRa interval for requests
LORA_INTERVAL = 90000

# Interval for interface requests
INTERFACE_INTERVAL = 60000

# Interval for GNSS requests
GNSS_INTERVAL = 2000