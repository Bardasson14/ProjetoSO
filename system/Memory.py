class Memory:
    def __init__(self):
        self.totalMemory, self.avaliableMemory = 16384
        self.criticalProcesses = []
        self.rq0 = []
        self.rq1 = []
        self.rq2 = []
        self.rq = [self.rq0, self.rq1, self.rq2]