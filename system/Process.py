from enum import Enum

class ProcessState(Enum):
    NEW = auto()
    READY_SUSPENDED = auto()
    READY = auto()
    RUNNING = auto()
    FINISH = auto()
    SUSPENDED_BLOCKED = auto()
    BLOCKED = auto()

class Process:
    def __init__(self, id, arrivalTime, priority, serviceTime, size, printers, disk):
        self.id = id
        self.priority = priority
        self.arrivalTime = arrivalTime
        self.priority = priority
        self.size = size
        self.printers = printers
        self.disk = disk
        self.currentStatus = ProcessState.NEW

