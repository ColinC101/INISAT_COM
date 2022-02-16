import math
from udpserver import UdpServer
from eventsource import EventSource
import utime
import config
from machine import PWM
from machine import UART
from machine import Pin
from ioctl import Ioctl
import wifi
import LoRa
import eventsource
import state
import tcpServer
import aliases

consoleEvent = EventSource("consoleEvent")
graphEvent = EventSource("graphEvent")
interfaceEvent = EventSource("interfaceEvent")
autotestEvent = EventSource("autotestEvent")
demagEvent = EventSource("demagEvent")

# UDP Server object
udpServ = None
udpPort = 9991

# Mapping between rotation direction command and pin value
rotationDirMap = {"h":0,"a":1}

def initWiFi():
    """
    Init WiFi
    """
    state.wifiObj.initWifi()

def initLoRa():
    """
    Init LoRa
    """
    state.loraObj.initLoRa()

def getState():
    """
    Return a string representing the current state of the server
    """
    return "S" + str(state.camStatus) + "#" + str(int(state.loraObj.getLoraStatus()))+"#Capteurs OK#"+str(state.consoleInterval)+"#"+str(state.modeGnss)+"@"

def uartFlush():
    """
    Flush the UART-OBC serial link
    """
    state.ioctlObj.getObject(Ioctl.KEY_UART_OBC).wait_tx_done(1000)

#### BEGIN - UDP COMMANDS ####

## BEGIN - UDP INTERFACE COMMANDS ##
def cbNone():
    """
    Disable UDP communication
    """
    state.udpCom = False
    return ""

def cbStopUDP():
    """
    Disable UDP communication
    """
    state.udpCom = False
    return "Fin de la communication avec INISAT 2U "

def cbBeginUDP():
    """
    Enable UDP communication
    """
    state.udpCom = True
    return "Client enregistre, debut de la communication avec INISAT 2U"

def cbState():
    """
    Send the current state of the server, over UDP
    """
    return getState()
## END - UDP INTERFACE COMMAND ##

## BEGIN - ARTH INERFACE COMMAND ##
def cbCameraOn():
    """
    Turn on the camera
    """
    state.camStatus = 1
    state.ioctlObj.getObject(Ioctl.KEY_CAM_CONTROL).value(1)
    print("Camera activee")
    return getState()

def cbCameraOff():
    """
    Turn off the camera
    """
    state.camStatus = 0
    state.ioctlObj.getObject(Ioctl.KEY_CAM_CONTROL).value(0)
    print("Camera desactivee")
    return getState()

def cbLoRaOn():
    """
    Turn on LoRa
    """
    state.loraObj.enableLora()
    print("Liaison LoRa activee")
    return getState()

def cbLoRaOff():
    """
    Turn off LoRa
    """
    state.loraObj.disableLora()
    print("Liaison LoRa desactivee")
    return getState()

def cbTest():
    """
    Start an auto test
    """
    uartFlush()
    state.ioctlObj.getObject(Ioctl.KEY_UART_OBC).write(aliases.UART_COMMAND_AUTOTEST)
    state.autoTesting = 1
    return getState()

def cbAutoTest():
    """
    Start also an auto test
    """
    uartFlush()
    state.ioctlObj.getObject(Ioctl.KEY_UART_OBC).write(aliases.UART_COMMAND_AUTOTEST)
    state.autoTesting = 1
    return "Config autotest lancee .."

def cbGNSSon():
    """
    Activate GNSS
    """
    state.modeGnss = aliases.MODE_GNSS_RUNNING
    state.gnssStartTime = utime.ticks_ms()
    uartFlush()

    # No console information fields
    state.consoleConfig = aliases.CONSOLE_CONFIG_DISABLED
    
    # No charts
    state.chartsConfig = aliases.CHARTS_CONFIG_DISABLED

    try:
        with open("web/Trajectoire_GNSS.txt", 'w') as infile:
            infile.close()
            print("Commande GNSS recue et fichier .txt cree ... ");
    except OSError:
        print("Echec lors de la creation du fichier Trajectoire_GNSS")

    return getState()

def cbGNSSoff():
    """
    Disable GNSS
    """
    state.modeGnss = aliases.MODE_GNSS_STOPPED
    return getState()

