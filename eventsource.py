class EventSource:
    """
    Class used to handle EventSource communication with the browser
    """

    def __init__(self,name):
        """
        Init a new event source
        @arg name(str) : the name of the event
        """
        self.name = name
        self.socketClientList = []

    def bind(self,socketClient):
        """
        Bind this event source to the given socket
        @arg socketClient(--) : the name of the socket client to bind to this
        event
        """
        self.socketClientList.append(socketClient)
        responseHeader = b"HTTP/1.1 200 OK\r\nCache-Control: no-cache\r\nContent-Type: text/event-stream\r\n\r\n"
        socketClient.send(responseHeader)

    def send(self,func_name,data,id):
        """
        Send an event to all the socket clients that are bound to this event source
        @arg func_name(str) : the name of the function to call in the browser
        @arg data(str) : the data associated to the event
        @arg id(int) : a unique ID to identify this event occurrence
        """
        messageBody = "id: "+str(id)+"\n"
        messageBody += "event: "+func_name+"\n"
        messageBody += "data: "+data+"\n\n"

        # List to store the index of sockets that hasve been closed and has
        # to be cleared
        removeSocketIdx = []

        idx = 0
        for socketClient in self.socketClientList:
            try:
                socketClient.send(bytes(messageBody, 'utf-8'))
            except OSError as err:
                socketClient.close()
                removeSocketIdx.append(idx)
                print("Err no:"+str(err.errno))
            idx += 1

        # Reverse the list in order to remove properly the items
        # (starting from the high index)
        removeSocketIdx.reverse()

        # Clear closed sockets
        for socketIdx in removeSocketIdx:
            del self.socketClientList[socketIdx]
