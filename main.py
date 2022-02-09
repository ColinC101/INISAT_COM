import pycom
import time
import LoRa

print("Begin Main")

pycom.heartbeat(False)



LoRa.loopSend()

print("End Main")
