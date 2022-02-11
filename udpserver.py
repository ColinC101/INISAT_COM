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
        self.activated = False
        self.lastRemoteAddr = ""
        self.lastRemotePort = 0
        self.cbList = cbList

    def listen(self,localIP,localPort):
        """
        Start a new thread for processing UDP requests
        """
        if not self.activated:
            self.activated = True
            self.udpSocket = socket(AF_INET,SOCK_DGRAM,IPPROTO_UDP)
            self.udpSocket.bind((localIP,localPort))
            _thread.start_new_thread(self.__main_loop__,())
    
    def __main_loop__(self):
        """
        The main loop of the UDP Server, used to process requests
        """
        
        # Put the socket in blocking mode
        self.udpSocket.settimeout(None)

        while self.activated:
            (bytesReceived,(self.lastRemoteAddr,self.lastRemotePort)) = self.udpSocket.recvfrom(UdpServer.RECEIVE_BUFFER_SZ)
            udpCommand = bytesReceived.decode('utf-8')
            print("Trame UDP recue de : "+self.lastRemoteAddr)
            print("Taille : "+len(udpCommand))
            print("Donnees : "+udpCommand)

            udpCommand = udpCommand.strip().lower()

            if udpCommand in self.cbList:
                self.cbList[udpCommand]()
            else:
                print("UDP command '"+udpCommand+"' is ignored (no associated callback)")            

    def getLastRemote(self):
        """
        Return the last remote IP and UDP port in a tuple: (IP,PORT)
        """
        return (self.lastRemoteAddr,self.lastRemotePort)

    def sendTo(self,msg,remoteAddr,remotePort):
        """
        Send a UDP packet to the given destination
        @arg msg(str): the content of the UDP packet
        @arg remoteAddr(str) : the destination IP address
        @arg remotePort(int) : the destination UDP port
        """
        self.udpSocket.sendto(bytes(msg,"utf-8"),(remoteAddr,remotePort))