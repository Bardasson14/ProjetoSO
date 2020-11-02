from .cpu import CPU
from .disk import Disk
from .printer import Printer
from .memory import Memory

class System:
    def __init__(self):
        self.CPUs = [CPU(None), CPU(None), CPU(None), CPU(None)]
        self.printers = [Printer(), Printer()]
        self.disks = [Disk(), Disk()]
        for i in range(2):
            self.printers[i].avaliable = True
            self.disks[i].avaliable = True
        self.memory = Memory()
        self.readySuspendedProcesses = []
        self.blockedSuspendedProcesses = []
