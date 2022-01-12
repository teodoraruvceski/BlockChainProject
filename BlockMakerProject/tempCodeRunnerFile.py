def compute_hash(self):
        block_string=self.toJSON()
        return sha256(block_string.encode()).hexdigest()