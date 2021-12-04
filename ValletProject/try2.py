from multiprocessing import Process, Manager
from multiprocessing.managers import BaseManager
import Vallet
from Vallet import Vallet
import multiprocessing
##import BlockMaker
import threading
import time
import socket
import Transaction
import pickle 
import time
import select

lock=multiprocessing.Lock()

# def process():
#     p1=multiprocessing.Process(target=vallet.ReceiveMoney,args=())
#     #p2=multiprocessing.Process(target=vallet.CreateTransaction,args=[500,'127.0.0.1'])
#     p1.start()
#     #p2.start()
#     while True:
#         vallet.CreateTransaction(200,'127.0.0.1')
#         time.sleep(2)
        
def CreateTransaction(sum,receiver,vallet):
        transaction=Transaction.Transaction(sum,vallet.getIP(),receiver,vallet.getBalance(),time.time())
        TCP_IP = '127.0.0.1'
        TCP_PORT = 5000
        BUFFER_SIZE = 1024
       ## MESSAGE = pickle.dumps(transaction)
        MESSAGE = pickle.dumps(transaction)##json.dumps(transaction)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        response=s.recv(1024)
        if(pickle.loads(response)=='ok'):
            lock.acquire()
            vallet.setBalance((int)(vallet.getBalance())-sum)
            print('balance=',vallet.getBalance())
            input()
            lock.release()
        else:
            print('Couldnt send money. Not enough balance.')
        print('SENDOVAO')
        s.close()
        
def ReceiveMoney(vallet):
    HOST=''
    PORT=5001 #self.GetPort()
    print(PORT)
    ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST,PORT))
    print('bindovao')
    ss.listen(5)
    print ("Listening on port",PORT)
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
                    StoreMoney(data,vallet)       
                else:
                    s.close()
                    read_list.remove(s)
                    
def StoreMoney(rcvData,vallet):
    transaction=pickle.loads(rcvData)
    print('income: ',transaction.sum)
    print('PRE LOCKA')
    lock.acquire()
    vallet.setBalance((int)(vallet.getBalance())+transaction.sum)
    print('balance =>  ',vallet.getBalance())
    vallet.addTransaction(transaction)
    lock.release()    
    print('POSLE LOCKA')



##transaction_thread=threading.Thread(target=vallet.CreateTransaction,args=(500,'123.4.5.6',))
##transaction_thread.start()
##transaction_thread.join()
##vallet.CreateTransaction(500,'123.4.5.6')
if __name__=='__main__':
    BaseManager.register('Vallet', Vallet)
    manager = BaseManager()
    manager.start()
    vallet = manager.Vallet()
    rcvProcess=multiprocessing.Process(target=ReceiveMoney,args=[vallet])
    #p2=multiprocessing.Process(target=vallet.CreateTransaction,args=[500,'127.0.0.1'])
    rcvProcess.start()
    #p2.start()
    while True:
        CreateTransaction(200,'127.0.0.1',vallet)
        time.sleep(2)
    rcvProcess.join()