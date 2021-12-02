import socket
import Transaction
import pickle 
import time
import json
import select
import sys
from multiprocessing import Queue
class BlockMaker:
    ##Transactions = Queue()
    def __init__(self):
        self.Block=[]
        self.Miners=[]
        self.ipAddr=socket.gethostbyname(socket.gethostname())
        ##self.Transactions=Queue()
        
    def recieveTransactions(self,msgQueue):
        HOST=''
        PORT=5000
        ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        ss.bind((HOST,PORT))
        print('bindovao')
        ss.listen(5)
        print ("Listening on port 5000")
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
                        s.send(data)
                        print(pickle.loads(data))
                        msgQueue.put(data)
                        ##BlockMaker.Transactions.
                        print(msgQueue.qsize())                      
                    else:
                        s.close()
                        read_list.remove(s)
                        
    def sendTransaction(self,msgQueue):

        print(msgQueue.qsize())
        while True:
            ##if(BlockMaker.Transactions.qsize()==0):
            ##  continue
            ##print()
            print('sending money',msgQueue.qsize())
            data=msgQueue.get()
            print('sending')
            TCP_IP = '127.0.0.1'
            TCP_PORT = 5000
            BUFFER_SIZE = 1024
       ## MESSAGE = pickle.dumps(transaction)
        # MESSAGE = pickle.dumps('message')##json.dumps(transaction)
        # s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # s.connect((TCP_IP, TCP_PORT))
        # s.send(MESSAGE)
        # print('SENDOVAO')
        # data = s.recv(BUFFER_SIZE)
        # s.close()
        # print ("received data:", data)

      
       