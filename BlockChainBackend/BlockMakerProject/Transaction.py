import json
class Transaction:
    def __init__(self,sum,sender,receiver,balance,timestamp):
        self.sum=sum
        self.sender=sender
        self.receiver=receiver
        self.balance=balance
        self.timestamp=timestamp
    def setSender(self,sender):
        self.sender=sender
    def setReceiver(self,receiver):
        self.receiver=receiver
    def getSender(self):
        return self.sender
    def getReceiver(self):
        return self.receiver
    def __str__(self):
        return "Sender : {sender}\nReceiver : {receiver}\nSum : {sum}\nTimestamp : {timestamp}".format(sender=self.sender,receiver=self.receiver,sum=self.sum,timestamp=self.timestamp)
    def toJSON(self):
        #return "{'sender' : {'port':{sport},'ip':'{sip}'},'receiver': {'port':{rport},'ip':'{rip}'}, 'sum' : {sum},'timestamp' : {timestamp},'balance':{balance}}".format(sport=self.sender.port,sip=self.sender.ip,rport=self.receiver.port,rip=self.receiver.ip,sum=self.sum,timestamp=self.timestamp,balance=self.balance)
        pom=self
        pom.setSender(json.dumps((self.sender).__dict__))
        pom.setReceiver(json.dumps((self.receiver).__dict__))
        print(pom.getSender())
        print(pom.getReceiver())
        ret=json.dumps(pom.__dict__)
        print(ret)
        return ret
    def dump(self):
        return{
            'sum':self.sum,
            'sender':self.sender,
            'receiver':self.receiver,
            'balance':self.balance,
            'timestamp':self.timestamp
        }