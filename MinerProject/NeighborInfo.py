class NeighborInfo:
    def __init__(self,miner,timestamp):
        self.miner=miner
        self.timestamp=timestamp
        self.iterationNum=-1
    
    def decIterationNum(self):
        self.interationNum -= 1
        
    def setIterationNum(self,num):
        self.iterationNum=num
    
    def getIterationNum(self):
        return self.iterationNum
    
    def getTimestamp(self):
        return self.timestamp
    
    def setTimestamp(self,timestamp):
        self.timestamp=timestamp
        