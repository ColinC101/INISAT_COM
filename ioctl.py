class Ioctl:
    """
    Class used to handle IOs of the board
    """
    KEY_PWM_X = "PWM_X"
    KEY_PWM_Y = "PWM_Y"
    KEY_DIR_X = "DIR_X"
    KEY_DIR_Y = "DIR_Y"
    KEY_LORA_LED = "LORA_LED"
    KEY_WIFI_LED = "WIFI_LED"
    KEY_CAM_CONTROL = "CAM_CONTROL"
    KEY_UART_OBC = "UART_OBC"
    
    def __init__(self):
        self.obj={}
    
    def setObject(self,key,val):
        """
        Set the given key of the dictionary with the given value
        """
        self.obj[key]=val
    
    def getObject(self,key):
        """
        Return the object associated to the given key of the IO 
        """
        if(key in self.obj):
            return self.obj[key]
        else:
            raise Exception("IOCTL : Key not found")