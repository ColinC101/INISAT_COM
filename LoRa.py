
from network import LoRa
import socket
import pycom
import time

"""
For complete documentation, see :
    https://docs.pycom.io/firmwareapi/pycom/network/lora/
For this implementation, we are focusing on LoPy to Lopy communication,
in simple LoRa mode (see https://docs.pycom.io/tutorials/networks/lora/module-module/)
"""


# Status of th LoRa link. (0 = disabled / 1 = enabled)
__loraStatus__ = True


loraMode = LoRa.LORA
loraRegion = LoRa.EU868  # Europe

# Parameters only for LoRa.LORA mode
#loraFrequency = 0  #TODO, est-ce qu'il y a une valeur par défaut ? Rien trouvé dans le code .ino
loraTxPower = 17  # 17dBm
loraBandwidth = LoRa.BW_125KHZ
loraSpreadingFactor = 7
loraPreamble = 8
loraCodingRate = LoRa.CODING_4_5
loraPowerMode = LoRa.ALWAYS_ON
loraTxIQ = False
loraRxIQ = False
loraPublicSync = True

# Parameters only for LoRa.LORAWAN mode
loraAdaptativeDataRate = 0
loraTxRetries = 0
loraDeviceClass = 0


# Getting LoRa object
lora = LoRa(mode=loraMode, region=loraRegion)

def initLoRa():
    """
    Initialisation of the LoRa transmission.
    Parameters (mode, region, ...) can be modified in config.py file
    """
    print("Initializing LoRa ...")
    lora.init(mode=loraMode, region=loraRegion,
            tx_power=loraTxPower, bandwidth=loraBandwidth,
            sf=loraSpreadingFactor, preamble=loraPreamble,
            coding_rate=loraCodingRate, power_mode=loraPowerMode,
            tx_iq=loraTxIQ, rx_iq=loraRxIQ,
            public=loraPublicSync)
    
    print("LoRa initialized")

######################################################
#################  CONNEXION STATUS  #################
######################################################

def getLoraStatus():
    """
    Gets the status of the Lora link
    @return True  if the link is On
            False if the link is Off
    """
    return __loraStatus__

def enableLora():
    """
    Enables the LoRa link.
    Communications will then be sent by the LoRa Antenna
    """
    __loraStatus__ = True

def disableLora():
    """
    Disnables the LoRa link.
    Communications will not be sent by the LoRa Antenna
    """
    __loraStatus__ = False


def sendReadings():
    """
    Sends the collected data via the LoRa link.
    """
    # Creating communication Socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    # TODO: Ajouter les envois des données
        # (quand les données seront ajoutées)
    s.close()





######################################################
##############  TESTS DE FONCTIONNEMENT ##############
######################################################


def testLoopSend():
    """
    A simple loop sending LoRa Ping messages every second.
    To do a complete test, please use testLoopReceive() on another node.
    """
    # Creating communication Socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    i = 0
    #while True:
    while i<10:
        s.send('Ping')
        print('Ping {}'.format(i))
        i += 1
        time.sleep(1)
    s.close

def testLoopReceive():
    """
    A simple loop waiting for LoRa Ping messages, and responding when received.
    To do a complete test, please use testLoopSend() on another node.
    """
    # Creating communication Socket
    s = socket.socket(socket.AF_LORA, socket.SOCK_RAW)
    s.setblocking(False)
    i = 0
    #while True:
    while i<10:
        if s.recv(64) == b'Ping':
            s.send('Pong')
            print('Pong {}'.format(i))
            i += 1
        time.sleep(1)
    s.close