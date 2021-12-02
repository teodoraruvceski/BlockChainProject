import socket
import Transaction
import pickle 
import time
import json
import select
import sys
from multiprocessing import Queue
import multiprocessing
class BlockMaker:
    ##Transactions = Queue()
    def __init__(self):
        self.Block=[]
        self.Miners=[]
        self.ipAddr=socket.gethostbyname(socket.gethostname())
        self.Transactions=Queue()
        
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

      
       