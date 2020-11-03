class Memory:
    def __init__(self):
        self.totalMemory = 16384
        self.avaliableMemory = 16384
        self.criticalProcesses = []
        self.rq0 = []
        self.rq1 = []
        self.rq2 = []
        self.rq = [self.rq0, self.rq1, self.rq2]
        self.blockedProcesses = []
        self.blockedSuspendedProcesses = []
        self.readySuspendedProcesses = []
        self.freeBlocks = [{'address': 0, 'space': 16384}]

    def adjustFreeBlocks(self):
        self.freeBlocks = sorted(self.freeBlocks, key = lambda x: x['address'])
        listSize = len(self.freeBlocks)
        for i in range(listSize-1):
            
            if i>=len(self.freeBlocks)-1:
                return
            
            if (self.freeBlocks[i+1] and self.freeBlocks[i]['address'] + self.freeBlocks[i]['space'] == self.freeBlocks[i+1]['address']):
                self.freeBlocks[i]['space'] += self.freeBlocks[i+1]['space']
                del self.freeBlocks[i+1]
                