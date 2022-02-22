from ioctl import Ioctl
from machine import UART
from network import WLAN
import utime
import json
import config
import general
import state
from aliases import *
import wifi
import LoRa
import uping
import json_ext

class OBCuart:
    """
    Class used to handle communication with OBC
    """

    def __init__(self):
        """
        Initialize the class with the given uart object
        """

        # Data for UDP transmission
        self.readingsUDP = {}

    def __readSlot__(self, separator='@'):
        """
        Reads data sent by UART until reception of the separator.
        Default separator is character '@'.
        Returns the characters read, excluding the separator.
        """
        uart = state.ioctlObj.getObject(Ioctl.KEY_UART_OBC)
        buf = ''
        while uart.any():
            nwChar = uart.read(1)
            buf += nwChar.decode("ascii")
            if (buf[-1] == separator):
                buf = buf[:-1]
                break
        return buf

    def getLoRaReading(self,pReadings):
        """
        Prepares the string containing data that will be transmitted on the LoRa link.
        pReadings: the dictionary of data read from OBC
        """
        excludedFields = [JSON_EPS_VIN,JSON_EPS_VOUT,JSON_EPS_IIN,JSON_LINEARACCELERATION_X,
        JSON_LINEARACCELERATION_Y,JSON_LINEARACCELERATION_Z]
        totalFields = list(map(lambda x: "var"+str(x),range(1,42))) # var41 is the last var 
                                                                    # that has to be sent
        
        for exclK in excludedFields:
            # Remove unwanted keys
            totalFields.remove(exclK)

        return json_ext.convertJSON(pReadings,totalFields,[])

    def getGraphReading(self,pReadings):
        """
        Prepares the string containing charts data, which will be sent to the
        browser's EventSource
        pReadings: the dictionary of data read from OBC
        """
        excludedFields = [JSON_EPS_VIN,JSON_EPS_VOUT,JSON_EPS_IIN,JSON_EPS_CHARGE_STATUS]
        totalFields = list(map(lambda x: "var"+str(x),range(1,38))) # var37 is the last var

        return json_ext.convertJSON(pReadings,totalFields,excludedFields)
    def serialRead(self):
        """
        Reads the command passed by the UART link and saves the data.
        """
        uart = state.ioctlObj.getObject(Ioctl.KEY_UART_OBC)
        if (uart.any()):
            # Reading the identifier of the command
            inChar = uart.read(uartCommandSize)
            inChar = inChar.decode("ascii")

            if (inChar == UART_COMMAND_AUTOTEST):
                print("Autotest read")
                # Autotest finished
                state.autoTesting = 0
                state.lastOBCTime = utime.ticks_ms()

                autotestData = {}
                autotestData[JSON_AUTOTEST_WIFI_MODE] = state.wifiObj.getMode()
                try:
                    autotestData[JSON_AUTOTEST_WIFI_POWER] = state.wifiObj.wlan.max_tx_power()/4
                except:
                    autotestData[JSON_AUTOTEST_WIFI_POWER] = "unknown"

                autotestData[JSON_AUTOTEST_WIFI_IP] = config.localIP

                pingRes = uping.ping(config.CAMERA_IP,count=1,quiet=True,timeout=1000)
                autotestData[JSON_AUTOTEST_PING_CAMERA] = "0" if pingRes == None else ("1"+str(pingRes))
                
                autotestData[JSON_AUTOTEST_LORA_POWER] = state.loraObj.lora.stats()[6]
                autotestData[JSON_AUTOTEST_LORA_SPREADINGFACTOR] = state.loraObj.lora.sf()
                autotestData[JSON_AUTOTEST_LORA_BANDWIDTH] = state.loraObj.lora.bandwidth()
                autotestData[JSON_AUTOTEST_LORA_FREQUENCY] = state.loraObj.lora.frequency()
                autotestData[JSON_AUTOTEST_LORA_CODINGRATE] = state.loraObj.lora.coding_rate()
                autotestData[JSON_AUTOTEST_LORA_PREAMBLE] = state.loraObj.lora.preamble()

                # Fillers for retro-compatibility
                autotestData[JSON_AUTOTEST_VOID1] = ""
                autotestData[JSON_AUTOTEST_VOID2] = ""
                autotestData[JSON_AUTOTEST_VOID3] = ""

                # Raw received data from uart
                autotestData[JSON_AUTOTEST_RAW] = self.__readSlot__()

                # Conversion towards JSON string
                testsResults = json.dumps(autotestData)

                # Sending the data to the web interface
                general.autotestEvent.send("TEST_readings",testsResults, utime.ticks_ms())
                # Sending the data through UDP, only if needed
                if (state.udpCom):
                    replyBuffer = "A"
                    # var14 is the last autotest variable, so range(1,15) is fine to
                    # get [1, 2, 3, ..., 14]
                    for k in list(map(lambda x: "var"+str(x),range(1,15))):
                        replyBuffer += "" if not (k in autotestData) else str(autotestData[k])
                        replyBuffer += "#"
                    replyBuffer = replyBuffer[:-1] + "@\r\n"
                    state.udpServ.sendToLastRemote(replyBuffer)
            

            elif (inChar == UART_COMMAND_EPS):
                tmpData = self.__readSlot__()
                tmpDataSplit = tmpData.split('#')
                if (len(tmpDataSplit) == 7):
                    state.readingsJSON[JSON_EPS_VBAT] = tmpDataSplit[0]
                    state.readingsJSON[JSON_EPS_VIN] = tmpDataSplit[1]
                    state.readingsJSON[JSON_EPS_VOUT] = tmpDataSplit[2]
                    state.readingsJSON[JSON_EPS_ICHARGE] = tmpDataSplit[3]
                    state.readingsJSON[JSON_EPS_IIN] = tmpDataSplit[4]
                    state.readingsJSON[JSON_EPS_TBAT] = tmpDataSplit[5]
                    state.readingsJSON[JSON_EPS_CHARGE_STATUS] = tmpDataSplit[6]
                    self.readingsUDP[CONSCONFIG_EPS] = UART_COMMAND_EPS + tmpData + '@'

            elif (inChar == UART_COMMAND_TEMPERATURE):
                tmpData = self.__readSlot__()
                state.readingsJSON[JSON_TEMPERATURE] = tmpData
                self.readingsUDP[CONSCONFIG_TEMPERATURE] = UART_COMMAND_TEMPERATURE + tmpData + '@'

            elif (inChar == UART_COMMAND_ALTITUDE):
                tmpData = self.__readSlot__()
                state.readingsJSON[JSON_ALTITUDE] = tmpData
                self.readingsUDP[CONSCONFIG_ALTITUDE] = UART_COMMAND_ALTITUDE + tmpData + '@'

            elif (inChar == UART_COMMAND_PRESSION):
                tmpData = self.__readSlot__()
                state.readingsJSON[JSON_PRESSION] = tmpData
                self.readingsUDP[CONSCONFIG_PRESSION] = UART_COMMAND_PRESSION + tmpData + '@'

            elif (inChar == UART_COMMAND_EULER):
                tmpData = self.__readSlot__()
                tmpDataSplit = tmpData.split('#')
                if (len(tmpDataSplit) == 3):
                    state.readingsJSON[JSON_EULER_ROLL] = tmpDataSplit[0]
                    state.readingsJSON[JSON_EULER_PITCH] = tmpDataSplit[1]
                    state.readingsJSON[JSON_EULER_YAW] = tmpDataSplit[2]
                    self.readingsUDP[CONSCONFIG_EULER] = UART_COMMAND_EULER + tmpData + '@'
                
            elif (inChar == UART_COMMAND_QUATERNION):
                tmpData = self.__readSlot__()
                tmpDataSplit = tmpData.split('#')
                if (len(tmpDataSplit) == 4):
                    state.readingsJSON[JSON_QUATERNION_W] = tmpDataSplit[0]
                    state.readingsJSON[JSON_QUATERNION_X] = tmpDataSplit[1]
                    state.readingsJSON[JSON_QUATERNION_Y] = tmpDataSplit[2]
                    state.readingsJSON[JSON_QUATERNION_Z] = tmpDataSplit[3]
                    self.readingsUDP[CONSCONFIG_QUATERNION] = UART_COMMAND_QUATERNION + tmpData + '@'
                
            elif (inChar == UART_COMMAND_ANGULAR_SPEED):
                tmpData = self.__readSlot__()
                tmpDataSplit = tmpData.split('#')
                if (len(tmpDataSplit) == 3):
                    state.readingsJSON[JSON_ANGULARSPEED_X] = tmpDataSplit[0]
                    state.readingsJSON[JSON_ANGULARSPEED_Y] = tmpDataSplit[1]
                    state.readingsJSON[JSON_ANGULARSPEED_Z] = tmpDataSplit[2]
                    self.readingsUDP[CONSCONFIG_ANGULAR_SPEED] = UART_COMMAND_ANGULAR_SPEED + tmpData + '@'
                
            elif (inChar == UART_COMMAND_ACCELERATION):
                tmpData = self.__readSlot__()
                tmpDataSplit = tmpData.split('#')
                if (len(tmpDataSplit) == 3):
                    state.readingsJSON[JSON_ACCELERATION_X] = tmpDataSplit[0]
                    state.readingsJSON[JSON_ACCELERATION_Y] = tmpDataSplit[1]
                    state.readingsJSON[JSON_ACCELERATION_Z] = tmpDataSplit[2]
                    self.readingsUDP[CONSCONFIG_ACCELERATION] = UART_COMMAND_ACCELERATION + tmpData + '@'
                
            elif (inChar == UART_COMMAND_MAGNETIC_FIELD):
                tmpData = self.__readSlot__()
                tmpDataSplit = tmpData.split('#')
                if (len(tmpDataSplit) == 3):
                    state.readingsJSON[JSON_MAGNETICFIELD_X] = tmpDataSplit[0]
                    state.readingsJSON[JSON_MAGNETICFIELD_Y] = tmpDataSplit[1]
                    state.readingsJSON[JSON_MAGNETICFIELD_Z] = tmpDataSplit[2]
                    self.readingsUDP[CONSCONFIG_MAGNETIC_FIELD] = UART_COMMAND_MAGNETIC_FIELD + tmpData + '@'
                
            elif (inChar == UART_COMMAND_LINEAR_ACCELERATION):
                tmpData = self.__readSlot__()
                tmpDataSplit = tmpData.split('#')
                if (len(tmpDataSplit) == 3):
                    state.readingsJSON[JSON_LINEARACCELERATION_X] = tmpDataSplit[0]
                    state.readingsJSON[JSON_LINEARACCELERATION_Y] = tmpDataSplit[1]
                    state.readingsJSON[JSON_LINEARACCELERATION_Z] = tmpDataSplit[2]
                    self.readingsUDP[CONSCONFIG_LINEAR_ACCELERATION] = UART_COMMAND_LINEAR_ACCELERATION + tmpData + '@'
                
            elif (inChar == UART_COMMAND_GRAVITY_VECTOR):
                tmpData = self.__readSlot__()
                tmpDataSplit = tmpData.split('#')
                if (len(tmpDataSplit) == 3):
                    state.readingsJSON[JSON_GRAVITY_X] = tmpDataSplit[0]
                    state.readingsJSON[JSON_GRAVITY_Y] = tmpDataSplit[1]
                    state.readingsJSON[JSON_GRAVITY_Z] = tmpDataSplit[2]
                    self.readingsUDP[CONSCONFIG_GRAVITY] = UART_COMMAND_GRAVITY_VECTOR + tmpData + '@'
                
            elif (inChar == UART_COMMAND_LUMINANCE):
                tmpData = self.__readSlot__()
                tmpDataSplit = tmpData.split('#')
                if (len(tmpDataSplit) == 5):
                    state.readingsJSON[JSON_LUMINANCE_X] = tmpDataSplit[0]
                    state.readingsJSON[JSON_LUMINANCE_NEGX] = tmpDataSplit[1]
                    state.readingsJSON[JSON_LUMINANCE_Y] = tmpDataSplit[2]
                    state.readingsJSON[JSON_LUMINANCE_NEGY] = tmpDataSplit[3]
                    state.readingsJSON[JSON_LUMINANCE_Z] = tmpDataSplit[4]
                    self.readingsUDP[CONSCONFIG_LUMINANCE] = UART_COMMAND_LUMINANCE + tmpData + '@'
                
            elif (inChar == UART_COMMAND_GNSS):
                tmpData = self.__readSlot__()
                tmpDataSplit = tmpData.split('#')
                if (len(tmpDataSplit) == 4):
                    state.readingsJSON[JSON_GNSS_UTC] = tmpDataSplit[0]
                    state.readingsJSON[JSON_GNSS_LATITUDE] = tmpDataSplit[1]
                    state.readingsJSON[JSON_GNSS_LONGITUDE] = tmpDataSplit[2]
                    state.readingsJSON[JSON_GNSS_NBSAT] = tmpDataSplit[3]
                    self.readingsUDP[CONSCONFIG_GNSS] = UART_COMMAND_GNSS + tmpData + '@'
                
            elif (inChar == UART_COMMAND_GNSS_NO_DATA):
                tmpData = self.__readSlot__()
                state.readingsJSON[JSON_GNSS_UTC] = tmpData
                state.readingsJSON[JSON_GNSS_LATITUDE] = tmpData
                state.readingsJSON[JSON_GNSS_LONGITUDE] = tmpData
                state.readingsJSON[JSON_GNSS_NBSAT] = tmpData
                self.readingsUDP[CONSCONFIG_GNSS] = UART_COMMAND_GNSS + tmpData + '@'
                
            elif (inChar == UART_COMMAND_NMEA):
                tmpData = self.__readSlot__()
                sizeSubstring = int(len(tmpData)/9)
                state.readingsJSON[JSON_NMEA_1] = tmpData[0:sizeSubstring]
                state.readingsJSON[JSON_NMEA_2] = tmpData[sizeSubstring: 2*sizeSubstring]
                state.readingsJSON[JSON_NMEA_3] = tmpData[2*sizeSubstring: 3*sizeSubstring]
                state.readingsJSON[JSON_NMEA_4] = tmpData[3*sizeSubstring: 4*sizeSubstring]
                state.readingsJSON[JSON_NMEA_5] = tmpData[4*sizeSubstring: 5*sizeSubstring]
                state.readingsJSON[JSON_NMEA_6] = tmpData[5*sizeSubstring: 6*sizeSubstring]
                state.readingsJSON[JSON_NMEA_7] = tmpData[6*sizeSubstring: 7*sizeSubstring]
                state.readingsJSON[JSON_NMEA_8] = tmpData[7*sizeSubstring: 8*sizeSubstring]
                state.readingsJSON[JSON_NMEA_9] = tmpData[8*sizeSubstring: len(tmpData)]
                self.readingsUDP[CONSCONFIG_NMEA] = UART_COMMAND_NMEA + tmpData + '@'
                
            elif (inChar == UART_COMMAND_NMEA_NO_DATA):
                tmpData = self.__readSlot__()
                state.readingsJSON[JSON_NMEA_1] = tmpData
                state.readingsJSON[JSON_NMEA_2] = ""
                state.readingsJSON[JSON_NMEA_3] = ""
                state.readingsJSON[JSON_NMEA_4] = ""
                state.readingsJSON[JSON_NMEA_5] = ""
                state.readingsJSON[JSON_NMEA_6] = ""
                state.readingsJSON[JSON_NMEA_7] = ""
                state.readingsJSON[JSON_NMEA_8] = ""
                state.readingsJSON[JSON_NMEA_9] = ""
                self.readingsUDP[CONSCONFIG_NMEA] = UART_COMMAND_NMEA + tmpData + '@'
                

            elif (inChar == UART_COMMAND_END):
                # Conversion towards JSON string
                state.readingsJSON[JSON_CONS_CONFIG] = "".join(state.consoleConfig)
                readingsResults = json.dumps(state.readingsJSON)

                if state.modeGnss != MODE_GNSS_RUNNING:
                    # Check that GNSS mode is disabled before triggering console and charts events

                    # Sending data to the console
                    if state.affCons_ex:
                        general.consoleEvent.send("CAP_readings",readingsResults, utime.ticks_ms())
                        print("Event 'CAP_readings' sent")
                        # Sending the data through UDP link too, only if needed
                        if (state.udpCom):
                            for idx,consoleCfg in enumerate(state.consoleConfig):
                                if consoleCfg == "1" and idx in self.readingsUDP:
                                    # This parameter from console config is enabled, so we need to 
                                    # send it
                                    state.udpServ.sendToLastRemote(self.readingsUDP[idx])           
                        state.affCons_ex = 0

                    # Sending data to the charts
                    if state.affGraph_ex:
                        print("Graph event")
                        general.graphEvent.send("CAP_readings2",self.getGraphReading(state.readingsJSON), utime.ticks_ms())
                        state.affGraph_ex = 0
                    else:
                        print("No need to aff graph")

                # Sending data to the web interface
                if state.affInterface_ex:
                    general.interfaceEvent.send("CAP_readings3", readingsResults, utime.ticks_ms())
                    state.affInterface_ex = 0

                # Saving GNSS data to a text file
                if state.modeGnss_ex:
                    print("GNSS DATA added")
                    GNSS_string = state.readingsJSON[JSON_GNSS_LATITUDE] + " , " + state.readingsJSON[JSON_GNSS_LONGITUDE] + "\r\n"
                    general.gnssSaveFile(GNSS_string)
                    state.modeGnss_ex = False

                # Transmitting data through LoRa link
                if (state.affLora_ex and state.loraObj.getLoraStatus()):
                    state.loraObj.sendReadings(self.getLoRaReading(state.readingsJSON))
                    state.affLora_ex = False


    def serialWrite(self):
        """
        Sends commands to the OBC
        """
        # Getting only once all the elements necessary to know what to send
        userConnected = state.userConnected
        loraOn = state.loraObj.getLoraStatus()
        
        requireResponse = False

        uart = state.ioctlObj.getObject(Ioctl.KEY_UART_OBC)

        if ((userConnected or loraOn or state.udpCom) and (not(state.autoTesting)) and (state.modeGnss != MODE_GNSS_RUNNING)):
            if (state.affCons and state.consoleConfig[CONSCONFIG_EPS]=='1') or (state.affGraph and (CHART_EPS in state.chartsConfig)) or (state.affInterface and userConnected) or (state.affLora and loraOn):
                requireResponse = True
                uart.write(UART_COMMAND_EPS)
            if (state.affCons and state.consoleConfig[CONSCONFIG_TEMPERATURE]=='1') or (state.affGraph and (CHART_TEMPERATURE in state.chartsConfig)) or (state.affInterface and userConnected) or (state.affLora and loraOn):
                requireResponse = True
                uart.write(UART_COMMAND_TEMPERATURE)
            if (state.affCons and state.consoleConfig[CONSCONFIG_ALTITUDE]=='1') or (state.affGraph and (CHART_ALTITUDE in state.chartsConfig)) or (state.affInterface and userConnected) or (state.affLora and loraOn):
                requireResponse = True
                uart.write(UART_COMMAND_ALTITUDE)
            if (state.affCons and state.consoleConfig[CONSCONFIG_PRESSION]=='1') or (state.affGraph and (CHART_PRESSION in state.chartsConfig)) or (state.affInterface and userConnected) or (state.affLora and loraOn):
                requireResponse = True
                uart.write(UART_COMMAND_PRESSION)
            if (state.affCons and state.consoleConfig[CONSCONFIG_EULER]=='1') or (state.affGraph and (CHART_EULER in state.chartsConfig)) or (state.affInterface and userConnected) or (state.affLora and loraOn):
                requireResponse = True
                uart.write(UART_COMMAND_EULER)
            if (state.affCons and state.consoleConfig[CONSCONFIG_QUATERNION]=='1') or (state.affGraph and (CHART_QUATERNION in state.chartsConfig)) or (state.affLora and loraOn):
                requireResponse = True
                uart.write(UART_COMMAND_QUATERNION)
            if (state.affCons and state.consoleConfig[CONSCONFIG_ANGULAR_SPEED]=='1') or (state.affGraph and (CHART_ANGULAR_SPEED in state.chartsConfig)) or (state.affInterface and userConnected) or (state.affLora and loraOn):
                requireResponse = True
                uart.write(UART_COMMAND_ANGULAR_SPEED)
            if (state.affCons and state.consoleConfig[CONSCONFIG_ACCELERATION]=='1') or (state.affGraph and (CHART_ACCELERATION in state.chartsConfig)) or (state.affInterface and userConnected) or (state.affLora and loraOn):
                requireResponse = True
                uart.write(UART_COMMAND_ACCELERATION)
            if (state.affCons and state.consoleConfig[CONSCONFIG_MAGNETIC_FIELD]=='1') or (state.affGraph and (CHART_MAGNETIC_FIELD in state.chartsConfig)) or (state.affInterface and userConnected) or (state.affLora and loraOn):
                requireResponse = True
                uart.write(UART_COMMAND_MAGNETIC_FIELD)
            if (state.affCons and state.consoleConfig[CONSCONFIG_LINEAR_ACCELERATION]=='1') or (state.affGraph and (CHART_LINEAR_ACCELERATION in state.chartsConfig)):
                requireResponse = True
                uart.write(UART_COMMAND_LINEAR_ACCELERATION)
            if (state.affCons and state.consoleConfig[CONSCONFIG_GRAVITY]=='1') or (state.affGraph and (CHART_GRAVITY in state.chartsConfig)) or (state.affInterface and userConnected) or (state.affLora and loraOn):
                requireResponse = True
                uart.write(UART_COMMAND_GRAVITY_VECTOR)
            if (state.affCons and state.consoleConfig[CONSCONFIG_LUMINANCE]=='1') or (state.affGraph and (CHART_LUMINANCE in state.chartsConfig)) or (state.affLora and loraOn):
                requireResponse = True
                uart.write(UART_COMMAND_LUMINANCE)
            if (state.affCons and state.consoleConfig[CONSCONFIG_GNSS]=='1') or (state.affLora and loraOn) or (state.affModeGnss):
                requireResponse = True
                uart.write(UART_COMMAND_GNSS)
            if (state.affCons and state.consoleConfig[CONSCONFIG_NMEA]=='1'):
                requireResponse = True
                uart.write(UART_COMMAND_NMEA)
        elif (state.modeGnss == MODE_GNSS_RUNNING) and (not state.autoTesting):
            if (state.affLora and loraOn) or (state.affModeGnss):
                requireResponse = True
                uart.write(UART_COMMAND_GNSS)

        # Tell the UART the command sequence is over, only if something has been sent
        if requireResponse:
            uart.write('Z')

        # Drop all the display flags, since we just served them
        state.affCons = False
        state.affGraph = False
        state.affInterface = False
        state.affLora = False
        state.affModeGnss = False
        
        # If no chart is activated, we drop the flag
        if (state.chartsConfig == CHARTS_CONFIG_DISABLED):
            state.affGraph_ex = False
