from Socket import Socket
import socket
class Miner:
    def __init__(self):
        self.socket=Socket(0,'localhost')
        self.blockMined=0
        self.neighbors=[]
        self.minername=""
        self.balance=0  
    def payment(self):
        self.balance += 1*(1 + self.balance/100000 + self.blockMined/1000 )
    def getBalance(self):
        return self.balance
    def setMinername(self,minername):
        self.minername=minername
    def getMinername(self):
        return self.minername
    def getPort(self):
        return self.socket.getPort()
    def getIp(self):
        return self.socket.getIp()
    def setPort(self,port):
        self.socket.setPort(port)
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
    
    def TakePort(self):
        with open('minerPorts.txt','r') as f:
            lines = f.readlines()
            f.close()
        idx=0
        max=7001
        array=[]
        if len(lines)!=0 :
            array = lines[0].split(',')
            for port in array:
                idx+=1
                if int(port)>max:
                    if int(port)>(max+1):
                        idx-=1
                        break
                    max = int(port)
            max+=1
        array.insert(idx,max)
        text=""
        for port in array:
            text=text+str(port)+","
        
        textlist = list(text)
        textlist.pop()
        text2= "".join(textlist)
        with open('minerPorts.txt', 'w') as f:
                f.write(text2)
        f.close()
        return max
    
    def ReleasePort(self):
        with open('minerPorts.txt','r') as f:
                lines = f.readlines()
        array = lines[0].split(',')
        print(array)
        myport=self.getSocket().getPort()
        print(myport)
        array.remove(str(myport))
        print(array)

        text=""
        if len(array)!=0 :
            for port in array:
                text=text+str(port)+","
            textlist = list(text)
            textlist.pop()
            text2= "".join(textlist)
            print(text2)
        else :
            text2=""
        with open('minerPorts.txt', 'w') as f:
            f.write(text2)
            f.close()
    