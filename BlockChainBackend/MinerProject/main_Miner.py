import multiprocessing
import pickle
import socket
from Miner import Miner
from Block import Block
from NeighborInfo import NeighborInfo
import time
import select
import Socket
import Transaction
import paho.mqtt.client as mqtt
from multiprocessing import Queue
from threading import Thread
import threading
import  time
import json
from logger import Logger
import sys
#global variables
miner=None
count=0
blockchain=[] #sadrzi hashove
savedBlock=None
confirmationMessages=Queue()
cond_obj=threading.Condition()
serverSocket=None
delayResponding=threading.Condition()
logger = Logger("minerLogs.log")
minername="-1"
broker="broker.emqx.io"
def proof_of_work( block):
    global difficulty
    global count
    block.nonce = 0
    computed_hash = block.compute_hash()
    #print('VALIDATING BLOCK:\n',block)
    while not computed_hash.startswith('0' * block.getDifficulty()):
        block.nonce += 1
        computed_hash = block.compute_hash()
        #print('POW=',computed_hash)
    #print('EXITING proof_of_work')
    return computed_hash
def checkValidatedBlock( block):
    global difficulty
    global count
    pom=block.getHash()
    block.setHash(None)
    computed_hash = block.compute_hash()
    block.setHash(pom)
    if(computed_hash==pom):
        return True
    return False

def SubscribeToBlockTopic():
    global broker
    mqttBroker = broker
    client = mqtt.Client()
    client.connect(mqttBroker)
    while True:
        client.loop_start()
        client.subscribe("block")
        client.on_message = on_messageBlockTopic
        time.sleep(1)
        client.loop_read()   

def SubscribeToConfirmationTopic():
    global broker
    mqttBroker = broker
    client = mqtt.Client()
    client.connect(mqttBroker)
    while True:
        client.loop_start()
        client.subscribe("confirmation")
        client.on_message = on_messageConfirmationTopic
        time.sleep(1)
        client.loop_read() 
                 
def PublishValidatedBlock(block):
    global minername
    global logger
    global broker
    logger.logMessage(f'Miner {minername} publishing block on block topic.')
    mqttBroker = broker
    client = mqtt.Client()
    client.connect(mqttBroker)
    #block=json.loads(block)
    #block=CreateBlockObject(block)
    bytes=json.dumps(block.dump(block.hash))
    client.publish("block", bytes)
    print('EXITING PublishValidatedBlock')
    
def PublishConfirmation(message):
    global logger
    global minername
    global broker
    logger.logMessage(f'Miner {minername} publishing message on confirmation topic: {message}')
    mqttBroker = broker
    client = mqtt.Client()
    client.connect(mqttBroker)
    client.publish("confirmation", message)

def CreateBlockObject(dict):
    #print(dict)
    retBlock =Block(dict["timestamp"],dict["previous_hash"],dict["nonce"])
    for i in dict["transactions"]:
        retBlock.addTransaction(CreateTransactionObject(i))
    retBlock.setHash(dict["hash"])
    #print(retBlock.getHash())
    return retBlock
def CreateTransactionObject(dict):
    tr=Transaction.Transaction(dict["sum"],dict["sender"],dict["receiver"],dict["balance"],dict["timestamp"])
    return tr
def on_messageBlockTopic(client, userdata, message):
    global minername
    global savedBlock
    newBlock=message.payload.decode()
    print("----Message on Block topic from MINER----")
    newBlock=json.loads(newBlock)
    newBlock2=CreateBlockObject(newBlock)
    savedBlock=newBlock2
    logger.logMessage(f'Miner {minername} received message on block topic')
    if(checkValidatedBlock(newBlock2)):
        message="True_"
        message += str(newBlock2.getHash())
        PublishConfirmation(message)
    else:
        message="False_"
        message += str(newBlock2.getHash())
        PublishConfirmation(message)
    
def on_messageConfirmationTopic(client, userdata, message):
    global confirmationMessages
    global minername
    print("----Message on Confirmation topic----")
    newMessage=message.payload.decode()
    logger.logMessage(f'Miner {minername} received message on confirmation topic: {newMessage}')
    print(newMessage)
    confirmationMessages.put(newMessage)
 
def AppendingBlock():
    global savedBlock
    global minername
    global confirmationMessages
    global blockchain
    positive=0
    negative=0
    while True:
        if(savedBlock==None):
            time.sleep(1)
            #print("no block to append")
            continue
        time.sleep(3)
        while True:
            time.sleep(1)
            if(confirmationMessages.empty()==False):
                message=confirmationMessages.get()
                if(message.split("_")[1]==savedBlock.getHash()):
                    if(message.split("_")[0]=='True'):
                        #print('+++++++POSITIVE = ',positive)
                        positive += 1
                    elif(message.split("_")[0]=='False'):
                        #print('+++++++NEGATIVE = ',negative)
                        negative += 1
            else:
                if(positive>negative):
                    blockchain.append(savedBlock.getHash())
                    logger.logMessage(f'Miner {minername} APPENDED block hash:{savedBlock.getHash()} timestamp:{savedBlock.timestamp}')
                else:
                    print('DENIED BLOCK')
                    logger.logMessage(f'Miner {minername} DENIED block hash:{savedBlock.getHash()} timestamp:{savedBlock.timestamp}')
                positive=0
                negative=0
                #semafor notifikuje
                savedBlock=None
                delayResponding.acquire()
                delayResponding.notify_all()
                delayResponding.release()
                break
            
