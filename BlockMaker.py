import socket
import Transaction
import pickle 
import time
import json
import select
import sys
class BlockMaker:
    def __init__(self):
        self.Block=[]
        self.Miners=[]
        self.ipAddr=socket.gethostbyname(socket.gethostname())
        
    def recieveTransactions(self):
        HOST=self.ipAddr
        PORT=5000
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.setblocking(0)
        s.bind((HOST,PORT))
        print('bindovao')
        s.listen(10)
        inputs = [s]
        outputs = []
        ##connection,addr=s.accept()
        while True:
          print('pocetak whilea')
          readable, writable, exceptional = select.select(inputs,outputs,inputs)
          for ss in readable:
               if ss is not s:
                   print(readable.count()) 
                   ##obj=json.loads(json.parse(s.recv(1024)))
                   ## data = Transaction(**obj)
                   data=s.recv(1024)
                   if data:
                    print(data)
                
