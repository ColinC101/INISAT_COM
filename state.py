import aliases

def init():
    """
    Init state variables
    """
    global consoleConfig,autoTesting,consoleInterval,modeGnss,modeGnss_ex,camStatus,udpCom,testMag,ioctlObj,wifiObj,loraObj,gnssStartTime,chartsConfig,deMag,readingsJSON, affCons, affGraph, affInterface, affLora, affModeGnss, affCons_ex, affGraph_ex, affInterface_ex, affLora_ex,wifiLastBlink,loraLastBlink,lastOBCTime,lastUserTime,userConnected,lastLoRaTime,lastConsoleTime,lastChartsTime,chartsInterval,lastInterfaceTime,udpServ

    # Console configuration
    consoleConfig = aliases.CONSOLE_CONFIG_DISABLED.copy()

    # Auto test status
    autoTesting = 0

    # Console updating interval (ms)
    consoleInterval = 5000

    # Charts updating interval (ms)
    chartsInterval = 5000

    # Enable / Disable GNSS
    modeGnss = 0
    modeGnss_ex = 0

    # Enable / Disable camera
    camStatus = 0

    # Enable / Disable UDP com
    udpCom = False

    # Active magneto-coupler test (when set to 1,2,3 or 4)
    testMag = 0

    # Activate degaussing (when set to 1)
    deMag = 0

    # IOCTL
    ioctlObj = None

    # WIFI
    wifiObj = None

    # LORA
    loraObj = None

    # Timing Management
    gnssStartTime = aliases.MODE_GNSS_FINISHED

    # Charts configuration
    chartsConfig = aliases.CHARTS_CONFIG_DISABLED.copy()

    # All the data retreived from OBC
    # Keys are listed in aliases.py under JSON ACCESS
    readingsJSON = {}

    # TODO: Pas sûr de ce que sont ces variables, glhf
    affCons = False
    affGraph = False
    affInterface = False
    affLora = False
    affModeGnss = False
    affCons_ex = False
    affGraph_ex = False
    affInterface_ex = False
    affLora_ex = False

    # Time in ms indicating the last blinking instant for WiFi LED
    wifiLastBlink = 0

    # Same for LoRa LED
    loraLastBlink = 0

    # startTime in .ino
    # Last time OBC has been read (in ms)
    lastOBCTime = 0

    # user_start in .ino
    # Last time instant of user's signaling request ('/ouvPage' or '/user')
    lastUserTime = 0

    # Indicate if a user is connected to the browser (0 => False, 1 => True)
    userConnected = 0

    #  Indicate the last time instant where LoRa request have been made
    lastLoRaTime = 0

    # Indicate the last time instant where console data have been requested
    lastConsoleTime = 0

    # Indicate the last time instant where charts data have been requested
    lastChartsTime = 0

    # Indicate the last time instant where interface data have been requested
    lastInterfaceTime = 0

    # UDP server
    udpServ = None

    #Current interface language
    curLang = DEFAULT_LANG

    #Current language structure
    lang = None
