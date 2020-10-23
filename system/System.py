from .CPU import CPU
from .Disk import Disk
from .Printer import Printer
from .Memory import Memory

class System:
    def __init__(self):
        self.CPUs = [CPU(None), CPU(None), CPU(None), CPU(None)]
        self.printers = [Printer(), Printer()]
        self.disks = [Disk(), Disk()]
        self.memory = Memory()
        self.readySuspendedProcesses = []
        self.blockedSuspendedProcesses = []
