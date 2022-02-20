import usocket
import _thread
import config
import uos

class TcpServer:

    # The size of receiving buffer
    RECEIVE_BUFFER_SZ = 4096

    def __init__(self,cbList, cbArgList, eventList):
        """
        Init the TCP server with the given port
        """
        self.tcpSocket = None
        self.cbList = cbList
        self.cbArgList = cbArgList
        self.eventList = eventList

    def bind(self,localIP,localPort):
        """
        Bind the TCP server to the given address/port
        """
        self.tcpSocket = usocket.socket(usocket.AF_INET, usocket.SOCK_STREAM) #Create the socket
        self.tcpSocket.setsockopt(usocket.SOL_SOCKET, usocket.SO_REUSEADDR, 1) #Initialize the socket
        self.tcpSocket.bind((localIP,localPort)) #Bind the socket
        self.tcpSocket.listen(config.maxFailedConnection) #Start listening for in coming connections

    def listen(self):
        _thread.start_new_thread(self.__accept_loop__,())

    def __accept_loop__(self):
        while True:
            try:
                (tcpClientsocket, tcpAddress) = self.tcpSocket.accept()
                self.readRequest(tcpClientsocket)
            except OSError as err:
                if err.errno==114:
                    print("Connexion reset")
                else:
                    print("Exception: errno="+str(err.errno))
                tcpClientsocket.close()

    def readRequest(self,clientSocket):
        """
        TCP request handler.

            Returns:
                sentBytes (int): The number of bytes sent in HTTP response
        """

        #Isolate request arguments as strings
        request = str(clientSocket.recv(TcpServer.RECEIVE_BUFFER_SZ))
        splitRequest = str(request).split(" ")

        #Default response header
        http_header = b"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\nConnection:close \r\n\r\n"

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
            requestParams = []
            if "?" in requestContent: #If request has parameters
                splitRequestContent = requestContent.split("?")
                requestContent = splitRequestContent[0]
                for i in splitRequestContent[1].split("&"):
                    requestParams.append(i.split("=")[1])

            #Check the type of the request

            #If event, bind the eventSource and return without closing the socket
            if requestContent.lower() in self.eventList:
                self.eventList[requestContent.lower()].bind(clientSocket)
                http_header = b"HTTP/1.1 200 OK\r\nCache-Control: no-cache\r\nContent-Type: text/event-stream\r\n\r\n"
                sentBytes = clientSocket.send(http_header)
                return sentBytes

            #If command, return command response
            elif requestContent.lower() in self.cbList:
                    http_body = self.cbList[requestContent.lower()]()

                #If command requesting args, retun command response
            elif requestContent.lower() in self.cbArgList:
                    http_body = self.cbArgList[requestContent.lower()](requestParams)

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
        sentBytes = clientSocket.send(http_header + http_body)
        clientSocket.close()

        #Clear string for memory saving (experimental)
        http_header = ""
        http_body = ""

        return sentBytes