def cbGNSSsave():
    """
    Save GNSS data
    """
    state.modeGnss = aliases.MODE_GNSS_FINISHED
    gnssTransmitUDP()
    return getState()

## END - ARTH INERFACE COMMAND ##

## BEGIN - RAW UDP COMMANDS ##

def cbEPSon():
    """
    Activate EPS logging in the console
    """
    state.consoleConfig[aliases.CONSCONFIG_EPS]="1"
    return "Config epson recue .."

def cbEPSoff():
    """
    Deactivate EPS logging
    """
    state.consoleConfig[aliases.CONSCONFIG_EPS]="0"
    return "Config epsoff recue .."

def cbMPLon():
    """
    Activate MPL logging 
    """
    state.consoleConfig[aliases.CONSCONFIG_TEMPERATURE]="1"
    state.consoleConfig[aliases.CONSCONFIG_ALTITUDE]="1"
    state.consoleConfig[aliases.CONSCONFIG_PRESSION]="1"
    return "Config mplon recue .."

def cbMPLoff():
    """
    Deactivate MPL logging 
    """
    state.consoleConfig[aliases.CONSCONFIG_TEMPERATURE]="0"
    state.consoleConfig[aliases.CONSCONFIG_ALTITUDE]="0"
    state.consoleConfig[aliases.CONSCONFIG_PRESSION]="0"
    return "Config mploff recue .."

def cbTempOn():
    """
    Activate temperature logging
    """
    state.consoleConfig[aliases.CONSCONFIG_TEMPERATURE]="1"
    return "Config tempon recue .."

def cbTempOff():
    """
    Deactivate temperature logging
    """
    state.consoleConfig[aliases.CONSCONFIG_TEMPERATURE]="0"
    return "Config tempoff recue .."

def cbAltOn():
    """
    Activate altitude logging
    """
    state.consoleConfig[aliases.CONSCONFIG_ALTITUDE]="1"
    return "Config alton recue .."

def cbAltOff():
    """
    Deactivate altitude logging
    """
    state.consoleConfig[aliases.CONSCONFIG_ALTITUDE]="0"
    return "Config altoff recue .."

def cbPresOn():
    """
    Activate pressure logging
    """
    state.consoleConfig[aliases.CONSCONFIG_PRESSION]="1"
    return "Config preson recue .."

def cbPresOff():
    """
    Deactivate pressure logging
    """
    state.consoleConfig[aliases.CONSCONFIG_PRESSION]="0"
    return "Config presoff recue .."

def cbBNOon():
    """
    Activate BNO logging
    """
    state.consoleConfig[aliases.CONSCONFIG_EULER]="1"
    state.consoleConfig[aliases.CONSCONFIG_QUATERNION]="1"
    state.consoleConfig[aliases.CONSCONFIG_ANGULAR_SPEED]="1"
    state.consoleConfig[aliases.CONSCONFIG_ACCELERATION]="1"
    state.consoleConfig[aliases.CONSCONFIG_MAGNETIC_FIELD]="1"
    state.consoleConfig[aliases.CONSCONFIG_LINEAR_ACCELERATION]="1"
    state.consoleConfig[aliases.CONSCONFIG_GRAVITY]="1"
    return "Config bnoon recue .."

def cbBNOoff():
    """
    Deactivate BNO logging
    """
    state.consoleConfig[aliases.CONSCONFIG_EULER]="0"
    state.consoleConfig[aliases.CONSCONFIG_QUATERNION]="0"
    state.consoleConfig[aliases.CONSCONFIG_ANGULAR_SPEED]="0"
    state.consoleConfig[aliases.CONSCONFIG_ACCELERATION]="0"
    state.consoleConfig[aliases.CONSCONFIG_MAGNETIC_FIELD]="0"
    state.consoleConfig[aliases.CONSCONFIG_LINEAR_ACCELERATION]="0"
    state.consoleConfig[aliases.CONSCONFIG_GRAVITY]="0"
    return "Config bnooff recue .."

def cbEulerOn():
    """
    Activate Euler logging
    """
    state.consoleConfig[aliases.CONSCONFIG_EULER]="1" 
    return "Config euleron recue .."

