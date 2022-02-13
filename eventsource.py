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
        self.lnkSocket = None

    def bind(self,socketClient):
        """
        Bind this event source to the given socket. Note : if a socket was already bound to this
        EventSource, it will be closed.
        @arg socketClient(--) : the name of the socket client to bind to this
        event
        """
        if(self.lnkSocket != None):
            self.lnkSocket.close()

        self.lnkSocket = socketClient

        responseHeader = b"HTTP/1.1 200 OK\r\nCache-Control: no-cache\r\nContent-Type: text/event-stream\r\n\r\n"
        socketClient.send(responseHeader)
    
    def send(self,func_name,data,id):
        """
        Send an event to the socket client that is bound to this event source
        @arg func_name(str) : the name of the function to call in the browser
        @arg data(str) : the data associated to the event
        @arg id(int) : a unique ID to identify this event occurrence
        """
        messageBody = "id: "+str(id)+"\n"
        messageBody += "event: "+func_name+"\n"
        messageBody += "data: "+data+"\n\n"
        
        try:
            self.lnkSocket.send(bytes(messageBody, 'utf-8'))
        except OSError as err:
            # Handle connection reset
            self.lnkSocket.close()
            self.lnkSocket = None