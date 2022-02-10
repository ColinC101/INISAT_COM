"""
All the commands used in the UART laison are listed here.
Please use theses aliases to imrpove readability and reliability.
"""

UART_COMMAND_AUTOTEST = 'A'
UART_COMMAND_EPS = 'B'
UART_COMMAND_TEMPERATURE = 'C'
UART_COMMAND_ALTITUDE = 'D'
UART_COMMAND_PRESSION = 'E'
UART_COMMAND_EULER = 'F'
UART_COMMAND_QUATERNION = 'G'
UART_COMMAND_ANGULAR_SPEED = 'H'
UART_COMMAND_ACCELERATION = 'I'
UART_COMMAND_MAGNETIC_FIELD = 'J'
UART_COMMAND_LINEAR_ACCELERATION = 'K'
UART_COMMAND_GRAVITY_VECTOR = 'L'
UART_COMMAND_LUMINANCE = 'M'
UART_COMMAND_GNSS = 'N'
UART_COMMAND_NMEA = 'O'


# TODO: Commands below not implemented in uart.py yet

# TODO: Didn't understand what this command does in former .ino implementation
UART_COMMAND_aucuneIdee = 'Z'
# TODO: In the former .ino implementation, these are received but never sent
UART_COMMAND_NO_DATA = 'P'
UART_COMMAND_NO_DATA2 = 'Q'
