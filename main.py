#COMMON
from ioctl import Ioctl
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

# Init system
general.initSystemHardware()

# Init WiFi
general.initWiFi()

# Init LoRa
general.initLoRa()

general.startTCPServer()
general.startUDPServer(config.localIP)
x=0


while True:
    # Blink WiFi LED if necessary
    general.blinkWiFiLED()

    if state.loraObj.getLoraStatus():
        # LoRa activated => blink the LED if necessary
        general.blinkLoRaLED()
    elif state.ioctlObj.getObject(Ioctl.KEY_LORA_LED).value() == 1:
        # Deactivate the LoRa LED if it is still active while LoRa is off
        state.ioctlObj.getObject(Ioctl.KEY_LORA_LED).value(0)


    utime.sleep(1)
    print("Attempt to read UDP...")
    general.udpServ.readPacket()
# Start WebServer
initWeb()



print("End Main")
