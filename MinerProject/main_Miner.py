import multiprocessing
import pickle
import socket
from Miner import Miner
from Block import Block
from NeighborInfo import NeighborInfo
import time
import select
def StartMining(miner,blockchain):
    TCP_IP = '127.0.0.1'
    TCP_PORT =6000
    BUFFER_SIZE = 1024
    MESSAGE = pickle.dumps(miner)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    print('registered')
    responseFromBlockMaker=pickle.loads(s.rcv(1024))
    if(type(responseFromBlockMaker)==type(Miner())):
        connectingMiner=responseFromBlockMaker
        miner.neighbors.append(NeighborInfo(connectingMiner,time.time()))
        TCP_IP = connectingMiner.getIp()
        TCP_PORT =(int)(connectingMiner.getPort())
        MESSAGE = pickle.dumps(miner)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        print('sent self to miner')
        responseFromMiner=pickle.loads(s.recv(2048))
        miner.setNeighbors(responseFromMiner[0])
        blockchain=responseFromMiner[1]
        s.close()
    elif(type(responseFromBlockMaker)==type(Block())):
        blockchain.append(responseFromBlockMaker)
    s.close()

def Mining():
    print()
    
def Listening(miner):
    HOST=''
    PORT=miner.getPort()
    ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST,PORT))
    ss.listen(5)
    print ("Listening on port ",PORT)
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
                    print('')
                    #to do: check message type
                else:
                    s.close()
                    read_list.remove(s)


    
if __name__=='__main__':
    blockchain=[]
    miner=Miner()
    miningProcess=multiprocessing.Process(target=StartMining,args=[miner,blockchain])
    miningProcess.start()
    
