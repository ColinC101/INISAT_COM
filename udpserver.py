from socket import AF_INET, IPPROTO_UDP, SOCK_DGRAM, socket
import _thread

class UdpServer:
    """
    This class implements the UDP server used for the INISAT
    """

    # The size of receiving buffer
    RECEIVE_BUFFER_SZ = 32

    def __init__(self,cbList,cbArgList,cbSingleChar):
        """
        Init the UdpServer
        @arg cbList : dictionary where key is the UDP command name, and value is the 
        associated callback function  
        @arg cbArgList : dictionnary where key is the UDP command, and value the associated
        callback function. 
        Note: the callback function must accept one argument (a tuple) whose content will
        be filled by the UDP command args.
        @arg cbSingleChar : a dictionary where key is a single-char UDP command, and value the
        associated callback which must accept one argument (the UDP command argument).
        """
        self.udpSocket = None
        self.lastRemoteAddr = ""
        self.lastRemotePort = 0
        self.cbList = cbList
        self.cbArgList = cbArgList
        self.cbSingleChar = cbSingleChar

    def bind(self,localIP,localPort):
        """
        Bind the UdpServer to the given address/port so that it can
        receive packets
        """
        self.udpSocket = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
        self.udpSocket.bind((localIP,localPort))

        # Put the socket in non-blocking mode
        self.udpSocket.setblocking(False)

            
    
    def readPacket(self):
        """
        Read a UDP packet and execute the associated command
        """
        lstRemote = ""
        lstRemotePort = 0
        try:
            (bytesReceived,(lstRemote,lstRemotePort)) = self.udpSocket.recvfrom(UdpServer.RECEIVE_BUFFER_SZ)
        except OSError as err:
            if err.errno == 11:
                print("No data")
            return
        print("Data!")
    
        self.lastRemoteAddr = lstRemote
        self.lastRemotePort = lstRemotePort
        udpCommand = bytesReceived.decode('utf-8')
        print("Trame UDP recue de : "+self.lastRemoteAddr)
        print("Taille : "+str(len(udpCommand)))
        print("Donnees : "+udpCommand)

        udpCommand = udpCommand.strip().lower()
        
        # The UDP response message

        if udpCommand in self.cbList:
            # Execute the command which has no argument
            responseMsg = self.cbList[udpCommand]()
            self.sendTo(responseMsg,(self.lastRemoteAddr,self.lastRemotePort))
        elif "+" in udpCommand:
            # The given command seems to have args (separated by +)
            commandArgs = udpCommand.split("+")
            commandName = commandArgs[0]
            if commandName in self.cbArgList:
                # Execute the command which takes arguments
                responseMsg = self.cbArgList[commandName](tuple(commandArgs[1:]))
                self.sendTo(responseMsg,(self.lastRemoteAddr,self.lastRemotePort))
            else:
                print("UDP command with args '"+commandName+"' is ignored (no associated callback)")
        else:
            # The given command seems to be a single-char command
            if len(udpCommand)>0:
                commandName = udpCommand[0]
                commandArg = udpCommand[1:]
                if commandName in self.cbSingleChar:
                    responseMsg = self.cbSingleChar[commandName](commandArg)
                    self.sendTo(responseMsg,(self.lastRemoteAddr,self.lastRemotePort))
                else:
                    print("UDP single char-command '"+udpCommand+"' is ignored (no associated callback)")      
            else:
                print("UDP command '"+udpCommand+"' is ignored (empty command)")      

    def getLastRemote(self):
        """
        Return the last remote IP and UDP port in a tuple: (IP,PORT)
        """
        return (self.lastRemoteAddr,self.lastRemotePort)

    def sendTo(self,msg,remote):
        """
        Send a UDP packet to the given destination
        @arg msg(str): the content of the UDP packet
        @arg remote((str,int)) : (the destination IP address,the destination UDP port)
        """
        self.udpSocket.sendto(bytes(msg,"utf-8"),remote)

    def sendToLastRemote(self,msg):
        """
        Send a UDP packet to the last remote machine
        @arg msg(str): the content of the UDP packet
        """
        self.udpSocket.sendto(bytes(msg,"utf-8"),(self.lastRemoteAddr,self.lastRemotePort))