def cbEulerOff():
    """
    Deactivate Euler logging
    """
    state.consoleConfig[aliases.CONSCONFIG_EULER]="0" 
    return "Config euleroff recue .."

def cbQuatOn():
    """
    Activate quaternion logging
    """
    state.consoleConfig[aliases.CONSCONFIG_QUATERNION]="1" 
    return "Config quaton recue .."

def cbQuatOff():
    """
    Deactivate quaternion logging
    """
    state.consoleConfig[aliases.CONSCONFIG_QUATERNION]="0" 
    return "Config quatoff recue .."

def cbVangOn():
    """
    Activate angular speed logging
    """
    state.consoleConfig[aliases.CONSCONFIG_ANGULAR_SPEED]="1" 
    return "Config vangon recue .."

def cbVangOff():
    """
    Deactivate angular speed logging
    """
    state.consoleConfig[aliases.CONSCONFIG_ANGULAR_SPEED]="0" 
    return "Config vangoff recue .."

def cbAccOn():
    """
    Activate acceleration logging
    """
    state.consoleConfig[aliases.CONSCONFIG_ACCELERATION]="1" 
    return "Config accon recue .."

def cbAccOff():
    """
    Deactivate acceleration logging
    """
    state.consoleConfig[aliases.CONSCONFIG_ACCELERATION]="0" 
    return "Config accoff recue .."

def cbMagOn():
    """
    Activate magnetic field logging
    """
    state.consoleConfig[aliases.CONSCONFIG_MAGNETIC_FIELD]="1" 
    return "Config magon recue .."

def cbMagOff():
    """
    Deactivate magnetic field logging
    """
    state.consoleConfig[aliases.CONSCONFIG_MAGNETIC_FIELD]="0" 
    return "Config magoff recue .."

def cbAccLinOn():
    """
    Activate linear acceleration logging
    """
    state.consoleConfig[aliases.CONSCONFIG_LINEAR_ACCELERATION]="1" 
    return "Config acclnon recue .."

def cbAccLinOff():
    """
    Deactivate linear acceleration logging
    """
    state.consoleConfig[aliases.CONSCONFIG_LINEAR_ACCELERATION]="0" 
    return "Config acclnoff recue .."

def cbGravOn():
    """
    Activate gravity logging
    """
    state.consoleConfig[aliases.CONSCONFIG_GRAVITY]="1" 
    return "Config gravon recue .."

def cbGravOff():
    """
    Deactivate gravity logging
    """
    state.consoleConfig[aliases.CONSCONFIG_GRAVITY]="0" 
    return "Config gravoff recue .."

def cbLumiOn():
    """
    Activate luminance logging
    """
    state.consoleConfig[aliases.CONSCONFIG_LUMINANCE]="1"
    return "Config lumion recue .."

def cbLumiOff():
    """
    Deactivate luminance logging
    """
    state.consoleConfig[aliases.CONSCONFIG_LUMINANCE]="0"
    return "Config lumioff recue .."

def cbLocOn():
    """
    Activate location (GNSS) logging
    """
    state.consoleConfig[aliases.CONSCONFIG_GNSS]="1"
    return "Config locon recue .."
    
def cbLocOff():
    """
    Deactivate location (GNSS) logging
    """
    state.consoleConfig[aliases.CONSCONFIG_GNSS]="0"
    return "Config locoff recue .."

def cbNMEAon():
    """
    Activate NMEA logging
    """
    state.consoleConfig[aliases.CONSCONFIG_NMEA]="1"
    return "Config nmeaon recue .."

def cbNMEAoff():
    """
    Deactivate NMEA logging
    """
    state.consoleConfig[aliases.CONSCONFIG_NMEA]="0"
    return "Config nmeaoff recue .."

def cbAllOn():
    """
    Activate all logs
    """
    state.consoleConfig = aliases.CONSOLE_CONFIG_ENABLED
    return "Config allon recue .."

def cbAllOff():
    """
    Deactivate all logs
    """
    state.consoleConfig = aliases.CONSOLE_CONFIG_DISABLED
    return "Config alloff recue .."

def cbLoraState():
    """
    Return LoRa state
    """ 
    if state.loraObj.getLoraStatus():
        return "Etat LORA est : ON"
    else:
        return "Etat LORA est : OFF"

