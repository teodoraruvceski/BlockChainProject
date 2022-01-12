# ##import Vallet
import BlockMaker
import Transaction
import multiprocessing
import Vallet
# multiprocessing.set_start_method('spawn')
from multiprocessing import Queue
import socket
import pickle 
import time
import select
from Socket import Socket
from Block import Block
from multiprocessing.managers import BaseManager
from flask import Flask
import json

app=Flask(__name__)
transactions=[]
@app.route("/transactions")
def transactionsForWeb():
    global transactions
    jsons={"transactions":[json.dumps([t.dump() for t in transactions])]}
    print(jsons)
    return {"transactions":[json.dumps([t.dump() for t in transactions])]}

def runServerForWeb():
    app.run(debug=True)
lock=multiprocessing.Lock()

def recieveTransactions(sendingQueue,savingQueue,blockmaker):
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
                    print(data)
                    if data:
                        trans=pickle.loads(data)
                        print('New transaction : \n',trans)
                        ind=False
                        for v in blockmaker.getVallets():
                            if(trans.getReceiver()==v.getUsername()):
                                ind=True
                                if(trans.balance>=trans.sum):  #proveravamo da li ima dovoljno sredstava na racunu
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
        print('qsize = ', q.qsize())
        if( q.empty()):
            time.sleep(2)
            print('queue empty')
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
        print('!!! blok KOJI SALJEM: \n',blockMaker.getBlock())
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
    sum=500
    global transactions
    while True:
        transaction=Transaction.Transaction(sum,"neca","dora",22222,time.time())
        savingQueue.put(transaction)
        transactions.append(transaction)
        print('savingQueue = ',savingQueue.qsize())
        time.sleep(1)
def RegisterVallet(blockMaker):
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
    recieveProcess=multiprocessing.Process(target=recieveTransactions,args=[sendingQueue,savingQueue,inst])
    sendProcess=multiprocessing.Process(target=sendTransaction,args=[sendingQueue,inst])
    saveProcess=multiprocessing.Process(target=saveTransaction,args=[savingQueue,inst])
    fakeReceiveProcess=multiprocessing.Process(target=FakeReceiveTransaction,args=[savingQueue])
    registerMinerProcess=multiprocessing.Process(target=RegisterMiner,args=[inst])
    registerValletProcess=multiprocessing.Process(target=RegisterVallet,args=[inst])
    webServerProcess=multiprocessing.Process(target=runServerForWeb,args=())
    registerValletProcess.start()
    recieveProcess.start() #receiving transactions from Vallet
    sendProcess.start()
    saveProcess.start()
    registerMinerProcess.start()
    #fakeReceiveProcess.start() #faking receiving transactions from Vallet
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

