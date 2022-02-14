"""
All the aliases used in the UART laison are listed here.
Please use theses aliases to improve readability and reliability.

UART COMMANDS aliases are used to determine what data are exchanged.

JSON ACCESS aliases are used to grant easier access to the data, in
a need for retro-compatibility with web interface. 
"""


########################################
############  UART COMMANDS ############
########################################

# Number of characters in the following commands.
# All commands must have the same size
uartCommandSize = 1

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
UART_COMMAND_GNSS_NO_DATA = 'P'
UART_COMMAND_NMEA = 'O'
UART_COMMAND_NMEA_NO_DATA = 'Q'
UART_COMMAND_END = 'Z'


#######################################
############  JSON ACCESS  ############
#######################################

# EPS
JSON_EPS_VBAT = "var1"
JSON_EPS_VIN = "var2"
JSON_EPS_VOUT = "var3"
JSON_EPS_ICHARGE = "var4"
JSON_EPS_IIN = "var5"
JSON_EPS_TBAT = "var6"
JSON_EPS_CHARGE_STATUS = "var7"

# Temperature
JSON_TEMPERATURE = "var8"

# Altitude
JSON_ALTITUDE = "var9"

# Pression
JSON_PRESSION = "var10"

# Euler
JSON_EULER_ROULIS = "var11"
JSON_EULER_TANGAGE = "var12"
JSON_EULER_LACET = "var13"

# Quaternion
JSON_QUATERNION_W = "var14"
JSON_QUATERNION_X = "var15"
JSON_QUATERNION_Y = "var16"
JSON_QUATERNION_Z = "var17"

# Angular Speed
JSON_ANGULARSPEED_X = "var18"
JSON_ANGULARSPEED_Y = "var19"
JSON_ANGULARSPEED_Z = "var20"

# Acceleration
JSON_ACCELERATION_X = "var21"
JSON_ACCELERATION_Y = "var22"
JSON_ACCELERATION_Z = "var23"

# Magnetic Field
JSON_MAGNETICFIELD_X = "var24"
JSON_MAGNETICFIELD_Y = "var25"
JSON_MAGNETICFIELD_Z = "var26"

# Linear acceleration
JSON_LINEARACCELERATION_X = "var27"
JSON_LINEARACCELERATION_Y = "var28"
JSON_LINEARACCELERATION_Z = "var29"

# Gravity Vector
JSON_GRAVITY_X = "var30"
JSON_GRAVITY_Y = "var31"
JSON_GRAVITY_Z = "var32"

# Luminance
JSON_LUMINANCE_X = "var33"
JSON_LUMINANCE_NEGX = "var34"
JSON_LUMINANCE_Y = "var35"
JSON_LUMINANCE_NEGY = "var36"
JSON_LUMINANCE_Z = "var37"

# GNSS
JSON_GNSS_UTC = "var38"
JSON_GNSS_LATITUDE = "var39"
JSON_GNSS_LONGITUDE = "var40"
JSON_GNSS_NBSAT = "var41"

# NMEA
JSON_NMEA_1 = "var42"
JSON_NMEA_2 = "var43"
JSON_NMEA_3 = "var44"
JSON_NMEA_4 = "var45"
JSON_NMEA_5 = "var46"
JSON_NMEA_6 = "var47"
JSON_NMEA_7 = "var48"
JSON_NMEA_8 = "var49"
JSON_NMEA_9 = "var50"

# Config
JSON_CONS_CONFIG = "var51"
