#COMMON
import aliases
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
import uart


################################################################
#######################     EXECUTION    #######################
################################################################
state.init()

print(config.wifiSsid)

# Init language structure
general.updateLang()

# Init system
general.initSystemHardware()

# Init WiFi
general.initWiFi()

# Init LoRa
general.initLoRa()

# Init UART with OBC
uartOBC = uart.OBCuart()

general.startTCPServer()
general.startUDPServer(config.localIP)

while True:
    # Blink WiFi LED if necessary
    general.blinkWiFiLED()

    if state.loraObj.getLoraStatus():
        # LoRa activated => blink the LED if necessary
        general.blinkLoRaLED()
    elif state.ioctlObj.getObject(Ioctl.KEY_LORA_LED).value() == 1:
        # Deactivate the LoRa LED if it is still active while LoRa is off
        state.ioctlObj.getObject(Ioctl.KEY_LORA_LED).value(0)

    if state.camStatus != state.ioctlObj.getObject(Ioctl.KEY_CAM_CONTROL).value():
        # Update camera control PIN if needed
        state.ioctlObj.getObject(Ioctl.KEY_CAM_CONTROL).value(state.camStatus)

    if (utime.ticks_ms() - state.lastOBCTime) > config.OBC_INTERVAL:
        # OBC requests can be done here

        if (state.disconnectCb) and (not state.udpCom):
            # Web interface user is diconnected
            state.userConnected = 0
            state.consoleConfig = aliases.CONSOLE_CONFIG_DISABLED.copy()
            state.chartsConfig = aliases.CHARTS_CONFIG_DISABLED.copy()
            print(state.lang["user_disconnected"])
            state.lastUserTime = utime.ticks_ms()

        if ((utime.ticks_ms() - state.lastLoRaTime) > config.LORA_INTERVAL):
            # LoRa request
            state.affLora = True
            state.affLora_ex = True
            state.lastLoRaTime = utime.ticks_ms()

        if ((utime.ticks_ms() - state.lastConsoleTime) > state.consoleInterval):
            # Console request
            state.affCons = True
            state.affCons_ex = True
            state.lastConsoleTime = utime.ticks_ms()

        if ((utime.ticks_ms() - state.lastChartsTime) > state.chartsInterval):
            # Charts request
            state.affGraph = True
            state.affGraph_ex = True
            state.lastChartsTime = utime.ticks_ms()

        if ((utime.ticks_ms() - state.lastInterfaceTime) > config.INTERFACE_INTERVAL):
            # Interface request
            state.affInterface = True
            state.affInterface_ex = True
            state.lastInterfaceTime = utime.ticks_ms()

        if ((utime.ticks_ms() - state.gnssStartTime) > config.GNSS_INTERVAL):
            # GNSS request
            if state.modeGnss == aliases.MODE_GNSS_RUNNING:
                state.affModeGnss = True
                state.modeGnss_ex = True
            state.gnssStartTime = utime.ticks_ms()

        if state.affCons or state.affInterface or state.affModeGnss or state.affGraph or state.affLora:
            uartOBC.serialWrite()

        state.lastOBCTime = utime.ticks_ms()

    uartOBC.serialRead()

    # Start degaussing (if required)
    if(state.deMag == 1):
        general.demag()

    # Start a magneto-coupler test (if required)
    if(state.testMag > 0) and (state.testMag < 5):
        general.testMagneto(state.testMag)

    state.udpServ.readPacket()
