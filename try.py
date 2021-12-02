##import Vallet
import BlockMaker
import multiprocessing
##vallet=Vallet.Vallet()

blockmaker=BlockMaker.BlockMaker()


def rcvProcess():
    blockmaker.recieveTransactions()
def sndProcess():
    blockmaker.sendTransaction()
    
def process():
    recieveProcess=multiprocessing.Process(target=rcvProcess,args=())
    sendProcess=multiprocessing.Process(target=sndProcess,args=())
    recieveProcess.start()
    sendProcess.start()
    
if __name__=='__main__':
    process()





#blockmaker.recieveTransactions()
##listen_thread=threading.Thread(target=blockmaker.recieveTransactions,args=None)
##listen_thread.start()
##transaction_thread=threading.Thread(target=vallet.CreateTransaction,args=(500,'123.4.5.6',))
##transaction_thread.start()
##listen_thread.join()
##transaction_thread.join()
##vallet.CreateTransaction(500,'123.4.5.6')

