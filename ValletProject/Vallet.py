import socket
from Socket import Socket
import Transaction
import pickle 
import time
import json
import sys
import select
import multiprocessing
import filelock
from filelock import FileLock
#import portalocker
lock=multiprocessing.Lock()

'''from filelock import FileLock

with FileLock("myfile.txt"(sad)
    # work with the file as it is now locked
    print("Lock acquired.")'''

class Vallet:
    counter=0
    def __init__(self):
        self.balance=1000
        self.id= self.counter +1
        self.counter += 1
        self.transactions=[]
        self.ipAddr=socket.gethostbyname(socket.gethostname())
        self.socket = Socket(self.TakePort(),socket.gethostbyname(socket.gethostname()))
        
    def getSocket(self):
        return self.socket
    def setSocket(self,port):
        self.socket.setPort(port)
    def getBalance(self):
        return self.balance
    def setBalance(self,balance):
        self.balance=balance
    def addTransaction(self,transaction):
        self.transactions.append(transaction)
    def getIP(self):
        return self.ipAddr
    
    def TakePort(self):
        with open('portconfig.txt','r') as f:
            lines = f.readlines()
            f.close()
      
        idx=0
        max=5001
        array=[]
        if len(lines)!=0 :
            array = lines[0].split(',')
            for port in array:
                idx+=1
                if int(port)>max:
                    if int(port)>(max+1): #5001,5002,5003,5004
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
        with open('portconfig.txt', 'w') as f:
                f.write(text2)
        f.close()
        return max
    
    def ReleasePort(self):
        with open('portconfig.txt','r') as f:
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
        with open('portconfig.txt', 'w') as f:
            f.write(text2)
            f.close()
        # with FileLock('portconfig.txt.lock'):
        #     with lock:
        #         lines = open('portconfig.txt','w').write(text2)
    # def GetPort(self):
    #     with open('portconfig.txt','r') as f:
    #          lines = f.readlines()
             
    #     print(lines)
    #     array = lines[0].split(',')
    #     print(array)
    #     max=5001
    #     idx=0
    #     for port in array:
    #         idx+=1
    #         if int(port)>max:
    #             if int(port)>(max+1): #5001,5002,5003,5004
    #                 #max=max+1
    #                 break
    #             max = int(port)
    #     max+=1
    #     array.insert(idx,max)
    #     text=""
    #     for port in array:
    #         text=text+str(port)+","
        
    #     textlist = list(text)
    #     #print("TEXTLIST:",textlist)
    #     textlist.pop()
    #     #print("TEXTLIST2:",textlist)
    #     text2= "".join(textlist)
    #     print(text2)
    #     with open('portconfig.txt', 'w') as f:
    #          f.write(text2)
    #     f.close()
    #     return max

    # def CreateTransaction(self,sum,receiver):
    #     transaction=Transaction.Transaction(sum,self.ipAddr,receiver,self.balance,time.time())
    #     TCP_IP = '127.0.0.1'
    #     TCP_PORT = 5000
    #     BUFFER_SIZE = 1024
    #    ## MESSAGE = pickle.dumps(transaction)
    #     MESSAGE = pickle.dumps(transaction)##json.dumps(transaction)
    #     s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #     s.connect((TCP_IP, TCP_PORT))
    #     s.send(MESSAGE)
    #     response=s.recv(1024)
    #     if(pickle.loads(response)=='ok'):
    #         lock.acquire()
    #         self.balance -= sum
    #         print('balance=',self.balance)
    #         input()
    #         lock.release()
    #     else:
    #         print('Couldnt send money. Not enough balance.')
    #     print('SENDOVAO')
    #     s.close()
        
    # def ReceiveMoney(self):
    #     HOST=''
    #     PORT=5001 #self.GetPort()
    #     print(PORT)
    #     ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #     ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     ss.bind((HOST,PORT))
    #     print('bindovao')
    #     ss.listen(5)
    #     print ("Listening on port",PORT)
    #     read_list = [ss]
    #     while True:
    #         readable, writable, errored = select.select(read_list, [], [])
    #         for s in readable:
    #             if s is ss:
    #                 client_socket, address = ss.accept()
    #                 read_list.append(client_socket)
    #                 print( "Connection from", address)
    #             else:
    #                 data = s.recv(1024)
    #                 if data:
    #                     #call method for money storing
    #                     #print('New transaction : \n',pickle.loads(data))
    #                     self.StoreMoney(data)       
    #                 else:
    #                     s.close()
    #                     read_list.remove(s)
                        
    # def StoreMoney(self,rcvData):
    #     transaction=pickle.loads(rcvData)
    #     print('income: ',transaction.sum)
    #     print('PRE LOCKA')
    #     lock.acquire()
    #     self.balance += transaction.sum
    #     print('balance =>  ',self.balance)
    #     self.transactions.append(transaction)
    #     lock.release()
    #     print('POSLE LOCKA')