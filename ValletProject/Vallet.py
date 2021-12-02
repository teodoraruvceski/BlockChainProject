import socket
import Transaction
import pickle 
import time
import json
import sys
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
        data = s.recv(BUFFER_SIZE)
        s.close()
        print ("received data:", data)