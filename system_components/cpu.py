from .resource import Resource

class CPU():

    def __init__(self, currentProcess):
        self.currentProcess = currentProcess
        self.lastQueueIndex = None
        self.empty = currentProcess == None

    def reset(self):
        self.currentProcess = None
        self.lastQueueIndex = None
        self.empty = True