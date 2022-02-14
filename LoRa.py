
from network import LoRa
import socket
import pycom
import config
import time

"""
For complete documentation, see :
    https://docs.pycom.io/firmwareapi/pycom/network/lora/
For this implementation, we are focusing on LoPy to Lopy communication,
in simple LoRa mode (see https://docs.pycom.io/tutorials/networks/lora/module-module/)
"""

class LoraObject:        
    def __init__(self):
        # Status of th LoRa link. (0 = disabled / 1 = enabled)
        self.__loraStatus__ = False
        # Getting LoRa object
        self.lora = LoRa(mode=config.loraMode, region=config.loraRegion)
   
    def initLoRa(self):
        """
        Initialisation of the LoRa transmission.
        Parameters (mode, region, ...) can be modified in config.py file
        """
        print("Initializing LoRa ...")
        self.lora.init(mode=config.loraMode, region=config.loraRegion,
                tx_power=config.loraTxPower, bandwidth=config.loraBandwidth,
                sf=config.loraSpreadingFactor, preamble=config.loraPreamble,
                coding_rate=config.loraCodingRate, power_mode=config.loraPowerMode,
                tx_iq=config.loraTxIQ, rx_iq=config.loraRxIQ,
                public=config.loraPublicSync)
        self.__loraStatus__ = True
        print("LoRa initialized")

    ######################################################
    #################  CONNEXION STATUS  #################
    ######################################################

    def getLoraStatus(self):
        """
        Gets the status of the Lora link
        @return True  if the link is On
                False if the link is Off
        """
        return self.__loraStatus__

    def enableLora(self):
        """
        Enables the LoRa link.
        Communications will then be sent by the LoRa Antenna
        """
        self.__loraStatus__ = True

    def disableLora(self):
        """
        Disnables the LoRa link.
        Communications will not be sent by the LoRa Antenna
        """
        self.__loraStatus__ = False


    def sendReadings(self):
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