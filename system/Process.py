class Process:
    def __init__(self, id, arrivalTime, priority, serviceTime, size, printers, disk):
        self.id = id
        self.priority = priority
        self.arrivalTime = arrivalTime
        self.priority = priority
        self.size = size
        self.printers = printers
        self.disk = disk
        self.currentStatus = None
        