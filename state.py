import aliases

def init():
    """
    Init state variables
    """
    global consoleConfig,autoTesting,consoleInterval,modeGnss,camStatus,udpCom,testMag,ioctlObj,loraObj,gnssStartTime,chartsConfig,deMag,readingsJSON, affCons, affGraph, affInterface, affLora, affCons_ex, affGraph_ex, affInterface_ex, affLora_ex

    # Console configuration
    consoleConfig = aliases.CONSOLE_CONFIG_DISABLED

    # Auto test status
    autoTesting = 0

    # Console updating interval (ms)
    consoleInterval = 5000

    # Enable / Disable GNSS
    modeGnss = 0

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
    affCons = 0
    affGraph = 0
    affInterface = 0
    affLora = 0
    affCons_ex = 0
    affGraph_ex = 0
    affInterface_ex = 0
    affLora_ex = 0

