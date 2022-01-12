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
#global variables
difficulty=1
count=0
savedBlock=None
confirmationMessages=Queue()
cond_obj=threading.Condition()
serverSocket=None
delayResponding=threading.Condition()

def proof_of_work( block):
    global difficulty
    global count
    block.nonce = 0
    computed_hash = block.compute_hash()
    #print('VALIDATING BLOCK:\n',block)
    while not computed_hash.startswith('0' * difficulty):
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
def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))
    #provjera da li je blok dobar, uvezuje li se dobro u lanac
    #to treba provjeriti kako tacno radi, neki broj se hesuje sanecim da se dobije to ocekivano...
def StartMining():
    mqttBroker = "test.mosquitto.org"
    client = mqtt.Client("Smartphone")
    client.connect(mqttBroker)
    while True:
        client.loop_start()
        client.subscribe("TEMPERATURE")
        client.on_message = on_message
        time.sleep(1)
        client.loop_read()

def SubscribeToBlockTopic():
    mqttBroker = "test.mosquitto.org"
    client = mqtt.Client()
    client.connect(mqttBroker)
    while True:
        client.loop_start()
        client.subscribe("block")
        client.on_message = on_messageBlockTopic
        time.sleep(1)
        client.loop_read()   

def SubscribeToConfirmationTopic():
    mqttBroker = "test.mosquitto.org"
    client = mqtt.Client()
    client.connect(mqttBroker)
    while True:
        client.loop_start()
        client.subscribe("confirmation")
        client.on_message = on_messageConfirmationTopic
        time.sleep(1)
        client.loop_read()   
   
        
def PublishValidatedBlock(block):
    
    mqttBroker = "test.mosquitto.org"
    client = mqtt.Client()
    client.connect(mqttBroker)
    #block=json.loads(block)
    #block=CreateBlockObject(block)
    bytes=json.dumps(block.dump(block.hash))
    client.publish("block", bytes)
    #print('EXITING PublishValidatedBlock')
    
def PublishConfirmation(message):
    mqttBroker = "test.mosquitto.org"
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
    global savedBlock
    newBlock=message.payload.decode()
    print("----Message on Block topic from MINER----")
    newBlock=json.loads(newBlock)
    newBlock2=CreateBlockObject(newBlock)
    savedBlock=newBlock2
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
    print("----Message on Confirmation topic----")
    newMessage=message.payload.decode()
    print(newMessage)
    confirmationMessages.put(newMessage)
 
def AppendingBlock(blockchain):
    global savedBlock
    global confirmationMessages
    positive=0
    negative=0
    while True:
        if(savedBlock==None):
            time.sleep(1)
            print("no block to append")
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
                else:
                    print('ODBIJENNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN')
                positive=0
                negative=0
                #semafor notifikuje
                savedBlock=None
                delayResponding.acquire()
                delayResponding.notify_all()
                delayResponding.release()
                break
            
def JoinBlockchain(miner,blockchain):
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
        s.close()
    elif(type(responseFromBlockMaker)==type(Block(time.time(),"0"))):
        blockchain.append(responseFromBlockMaker.hash)
        print("Received genesis block. Appended to my blockchain.\n")
    s.close()
    
def Listening(miner,blockchain,ss):
    global savedBlock
    global cond_obj
    global serverSocket
    print ("Listening on port ",miner.getPort())
    read_list = [ss]
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
                        data.setPreviousHash(blockchain[len(blockchain)-1])
                        hash=proof_of_work(data)
                        data.setHash(hash)
                        print(str(data))
                        PublishValidatedBlock(data)
                        #semafor ceka
                        serverSocket=s
                        print('^^^^^^^^^^set socket ')
                        #cond_obj.wait()
                        #print('notified : sending "done" to blockmaker')
                        #MESSAGE="done"
                        #s.send(pickle.dumps(MESSAGE))
                        #cond_obj.release()
                    elif(type(data)==type(Miner())):
                        print('Received new miner: ')
                        print(data)
                        print("Sending blockchain...")
                        s.send(pickle.dumps(blockchain))     
                else:
                    s.close()
                    read_list.remove(s)

def Responding():
    global serverSocket
    global delayResponding
    while True:
        delayResponding.acquire()
        print("BLOCKED IN WAITING FOR NOTIFICATION")
        delayResponding.wait()
        if(serverSocket!=None):
            print('notified : sending "done" to blockmaker')
            serverSocket.send(pickle.dumps("done"))
            serverSocket=None
        delayResponding.release()
        
    
if __name__=='__main__':
    blockchain=[] #sadrzi hashove
    miner=Miner()
    HOST=''
    PORT=miner.getPort()
    ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST,PORT))
    ss.listen(5)
    miner.setPort(ss.getsockname()[1])
    JoinBlockchain(miner,blockchain)
    listeningProcess=Thread(target=Listening,args=[miner,blockchain,ss])
    subscribeBlockProcess=Thread(target=SubscribeToBlockTopic,args=())
    subscribeConfirmationProcess=Thread(target=SubscribeToConfirmationTopic,args=())
    appendingBlockProcess=Thread(target=AppendingBlock,args=[blockchain])
    respondingThread=Thread(target=Responding,args=())
    listeningProcess.start()
    subscribeBlockProcess.start()
    subscribeConfirmationProcess.start()
    appendingBlockProcess.start()
    respondingThread.start()