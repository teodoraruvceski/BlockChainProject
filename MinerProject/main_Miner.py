import multiprocessing
import pickle
import socket
from Miner import Miner
from Block import Block
from NeighborInfo import NeighborInfo
import time
import select
import Socket
import paho.mqtt.client as mqtt
from multiprocessing import Queue
import json
import Transaction
difficulty=1
def proof_of_work( block):
    global difficulty
    block.nonce = 0
    computed_hash = block.compute_hash()
    while not computed_hash.startswith('0' * difficulty):
        block.nonce += 1
        computed_hash = block.compute_hash()
    difficulty += 1
    return computed_hash

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
    bytes=json.dumps(block.dump(block.hash))
    client.publish("block", bytes)
    
def PublishConfirmation(message):
    mqttBroker = "test.mosquitto.org"
    client = mqtt.Client()
    client.connect(mqttBroker)
    client.publish("confirmation", message)


def on_messageBlockTopic(client, userdata, message):
    print("----Message on Block topic----")
    print(message.payload.decode())
    #print(pickle.loads(message))
    
def on_messageConfirmationTopic(client, userdata, message):
    print("----Message on Confirmation topic----")
    print(message.payload.decode())
    #print(pickle.loads(message))
    
# def on_message2(client, userdata, message):
#     print(message.payload.decode())
    

def JoinBlockchain(miner,blockchain):
    TCP_IP='localhost'
    TCP_PORT=6000
    BUFFER_SIZE = 1024
    MESSAGE = pickle.dumps(miner)
    #MESSAGE='Hello'
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((TCP_IP, TCP_PORT))
    #sending hello to BlockchainMaker
    s.send(MESSAGE)
    print('sent registration message - sending self')
    pom=s.recv(BUFFER_SIZE)
    responseFromBlockMaker=pickle.loads(pom)
    print(responseFromBlockMaker)
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
        for b in blockchain:
            print(b)
        s.close()
    elif(type(responseFromBlockMaker)==type(Block(time.time(),"0"))):
        blockchain.append(responseFromBlockMaker.hash)
        print("Received genesis block. Appended to my blockchain.\n")
    s.close()

# def Mining():
#     print()
    
def Listening(miner,blockchain,ss):
    
    print ("Listening on port ",miner.getPort())
    read_list = [ss]
    while True:
        print('Still listening...')
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
                        print('Received new block from blockmaker')
                        data.setPreviousHash(blockchain[len(blockchain)-1])
                        hash=proof_of_work(data)
                        data.setHash(hash)
                        blockchain.append(hash)
                        print(str(data))
                        PublishValidatedBlock(data)
                    elif(type(data)==type(Miner())):
                        print('Received new miner: ')
                        print(data)
                        print("Sending blockchain...")
                        s.send(pickle.dumps(blockchain))     
                else:
                    s.close()
                    read_list.remove(s)


    
if __name__=='__main__':
    
    blockchain=[] #sadrzi hashove
    #transaction=Transaction.Transaction(sum,Socket.Socket(8500,'localhost'),Socket.Socket(8600,'localhost'),22222,time.time())
    #print(transaction.toJSON())
    miner=Miner()
     #finishProcess = Value('i',1)
    HOST=''
    PORT=miner.getPort()
    ss=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    ss.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ss.bind((HOST,PORT))
    ss.listen(5)
    miner.setPort(ss.getsockname()[1])
    
    JoinBlockchain(miner,blockchain)
    listeningProcess=multiprocessing.Process(target=Listening,args=[miner,blockchain,ss])
    subscribeBlockProcess=multiprocessing.Process(target=SubscribeToBlockTopic,args=[])
    subscribeConfirmationProcess=multiprocessing.Process(target=SubscribeToBlockTopic,args=[])
    #miningProcess=multiprocessing.Process(target=StartMining,args=[q])
    #miningProcess2=multiprocessing.Process(target=StartMining2,args=[q])
    #miningProcess.start()
    #miningProcess2.start()
    listeningProcess.start()
    subscribeBlockProcess.start()
    subscribeConfirmationProcess.start()

    
