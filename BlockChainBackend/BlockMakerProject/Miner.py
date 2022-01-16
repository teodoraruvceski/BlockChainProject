from Socket import Socket
import socket
class Miner:
    def __init__(self):
        self.socket=Socket("7005",'localhost')
        self.blockMined=0
        self.neighbors=[]
    def getPort(self):
        return self.socket.getPort()
    def getIp(self):
        return self.socket.getIp()
    
    def setBlockMined(self,value):
        self.blockMined=value
    def getBlockMined(self):
        return self.blockMined
    def incrementBlockMined(self):
        self.blockMined+=1
    def addNeighbor(self,neighbor):
        self.neighbors.append(neighbor)
    def setNeighbors(self,neighbors):
        self.neighbors=neighbors
    def __str__(self):
        return "Miner:\n\tPort : {port}\n\tIp : {ip}\n\tBlock mined: {bm}".format(port=self.socket.getPort(),ip=self.socket.getIp(),bm=self.blockMined)
    
    def dump(self):
        return{
            "ipAddress":self.getIp(),
            "port":self.getPort(),
            "blockMined":self.blockMined()
        }