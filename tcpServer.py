import usocket
import _thread

class TcpServer:

    # The size of receiving buffer
    RECEIVE_BUFFER_SZ = 4096

    def __init__(self,cbList, eventList):
        """
        Init the TCP server with the given port
        """
        self.tcpSocket = None
        self.lastRemoteAddr = ""
        self.lastRemotePort = 0
        self.cbList = cbList
        self.eventList = eventList

    def bind(self,localIP,localPort):
        """
        Bind the TCP server to the given address/port
        """
        self.tcpSocket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM) #Create the socket
        self.tcpSocket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1) #Initialize the socket
        self.tcpSocket.bind((localIP,localPort)) #Bind the socket
        self.tcpSocket.listen(maxFailedConnection) #Start listening for in coming connections

    def getLastRemote(self):
        """
        Return the last remote IP and UDP port in a tuple: (IP,PORT)
        """
        return (self.lastRemoteAddr,self.lastRemotePort)

            """while True:

                (tcpClientsocket, tcpAddress) = tcpServersocket.accept()
                tcpClientThread(tcpClientsocket, utime.ticks_ms()) #Start a new thread to handler the new connection

            tcpServersocket.close() #Close the server-side socket"""

    def readRequest(self):
        """
        TCP request handler.

            Returns:
                sentBytes (int): The number of bytes sent in HTTP response
        """

        lstRemote = ""
        lstRemotePort = 0

        #Isolate request arguments as strings
        (request,(lstRemote,lstRemotePort)) = self.tcpSocket.recvfrom(TcpServer.RECEIVE_BUFFER_SZ)
        splitRequest = str(request).split(" ")

        #Default response header
        http_header = b"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\nConnection:close \r\n\r\n"

        #List of possible response file types
        mimeTypeList = [(".html", b"text/html"),
                        (".css", b"text/css"),
                        (".jpg", b"image/jpeg"),
                        (".js", b"application/javascript"),
                        (".txt", b"text/plain"),
                        (".woff", b"font/woff"),
                        (".woff2", b"font/woff2")]

        if len(splitRequest) <= 1: #If request is empty
            http_body = b"Invalid request, ignoring ..."
        else:
            #Get the requested ressource
            requestContent = "index.html" if splitRequest[1]=="/" else splitRequest[1][1:]

            #Check the type of the request

            #If event, bind the eventSource and return withour closing the socket
            if requestContent in self.eventList:
                self.eventList[requestContent].bind(self.tcpSocket)
                http_body = requestContent + " bounded."
                sentBytes = self.tcpSocket.send(http_header + http_body)
                return sentBytes

            #If command, return command response
            elif requestContent in self.cbList:
                http_body = self.cbList[requestContent]()

            #If file
            else:
                #Get the file type
                mimeType = b"application/octet-string"
                for i in mimeTypeList:
                    if i[0] in requestContent:
                        mimeType = i[1]

                #Read the file content in binary mode
                try:
                    with open("web/" + requestContent, 'rb') as infile:
                        http_header = b"HTTP/1.1 200 OK\r\nContent-Type: " + mimeType + b"\r\nContent-Lenght: " + str(uos.stat("web/" + requestContent)[6]) + b"\r\nConnection:close \r\n\r\n"
                        http_body = infile.read()
                        infile.close()
                except OSError:
                    http_body = b"Requested content not found .."

        #Send the HTTP response and close the connection
        sentBytes = self.tcpSocket.send(http_header + http_body)
        self.socket.close()

        #Clear string for memory saving (experimental)
        http_header = ""
        http_body = ""

        return sentBytes
