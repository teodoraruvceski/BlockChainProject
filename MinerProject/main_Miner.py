import multiprocessing
import pickle
import socket
from Miner import Miner
from Block import Block
from NeighborInfo import NeighborInfo
import time
import select
import paho.mqtt.client as mqtt
from multiprocessing import Queue

def on_message(client, userdata, message):
    print("Received message: ", str(message.payload.decode("utf-8")))
    #provjera da li je blok dobar, uvezuje li se dobro u lanac
    #to treba provjeriti kako tacno radi, neki broj se hesuje sanecim da se dobije to ocekivano...
        
    

def StartMining():
    mqttBroker = "mqtt.eclipseprojects.io"
    client = mqtt.Client("Smartphone")
    client.connect(mqttBroker)
    while True:
        client.loop_start()
        client.subscribe("TEMPERATURE")
        client.on_message = on_message
        time.sleep(1)
        client.loop_read()

def SubscribeToBlockTopic():
    mqttBroker = "mqtt.eclipseprojects.io"
    client = mqtt.Client()
    client.connect(mqttBroker)
    while True:
        client.loop_start()
        client.subscribe("block")
        client.on_message = on_messageBlockTopic
        time.sleep(1)
        client.loop_read()   

def SubscribeToConfirmationTopic():
    mqttBroker = "mqtt.eclipseprojects.io"
    client = mqtt.Client()
    client.connect(mqttBroker)
    while True:
        client.loop_start()
        client.subscribe("confirmation")
        client.on_message = on_messageConfirmationTopic
        time.sleep(1)
        client.loop_read()   
   
        
def PublishValidatedBlock(block):
    mqttBroker = "mqtt.eclipseprojects.io"
    client = mqtt.Client()
    client.connect(mqttBroker)
    client.publish("block", block)
    
def PublishConfirmation(message):
    mqttBroker = "mqtt.eclipseprojects.io"
    client = mqtt.Client()
    client.connect(mqttBroker)
    client.publish("confirmation", message)


def on_messageBlockTopic(client, userdata, message):
    print(message.payload.decode())
    
def on_messageConfirmationTopic(client, userdata, message):
    print(message.payload.decode())
    
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
        print("Response from blockmaker: ")
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
        blockchain.append(responseFromBlockMaker)
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
                data = s.recv(1024)
                if data:
                    data=pickle.loads(data)
                    if(type(data)==type(Block(time.time(),"0"))):
                        time.sleep(5) #time for validating
                        print('Received new block from blockmaker')
                    elif(type(data)==type(Miner())):
                        print('Miner recieved: ')
                        print(data)
                        s.send(pickle.dumps(blockchain))     
                else:
                    s.close()
                    read_list.remove(s)


    
if __name__=='__main__':
    
    blockchain=[]
    miner=Miner()
    
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

    
