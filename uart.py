from ioctl import Ioctl
from machine import UART
from network import WLAN
import time
import json
import general
import state
import udpserver
from aliases import *
import main # To remove when we move WiFi out of main
import LoRa

# Getting the UART object initialized in general.py
uart = state.ioctlObj.getObject(Ioctl.KEY_UART_OBC)


# JSON object for console
readingsJSON = {}

# Data for UDP transmission
readingsUDP = []

# Lambda function to get the time since epoch in milliseconds
milliseconds = lambda: int(time() * 1000)

def readSlot():
    """
    Reads data sent by UART until reception of the separator '@'.
    Returns the characters read, excluding the separator.
    """
    buf = ''
    if (uart.any()):
        while True:
            buf += uart.read(1)
            if (buf[-1] == '@'):
                buf = buf[:-1]
                break
    return buf


def serialRead():
    """
    Reads the command passed by the UART link and acts accordingly
    """
    if (uart.any()):
        # TODO: Add the treatments
        inChar = uart.read(uartCommandSize)
        if (inChar == UART_COMMAND_AUTOTEST):
            autotestData = {}
            # TODO: May need to be changed if WiFi implementation is put in a separate file
            autotestData[JSON_AUTOTEST_WIFI_MODE] = main.wlan.mode()
            autotestData[JSON_AUTOTEST_WIFI_POWER] = main.wlan.max_tx_power()
            autotestData[JSON_AUTOTEST_WIFI_IP] = main.localIp  # TODO: Find a better way to get this

            autotestData[JSON_AUTOTEST_PING_CAMERA] = 0  # TODO: Implement a pingCamera function to get the status (see .ino)
            
            autotestData[JSON_AUTOTEST_LORA_POWER] = LoRa.lora.stats()[6]
            autotestData[JSON_AUTOTEST_LORA_SPREADINGFACTOR] = LoRa.lora.sf()
            autotestData[JSON_AUTOTEST_LORA_BANDWIDTH] = LoRa.lora.bandwidth()
            autotestData[JSON_AUTOTEST_LORA_FREQUENCY] = LoRa.lora.frequency()
            autotestData[JSON_AUTOTEST_LORA_CODINGRATE] = LoRa.lora.coding_rate()
            autotestData[JSON_AUTOTEST_LORA_PREAMBLE] = LoRa.lora.preamble()

            # Fillers for retro-compatibility
            autotestData[JSON_AUTOTEST_VOID1] = ""
            autotestData[JSON_AUTOTEST_VOID2] = ""
            autotestData[JSON_AUTOTEST_VOID3] = ""

            # Raw received data from uart
            autotestData[JSON_AUTOTEST_RAW] = readSlot()

            # Conversion towards JSON string
            testsResults = json.dumps(autotestData)
            del autotestData

            # Sending the data to the web interface
            general.autotestEvent.send(testsResults, "TEST_readings", milliseconds())
            # Sending the data through UDP, only if needed
            if (state.udpCom):
                replyBuffer = "A"
                for v in autotestData.values():
                    replyBuffer += v
                    replyBuffer += "#"
                replyBuffer = replyBuffer[:-1] + "@"
                udpserver.sendToLastRemote(replyBuffer)
        

        if (inChar == UART_COMMAND_EPS):
            tmpData = readSlot()
            

            pass
        if (inChar == UART_COMMAND_TEMPERATURE):
            tmpData = readSlot()
            readingsJSON[JSON_TEMPERATURE] = tmpData
            # TODO: As in all cases, add the UDP version (how to declare tab ?)

            pass
        if (inChar == UART_COMMAND_ALTITUDE):
            tmpData = readSlot()
            readingsJSON[JSON_ALTITUDE] = tmpData
            pass
        if (inChar == UART_COMMAND_PRESSION):
            tmpData = readSlot()
            pass
        if (inChar == UART_COMMAND_EULER):
            tmpData = readSlot()
            pass
        if (inChar == UART_COMMAND_QUATERNION):
            tmpData = readSlot()
            pass
        if (inChar == UART_COMMAND_ANGULAR_SPEED):
            tmpData = readSlot()
            pass
        if (inChar == UART_COMMAND_ACCELERATION):
            tmpData = readSlot()
            pass
        if (inChar == UART_COMMAND_MAGNETIC_FIELD):
            tmpData = readSlot()
            pass
        if (inChar == UART_COMMAND_LINEAR_ACCELERATION):
            tmpData = readSlot()
            pass
        if (inChar == UART_COMMAND_GRAVITY_VECTOR):
            tmpData = readSlot()
            pass
        if (inChar == UART_COMMAND_LUMINANCE):
            tmpData = readSlot()
            pass
        if (inChar == UART_COMMAND_GNSS):
            tmpData = readSlot()
            pass
        if (inChar == UART_COMMAND_GNSS_NO_DATA):
            tmpData = readSlot()
            pass
        if (inChar == UART_COMMAND_NMEA):
            tmpData = readSlot()
            pass
        if (inChar == UART_COMMAND_NMEA_NO_DATA):
            tmpData = readSlot()
            pass
        if (inChar == UART_COMMAND_END):
            tmpData = readSlot()
            pass
    else:
        print("Nothing to read")

    # Emptying all possible remaining characters in UART buffer
    uart.read()



def serialWrite():
    """
    Sends a command corresponding to the state
    """
    # Getting only once all the elements necessary to know what to send

    # TODO: Comprendre les éléments déclencheurs et implémenter
    pass