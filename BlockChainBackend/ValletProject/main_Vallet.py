from multiprocessing import Process, Manager, Value
from multiprocessing.managers import BaseManager
from logger import Logger
from Socket import Socket
import Vallet
from Vallet import Vallet
from BlockMaker import BlockMaker
import multiprocessing
from random import randint
import threading
import time
import socket
import Transaction
import pickle 
import time
import select
import socketserver
import sys
import time
from threading import Thread
from random import randint
from random import choice
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


def ReceiveMoney(vallet,finishProcess,username,logger):
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
                    transaction=pickle.loads(data)
                    logger.logMessage(f"Vallet {username} received {transaction.sum} from vallet {transaction.sender}")      
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


def SendTransaction(vallet,username,users,logger): #mijenjana funkcija
    #receiverUsername=input('Enter receiver\'s username: ')
    receiverUsername = choice(users)
    while True:
        # sum=input('Enter sending sum: ')
        # sum=int(sum)
        sum = randint(10,100)
        if(sum>vallet.getBalance()):
            print('Not enough balance.')
            continue
        else:
            CreateTransaction(sum,vallet,receiverUsername)
            logger.logMessage(f"Vallet {username} sent {sum} to vallet {receiverUsername}.")
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
    # je broj na kome se u narednim agrumentima nalazi username
    # ostali su drugi voleti kojima moze slati
    users = sys.argv[2:len(sys.argv)]
    username=users[int(sys.argv[1])]
    print("username:",username)
    users.remove(username)
    print("users2:",users)
    logger = Logger("valletLogs.log")
    logger.logMessage(f"Vallet {username} started.")
    with socketserver.TCPServer(("localhost", 0), None) as s:
        free_port = s.server_address[1]
        print(free_port)
    
    BaseManager.register('Vallet', Vallet) 
    finishProcess = Value('i',False)
    manager = BaseManager()
    manager.start()
    vallet = manager.Vallet(username,free_port)
    valletCopy=Vallet(username,free_port)
    Register(valletCopy)
    rcvProcess=Thread(target=ReceiveMoney,args=[vallet,finishProcess,username,logger])
    #p2=multiprocessing.Process(target=vallet.CreateTransaction,args=[500,'127.0.0.1'])
    rcvProcess.start()
    #p2.start()
    while True:
        time.sleep(randint(5,10))
        SendTransaction(vallet,username,users,logger)
        #logger.logMessage(f"Vallet {username} sent transaction.")

        # print('1. Posalji novu transakciju')
        # print('2. Provjeri stanje racuna')
        # print('3. Ugasi klijenta')
        # try:
        #     inPut = (int)(input())
        # except:
        #     inPut=55
        # if inPut==1:
        #     SendTransaction(vallet)
        # elif inPut==2:
        #     print(vallet.getBalance())
        # elif inPut==3:
        #     finishLock.acquire()
        #     finishProcess.value=True
        #     finishLock.release()
        #     break
        # else:
        #     print('Nepostojeca komanda')  
            
      
    rcvProcess.join()
    print('Kraj programa')
    vallet.ReleasePort()