def cbCameraState():
    """
    Return camera state
    """ 
    if state.camStatus == 1:
        return "Etat CAM est : ON"
    else:
        return "Etat CAM est : OFF"

def cbDemagOn():
    """
    Start degaussing
    """
    state.deMag = 1
    return "Config dmagon recue, veuillez attendre la fin .."

def cbMagt1():
    """
    Start test 1 for magneto-coupler
    """
    # state.testMag = 1
    return "Config magt1 recue .. COMMANDE DESACTIVEE POUR L'INSTANT .."

def cbMagt2():
    """
    Start test 2 for magneto-coupler
    """
    # state.testMag = 2
    return "Config magt2 recue .. COMMANDE DESACTIVEE POUR L'INSTANT .."

def cbMagt3():
    """
    Start test 3 for magneto-coupler
    """
    # state.testMag = 3
    return "Config magt3 recue .. COMMANDE DESACTIVEE POUR L'INSTANT .."

def cbMagt4():
    """
    Start test 4 for magneto-coupler
    """
    # state.testMag = 4
    return "Config magt4 recue .. COMMANDE DESACTIVEE POUR L'INSTANT .."
    
def cbStopMgt():
    """
    Stop magneto-coupler test
    """
    state.testMag = 0
    return "Config stpmgt recue, veuillez attendre la fin .."

def cbHelp():
    """
    Return help message
    """
    try:
        with open("help.txt", 'rb') as infile:
            fileLines = infile.read()
            infile.close()
            return fileLines.decode("utf-8")
    except OSError:
        print("Echec lors de l'ouverture du fichier d'aide")

def cbCamOn():
    """
    Turn on the camera
    """
    state.camStatus = 1
    state.ioctlObj.getObject(Ioctl.KEY_CAM_CONTROL).value(1)
    print("Camera activee")
    return "Config camon recue .."

def cbCamOff():
    """
    Turn off the camera
    """
    state.camStatus = 0
    state.ioctlObj.getObject(Ioctl.KEY_CAM_CONTROL).value(0)
    print("Camera desactivee")
    return "Config camoff recue .."


## END - RAW UDP COMMANDS ##

## BEGIN - UDP COMMANDS WITH ARGS ##
def cbTCons(args):
    """
    Change the console updating interval
    """
    if len(args) != 1:
        return "Commande ERROR !"
    
    try:
        periodValue = int(args[0])
    except:
        return "Veuillez choisir une periode entre 5 et 3600 secondes !"

    if (periodValue>4 and periodValue<3601):
        state.consoleInterval = periodValue * 1000
        return "Config tcons+"+args[0]+" recue .."

    return "Veuillez choisir une periode entre 5 et 3600 secondes !"

def cbRiRot(args):
    """
    Set the inertia wheel rotation speed and direction
    """
    if len(args) != 2:
        return "Commande ERROR !"

    rotationDir = args[0]
    if not(rotationDir in rotationDirMap):
        return "Veuillez choisir A ou H pour le Sens de rotation !"
    try:  
        angularSpeedRatio = int(args[1])
    except:
        return "Veuillez choisir une valeur entre 0 et 100 % !"

    if (angularSpeedRatio<0 or angularSpeedRatio >100):
        return "Veuillez choisir une valeur entre 0 et 100 % !"

    unitAngularSpeed = angularSpeedRatio / 100
    setInertiaWheelSpeed(unitAngularSpeed,rotationDir)

    return "Config rirot+"+args[0]+"+"+args[1]+" recue .."

        
def cbMgRot(args):
    """
    Initiate a rotation of the satellite via the magneto-couplers
    """
    if len(args) != 1:
        return "Commande ERROR !"
    
    try:
        rotationAngle = int(args[0])
    except:
        return "Veuillez choisir une valeur entre -30 et 30° (et != 0) !"

    if ((rotationAngle < -30) or (rotationAngle > 30) or (rotationAngle == 0)):
        return "Veuillez choisir une valeur entre -30 et 30° (et != 0) !"

    print("Commande Magnetocoupleur recue pour: " + str(rotationAngle) + "°")
    magnetoRotate(rotationAngle)
    return "Config mgrot+"+args[0]+" recue .."

## END - UDP COMMANDS WITH ARGS ##

