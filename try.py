##import Vallet
import BlockMaker
import threading
##vallet=Vallet.Vallet()
blockmaker=BlockMaker.BlockMaker()
blockmaker.recieveTransactions()
##listen_thread=threading.Thread(target=blockmaker.recieveTransactions,args=None)
##listen_thread.start()
##transaction_thread=threading.Thread(target=vallet.CreateTransaction,args=(500,'123.4.5.6',))
##transaction_thread.start()
##listen_thread.join()
##transaction_thread.join()
##vallet.CreateTransaction(500,'123.4.5.6')