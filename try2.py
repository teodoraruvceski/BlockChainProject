import Vallet
##import BlockMaker
import threading
vallet=Vallet.Vallet()
vallet.CreateTransaction(500,'123.4.5.6')
##transaction_thread=threading.Thread(target=vallet.CreateTransaction,args=(500,'123.4.5.6',))
##transaction_thread.start()
##transaction_thread.join()
##vallet.CreateTransaction(500,'123.4.5.6')