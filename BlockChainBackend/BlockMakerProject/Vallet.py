import socket
from Socket import Socket
from filelock import FileLock
#import portalocker

class Vallet:
    counter=0
    def __init__(self,username,port):
        self.balance=1000
        self.transactions=[]
        self.ipAddr=socket.gethostbyname(socket.gethostname())
        self.socket = Socket(port,socket.gethostbyname(socket.gethostname()))
        self.username=username
    def getSocket(self):
        return self.socket
    def setSocket(self,port):
        self.socket.setPort(port)
    def getBalance(self):
        return self.balance
    def setBalance(self,balance):
        self.balance=balance
    def getPort(self):
        self.socket.getPort()
    def addTransaction(self,transaction):
        self.transactions.append(transaction)
    def getIP(self):
        return self.ipAddr
    def getUsername(self):
        return self.username
    def __str__(self):
        return "username:{u}\nbalance:{b}\n".format(u=self.username,b=self.balance)
    def dump(self):
        return {
            "username":self.username,
            "balance":self.balance,
            "ipAddress":self.getIP(),
            "port":self.getPort()
        }