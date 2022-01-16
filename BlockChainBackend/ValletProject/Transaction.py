class Transaction:
    def __init__(self,sum,sender,receiver,balance,timestamp):
        self.sum=sum
        self.sender=sender
        self.receiver=receiver
        self.balance=balance
        self.timestamp=timestamp
    def __str__(self):
        return "Sender : {sender}\nReceiver : {receiver}\nSum : {sum}\nTimestamp : {timestamp}".format(sender=self.sender,receiver=self.receiver,sum=self.sum,timestamp=self.timestamp)