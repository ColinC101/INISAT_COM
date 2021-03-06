"""
All the aliases used are listed here.
Please use theses aliases to improve readability and reliability.

UART COMMANDS aliases are used to determine what data are exchanged.

JSON ACCESS aliases are used to grant easier access to the data, in
a need for retro-compatibility with web interface. 

CONS CONFIG aliases are used to access easily the data in consConfig table.
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

# Autotests
JSON_AUTOTEST_WIFI_MODE = "var1"
JSON_AUTOTEST_WIFI_POWER = "var2"
JSON_AUTOTEST_WIFI_IP = "var3"
JSON_AUTOTEST_PING_CAMERA = "var4"
JSON_AUTOTEST_LORA_POWER = "var5"
JSON_AUTOTEST_LORA_SPREADINGFACTOR = "var6"
JSON_AUTOTEST_LORA_BANDWIDTH = "var7"
JSON_AUTOTEST_LORA_FREQUENCY = "var8"
JSON_AUTOTEST_LORA_CODINGRATE = "var9"
JSON_AUTOTEST_LORA_PREAMBLE = "var10"
JSON_AUTOTEST_VOID1 = "var11"
JSON_AUTOTEST_VOID2 = "var12"
JSON_AUTOTEST_VOID3 = "var13"
JSON_AUTOTEST_RAW = "var14"


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
JSON_EULER_ROLL = "var11"
JSON_EULER_PITCH = "var12"
JSON_EULER_YAW = "var13"

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



#######################################
############  CONS CONFIG  ############
#######################################

CONSCONFIG_EPS = 0
CONSCONFIG_TEMPERATURE = 1
CONSCONFIG_ALTITUDE = 2
CONSCONFIG_PRESSION = 3
CONSCONFIG_EULER = 4
CONSCONFIG_QUATERNION = 5
CONSCONFIG_ANGULAR_SPEED = 6
CONSCONFIG_ACCELERATION = 7
CONSCONFIG_MAGNETIC_FIELD = 8
CONSCONFIG_LINEAR_ACCELERATION = 9
CONSCONFIG_GRAVITY = 10
CONSCONFIG_LUMINANCE = 11
CONSCONFIG_GNSS = 12
CONSCONFIG_NMEA = 13



#######################################
###############  GNSS  ################
#######################################

MODE_GNSS_FINISHED = 0
MODE_GNSS_RUNNING = 1
MODE_GNSS_STOPPED = 2



#######################################
###########  CONSOLE CONFIG  ##########
#######################################

CONSOLE_CONFIG_DISABLED = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0"]
CONSOLE_CONFIG_ENABLED = ["1","1","1","1","1","1","1","1","1","1","1","1","1","1"]



#######################################
############  CHART CONFIG ############
#######################################

# General aliases for setup
CHARTS_CONFIG_DISABLED = ["0","0","0","0","0","0"]

# Chart types
CHART_DISABLED = '0'
CHART_EPS = 'k'
CHART_TEMPERATURE = 'h'
CHART_ALTITUDE = 'j'
CHART_PRESSION = 'j'
CHART_EULER = 'a'
CHART_QUATERNION = 'b'
CHART_ANGULAR_SPEED = 'c'
CHART_ACCELERATION = 'd'
CHART_MAGNETIC_FIELD = 'e'
CHART_LINEAR_ACCELERATION = 'f'
CHART_GRAVITY = 'g'
CHART_LUMINANCE = 'l'


#######################################
############  TEST MAGNETO ############
#######################################
MAGNETO_TEST_FIN = "B"
MAGNETO_DEMAG_FIN = "A"
