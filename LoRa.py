
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
    print("Initializing LoRa ...")
    lora.init(mode=loraMode, region=loraRegion,
            tx_power=loraTxPower, bandwidth=loraBandwidth,
            sf=loraSpreadingFactor, preamble=loraPreamble,
            coding_rate=loraCodingRate, power_mode=loraPowerMode,
            tx_iq=loraTxIQ, rx_iq=loraRxIQ,
            public=loraPublicSync)
    
    print("LoRa initialized")


def loopSend():
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

def loopReceive():
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