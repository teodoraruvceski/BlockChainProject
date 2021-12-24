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
    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()
    def __str__(self):
        return "Timestamp: {ts}\nPrev_hash: {ph}".format(ts=self.timestamp,ph=self.previous_hash)        