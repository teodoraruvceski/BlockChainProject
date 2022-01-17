# ##import Vallet
import BlockMaker
import Transaction
import multiprocessing
import Vallet
import Miner
# multiprocessing.set_start_method('spawn')
from multiprocessing import Queue
import socket
import pickle 
import time
import select
from Socket import Socket
from threading import Thread
from Block import Block
from multiprocessing.managers import BaseManager
from flask import Flask
from flask_socketio import SocketIO, send
import json
from time import sleep

lock=multiprocessing.Lock()

webclientQueue = Queue() ###################################################dodao
app=Flask(__name__)
app.config['SECRET_KEY'] = 'mysecret'
socketIo = SocketIO(app, cors_allowed_origins="*")
app.debug=True 
app.host='localhost'

@socketIo.on("connectt")
def handleMessage (msg):
    global webclientQueue
    print("Client connected: ", msg)
    while True:
        print("nijeusao")
        message =  webclientQueue.get()
        print("usao")
        print("Sent to react: ",  message)
        if(type(message )==type(Block(time.time(),None))):
            message=message.dumpForWeb()
        else:
            message=message.dump()
        socketIo.emit("message",message)      
        time.sleep(1)
#########################################################################

def recieveTransactions(sendingQueue,savingQueue,blockmaker):
    global webclientQueue ######################################################
    HOST=''
    PORT=5015
    ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST,PORT))
    print('bindovao')
    ss.listen(5)
    print ("Listening on port 5015.")
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
                print(data)
                if data:
                    trans=pickle.loads(data)
                    print('New transaction : \n',trans)
                    ind=False
                    for v in blockmaker.getVallets():
                        if(trans.getReceiver()==v.getUsername()):
                            ind=True
                            if(trans.balance>=trans.sum):  #proveravamo da li ima dovoljno sredstava na racunu
                                webclientQueue.put(trans)##################################################dodao
                                sendingQueue.put(trans)
                                savingQueue.put(trans)    
                                s.send('ok'.encode())  
                                
                            else:
                                s.send('ERROR: not enough balance.'.encode())  
                            break  
                    if(ind!=True):
                        s.send('ERROR: invalid receiver\'s username.'.encode())                  
                else:
                    s.close()
                    read_list.remove(s)
                        
def sendTransaction(q,blockmaker):
    while True:
        #print('qsize = ', q.qsize())
        if( q.empty()):
            time.sleep(2)
            #print('queue empty')
            continue
        time.sleep(2)
        data= q.get()
        data.balance=None
        for v in blockmaker.getVallets():
            if(v.getUsername()==data.getReceiver()):
                print('sending money')
                TCP_IP = v.getSocket().getIp()
                TCP_PORT =(int)(v.getSocket().getPort())
                MESSAGE = pickle.dumps(data)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((TCP_IP, TCP_PORT))
                s.send(MESSAGE)
                print('sent transaction to client')
                s.close()

def saveTransaction(q,blockMaker):
    global webclientQueue
    start=None
    while True:
        start=time.time()
        while True:
            transaction=q.get()
            blockMaker.addTransaction(transaction)
            if(time.time()-start>= 10):
                break
        lock.acquire()
        if(len(blockMaker.getBlock().getTransactions())==0):
            continue
        if(blockMaker.getMinersCount()==0):
            print(blockMaker.getMinersCount())
            lock.release()
            continue
        chosenMiner=blockMaker.getRandomMiner()
        lock.release()
        TCP_IP = chosenMiner.getIp()
        TCP_PORT =(int)(chosenMiner.getPort())
        webclientQueue.put(blockMaker.getBlock())
        MESSAGE = pickle.dumps(blockMaker.getBlock())
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        blockMaker.newBlock()
        print('------RESETOVANJE BLOKA------')
        print(blockMaker.getBlock())
        print('Prije blokiranja i cekanja potvrde da je blok sredjen')
        data = s.recv(1024)
        print('Nakon primanja poruke')
        if data:
            mess=pickle.loads(data)
            print(mess)