## BEGIN - SINGLE-CHAR UDP COMMANDS ##
def cbSingleT(arg):
    """
    ARTH command used to control the console updating interval
    """
    try:
        periodValue = int(arg)
    except:
        return "Veuillez choisir une periode entre 5 et 3600 secondes !"

    if (periodValue>4 and periodValue<3601):
        state.consoleInterval = periodValue * 1000
        return getState()
    
    return "Veuillez choisir une periode entre 5 et 3600 secondes !"

    

def cbSingleR(arg):
    """
    ARTH command used to set the inertia wheel rotation / direction
    """
    if len(arg)<2:
        return "Commande ERROR !"
    
    rotationDir = arg[0]
    if not(rotationDir in rotationDirMap):
        return "Veuillez choisir A ou H pour le Sens de rotation !"

    try:  
        angularSpeedRatio = int(arg[1:])
    except:
        return "Veuillez choisir une valeur entre 0 et 100 % !"

    if (angularSpeedRatio<0 or angularSpeedRatio >100):
        return "Veuillez choisir une valeur entre 0 et 100 % !"

    unitAngularSpeed = angularSpeedRatio / 100
    setInertiaWheelSpeed(unitAngularSpeed,rotationDir)

    return getState()

def cbSingleM(arg):
    """
    ARTH command used to initiate a rotation of the satellite via the magneto-couplers
    """
    try:
        rotationAngle = int(arg)
    except:
        return "Veuillez choisir une valeur entre -30 et 30° (et != 0) !"

    if ((rotationAngle < -30) or (rotationAngle > 30) or (rotationAngle == 0)):
        return "Veuillez choisir une valeur entre -30 et 30° (et != 0) !"

    print("Commande Magnetocoupleur recue pour: " + str(rotationAngle) + "°")
    magnetoRotate(rotationAngle)

    return getState()

## END - SINGLE-CHAR UDP COMMANDS ##
#### END - UDP COMMANDS #####

def gnssTransmitUDP():
    """
    Transmit GNSS data stored in a file, over UDP
    """
    try:
        with open("web/Trajectoire_GNSS.txt", 'rb') as infile:
            fileLines = infile.readlines()
            msgToSend = ""
            for line in fileLines:
                strLine  = line.decode("utf-8")
                if strLine[-1] == "\n":
                    # Remove trailing new line if it exists
                    strLine = strLine[:-1]     
                msgToSend = "W"+strLine+"@"+"\r\n"
                udpServ.sendToLastRemote(msgToSend)
                print("Ligne envoyee: "+msgToSend)
                utime.sleep_ms(100)
            udpServ.sendToLastRemote("W#@\r\n")
    except OSError:
        print("Echec lors de l'ouverture du fichier Trajectoire_GNSS pour transmission sur la liaison UDP")

def setInertiaWheelSpeed(speed,dir):
    """
    Set the inertia wheel speed to the given value
    @arg speed(float): the speed of the inertia wheel (1.0 => full speed, 0 => stopped)
    @arg dir(string): the direction of rotation ("h" or "a" according to rotationDirMap)
    """
    
    # Set speed to null by opening P-Channel transistor
    state.ioctlObj.getObject(Ioctl.KEY_PWM_X).duty_cycle(1.0) 
    
    # Set the new direction for rotation
    state.ioctlObj.getObject(Ioctl.KEY_DIR_X).value(rotationDirMap[dir])

    # Set new speed for inertial wheel
    state.ioctlObj.getObject(Ioctl.KEY_PWM_X).duty_cycle(1-speed)
    
    print("Commande recue pour (R.cyclique): " + str(speed) + ", sens :" + dir)
    
