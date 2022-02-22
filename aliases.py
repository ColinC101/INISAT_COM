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
JSON_AUTOTEST_WIFI_MODE = "autotest_wifi_mode"
JSON_AUTOTEST_WIFI_POWER = "autotest_wifi_power"
JSON_AUTOTEST_WIFI_IP = "autotest_wifi_ip"
JSON_AUTOTEST_PING_CAMERA = "autotest_ping_camera"
JSON_AUTOTEST_LORA_POWER = "autotest_lora_power"
JSON_AUTOTEST_LORA_SPREADINGFACTOR = "autotest_lora_spedingfactor"
JSON_AUTOTEST_LORA_BANDWIDTH = "autotest_lora_bandwidth"
JSON_AUTOTEST_LORA_FREQUENCY = "autotest_lora_frequency"
JSON_AUTOTEST_LORA_CODINGRATE = "autotest_lora_codingrate"
JSON_AUTOTEST_LORA_PREAMBLE = "autotest_lora_preamble"
JSON_AUTOTEST_VOID1 = "autotest_void1"
JSON_AUTOTEST_VOID2 = "autotest_void2"
JSON_AUTOTEST_VOID3 = "autotest_void3"
JSON_AUTOTEST_RAW = "autotest_raw"


# EPS
JSON_EPS_VBAT = "eps_vbat"
JSON_EPS_VIN = "eps_vin"
JSON_EPS_VOUT = "eps_vout"
JSON_EPS_ICHARGE = "eps_icharge"
JSON_EPS_IIN = "eps_iin"
JSON_EPS_TBAT = "eps_tbat"
JSON_EPS_CHARGE_STATUS = "eps_charge_status"

# Temperature
JSON_TEMPERATURE = "temperature"

# Altitude
JSON_ALTITUDE = "altitude"

# Pression
JSON_PRESSION = "pression"

# Euler
JSON_EULER_ROLL = "euler_roll"
JSON_EULER_PITCH = "euler_pitch"
JSON_EULER_YAW = "euler_yaw"

# Quaternion
JSON_QUATERNION_W = "quaternion_w"
JSON_QUATERNION_X = "quaternion_x"
JSON_QUATERNION_Y = "quaternion_y"
JSON_QUATERNION_Z = "quaternion_z"

# Angular Speed
JSON_ANGULARSPEED_X = "angularspeed_x"
JSON_ANGULARSPEED_Y = "angularspeed_y"
JSON_ANGULARSPEED_Z = "angularspeed_z"

# Acceleration
JSON_ACCELERATION_X = "acceleration_x"
JSON_ACCELERATION_Y = "acceleration_y"
JSON_ACCELERATION_Z = "acceleration_z"

# Magnetic Field
JSON_MAGNETICFIELD_X = "magneticfield_x"
JSON_MAGNETICFIELD_Y = "magneticfield_y"
JSON_MAGNETICFIELD_Z = "magneticfield_z"

# Linear acceleration
JSON_LINEARACCELERATION_X = "linearacceleration_x"
JSON_LINEARACCELERATION_Y = "linearacceleration_y"
JSON_LINEARACCELERATION_Z = "linearacceleration_z"

# Gravity Vector
JSON_GRAVITY_X = "gravity_x"
JSON_GRAVITY_Y = "ravity_y"
JSON_GRAVITY_Z = "gravity_z"

# Luminance
JSON_LUMINANCE_X = "luminance_x"
JSON_LUMINANCE_NEGX = "luminance_negx"
JSON_LUMINANCE_Y = "luminance_y"
JSON_LUMINANCE_NEGY = "luminance_negy"
JSON_LUMINANCE_Z = "luminance_z"

# GNSS
JSON_GNSS_UTC = "gnss_utc"
JSON_GNSS_LATITUDE = "gnss_latitude"
JSON_GNSS_LONGITUDE = "gnss_longitude"
JSON_GNSS_NBSAT = "gnss_nbsat"

# NMEA
JSON_NMEA_1 = "nmea_1"
JSON_NMEA_2 = "nmea_2"
JSON_NMEA_3 = "nmea_3"
JSON_NMEA_4 = "nmea_4"
JSON_NMEA_5 = "nmea_5"
JSON_NMEA_6 = "nmea_6"
JSON_NMEA_7 = "nmea_7"
JSON_NMEA_8 = "nmea_8"
JSON_NMEA_9 = "nmea_9"

# Config
JSON_CONS_CONFIG = "cons_config"



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
CHARTS_CONFIG_DISABLED = ["0","0","0","0","0","0","0","0","0","0","0","0","0","0"]

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

CHARTS_ACCEPTED_VALUES = [CHART_DISABLED,CHART_EPS,CHART_TEMPERATURE,CHART_ALTITUDE,CHART_PRESSION,CHART_EULER,
CHART_QUATERNION,CHART_ANGULAR_SPEED,CHART_ACCELERATION,CHART_MAGNETIC_FIELD,CHART_LINEAR_ACCELERATION,
CHART_GRAVITY,CHART_LUMINANCE]


#######################################
############  TEST MAGNETO ############
#######################################
MAGNETO_TEST_FIN = "B"
MAGNETO_DEMAG_FIN = "A"

#######################################
############  SYSTEM EVENTS ###########
#######################################
EVENT_READING_CONSOLE = "CAP_reading_cons"
EVENT_READING_GRAPH = "CAP_reading_graph"
EVENT_READING_INTERFACE = "CAP_reading_index"
EVENT_READING_AUTOTEST = "AUTOTEST_reading"
EVENT_DEMAG_FIN = "DEMAG_fin"