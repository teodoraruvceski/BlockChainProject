##import Vallet
import BlockMaker
import Transaction
import multiprocessing
from multiprocessing import Queue
import socket
import pickle 
import time
import select


def recieveTransactions(sendingQueue,savingQueue):
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
                        print('New transaction : \n',pickle.loads(data))
                        if(trans.balance>=trans.sum):  #proveravamo da li ima dovoljno sredstava na racunu
                            sendingQueue.put(data)
                            savingQueue.put(data)    
                            s.send('ok'.encode())    
                        else:
                            s.send('invalid'.encode())                     
                    else:
                        s.close()
                        read_list.remove(s)
                        
def sendTransaction(q):
    while True:
        print('qsize = ', q.qsize())
        if( q.empty()):
            time.sleep(2)
            print('queue empty')
            continue
        time.sleep(2)
        data= pickle.loads(q.get())
        data.balance=None
        print('sending money')
        TCP_IP = data.receiver.getIp()
        TCP_PORT =(int)(data.receiver.getPort())
        BUFFER_SIZE = 1024
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
            transaction=pickle.loads(q.get())
            blockMaker.block.transactions.append(transaction)
            if(time.time()-start>= 6):
                break
        chosenMiner=blockMaker.getRandomMiner()
        TCP_IP = chosenMiner.getIp()
        TCP_PORT =(int)(chosenMiner.getPort())
        BUFFER_SIZE = 1024
        MESSAGE = pickle.dumps(blockMaker.getBlock())
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        print('sent block to random miner')
        s.close()
        blockMaker.newBlock()

def RegisterMiner(blockMaker):
    HOST=''
    PORT=6000
    ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST,PORT))
    ss.listen(5)
    print ("Listening for registration on port 6000")
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
                    newMiner=pickle.loads(data)
                    if(blockMaker.setMiners().count()==0):
                        print('')
                        #get initial block and send it to first miner             
                else:
                    s.close()
                    read_list.remove(s)


    
if __name__=='__main__':
    blockmaker=BlockMaker.BlockMaker()
    sendingQueue = Queue() #red iz kog cita metoda sendTransaction
    savingQueue = Queue()  #red iz kog cita metoda saveTransaction
    recieveProcess=multiprocessing.Process(target=recieveTransactions,args=[sendingQueue,savingQueue])
    sendProcess=multiprocessing.Process(target=sendTransaction,args=[sendingQueue])
    saveProcess=multiprocessing.Process(target=saveTransaction,args=[savingQueue,blockmaker])
    recieveProcess.start()
    sendProcess.start()
    saveProcess.start()







#blockmaker.recieveTransactions()
##listen_thread=threading.Thread(target=blockmaker.recieveTransactions,args=None)
##listen_thread.start()
##transaction_thread=threading.Thread(target=vallet.CreateTransaction,args=(500,'123.4.5.6',))
##transaction_thread.start()
##listen_thread.join()
##transaction_thread.join()
##vallet.CreateTransaction(500,'123.4.5.6')

