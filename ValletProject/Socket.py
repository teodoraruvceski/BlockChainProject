class Socket:
    def __init__(self,port,ip):
        self.port=port
        self.ip=ip
    def setPort(self,port):
        self.port = port
        
    def getPort(self):
        return self.port
    
    def __str__(self):
        return "Port : {port}\nIp : {ip}}".format(port=self.port,ip=self.ip)