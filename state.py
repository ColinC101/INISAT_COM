import aliases

def init():
    """
    Init state variables
    """
    global consoleConfig,autoTesting,consoleInterval,modeGnss,modeGnss_ex,camStatus,udpCom,testMag,ioctlObj,wifiObj,loraObj,gnssStartTime,chartsConfig,deMag,readingsJSON, affCons, affGraph, affInterface, affLora, affModeGnss, affCons_ex, affGraph_ex, affInterface_ex, affLora_ex

    # Console configuration
    consoleConfig = aliases.CONSOLE_CONFIG_DISABLED

    # Auto test status
    autoTesting = 0

    # Console updating interval (ms)
    consoleInterval = 5000

    # Enable / Disable GNSS
    modeGnss = 0
    modeGnss_ex = 0

    # Enable / Disable camera
    camStatus = 0

    # Enable / Disable UDP com
    udpCom = False

    # Active magneto-coupler test (when set to 1)
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
    chartsConfig = aliases.CHARTS_CONFIG_DISABLED

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

