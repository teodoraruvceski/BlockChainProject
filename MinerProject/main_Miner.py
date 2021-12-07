import multiprocessing
import pickle
import socket
from Miner import Miner
def StartMining(miner):
    TCP_IP = '127.0.0.1'
    TCP_PORT =6000
    BUFFER_SIZE = 1024
    MESSAGE = pickle.dumps(miner)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    print('registered')
    response=pickle.loads(s.rcv(1024))
    if(type(response)==type(Miner())):
        
    s.close()

def Mining():
    print()
    
if __name__=='__main__':
    print('Nebojsa mozak, teodora kucac kodova')
    StartMining()
    miningProcess=multiprocessing.Process(target=StartMining,args=())
    miningProcess.start()
    
