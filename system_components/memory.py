class Memory:
    def __init__(self):
        self.totalMemory = 16384
        self.availableMemory = 16384
        self.criticalProcesses = []
        self.rq0 = []
        self.rq1 = []
        self.rq2 = []
        self.rq = [self.rq0, self.rq1, self.rq2]
        self.blockedProcesses = []
        self.blockedSuspendedProcesses = []
        self.readySuspendedProcesses = []
        self.memoryBlocks = [{'address': 0, 'space': 16384}]
