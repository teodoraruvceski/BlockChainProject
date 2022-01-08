import socket
import Transaction
import random
import pickle 
import time
import json
import select
import sys
from multiprocessing import Queue
# from Block import Block
import multiprocessing
class BlockMaker:
    def __init__(self):
       # self.block=Block(time.time(),None)
        self.miners=[]
        self.ipAddr=socket.gethostbyname(socket.gethostname())
        
    def addTransaction(self,transaction):
        self.block.transactions.append(transaction)
        
    # def newBlock(self):
    #     self.Block=Block(time.time(),None)
        
    # def getRandomMiner(self):
    #     if(len(self.miners)==0):
    #         return -1
    #     return random.choice(self.miners)
    
    # def getBlock(self):
    #     return self.block
    
    # def getMiners(self):
    #     return self.miners
    
    # def addMiner(self,miner):
    #     self.miners.append(miner)
    #     print("-----DODAO MINERA")
    #     print(len(self.getMiners()))
        
    # def getMinersCount(self):
    #     lenn=len(self.miners)
    #     print('GETMINERSCOUNT: ',lenn)
    #     return lenn
    
    # def create_genesis_block(self):
    #     genesis_block = Block(time.time(), "0")
    #     genesis_block.hash = genesis_block.compute_hash()
    #     print("CREATED GENESIS: "+str(genesis_block))
    #     return genesis_block
    # def recieveTransactions(self):
    #     q=Queue()
    #     sendProcess=multiprocessing.Process(target=self.sendTransaction,args=[q])
    #     sendProcess.start()
    #     HOST=''
    #     PORT=5000
    #     ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #     ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #     ss.bind((HOST,PORT))
    #     print('bindovao')
    #     ss.listen(5)
    #     print ("Listening on port 5000")
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
                        
    #                     #print('New transaction : \n',pickle.loads(data))
    #                     q.put(data)
                                      
    #                 else:
    #                     s.close()
    #                     read_list.remove(s)
                        
    # def sendTransaction(self,q):
    #     while True:
    #         print('qsize = ', q.qsize())
    #         if( q.empty()):
    #             time.sleep(2)
    #             print('queue empty')
    #             continue
    #         time.sleep(2)
    #         data= pickle.loads(q.get())
    #         print('sending money')
    #         TCP_IP = data.receiver
    #         TCP_PORT = 5001
    #         BUFFER_SIZE = 1024
    #         MESSAGE = pickle.dumps(data)
    #         s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #         s.connect((TCP_IP, TCP_PORT))
    #         s.send(MESSAGE)
    #         print('SENDOVAO transakciju klijentu')
    #         s.close()

   
       