def magnetoRotate(angle):
    """
    Rotate the satellite to the specified angle, via the magneto-couplers
    """
    Bx = float(state.readingsJSON[aliases.JSON_MAGNETICFIELD_X])
    By = float(state.readingsJSON[aliases.JSON_MAGNETICFIELD_Y])
    angB = round(math.atan2(By,Bx) * 180 / math.pi)
    angTot = angB - angle
    if(angTot > 360):
        angTot -= 360
    if(angTot < -360):
        angTot += 360
    
    Ix = math.cos(angTot * math.pi / 180)
    Iy = math.sin(angTot * math.pi / 180)

    dirX = 0
    dirY = 0
    if (Ix > 0):
        dirX = 0
    else:
        dirX = 1
    
    if (Iy > 0):
        dirY = 0
    else:
        dirY = 1

    iXdc = funcMap(abs(Ix*100), 100, 0, 150, 255)
    iYdc = funcMap(abs(Iy*100), 100, 0, 150, 255)

    # Defining current direction of magneto-coupler X
    state.ioctlObj.getObject(Ioctl.KEY_DIR_X).value(dirX)
    
    # And its new duty cycle
    state.ioctlObj.getObject(Ioctl.KEY_PWM_X).duty_cycle(iXdc)

    # Same for magneto-coupler Y
    state.ioctlObj.getObject(Ioctl.KEY_DIR_Y).value(dirY)
    state.ioctlObj.getObject(Ioctl.KEY_PWM_Y).duty_cycle(iYdc)

    print("Commande recue pour : " + str(angle) + "°.")


def funcMap(val,inMin,inMax,outMin,outMax):
    return ((val - inMin) * (outMax - outMin) / (inMax - inMin)) + outMin  

cbList = {"none":cbNone,"stopudp":cbStopUDP,"beginudp":cbBeginUDP,"state":cbState,"cameraon":cbCameraOn,
"cameraoff":cbCameraOff,"loraon":cbLoRaOn,"loraoff":cbLoRaOff,"test":cbTest,"autotest":cbAutoTest,
"gnsson":cbGNSSon,"gnssoff":cbGNSSoff,"gnsssave":cbGNSSsave,"epson":cbEPSon,"epsoff":cbEPSoff,
"mplon":cbMPLon,"mploff":cbMPLoff,"tempon":cbTempOn,"tempoff":cbTempOff,"alton":cbAltOn,
"altoff":cbAltOff,"preson":cbPresOn,"presoff":cbPresOff,"bnoon":cbBNOon,"bnooff":cbBNOoff,
"euleron":cbEulerOn,"euleroff":cbEulerOff,"quaton":cbQuatOn,"quatoff":cbQuatOff,"vangon":cbVangOn,
"vangoff":cbVangOff,"accon":cbAccOn,"accoff":cbAccOff,"magon":cbMagOn,"magoff":cbMagOff,
"acclnon":cbAccLinOn,"acclnoff":cbAccLinOff,"gravon":cbGravOn,"gravoff":cbGravOff,"lumion":cbLumiOn,
"lumioff":cbLumiOff,"locon":cbLocOn,"locoff":cbLocOff,"nmeaon":cbNMEAon,"nmeaoff":cbNMEAoff,
"allon":cbAllOn,"alloff":cbAllOff,"lorastate":cbLoraState,"camstate":cbCameraState,"dmagon":cbDemagOn,
"magt1":cbMagt1,"mcamoffagt2":cbMagt2,"magt3":cbMagt3,"magt4":cbMagt4,"stpmgt":cbStopMgt,"help":cbHelp,
"camon":cbCamOn,"":cbCamOff}

cbArgList = {"tcons":cbTCons,"rirot":cbRiRot,"mgrot":cbMgRot}

cbSingleCharList = {"t":cbSingleT,"r":cbSingleR,"m":cbSingleM}

eventList = {"events": consoleEvent, "events2": graphEvent,
             "events3": interfaceEvent, "events4": autotestEvent,
             "events5": demagEvent}

def startUDPServer(localIP):
    """
    Start the UDP Server
    """
    global udpServ
    udpServ = UdpServer(cbList,cbArgList,cbSingleCharList)
    udpServ.bind(localIP,udpPort)

def initSystemHardware():
    """ 
    Init function for IOs and LoRa
    """
    # Ioctl object for IO interfaces
    state.ioctlObj = Ioctl()
    setupGPIO()

    # WiFi
    state.wifiObj = wifi.WifiObject()

    # LoRa
    state.loraObj = LoRa.LoraObject()
 
def startTCPServer():
    """
    Start the TCP Server
    """
    global tcpServ
    tcpServ = tcpServer.TcpServer(cbList, eventList)
    tcpServ.bind(config.localIP, config.tcpPort)
    tcpServ.listen()

