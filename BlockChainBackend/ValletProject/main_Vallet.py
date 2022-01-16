from multiprocessing import Process, Manager, Value
from multiprocessing.managers import BaseManager
from Socket import Socket
import Vallet
from Vallet import Vallet
from BlockMaker import BlockMaker
import multiprocessing
##import BlockMaker
import threading
import time
import socket
import Transaction
import pickle 
import time
import select
import socketserver

#import keyboard

lock=multiprocessing.Lock()
finishLock=multiprocessing.Lock()
configLock=multiprocessing.Lock()
# def process():
#     p1=multiprocessing.Process(target=vallet.ReceiveMoney,args=())
#     #p2=multiprocessing.Process(target=vallet.CreateTransaction,args=[500,'127.0.0.1'])
#     p1.start()
#     #p2.start()
#     while True:
#         vallet.CreateTransaction(200,'127.0.0.1')
#         time.sleep(2)
        
        #PRVI ARGUMENT f-je bio port pa sam izbacio jer je pracvilo problem
def CreateTransaction(sum,vallet,username):
    transaction=Transaction.Transaction(sum,vallet.getUsername(),username,vallet.getBalance(),time.time())
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5015
    MESSAGE = pickle.dumps(transaction)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    response=s.recv(1024)
    print(response.decode())
    if(response.decode()=='ok'):
        lock.acquire()
        vallet.setBalance((int)(vallet.getBalance())-sum)
        print('balance=',vallet.getBalance())
        
        lock.release()
    elif(response.decode()=="ERROR: not enough balance."):
        print(response.decode())
    elif(response.decode()=="ERROR: invalid receiver's username."):
        print(response.decode())
    s.close()


def ReceiveMoney(vallet,finishProcess):
    HOST=''
    PORT=vallet.getSocket().getPort()
    vallet.setSocket(PORT)
    print(PORT)
    ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST,PORT))
    print('bindovao')
    ss.listen(5)
    print ("Listening on port",PORT)
    read_list = [ss]
    while True:
        finishLock.acquire()
        if finishProcess.value==True:
            finishLock.release()
            return
        finishLock.release()
        readable, writable, errored = select.select(read_list, [], [],3)
        for s in readable:
            if s is ss:
                client_socket, address = ss.accept()
                read_list.append(client_socket)
                print( "Connection from", address)
            else:
                data = s.recv(1024)
                if data:
                    #call method for money storing
                    StoreMoney(data,vallet)       
                else:
                    s.close()
                    read_list.remove(s)
                    
def StoreMoney(rcvData,vallet):
    transaction=pickle.loads(rcvData)
    print('income: ',transaction.sum)
    lock.acquire()
    vallet.setBalance((int)(vallet.getBalance())+transaction.sum)
    print('new balance =>  ',vallet.getBalance())
    vallet.addTransaction(transaction)
    lock.release()    


def SendTransaction(vallet):
    receiverUsername=input('Enter receiver\'s username: ')
    while True:
        sum=input('Enter sending sum: ')
        sum=int(sum)
        if(sum>vallet.getBalance()):
            print('Not enough balance.')
            continue
        else:
            CreateTransaction(sum,vallet,receiverUsername)
            break
def Register(vallet):
    TCP_IP = '127.0.0.1'
    TCP_PORT = 5001
    MESSAGE = pickle.dumps(vallet)
    print(pickle.loads(MESSAGE))
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    s.close()

if __name__=='__main__':
    with socketserver.TCPServer(("localhost", 0), None) as s:
        free_port = s.server_address[1]
        print(free_port)
    username=input('Enter username\n')
    
    BaseManager.register('Vallet', Vallet) 
    finishProcess = Value('i',False)
    manager = BaseManager()
    manager.start()
    vallet = manager.Vallet(username,free_port)
    valletCopy=Vallet(username,free_port)
    Register(valletCopy)
    rcvProcess=multiprocessing.Process(target=ReceiveMoney,args=[vallet,finishProcess])
    #p2=multiprocessing.Process(target=vallet.CreateTransaction,args=[500,'127.0.0.1'])
    rcvProcess.start()
    #p2.start()
    while True:
        print('1. Posalji novu transakciju')
        print('2. Provjeri stanje racuna')
        print('3. Ugasi klijenta')
        try:
            inPut = (int)(input())
        except:
            inPut=55
        if inPut==1:
            SendTransaction(vallet)
        elif inPut==2:
            print(vallet.getBalance())
        elif inPut==3:
            finishLock.acquire()
            finishProcess.value=True
            finishLock.release()
            break
        else:
            print('Nepostojeca komanda')  
            
      
    rcvProcess.join()
    print('Kraj programa')
    vallet.ReleasePort()