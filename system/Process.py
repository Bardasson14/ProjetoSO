from enum import Enum


class ProcessState(Enum):
    NEW = 1
    READY_SUSPENDED = 2
    READY = 3
    RUNNING = 4
    FINISHED = 5
    SUSPENDED_BLOCKED = 6
    BLOCKED = 7

class Process:

    #criacao de Process será pelo Dispatcher
    def __init__(self, id, arrivalTime, priority, serviceTime, size, printers, disk):
        self.id = id
        self.priority = priority
        self.arrivalTime = arrivalTime
        self.priority = priority
        self.size = size
        self.printers = printers
        self.disk = disk
        self.currentStatus = ProcessState.NEW
        self.currentStatusTime = 0
