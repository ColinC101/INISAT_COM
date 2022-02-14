def init():
    """
    Init state variables
    """
    global consoleConfig,autoTesting,consoleInterval,modeGnss,camStatus,udpCom,testMag,ioctlObj,loraObj

    # Console configuration
    consoleConfig = "00000000000000"

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

    # Active magneto-coupler test
    testMag = 0

    ioctlObj = None

    loraObj = None