def setupGPIO():
    """
    Init function used to setup the GPIOs of the board. In particular, it configures output pins
    for leds (status of the board), PWM + direction output pins(inertia wheel),
    the UART connection with OBC, and the control pin for the PyCam.
    """
    utime.sleep_ms(100)

    # PWM init
    pwm = PWM(0, frequency=5000)
    pwmX_chan = pwm.channel(0, pin=config.PIN_PWM_X, duty_cycle=1.0)
    pwmY_chan = pwm.channel(1, pin=config.PIN_PWM_Y, duty_cycle=1.0)

    # UART OBC init
    uartOBC = UART(1, baudrate=config.UART_OBC_BAUD, pins=(config.PIN_UART_OBC_TX,config.PIN_UART_OBC_RX))
    uartOBC.init(config.UART_OBC_BAUD, bits=8, parity=None, stop=1)

    # LED output pins init
    loraLED = Pin(config.PIN_LORA_LED, mode=Pin.OUT)
    wifiLED = Pin(config.PIN_WIFI_LED, mode=Pin.OUT)

    # Magneto-couplers direction output pins init
    dirX = Pin(config.PIN_DIR_X, mode=Pin.OUT)
    dirY = Pin(config.PIN_DIR_Y, mode=Pin.OUT)

    # Camera control pin init
    cameraControl = Pin(config.PIN_CAM_CONTROL, mode=Pin.OUT)

    # Set the objects in Ioctl
    state.ioctlObj.setObject(Ioctl.KEY_PWM_X,pwmX_chan)
    state.ioctlObj.setObject(Ioctl.KEY_PWM_Y,pwmY_chan)
    state.ioctlObj.setObject(Ioctl.KEY_UART_OBC,uartOBC)
    state.ioctlObj.setObject(Ioctl.KEY_LORA_LED,loraLED)
    state.ioctlObj.setObject(Ioctl.KEY_WIFI_LED,wifiLED)
    state.ioctlObj.setObject(Ioctl.KEY_CAM_CONTROL,cameraControl)
    state.ioctlObj.setObject(Ioctl.KEY_DIR_X,dirX)
    state.ioctlObj.setObject(Ioctl.KEY_DIR_Y,dirY)

    # Default state
    state.ioctlObj.getObject(Ioctl.KEY_PWM_X).duty_cycle(1.0)
    state.ioctlObj.getObject(Ioctl.KEY_PWM_Y).duty_cycle(1.0)
    state.ioctlObj.getObject(Ioctl.KEY_LORA_LED).value(0)
    state.ioctlObj.getObject(Ioctl.KEY_WIFI_LED).value(0)
    state.ioctlObj.getObject(Ioctl.KEY_CAM_CONTROL).value(0)

    utime.sleep_ms(100)

"""def eventHandler(event, socket):
    eventList = [("events", consoleEvent), ("events2", graphEvent),
                 ("events3", interfaceEvent), ("events4", autotestEvent),
                 ("events5", demagEvent)]
    for i in eventList:
        if i[0] == event:
            i[1].bind(socket)
            return (1, "Event " + event + " bounded")
    return (-1, "Event Not Found")

def nullCommand(paramStruct):
    return "No implementation for this command"

def commandHandler(command):
    commandList = [("LoraON", toggleLora, (True)), ("LoraOFF", toggleLora, (False)),
                   ("camON", nullCommand, ()), ("camOFF", nullCommand, ()),
                   ("t_console", nullCommand, ()), ("t_graph", nullCommand, ()),
                   ("tst1", testMagneto, (1,)), ("tst2", testMagneto, (2,)), ("tst3", testMagneto, (3,)),
                   ("tst4", testMagneto, (4,)), ("tststp", stopTestMag, ()),
                   ("ang_couple", nullCommand, ()), ("demag", nullCommand, ()),  ("roue", nullCommand, ()),
                   ("startgnss", nullCommand, ()), ("stopgnss", nullCommand, ()), ("savegnss", nullCommand, ()),
                   ("ouvPage", nullCommand, ()),  ("cons_config", nullCommand, ()),
                   ("autoTest", nullCommand, ()), ("user", nullCommand, ()),
                   ("configGraph1", nullCommand, ()), ("configGraph2", nullCommand, ()), ("configGraph3", nullCommand, ()),
                   ("configGraph4", nullCommand, ()), ("configGraph5", nullCommand, ()), ("configGraph6", nullCommand, ())]
    for i in commandList:
        if i[0] == command:
            return (1, i[1](i[2]))
    return (-1, "Command Not Found")"""

