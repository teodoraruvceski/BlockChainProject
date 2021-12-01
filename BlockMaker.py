import socket
import Transaction
import pickle 
import time
import json
import select
import sys
class BlockMaker:
    def __init__(self):
        self.Block=[]
        self.Miners=[]
        self.ipAddr=socket.gethostbyname(socket.gethostname())
        
    def recieveTransactions(self):
        HOST=''
        PORT=5000
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        #s.setblocking(0)
        s.bind((HOST,PORT))
        print('bindovao')
        s.listen(10)
        inputs = [s]
        outputs = []
        #connection,addr=s.accept()
        # while True:
        #   print('pocetak whilea')
        #   readable, writable, exceptional = select.select(inputs,outputs,inputs)
        #   for ss in readable:
        #        if ss is not s:
        #            print(readable.count()) 
        #            ##obj=json.loads(json.parse(s.recv(1024)))
        #            ## data = Transaction(**obj)
        #            data=s.recv(1024)
        #            if data:
        #             print(data)
        while True:
        # Wait for a connection
            print('waiting for a connection') 
            connection, client_address = s.accept()       
            try:
                print('connection from', client_address)

                # Receive the data in small chunks and retransmit it
                while True:
                    data = connection.recv(1024)
                    print('received "%s"' % pickle.loads(data))
                    if data:
                        print ('sending data back to the client')
                        #connection.sendall(data)
                    else:
                        #print >>sys.stderr, 'no more data from', client_address
                        break
                    
            finally:
                # Clean up the connection
                connection.close()