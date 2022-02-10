import utime
import config
from machine import PWM
from machine import UART
from machine import Pin
from ioctl import Ioctl

# Active magneto-coupler test
testMag = 0

# Ioctl object for IO interfaces
ioctlObj = Ioctl()

def setupGPIO():
    """
    Init function used to setup the GPIOs of the board. In particular, it configures output pins
    for leds (status of the board), PWM + direction output pins(inertia wheel),
    the UART connection with OBC, and the control pin for the PyCam.
    """
    global ioctlObj
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
    ioctlObj.setObject(Ioctl.KEY_PWM_X,pwmX_chan)
    ioctlObj.setObject(Ioctl.KEY_PWM_Y,pwmY_chan)
    ioctlObj.setObject(Ioctl.KEY_UART_OBC,uartOBC)
    ioctlObj.setObject(Ioctl.KEY_LORA_LED,loraLED)
    ioctlObj.setObject(Ioctl.KEY_WIFI_LED,wifiLED)
    ioctlObj.setObject(Ioctl.KEY_CAM_CONTROL,cameraControl)
    ioctlObj.setObject(Ioctl.KEY_DIR_X,dirX)
    ioctlObj.setObject(Ioctl.KEY_DIR_Y,dirY)

    utime.sleep_ms(100)

<<<<<<< HEAD
def nullCommand():
    return "No implementation for this command"

def commandHandler(command):
    commandList = [("LoraON", nullCommand), ("LoraOFF", nullCommand),
                   ("camON", nullCommand), ("camOFF", nullCommand),
                   ("t_console", nullCommand), ("t_graph", nullCommand),
                   ("tst1", nullCommand), ("tst2", nullCommand), ("tst3", nullCommand),
                   ("tst4", nullCommand), ("tststp", nullCommand),
                   ("ang_couple", nullCommand), ("demag", nullCommand,  ("roue", nullCommand),
                   ("startgnss", nullCommand), ("stopgnss", nullCommand), ("savegnss", nullCommand),
                   ("ouvPage", nullCommand),  ("cons_config", nullCommand),
                   ("autoTest", nullCommand), ("user", nullCommand),
                   ("configGraph1", nullCommand), ("configGraph2", nullCommand), ("configGraph3", nullCommand),
                   ("configGraph4", nullCommand), ("configGraph5", nullCommand), ("configGraph6", nullCommand)]
    for i in commandList:
        if i[0] == command
            return (1, i[1])
    else:
        return (-1, "Command Not Found")



def testMagneto(tstIdx):
    """
    Test function for magneto-coupler
    @arg tstIdx (int) : Indicates the test to execute. Accepted values : 1,2,3,4 
    """
    global testMag
    testMag = 1

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
    
    while(testMag>0):
        phaseIdx = 0 # Store the running phase
        for currentDirection in selectedPhasesDir:      
            phaseIdx = phaseIdx + 1
            # Set current direction for magneto coupler X and Y      
            ioctlObj.getObject(Ioctl.KEY_DIR_X).value(currentDirection[0])
            ioctlObj.getObject(Ioctl.KEY_DIR_Y).value(currentDirection[1])

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
                ioctlObj.getObject(Ioctl.KEY_PWM_X).duty_cycle(Sx)
                ioctlObj.getObject(Ioctl.KEY_PWM_Y).duty_cycle(Sy)
                utime.sleep_ms(selectedP)
    utime.sleep_ms(100)

    # Event source fin --
    # UDP fin 
    utime.sleep_ms(100)
    ioctlObj.getObject(Ioctl.KEY_PWM_X).duty_cycle(1.0)
    utime.sleep_ms(100)
    ioctlObj.getObject(Ioctl.KEY_PWM_Y).duty_cycle(1.0)
    utime.sleep_ms(100)

    print("Stop test magneto-coupler "+str(tstIdx))

    # Send event5 fin
    utime.sleep_ms(100)
    # Send event5 fin
    utime.sleep_ms(100)




def stopTestMag():
    """
    Stops all running tests on the magneto-couplers
    """
    global testMag
    testMag = 0