def RegisterMiner(blockMaker):
    global webclientQueue
    HOST=''
    PORT=6000
    ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST,PORT))
    print('bindovao')
    ss.listen(5)
    print ("Listening on port 6000")
    read_list = [ss]
    while True:
       # readable, writable, errored = select.select(read_list, [], [])
        readable, writable, errored = select.select(read_list, [], [])
        for s in readable:
            if s is ss:
                client_socket, address = ss.accept()
                read_list.append(client_socket)
                print( "Connection from", address)
            else:
                data = s.recv(1024)
                if data:
                    newMiner=pickle.loads(data)
                    print(newMiner)
                    if(len(blockMaker.getMiners())==0):
                        genesisBlock=blockMaker.create_genesis_block()  
                        genesisBlock.hash=0
                        MESSAGE = pickle.dumps(genesisBlock)
                        print('sent genesis block to first miner')
                    else:
                        chosenMiner=blockMaker.getRandomMiner()
                        MESSAGE = pickle.dumps(chosenMiner)
                        print('sent random miner to new miner')
                    webclientQueue.put(newMiner)
                    print(str(pickle.loads(MESSAGE)))
                    s.send(MESSAGE)
                    lock.acquire()
                    blockMaker.addMiner(newMiner)
                    lock.release()
                    #s.close()
                else:
                    s.close()
                    read_list.remove(s)

def FakeReceiveTransaction(savingQueue):
    global webclientQueue
    print('FAKE STARTDED')
    sum=500
    while True:
        transaction=Transaction.Transaction(sum,"neca","dora",22222,time.time())
        savingQueue.put(transaction)
        #webclientQueue.put(transaction)
        #webclientQueue.put(Miner.Miner())
        #webclientQueue.put(Vallet.Vallet("nebojsa",3))
        webclientQueue.put(Block(12,12))
        #print('savingQueue = ',savingQueue.qsize())
        time.sleep(2)
def RegisterVallet(blockMaker):
    global webclientQueue
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
        try:
            readable, writable, errored = select.select(read_list, [], [])
            for s in readable:
                if s is ss:
                    client_socket, address = ss.accept()
                    read_list.append(client_socket)
                    print( "Connection from", address)
                else:
                    data = s.recv(8192)
                    if data:
                        newVallet=pickle.loads(data)
                        print(newVallet)
                        ind =True
                        for v in blockMaker.getVallets():
                            if(v.getUsername()==newVallet.getUsername()):
                                ind=False
                                break
                        if(ind==True):
                            blockMaker.addVallet(newVallet)
                            print("ubacuje u red") 
                            webclientQueue.put(newVallet)
                            print(webclientQueue.qsize())
                    else:
                        read_list.remove(s)
        except:
            print(readable)
            
if __name__=='__main__':
    BaseManager.register('BlockMaker', BlockMaker.BlockMaker)
    manager = BaseManager()
    manager.start()
  
    inst = manager.BlockMaker()
    
    sendingQueue = Queue() #red iz kog cita metoda sendTransaction
    savingQueue = Queue()  #red iz kog cita metoda saveTransaction
    
    recieveProcess=Thread(target=recieveTransactions,args=[sendingQueue,savingQueue,inst])
    sendProcess=Thread(target=sendTransaction,args=[sendingQueue,inst])
    saveProcess=Thread(target=saveTransaction,args=[savingQueue,inst])
    fakeReceiveProcess=Thread(target=FakeReceiveTransaction,args=[savingQueue])
    registerMinerProcess=Thread(target=RegisterMiner,args=[inst])
    registerValletProcess=Thread(target=RegisterVallet,args=[inst])
    #webServerProcess=multiprocessing.Process(target=runServerForWeb,args=())
    
    registerValletProcess.start()
    recieveProcess.start() #receiving transactions from Vallet
    sendProcess.start()
    saveProcess.start()
    #fakeReceiveProcess.start() #faking receiving transactions from Vallet
    registerMinerProcess.start()
    socketIo.run(app)#############################################################dodao

    #webServerProcess.start()
    inp=""
    input(inp)





#blockmaker.recieveTransactions()
##listen_thread=threading.Thread(target=blockmaker.recieveTransactions,args=None)
##listen_thread.start()
##transaction_thread=threading.Thread(target=vallet.CreateTransaction,args=(500,'123.4.5.6',))
##transaction_thread.start()
##listen_thread.join()
##transaction_thread.join()
##vallet.CreateTransaction(500,'123.4.5.6')

