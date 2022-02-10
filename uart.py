from ioctl import Ioctl
from machine import UART
from general import ioctlObj
from uartCommands import *

# Getting the UART object initialized in general.py
uart = ioctlObj.getObject(Ioctl.KEY_UART_OBC)

# Line 709 in .ino
def serialRead():
    """
    Reads the command passed by the UART link and acts accordingly
    """
    if (uart.any()):
        # TODO: Add the treatments
        inChar = uart.read(1)
        if (inChar == UART_COMMAND_AUTOTEST):
            pass
        elif (inChar == UART_COMMAND_EPS):
            pass
        elif (inChar == UART_COMMAND_TEMPERATURE):
            pass
        elif (inChar == UART_COMMAND_ALTITUDE):
            pass
        elif (inChar == UART_COMMAND_PRESSION):
            pass
        elif (inChar == UART_COMMAND_EULER):
            pass
        elif (inChar == UART_COMMAND_QUATERNION):
            pass
        elif (inChar == UART_COMMAND_ANGULAR_SPEED):
            pass
        elif (inChar == UART_COMMAND_ACCELERATION):
            pass
        elif (inChar == UART_COMMAND_MAGNETIC_FIELD):
            pass
        elif (inChar == UART_COMMAND_LINEAR_ACCELERATION):
            pass
        elif (inChar == UART_COMMAND_GRAVITY_VECTOR):
            pass
        elif (inChar == UART_COMMAND_LUMINANCE):
            pass
        elif (inChar == UART_COMMAND_GNSS):
            pass
        elif (inChar == UART_COMMAND_NMEA):
            pass
        elif (inChar == UART_COMMAND_AUTOTEST):
            pass
        elif (inChar == UART_COMMAND_AUTOTEST):
            pass
    else:
        print("Nothing to read")


# Line 598 in .ino
def serialWrite():
    """
    Sends a command corresponding to the state
    """
    # TODO: Comprendre les éléments déclencheurs et implémenter
    pass