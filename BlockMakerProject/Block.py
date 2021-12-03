import json
from hashlib import sha256

class Block:
    def __init__(self, timestamp, previous_hash ):
        self.transactions = []
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = 0
    
    def compute_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True)
        return sha256(block_string.encode()).hexdigest()