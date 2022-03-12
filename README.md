# INISAT_COM
COM Board implementation for INISAT CubeSat project
## File description
- **main.py** is the entry point of the program, it will be loaded as soon as *boot.py* finishes
- **boot.py** may contain a hardware initilization sequence for the LoPy/FiPy board, but is currently unused
- **aliases.py** stores a list of aliases, used to ensure compatibility with the Web application
- **config.py** defines all the hardware and software configuration
- **eventsource.py** contains a small class used to manage Javascript EventSources
- **fr.json** is the French language pack
- **general.py** contains all the commands supported by the UDP and TCP server, as well as some hardware initialization functions
- **help.txt** contains the help message sent to the UDP client when the command "help" is received
- **ioctl.py** is a simple class used to access LoPy/FiPy hardware interfaces (PWM,GPIO,UART)
- **json_ext.py** defines some utility functions used to convert a Python dictionnary into a JSON string
- **LoRa.py** defines a class used to send messages through the LoRa link
- **state.py** defines a set of state-variables (global variables), shared between every modules
- **tcpServer.py** is a class implementing a basic HTTP server
- **uart.py** is a class used to handle the communication with the OBC, and update the sensors data read in a state-variable
- **udpserver.py** is a class implementing a simple UDP responder
- **uping.py** implements the ping function to check whether the camera is active or not
- **wifi.py** is a class used to manage the WiFi
- **web/** is a folder containing the Web application
# LoPy/FiPy setup
In order to setup the LoPy/FiPy it is first necessary to install the firmware of the expansion board. Then, the LoPy/FiPy firmware can be installed
## 1. Install the expansion board firmware
To install the expansion board firmware, please refer to the following guide from Pycom : https://docs.pycom.io/updatefirmware/expansionboard/ 
## 2. Install the LoPy/FiPy firmware
To install the LoPy/FiPy firmware, check the next guide : https://docs.pycom.io/updatefirmware/device/
## 3. Install an IDE
LoPy/FiPy board can be programmed using either VS code or Atom. To prepare you favourite IDE, install the Pymakr extension.

Detailed guides :
- Atom : https://docs.pycom.io/gettingstarted/software/atom/
- VS code : https://docs.pycom.io/gettingstarted/software/vscode/

## 4. Upload the file system
1. Make sure that the root directory of your workspace contains all the **.py* files. Also, verify that the Pymakr console is opened (on VS Code).
2. Connect the board to your computer using a USB-microUSB cable while maintaining the "Safe Boot" button of the expansion board pushed. 
3. Release the button after 2-3 seconds. 
4. The Python console should appear. Then, just click on the *Upload* button. The files of the current filesystem will be copied / updated on the board.
5. Once the *Upload* process is finished, the board should run the program. 

## 5. Troubleshooting
Some files are missing on the LoPy/FiPy or have not been uploaded => Open *All commands* (in the bottom banner in VS code), then click on *Pymakr > Global Setting*. This should open a JSON file called *pymakr.json*. Check whether the file extension of the missing files is present in the value of the key *sync_file_types*. If the file extension is not in the list, you may add it. Do not forget to save this configuration file before trying to upload the code.