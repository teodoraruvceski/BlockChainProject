import socket
import Transaction
import pickle 
import time
import json
import sys
import select
class Vallet:
    counter=0
    def __init__(self):
        self.balance=0
        self.id= self.counter +1
        self.counter += 1
        self.transactions=[]
        self.ipAddr=socket.gethostbyname(socket.gethostname())
        
    def CreateTransaction(self,sum,receiver):
        transaction=Transaction.Transaction(sum,self.ipAddr,receiver,self.balance,time.time())
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5000
        BUFFER_SIZE = 1024
       ## MESSAGE = pickle.dumps(transaction)
        MESSAGE = pickle.dumps(transaction)##json.dumps(transaction)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        print('SENDOVAO')
        s.close()
        
    def ReceiveMoney(self):
        HOST=''
        PORT=5001
        ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ss.bind((HOST,PORT))
        print('bindovao')
        ss.listen(5)
        print ("Listening on port 5001")
        read_list = [ss]
        while True:
            readable, writable, errored = select.select(read_list, [], [])
            for s in readable:
                if s is ss:
                    client_socket, address = ss.accept()
                    read_list.append(client_socket)
                    print( "Connection from", address)
                else:
                    data = s.recv(1024)
                    if data:
                        #call method for money storing
                        #print('New transaction : \n',pickle.loads(data))
                        self.StoreMoney(data)       
                    else:
                        s.close()
                        read_list.remove(s)
                        
    def StoreMoney(self,rcvData):
        transaction=pickle.loads(rcvData)
        print('income: ',transaction.sum)
        self.balance += transaction.sum
        self.transactions.append(transaction)