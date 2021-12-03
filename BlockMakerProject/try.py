##import Vallet
import BlockMaker
import multiprocessing
from multiprocessing import Queue
import socket
import pickle 
import time
import select



def recieveTransactions(q):
        
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
                        
                        #print('New transaction : \n',pickle.loads(data))
                        q.put(data)
                                      
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
        print('sending money')
        TCP_IP = data.receiver
        TCP_PORT = 5001
        BUFFER_SIZE = 1024
        MESSAGE = pickle.dumps(data)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        print('SENDOVAO transakciju klijentu')
        s.close()


    
def process():
    recieveProcess=multiprocessing.Process(target=recieveTransactions,args=())
    sendProcess=multiprocessing.Process(target=sendTransaction,args=())
    recieveProcess.start()
    sendProcess.start()
    
if __name__=='__main__':
    blockmaker=BlockMaker.BlockMaker()
    q = Queue()
    recieveProcess=multiprocessing.Process(target=recieveTransactions,args=[q])
    sendProcess=multiprocessing.Process(target=sendTransaction,args=[q])
    recieveProcess.start()
    sendProcess.start()

    #process()





#blockmaker.recieveTransactions()
##listen_thread=threading.Thread(target=blockmaker.recieveTransactions,args=None)
##listen_thread.start()
##transaction_thread=threading.Thread(target=vallet.CreateTransaction,args=(500,'123.4.5.6',))
##transaction_thread.start()
##listen_thread.join()
##transaction_thread.join()
##vallet.CreateTransaction(500,'123.4.5.6')