def toggleLora(paramStruct):
    loraActive = state.loraObj.getLoraStatus()
    if (paramStruct == () or paramStruct[0]) and not loraActive:
        state.loraObj.enableLora()
        return "Liaison LoRa activée"
    elif (paramStruct == () or not paramStruct[0]) and loraActive:
        state.loraObj.disableLora()
        return "Liaison LoRa désactivée"
    elif paramStruct[0] and loraActive:
        return "Liaison LoRa déjà active !"
    elif not paramStruct[0] and not loraActive:
        return "Liaison LoRa déjà éteinte !"

def testMagneto(paramStruct):
    """
    Test function for magneto-coupler
    @arg paramStruct (int, ) : Indicates the test to execute. Accepted values : 1,2,3,4
    """
    tstIdx = paramStruct[0]
    state.testMag = 1

    Imax = 150
    t = 34

    print("Start test magneto-coupler "+str(tstIdx))

    # Values of p for the 4 different tests [p-Phase1,p-Phase2,p-Phase3,p-Phase4]
    pVal = [90,450,90,450]

    # List of current direction for the 4 different phases (directionX,directionY)
    sysPhasesDirectionTst1 = [(0,1),(0,0),(1,0),(1,1)]
    sysPhasesDirectionTst2 = [(0,1),(0,0),(1,0),(1,1)]
    sysPhasesDirectionTst3 = [(1,1),(1,0),(0,0),(0,1)]
    sysPhasesDirectionTst4 = [(1,1),(1,0),(0,0),(0,1)]

    # Store all the current direction [Phase1,Phase2,Phase3,Phase4]
    sysTestDir = [sysPhasesDirectionTst1,sysPhasesDirectionTst2,sysPhasesDirectionTst3,sysPhasesDirectionTst4]

    # Retrieve the current direction of the different phases for the selected test
    selectedPhasesDir = sysTestDir[tstIdx-1]
    # And the value of p
    selectedP = pVal[tstIdx-1]

    while(state.testMag>0):
        phaseIdx = 0 # Store the running phase
        for currentDirection in selectedPhasesDir:
            phaseIdx = phaseIdx + 1
            # Set current direction for magneto coupler X and Y
            state.ioctlObj.getObject(Ioctl.KEY_DIR_X).value(currentDirection[0])
            state.ioctlObj.getObject(Ioctl.KEY_DIR_Y).value(currentDirection[1])

            jMin = (Imax+t) if ((tstIdx == 2) and (phaseIdx == 4)) else Imax
            for j in range(255,(jMin-1),-t):
                # ^ is XOR
                if bool(currentDirection[0]^currentDirection[1]):
                    Sx = j/255.0
                    Sy = (255.0-j)/255.0
                else:
                    Sx = (255.0-j)/255.0
                    Sy = j/255.0

                # Set the PWM duty cycle for magneto coupler X and Y
                state.ioctlObj.getObject(Ioctl.KEY_PWM_X).duty_cycle(Sx)
                state.ioctlObj.getObject(Ioctl.KEY_PWM_Y).duty_cycle(Sy)
                utime.sleep_ms(selectedP)
    utime.sleep_ms(100)

    # Event source fin --
    # UDP fin
    utime.sleep_ms(100)
    state.ioctlObj.getObject(Ioctl.KEY_PWM_X).duty_cycle(1.0)
    utime.sleep_ms(100)
    state.ioctlObj.getObject(Ioctl.KEY_PWM_Y).duty_cycle(1.0)
    utime.sleep_ms(100)

    print("Stop test magneto-coupler "+str(tstIdx))


    # Send event5 fin
    utime.sleep_ms(100)
    return "Test du magnéto-coupleur " + str(tstIdx) + " terminé !"




def stopTestMag(paramStruct):
    """
    Stops all running tests on the magneto-couplers
    """
    state.testMag = 0
    demagEvent.send("fct_fin", "B", utime.ticks_ms())
    return "Arrêt du test ..."