def JoinBlockchain(miner):
    global minername
    global logger
    global blockchain
    TCP_IP='localhost'
    TCP_PORT=6000
    BUFFER_SIZE = 1024
    #sending self to blockmaker
    MESSAGE = pickle.dumps(miner)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    s.send(MESSAGE)
    print('sent registration message - sending self')
    pom=s.recv(BUFFER_SIZE)
    responseFromBlockMaker=pickle.loads(pom)
    if(type(responseFromBlockMaker)==type(Miner())):
        connectingMiner=responseFromBlockMaker
        print("Received miner from blockmaker: ")
        print(str(connectingMiner))
        TCP_IP = connectingMiner.getIp()
        TCP_PORT =(int)(connectingMiner.getPort())
        print(TCP_PORT)
        print(TCP_IP)
        MESSAGE = pickle.dumps(miner)
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((TCP_IP, TCP_PORT))
        s.send(MESSAGE)
        responseFromMiner=pickle.loads(s.recv(1024))
        blockchain=responseFromMiner
        print("dobio bc od majnera len:",len(blockchain))
        s.close()
        logger.logMessage(f"Miner {minername} se prikljucio blockchain-u preko drugog minera: {connectingMiner.minername}.")
    elif(type(responseFromBlockMaker)==type(Block(time.time(),"0"))):
        blockchain.append(responseFromBlockMaker.hash)
        print("Received genesis block. Appended to my blockchain.\n")
        logger.logMessage(f"Miner {minername} se prikljucio blockchain-u kao prvi miner. Primio genesis block.")
    s.close()
    
def Listening(miner,ss):
    global savedBlock
    global blockchain
    global cond_obj
    global serverSocket
    global minername
    global logger
    print ("Listening on port ",miner.getPort())
    read_list = [ss]
    # client_socket=None 
    # address = None
    while True:
        readable, writable, errored = select.select(read_list, [], [])
        for s in readable:
            if s is ss:
                client_socket, address = ss.accept()
                read_list.append(client_socket)
                print( "Connection from", address)
            else:
                data = s.recv(4096)
                if data:
                    data=pickle.loads(data)
                    if(type(data)==type(Block(time.time(),"0"))):
                        time.sleep(5) #time for validating
                        #cond_obj.acquire()
                        print('Received new block from blockmaker')
                        logger.logMessage(f"Miner {minername} dobio blok na hash-ovanje. Timestamp bloka:{data.timestamp}.")
                        print("BC len:", len(blockchain))
                        data.setPreviousHash(blockchain[len(blockchain)-1])
                        hash=proof_of_work(data)
                        data.setHash(hash)
                        logger.logMessage(f"Miner {minername} hash-ovao blok. Hash: {data.hash} Timestamp bloka:{data.timestamp}.")
                        print(str(data))
                        PublishValidatedBlock(data)
                        logger.logMessage(f"Miner {minername} poslao blok na validaciju. Hash: {data.hash} Timestamp bloka:{data.timestamp}.")
                        #semafor ceka
                        serverSocket=s
                     
                        #cond_obj.wait()
                        #print('notified : sending "done" to blockmaker')
                        #MESSAGE="done"
                        #s.send(pickle.dumps(MESSAGE))
                        #cond_obj.release()
                    elif(type(data)==type(Miner())):
                        print('Received new miner: ')
                        print(data)
                        while(len(blockchain)==0):
                            time.sleep(1)
                        print("Sending blockchain...")
                        s.send(pickle.dumps(blockchain))   
                        logger.logMessage(f"Miner {minername} poslao blockchain miner-u.")
  
                else:
                    s.close()
                    read_list.remove(s)

def Responding():
    global serverSocket
    global delayResponding
    global minername
    global logger
    global miner

    while True:
       
        delayResponding.acquire()
        print(f'Miner {minername} is blocked and waiting for notification to send "done" to Blockmaker.')
        logger.logMessage(f'Miner {minername} is blocked and waiting for notification to send "done" to Blockmaker.')
        delayResponding.wait()
        if(serverSocket!=None):
            logger.logMessage(f'Miner {minername} is notified and sending "done" to Blockmaker.')
            print(f'Miner {minername} is notified and sending "done" to Blockmaker.')
            serverSocket.send(pickle.dumps("done"))
            logger.logMessage(f'--------------Miner {minername} is notified and sending "done" to Blockmaker.')
            serverSocket=None
            miner.incrementBlockMined()
            miner.payment()
            logger.logMessage(f'+Miner {minername} new balance {miner.getBalance()}')
        delayResponding.release()

    
if __name__=='__main__':
    minername = sys.argv[1]
    #minername="Miner"
    print('Miner started with work.')
    
    miner=Miner()
    miner.setMinername(minername)
    HOST=''
    PORT=miner.getPort()
    ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST,PORT))
    ss.listen(5)
    miner.setPort(ss.getsockname()[1])
    logger.logMessage(f"Miner {minername} pokrenut.")
    JoinBlockchain(miner)
    listeningProcess=Thread(target=Listening,args=[miner,ss])
    subscribeBlockProcess=Thread(target=SubscribeToBlockTopic,args=())
    subscribeConfirmationProcess=Thread(target=SubscribeToConfirmationTopic,args=())
    appendingBlockProcess=Thread(target=AppendingBlock,args=())
    respondingThread=Thread(target=Responding,args=())
    listeningProcess.start()
    subscribeBlockProcess.start()
    subscribeConfirmationProcess.start()
    appendingBlockProcess.start()
    respondingThread.start()