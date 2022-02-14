from socket import AF_INET, IPPROTO_UDP, SOCK_DGRAM, socket
import _thread

class UdpServer:
    # The size of receiving buffer
    RECEIVE_BUFFER_SZ = 32

    """
    This class implements the UDP server used for the INISAT
    @arg cbList : dictionary where key is the UDP command name, and value is the 
    associated callback function  
    """
    def __init__(self,cbList):
        """
        Init the UDP server with the given port
        """
        self.udpSocket = None
        self.lastRemoteAddr = ""
        self.lastRemotePort = 0
        self.cbList = cbList

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

        if udpCommand in self.cbList:
            # Execute the command
            responseMsg = self.cbList[udpCommand]()
            # Send the response
            self.sendTo(responseMsg,(self.lastRemoteAddr,self.lastRemotePort))
        else:
            print("UDP command '"+udpCommand+"' is ignored (no associated callback)")            

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