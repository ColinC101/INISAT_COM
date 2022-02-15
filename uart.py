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

# Data for UDP transmission
readingsUDP = {}

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
    Reads the command passed by the UART link and saves the data.
    """
    if (uart.any()):
        # Reading the identifier of the command
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
        
        elif (inChar == UART_COMMAND_EPS):
            tmpData = readSlot()
            tmpDataSplit = tmpData.split('#')
            state.readingsJSON[JSON_EPS_VBAT] = tmpDataSplit[0]
            state.readingsJSON[JSON_EPS_VIN] = tmpDataSplit[1]
            state.readingsJSON[JSON_EPS_VOUT] = tmpDataSplit[2]
            state.readingsJSON[JSON_EPS_ICHARGE] = tmpDataSplit[3]
            state.readingsJSON[JSON_EPS_IIN] = tmpDataSplit[4]
            state.readingsJSON[JSON_EPS_TBAT] = tmpDataSplit[5]
            state.readingsJSON[JSON_EPS_CHARGE_STATUS] = tmpDataSplit[6]
            readingsUDP[CONSCONFIG_EPS] = UART_COMMAND_EPS + tmpData + '@'

        elif (inChar == UART_COMMAND_TEMPERATURE):
            tmpData = readSlot()
            state.readingsJSON[JSON_TEMPERATURE] = tmpData
            readingsUDP[CONSCONFIG_TEMPERATURE] = UART_COMMAND_TEMPERATURE + tmpData + '@'

        elif (inChar == UART_COMMAND_ALTITUDE):
            tmpData = readSlot()
            state.readingsJSON[JSON_ALTITUDE] = tmpData
            readingsUDP[CONSCONFIG_ALTITUDE] = UART_COMMAND_ALTITUDE + tmpData + '@'

        elif (inChar == UART_COMMAND_PRESSION):
            tmpData = readSlot()
            state.readingsJSON[JSON_PRESSION] = tmpData
            readingsUDP[CONSCONFIG_PRESSION] = UART_COMMAND_PRESSION + tmpData + '@'

        elif (inChar == UART_COMMAND_EULER):
            tmpData = readSlot()
            tmpDataSplit = tmpData.split('#')
            state.readingsJSON[JSON_EULER_ROLL] = tmpDataSplit[0]
            state.readingsJSON[JSON_EULER_PITCH] = tmpDataSplit[1]
            state.readingsJSON[JSON_EULER_YAW] = tmpDataSplit[2]
            readingsUDP[CONSCONFIG_EULER] = UART_COMMAND_EULER + tmpData + '@'
            
        elif (inChar == UART_COMMAND_QUATERNION):
            tmpData = readSlot()
            tmpDataSplit = tmpData.split('#')
            state.readingsJSON[JSON_QUATERNION_W] = tmpDataSplit[0]
            state.readingsJSON[JSON_QUATERNION_X] = tmpDataSplit[1]
            state.readingsJSON[JSON_QUATERNION_Y] = tmpDataSplit[2]
            state.readingsJSON[JSON_QUATERNION_Z] = tmpDataSplit[3]
            readingsUDP[CONSCONFIG_QUATERNION] = UART_COMMAND_QUATERNION + tmpData + '@'
            
        elif (inChar == UART_COMMAND_ANGULAR_SPEED):
            tmpData = readSlot()
            tmpDataSplit = tmpData.split('#')
            state.readingsJSON[JSON_ANGULARSPEED_X] = tmpDataSplit[0]
            state.readingsJSON[JSON_ANGULARSPEED_Y] = tmpDataSplit[1]
            state.readingsJSON[JSON_ANGULARSPEED_Z] = tmpDataSplit[2]
            readingsUDP[CONSCONFIG_ANGULAR_SPEED] = UART_COMMAND_ANGULAR_SPEED + tmpData + '@'
            
        elif (inChar == UART_COMMAND_ACCELERATION):
            tmpData = readSlot()
            tmpDataSplit = tmpData.split('#')
            state.readingsJSON[JSON_ACCELERATION_X] = tmpDataSplit[0]
            state.readingsJSON[JSON_ACCELERATION_Y] = tmpDataSplit[1]
            state.readingsJSON[JSON_ACCELERATION_Z] = tmpDataSplit[2]
            readingsUDP[CONSCONFIG_ACCELERATION] = UART_COMMAND_ACCELERATION + tmpData + '@'
            
        elif (inChar == UART_COMMAND_MAGNETIC_FIELD):
            tmpData = readSlot()
            tmpDataSplit = tmpData.split('#')
            state.readingsJSON[JSON_MAGNETICFIELD_X] = tmpDataSplit[0]
            state.readingsJSON[JSON_MAGNETICFIELD_Y] = tmpDataSplit[1]
            state.readingsJSON[JSON_MAGNETICFIELD_Z] = tmpDataSplit[2]
            readingsUDP[CONSCONFIG_MAGNETIC_FIELD] = UART_COMMAND_MAGNETIC_FIELD + tmpData + '@'
            
        elif (inChar == UART_COMMAND_LINEAR_ACCELERATION):
            tmpData = readSlot()
            tmpDataSplit = tmpData.split('#')
            state.readingsJSON[JSON_LINEARACCELERATION_X] = tmpDataSplit[0]
            state.readingsJSON[JSON_LINEARACCELERATION_Y] = tmpDataSplit[1]
            state.readingsJSON[JSON_LINEARACCELERATION_Z] = tmpDataSplit[2]
            readingsUDP[CONSCONFIG_LINEAR_ACCELERATION] = UART_COMMAND_LINEAR_ACCELERATION + tmpData + '@'
            
        elif (inChar == UART_COMMAND_GRAVITY_VECTOR):
            tmpData = readSlot()
            tmpDataSplit = tmpData.split('#')
            state.readingsJSON[JSON_GRAVITY_X] = tmpDataSplit[0]
            state.readingsJSON[JSON_GRAVITY_Y] = tmpDataSplit[1]
            state.readingsJSON[JSON_GRAVITY_Z] = tmpDataSplit[2]
            readingsUDP[CONSCONFIG_GRAVITY] = UART_COMMAND_GRAVITY_VECTOR + tmpData + '@'
            
        elif (inChar == UART_COMMAND_LUMINANCE):
            tmpData = readSlot()
            tmpDataSplit = tmpData.split('#')
            state.readingsJSON[JSON_LUMINANCE_X] = tmpDataSplit[0]
            state.readingsJSON[JSON_LUMINANCE_NEGX] = tmpDataSplit[1]
            state.readingsJSON[JSON_LUMINANCE_Y] = tmpDataSplit[2]
            state.readingsJSON[JSON_LUMINANCE_NEGY] = tmpDataSplit[3]
            state.readingsJSON[JSON_LUMINANCE_Z] = tmpDataSplit[4]
            readingsUDP[CONSCONFIG_LUMINANCE] = UART_COMMAND_LUMINANCE + tmpData + '@'
            
        elif (inChar == UART_COMMAND_GNSS):
            tmpData = readSlot()
            tmpDataSplit = tmpData.split('#')
            state.readingsJSON[JSON_GNSS_UTC] = tmpDataSplit[0]
            state.readingsJSON[JSON_GNSS_LATITUDE] = tmpDataSplit[1]
            state.readingsJSON[JSON_GNSS_LONGITUDE] = tmpDataSplit[2]
            state.readingsJSON[JSON_GNSS_NBSAT] = tmpDataSplit[3]
            readingsUDP[CONSCONFIG_GNSS] = UART_COMMAND_GNSS + tmpData + '@'
            
        elif (inChar == UART_COMMAND_GNSS_NO_DATA):
            tmpData = readSlot()
            state.readingsJSON[JSON_GNSS_UTC] = tmpData
            state.readingsJSON[JSON_GNSS_LATITUDE] = tmpData
            state.readingsJSON[JSON_GNSS_LONGITUDE] = tmpData
            state.readingsJSON[JSON_GNSS_NBSAT] = tmpData
            readingsUDP[CONSCONFIG_GNSS] = UART_COMMAND_GNSS + tmpData + '@'
            
        elif (inChar == UART_COMMAND_NMEA):
            tmpData = readSlot()
            sizeSubstring = len(tmpData)/9
            state.readingsJSON[JSON_NMEA_1] = tmpData[0, sizeSubstring]
            state.readingsJSON[JSON_NMEA_2] = tmpData[sizeSubstring, 2*sizeSubstring]
            state.readingsJSON[JSON_NMEA_3] = tmpData[2*sizeSubstring, 3*sizeSubstring]
            state.readingsJSON[JSON_NMEA_4] = tmpData[3*sizeSubstring, 4*sizeSubstring]
            state.readingsJSON[JSON_NMEA_5] = tmpData[4*sizeSubstring, 5*sizeSubstring]
            state.readingsJSON[JSON_NMEA_6] = tmpData[5*sizeSubstring, 6*sizeSubstring]
            state.readingsJSON[JSON_NMEA_7] = tmpData[6*sizeSubstring, 7*sizeSubstring]
            state.readingsJSON[JSON_NMEA_8] = tmpData[7*sizeSubstring, 8*sizeSubstring]
            state.readingsJSON[JSON_NMEA_9] = tmpData[8*sizeSubstring, len(tmpData)]
            readingsUDP[CONSCONFIG_NMEA] = UART_COMMAND_NMEA + tmpData + '@'
            
        elif (inChar == UART_COMMAND_NMEA_NO_DATA):
            tmpData = readSlot()
            state.readingsJSON[JSON_NMEA_1] = tmpData
            state.readingsJSON[JSON_NMEA_2] = ""
            state.readingsJSON[JSON_NMEA_3] = ""
            state.readingsJSON[JSON_NMEA_4] = ""
            state.readingsJSON[JSON_NMEA_5] = ""
            state.readingsJSON[JSON_NMEA_6] = ""
            state.readingsJSON[JSON_NMEA_7] = ""
            state.readingsJSON[JSON_NMEA_8] = ""
            state.readingsJSON[JSON_NMEA_9] = ""
            readingsUDP[CONSCONFIG_NMEA] = UART_COMMAND_NMEA + tmpData + '@'
            
        elif (inChar == UART_COMMAND_END):
            # Conversion towards JSON string
            readingsResults = json.dumps(state.readingsJSON)

            # Sending the data to the web interface
            general.interfaceEvent.send(readingsResults, "CAP_readings", milliseconds())
            print("Event 'CAP_readings' sent")
            # Sending the data through UDP, only if needed
            if (state.udpCom):
                for v in readingsUDP.values():
                    udpserver.sendToLastRemote(v) 
    
    else:
        print("Nothing to read")


def serialWrite():
    """
    Sends a command corresponding to the state
    """
    # Getting only once all the elements necessary to know what to send

    # TODO: Comprendre les éléments déclencheurs et implémenter
    pass