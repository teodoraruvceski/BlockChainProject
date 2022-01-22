import json
from hashlib import sha256
class Block:
    cnt=0
    def __init__(self, timestamp, previous_hash ,nonce=0):
        self.transactions = []
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.index=0
        Block.cnt+=1
        self.hash=None
        self.difficulty=1
    def addTransaction(self,transaction):
        self.transactions.append(transaction)
    def setDifficulty(self,d):
        self.difficulty = d
    def getDifficulty(self):
        return self.difficulty
    def compute_hash(self):
        block_string=self.toJSON()
        return sha256(block_string.encode()).hexdigest()
    def setTransactions(self,t):
        self.transactions=t
    def getTransactions(self):
        return self.transactions
    def __str__(self):
            return "Timestamp: {ts}\nPrev_hash: {ph} \nTransactionsCnt: {cnt}\nNonce: {non}\nHash:{h}".format(ts=self.timestamp,ph=self.previous_hash,cnt=len(self.transactions),non=self.nonce,h=self.hash)  
    def setHash(self,hash):
        self.hash=hash
    def getHash(self):
        return self.hash
    def setPreviousHash(self,hash):
        self.previous_hash=hash
    def toJSON(self):
       s= "'timestamp': {ts},\n'previous_hash': '{ph}' ,\n'nonce': {non},\n'index':{ind},\n'transactions':[\n".format(ts=self.timestamp,ph=self.previous_hash,non=self.nonce,ind=self.index);
       for t in self.transactions:
           s +=  "'sender' : {s}','receiver': {r}', 'sum' : {sum},'timestamp' : {timestamp},'balance':{balance}\n".format(s=t.sender,r=t.receiver,sum=t.sum,timestamp=t.timestamp,balance=t.balance)
           s+=','
       s=s[:len(s)-1]
       s+=']'
       return s
    def dump(self,hash):
        return {
            'transactions': [t.dump() for t in self.transactions],
            'timestamp':self.timestamp,
            'nonce':self.nonce,
            'previous_hash':self.previous_hash,
            'hash':self.hash,
            'index':self.index
        }
    def dumpForWeb(self):
        return{
            'hash':self.hash,
            'previous_hash':self.previous_hash,
            'nonce':self.nonce,
            'timestamp':self.timestamp,
        }
       
     