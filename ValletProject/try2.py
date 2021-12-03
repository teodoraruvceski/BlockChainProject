import Vallet
import multiprocessing
##import BlockMaker
import threading
import time

vallet=Vallet.Vallet()
def process():
    p1=multiprocessing.Process(target=vallet.ReceiveMoney,args=())
    #p2=multiprocessing.Process(target=vallet.CreateTransaction,args=[500,'127.0.0.1'])
    p1.start()
    #p2.start()
    while True:
        vallet.CreateTransaction(200,'127.0.0.1')
        time.sleep(2)
    

##transaction_thread=threading.Thread(target=vallet.CreateTransaction,args=(500,'123.4.5.6',))
##transaction_thread.start()
##transaction_thread.join()
##vallet.CreateTransaction(500,'123.4.5.6')
if __name__=='__main__':
    process()