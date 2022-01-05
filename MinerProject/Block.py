import json
from hashlib import sha256
class Block:
    cnt=0
    def __init__(self, timestamp, previous_hash ,nonce=0):
        self.transactions = []
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.index=Block.cnt
        Block.cnt+=1
    def addTransaction(self,transaction):
        self.transactions.append(transaction)
    def compute_hash(self):
        block_string=self.toJSON()
        return sha256(block_string.encode()).hexdigest()
    def __str__(self):
        return "Timestamp: {ts}\nPrev_hash: {ph} \nTransactionsCnt: {cnt}\nNonce: {non}".format(ts=self.timestamp,ph=self.previous_hash,cnt=len(self.transactions),non=self.nonce)  
    def setHash(self,hash):
        self.hash=hash
    def setPreviousHash(self,hash):
        self.previous_hash=hash
    def toJSON(self):
       s= "'timestamp': {ts},\n'previous_hash': '{ph}' ,\n'nonce': {non},\n'index':{ind},\n'transactions':[\n".format(ts=self.timestamp,ph=self.previous_hash,non=self.nonce,ind=self.index);
       for t in self.transactions:
           s +=  "'sender' : 'port':{sport},'ip':'{sip}','receiver': 'port':{rport},'ip':'{rip}', 'sum' : {sum},'timestamp' : {timestamp},'balance':{balance}\n".format(sport=t.sender.port,sip=t.sender.ip,rport=t.receiver.port,rip=t.receiver.ip,sum=t.sum,timestamp=t.timestamp,balance=t.balance)
           s+=','
       s=s[:len(s)-1]
       s+=']'
       
       return s
    def dump(self,hash):
        return {
            'transactions': json.dumps([t.dump() for t in self.transactions]),
            'timestamp':self.timestamp,
            'nonce':self.nonce,
            'previous_hash':self.previous_hash,
            'hash':hash,
            'index':self.index
        }
        # pom=self
        # pom_niz=[]
        # for t in self.transactions:
        #    pom_niz.append(t.toJSON)
        # for i in pom_niz:
        #     print(i)
        # pom.transactions=json.dumps(pom_niz)
        # return json.dumps(pom.__dict__)